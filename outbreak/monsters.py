class Monster:
    name = "Monster"
    max_hp = 1
    damage = 1
    gold = 0
    xp = 0
    drops = {}
    can_flee = True

    def __init__(self):
        self.hp = self.max_hp

    def attack(self, turn):
        return self.damage, f"{self.name} strikes"


class Drowned(Monster):
    name, max_hp, damage = "Drowned Clerk", 24, 5
    gold, xp, drops = 10, 15, {"ammo": 2}


class Hound(Monster):
    name, max_hp, damage = "Sluice Hound", 29, 6
    gold, xp, drops = 12, 16, {"bandage": 1}

    def attack(self, turn):
        if turn % 2 == 0:
            return 9, "The hound lunges from the dark"
        return super().attack(turn)


class Orderly(Monster):
    name, max_hp, damage = "Glass Orderly", 40, 7
    gold, xp, drops = 15, 22, {"ammo": 3}


class Lurker(Monster):
    name, max_hp, damage = "Ceiling Lurker", 35, 8
    gold, xp, drops = 14, 20, {"tonic": 1}

    def attack(self, turn):
        if turn == 1:
            return 13, "The lurker drops from the ceiling"
        return super().attack(turn)


class Husk(Monster):
    name, max_hp, damage = "Pump Husk", 47, 9
    gold, xp, drops = 19, 27, {"ammo": 4}


class Undertow(Monster):
    name, max_hp, damage = "The Undertow", 110, 10
    gold, xp, drops = 45, 60, {"tonic": 1}
    can_flee = False

    def attack(self, turn):
        if self.hp <= self.max_hp // 2 and turn % 2 == 0:
            return 18, "The Undertow tears loose a section of the grating"
        return super().attack(turn)


MONSTERS = {
    "drowned": Drowned, "hound": Hound, "orderly": Orderly,
    "lurker": Lurker, "husk": Husk, "undertow": Undertow,
}
