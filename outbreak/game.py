from getpass import getpass
from pathlib import Path

from .combat import Fight
from .items import heal_with_item, inventory_text
from .maps import AREAS, DIRECTIONS, ENCOUNTERS, EXITS, draw, encounter_id
from .monsters import MONSTERS
from .npcs import NPCS
from .quests import journal, talk
from .shop import buy, show_shop
from .skills import SKILLS
from .storage import Saves
from .ui import intro, menu, title, warning

SAVE_PATH = Path(__file__).resolve().parents[1] / "data" / "saves.json"
HELP = """w/a/s/d move  |  e interact on your tile  |  map  |  look  |  journal
status  |  inventory  |  use bandage/tonic  |  shop  |  buy <item>
help  |  save  |  logout  |  quit"""


class Game:
    def __init__(self, saves, player):
        self.saves = saves
        self.player = player

    @property
    def area(self):
        return AREAS[self.player.area]

    @property
    def tile(self):
        return self.area.tile(self.player.position)

    def move(self, command):
        player = self.player
        dx, dy = DIRECTIONS[command]
        x, y = player.position
        target = [x + dx, y + dy]
        mark = self.area.tile(target)
        if mark == "#":
            warning("A wall or barricade blocks the way.")
            return
        if mark in ENCOUNTERS and encounter_id(player.area, mark) not in player.cleared:
            result = Fight(player, MONSTERS[ENCOUNTERS[mark]]()).run()
            if result == "defeated":
                warning("You black out. Your last checkpoint is available on login.")
                return "logout"
            if result == "fled":
                return
            player.cleared.append(encounter_id(player.area, mark))
            if mark == "B":
                player.stage = 4
                title("VICTORY | The Undertow goes still.")
                print("You open the floodgate. From the roof, you hear the siren")
                print("answer Mara's radio. For the first time tonight, the streets are draining.")
                print("Main quest complete. You can finish any remaining side quests.")
        player.position = target
        draw(player)

    def interact(self):
        player = self.player
        mark = self.tile
        exit_route = EXITS.get((player.area, mark))
        if exit_route:
            destination, arrival, required_stage = exit_route
            if player.stage < required_stage:
                warning("The door is locked. Check your journal.")
                return
            player.area = destination
            player.position = self.area.find(arrival)
            draw(player)
        elif mark in NPCS:
            npc = NPCS[mark]
            print(f'{npc.name}, {npc.role}: "{npc.dialogue}"')
            talk(player, mark)
        elif mark == "R" and player.stage == 1:
            player.stage = 2
            print("You pocket the relay. Find Engineer Lin.")
        elif mark == "C" and player.side_quests.get("medicine") is None:
            print("The case is sealed with a medical tag. Ask Inez about it.")
        elif mark == "C" and player.side_quests.get("medicine", "").startswith("Find"):
            player.side_quests["medicine"] = "Case found"
            print("You pick up the sealed case. Return it to Inez.")
        else:
            print("Nothing here needs your attention.")

    def look(self):
        if self.tile in NPCS:
            npc = NPCS[self.tile]
            print(f"{npc.name} is here. Press e to talk.")
        else:
            print(f"You are on tile {self.tile} at {tuple(self.player.position)}.")

    def status(self):
        player = self.player
        print(f"{player.name} | HP {player.hp}/{player.max_hp} | Level {player.level} | "
              f"XP {player.xp}/{player.level * 25} | Gold {player.gold}")
        print("Inventory | " + inventory_text(player))
        print("Skills | " + (", ".join(SKILLS[key].name for key in player.skills) or "None"))
        for key in player.skills:
            skill = SKILLS[key]
            print(f"  skill {key} | {skill.description} Cooldown {skill.cooldown} turns.")

    def command(self, command):
        player = self.player
        verb, _, argument = command.partition(" ")
        argument = argument.strip()
        if command in DIRECTIONS:
            return self.move(command)
        if command == "e":
            self.interact()
        elif command == "status":
            self.status()
        elif command == "journal":
            journal(player)
        elif command == "inventory":
            print(inventory_text(player))
        elif command == "map":
            draw(player)
        elif command == "look":
            self.look()
        elif command == "help":
            print(HELP)
        elif command == "shop" or verb == "buy":
            if self.tile != "o":
                print("Stand on Oren's tile (o) to use the shop.")
            elif verb == "buy":
                print(buy(player, argument))
            else:
                show_shop(player)
        elif verb == "use":
            if argument not in ("bandage", "tonic"):
                print("Use 'use bandage' or 'use tonic'.")
            else:
                message, _ = heal_with_item(player, argument)
                print(message)
        elif command == "save":
            print("Checkpoint saved.")
        elif command in ("logout", "quit"):
            return command
        else:
            warning("Unknown command. Type help.")

    def run(self):
        title(f"Radio check, {self.player.name}.")
        journal(self.player)
        draw(self.player)
        print(HELP)
        while True:
            before = self.player.snapshot()
            command = input("explore> ").strip().lower()
            result = self.command(command)
            if self.player.hp > 0 and (command == "save" or self.player.snapshot() != before):
                self.saves.save(self.player)
            if result:
                return result


def main(path=SAVE_PATH):
    intro()
    saves = None
    try:
        saves = Saves(path)
        while True:
            action = menu("[R]egister, [L]ogin, [Q]uit > ", ("r", "l", "q"))
            if action == "q":
                break
            name = input("Username: ").strip()
            password = getpass("Password: ")
            try:
                if action == "r":
                    saves.register(name, password)
                    print("Account created. Log in to begin.")
                    continue
                player = saves.login(name, password)
            except ValueError as exc:
                warning(str(exc))
                continue
            if Game(saves, player).run() == "quit":
                break
    except (EOFError, KeyboardInterrupt):
        print("\nSession closed. Your last completed checkpoint is available.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        warning(f"Could not open or update the saved game: {exc}")
    finally:
        if saves is not None:
            saves.close()
