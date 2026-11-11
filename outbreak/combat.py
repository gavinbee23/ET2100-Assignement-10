from .items import ITEMS, heal_with_item
from .skills import SKILLS
from .ui import title, warning

COMBAT_HELP = "shoot | strike | bandage | tonic | skill <key> | flee | help"


class Fight:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.turn = 1
        self.ready_on = {}
        self.guarding = False

    def hit(self, amount, label):
        damage = min(self.monster.hp, amount)
        self.monster.hp -= damage
        return f"{label} dealt {damage} damage."

    def action(self, command):
        if command == "shoot":
            if not self.player.inventory.get("ammo"):
                return "No cartridges left. Try strike.", False
            self.player.remove("ammo")
            return self.hit(16 + self.player.level, "Pistol"), True
        if command == "strike":
            return self.hit(7 + self.player.level, "Crowbar"), True
        if command in ("bandage", "tonic"):
            return heal_with_item(self.player, command)
        if command.startswith("skill "):
            key = command[6:].strip()
            if key not in self.player.skills:
                return "You haven't learned that skill. Type help for skill keys.", False
            remaining = self.ready_on.get(key, 0) - self.turn
            if remaining > 0:
                return f"Ready after {remaining} more combat turn(s).", False
            skill = SKILLS[key]
            message, used = skill.activate(self)
            if used:
                self.ready_on[key] = self.turn + skill.cooldown + 1
            return message, used
        return "Unknown combat command. Type help.", False

    def run(self):
        title(f"Something moves. {self.monster.name} approaches.")
        print(COMBAT_HELP)
        while self.player.hp > 0 and self.monster.hp > 0:
            ammo = self.player.inventory.get("ammo", 0)
            print(f"HP {self.player.hp}/{self.player.max_hp} | "
                  f"{self.monster.name} HP {self.monster.hp} | Cartridges {ammo}")
            command = input("combat> ").strip().lower()
            if command == "help":
                print(COMBAT_HELP)
                for key in self.player.skills:
                    skill = SKILLS[key]
                    print(f"skill {key} / {skill.name}. {skill.description}")
                continue
            if command == "flee":
                if not self.monster.can_flee:
                    warning("The hatch slammed shut behind you.")
                    continue
                print("You retreat. The creature slips back into the dark.")
                return "fled"
            message, used = self.action(command)
            print(message)
            if not used or self.monster.hp <= 0:
                continue
            damage, narration = self.monster.attack(self.turn)
            if self.guarding:
                damage //= 2
                self.guarding = False
            self.player.hp = max(0, self.player.hp - damage)
            warning(f"{narration} for {damage} damage.")
            self.turn += 1
        if self.player.hp == 0:
            return "defeated"
        self.reward()
        return "won"

    def reward(self):
        self.player.gold += self.monster.gold
        print(f"{self.monster.name} defeated. +{self.monster.gold} gold, "
              f"+{self.monster.xp} XP.")
        for key, quantity in self.monster.drops.items():
            self.player.add(key, quantity)
            print(f"Found {ITEMS[key].name} x{quantity}.")
        self.player.gain_xp(self.monster.xp)
