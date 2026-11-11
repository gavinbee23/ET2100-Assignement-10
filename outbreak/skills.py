class Skill:
    name = ""
    cooldown = 0
    description = ""

    def activate(self, fight):
        raise NotImplementedError


class PrecisionShot(Skill):
    name = "Precision Shot"
    cooldown = 2
    description = "Spend one cartridge to deal 28 damage plus level."

    def activate(self, fight):
        if not fight.player.inventory.get("ammo"):
            return "Precision Shot needs a cartridge.", False
        fight.player.remove("ammo")
        return fight.hit(28 + fight.player.level, self.name), True


class FirstAid(Skill):
    name = "First Aid"
    cooldown = 3
    description = "Restore up to 22 HP without spending an item."

    def activate(self, fight):
        if fight.player.hp == fight.player.max_hp:
            return "You're already at full health.", False
        restored = fight.player.heal(22)
        return f"First Aid restored {restored} HP.", True


class AdrenalineRush(Skill):
    name = "Adrenaline Rush"
    cooldown = 3
    description = "Strike for 14 damage plus level and halve the next incoming hit."

    def activate(self, fight):
        fight.guarding = True
        return fight.hit(14 + fight.player.level, self.name), True


SKILLS = {"precision": PrecisionShot(), "firstaid": FirstAid(),
          "rush": AdrenalineRush()}


def teach(player, key):
    if key in player.skills:
        return
    player.skills.append(key)
    skill = SKILLS[key]
    print(f"Learned {skill.name}. {skill.description}")
