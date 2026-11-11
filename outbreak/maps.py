from dataclasses import dataclass


@dataclass(frozen=True)
class Area:
    name: str
    atmosphere: str
    rows: tuple

    def tile(self, position):
        x, y = position
        if 0 <= y < len(self.rows) and 0 <= x < len(self.rows[y]):
            return self.rows[y][x]
        return "#"

    def find(self, mark):
        for y, row in enumerate(self.rows):
            if mark in row:
                return [row.index(mark), y]
        raise ValueError(f"{mark!r} is missing from {self.name}")


AREAS = {
    "station": Area("Ninth Ward Station", "Rain hammers the wired glass.", (
        "#############",
        "#...m#.....H#",
        "#.##.#.###.##",
        "#.o..#...#..#",
        "###.####.#..#",
        "#...Z....#..#",
        "#.###.####..#",
        "#.....D...t.#",
        "#############",
    )),
    "hospital": Area("Gannet Memorial Hospital", "A call bell rings in an empty room.", (
        "###############",
        "#S.i..#....R..#",
        "#.###.#.###.#.#",
        "#...#...#...#.#",
        "###.#####.###.#",
        "#C..O.....#...#",
        "#.#########.###",
        "#.....V.....lL#",
        "###############",
    )),
    "lab": Area("Bellwether Pump Lab", "Water rises through the floor grates.", (
        "#############",
        "#H....#....B#",
        "###.#.#.###.#",
        "#...#.#.....#",
        "#.###.#####.#",
        "#.....P.....#",
        "#############",
    )),
}
DIRECTIONS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
ENCOUNTERS = {"Z": "drowned", "D": "hound", "O": "orderly",
              "V": "lurker", "P": "husk", "B": "undertow"}
EXITS = {
    ("station", "H"): ("hospital", "S", 1),
    ("hospital", "S"): ("station", "H", 1),
    ("hospital", "L"): ("lab", "H", 3),
    ("lab", "H"): ("hospital", "L", 3),
}


def encounter_id(area, mark):
    return f"{area}:{ENCOUNTERS[mark]}"


def draw(player):
    area = AREAS[player.area]
    print(f"\n{area.name} | {area.atmosphere}")
    for y, row in enumerate(area.rows):
        tiles = []
        for x, mark in enumerate(row):
            if [x, y] == player.position:
                tiles.append("@")
            elif mark in ENCOUNTERS and encounter_id(player.area, mark) in player.cleared:
                tiles.append(".")
            elif mark == "R" and player.stage >= 2:
                tiles.append(".")
            elif mark == "C" and player.side_quests.get("medicine") in ("Case found", "Complete"):
                tiles.append(".")
            else:
                tiles.append(mark)
        print("".join(tiles))
    print("@ you  # wall  lowercase NPC  S/H/L doors  R relay  C case  Z/D/O/V/P/B threats")
