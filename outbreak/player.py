from dataclasses import asdict, dataclass, field


@dataclass
class Player:
    name: str
    hp: int = 80
    max_hp: int = 80
    xp: int = 0
    level: int = 1
    gold: int = 16
    inventory: dict = field(default_factory=lambda: {"ammo": 7, "bandage": 2})
    skills: list = field(default_factory=list)
    stage: int = 0
    side_quests: dict = field(default_factory=dict)
    cleared: list = field(default_factory=list)
    area: str = "station"
    position: list = field(default_factory=lambda: [1, 1])

    def add(self, key, quantity=1):
        self.inventory[key] = self.inventory.get(key, 0) + quantity

    def remove(self, key):
        self.inventory[key] -= 1
        if self.inventory[key] == 0:
            del self.inventory[key]

    def heal(self, amount):
        restored = min(amount, self.max_hp - self.hp)
        self.hp += restored
        return restored

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 25:
            self.xp -= self.level * 25
            self.level += 1
            self.max_hp += 8
            self.heal(12)
            print(f"Level {self.level}. Maximum HP is now {self.max_hp}.")

    def snapshot(self):
        return asdict(self)
