# Dead City — Outbreak

An original Python terminal survival-horror RPG for ET2100. The rain, scarce ammunition, and locked routes take inspiration from Resident Evil 2. The story, characters, dialogue, and maps are original.

At 02:13, flood sirens go quiet in Bellwether. A distress broadcast draws you to Ninth Ward Station, where dispatcher Mara Venn traces it to a hospital built over an old pumping lab. Follow the signal, help the stranded survivors, and open the floodgate before the lower wards go under.

## Run in Windows PowerShell or VS Code

1. Extract the ZIP. Open the extracted **Dead_City_Outbreak** folder in VS Code.
2. Select **Terminal → New Terminal**. Run these commands from the folder containing `main.py`.

   ```powershell
   uv sync
   uv run python main.py
   ```

3. Type `r` to register, then `l` to log in. Use a username with 3–20 letters, digits, or underscores and a password of 6–128 characters. The terminal usually hides characters as you type the password.
4. Type `journal` for your current objective. From the starting square, enter `d` three times to reach Mara (`m`), then `e` to talk.

Python 3.10 or newer is required. If you have Python and pip but no uv, run `python -m pip install -r requirements.txt` and then `python main.py`.

## Controls

| Command | What it does |
| --- | --- |
| `w`, `a`, `s`, `d` | Move one tile. Walls and barricades block movement. Entering a threat tile starts combat. |
| `e` | Interact while standing on an NPC, door, relay, or supply case. |
| `map`, `look`, `journal` | Show the map, inspect your tile, or see quest objectives. |
| `status`, `inventory` | Inspect HP, level, XP, gold, learned skills, and supplies. |
| `shop`, `buy ammo` | Browse or buy on Oren's tile (`o`). Try `buy bandage` or `buy tonic` too. |
| `use bandage`, `use tonic` | Heal while exploring. |
| `help`, `save`, `logout`, `quit` | See commands, save, return to login, or close the game. |

In combat, `shoot` spends a cartridge and `strike` uses the crowbar. Enter `bandage` or `tonic` to heal. Enter `skill precision`, `skill firstaid`, or `skill rush` once you learn the corresponding ability. `help` lists your options. Valid actions advance the fight. A successful nonlethal turn gives the enemy a chance to attack. You can flee ordinary fights. Fleeing keeps the HP and supplies you spent and the enemy recovers. The boss locks the hatch.

## Where progress goes

Each account has its own TinyDB record in `data/saves.json`. Completed exploration commands that change progress save automatically, including the results of completed fights. If you are defeated or interrupt a fight, log in again to resume at the last completed checkpoint. Passwords are stored as salted hashes. Use one running copy of the game per extracted folder. The save folder, Python caches, and virtual environment are ignored by Git.

## ET2100 requirement checklist

| Requirement | Where to find it |
| --- | --- |
| Intro and Colorama | `ui.py` provides the opening and colored headings and warnings. |
| Registration, login, and TinyDB persistence | `game.py` handles the prompts. `storage.py` verifies credentials and saves player snapshots. |
| At least 10 meaningful Python files | 13 implementation files counting `main.py`, plus the package initializer and test file. |
| Five unique NPCs | Mara Venn, Oren Pike, Inez Calder, Tavi Rowe, and Lin Sato in `npcs.py`. Each has a distinct role and dialogue. |
| Multi-stage main quest and final boss | Receive Mara's badge, recover the ward relay, have Lin open the lab, and defeat the Undertow. |
| Two rewarding side quests | Lost Courier rewards gold, ammo, and XP. Cold Chain rewards gold, field injectors, and XP. |
| Monster inheritance and loot | Six subclasses of `Monster`, including the boss. Victories award gold, XP, and items. |
| Shop and inventory | Buy supplies from Oren. Combat and exploration share the same inventory. |
| Learnable skills and cooldowns | Three subclasses of `Skill`: Precision Shot, First Aid, and Adrenaline Rush. Learn them by interacting with survivors. |
| Player progress and status | HP, maximum HP, XP, level, gold, items, skills, quest stages, cleared encounters, and position are saved. |
| Two or more obstacle maps | Ninth Ward Station, Gannet Memorial Hospital, and Bellwether Pump Lab all have walls and branching routes. |
| Input validation and error handling | Invalid commands, blocked movement, locked doors, invalid login, unavailable skills, and failed purchases receive feedback. |

## Code tour

| Files | Responsibility |
| --- | --- |
| `main.py`, `outbreak/game.py` | Start the game and coordinate account prompts, exploration, combat, and checkpoints. |
| `outbreak/ui.py`, `outbreak/maps.py` | Format terminal output and define rooms, walls, exits, and encounters. |
| `outbreak/npcs.py`, `outbreak/quests.py` | Store dialogue and handle quest transitions and rewards. |
| `outbreak/player.py`, `outbreak/storage.py` | Hold player state and persist it between sessions. |
| `outbreak/items.py`, `outbreak/shop.py` | Define supplies, healing, prices, and purchases. |
| `outbreak/combat.py`, `outbreak/monsters.py`, `outbreak/skills.py` | Run turns, enemy behavior, loot, abilities, and cooldowns. |

See [TESTING.md](TESTING.md) for tests, a walkthrough, and a midterm rehearsal.
