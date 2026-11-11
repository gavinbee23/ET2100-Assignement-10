import hashlib
import hmac
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from tinydb import Query, TinyDB
from tinydb.storages import Storage

from .player import Player


class AtomicJSONStorage(Storage):
    """Write a full TinyDB snapshot before replacing the previous save."""

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def read(self):
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write(self, data):
        temporary = None
        try:
            with NamedTemporaryFile(mode="w", encoding="utf-8", delete=False,
                                    dir=self.path.parent) as handle:
                temporary = Path(handle.name)
                json.dump(data, handle, indent=2)
            temporary.replace(self.path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 300_000).hex()


class Saves:
    def __init__(self, path):
        self.db = TinyDB(path, storage=AtomicJSONStorage)
        self.accounts = self.db.table("accounts")

    def register(self, name, password):
        if not (3 <= len(name) <= 20 and name.isascii()
                and name.replace("_", "").isalnum()):
            raise ValueError("Use 3-20 letters, digits, or underscores in your name.")
        if not 6 <= len(password) <= 128:
            raise ValueError("Use a password with 6-128 characters.")
        key = name.lower()
        if self.accounts.contains(Query().key == key):
            raise ValueError("That account already exists.")
        salt = os.urandom(16)
        self.accounts.insert({"key": key, "salt": salt.hex(),
                              "hash": password_hash(password, salt),
                              "player": Player(name).snapshot()})

    def login(self, name, password):
        row = self.accounts.get(Query().key == name.lower())
        if row is None or not hmac.compare_digest(
            row["hash"], password_hash(password, bytes.fromhex(row["salt"]))
        ):
            raise ValueError("Incorrect username or password.")
        return Player(**row["player"])

    def save(self, player):
        self.accounts.update({"player": player.snapshot()},
                             Query().key == player.name.lower())

    def close(self):
        self.db.close()
