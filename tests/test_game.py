import io
import json
import unittest
from collections import deque
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from outbreak.combat import Fight
from outbreak.game import Game, main
from outbreak.maps import AREAS, DIRECTIONS, ENCOUNTERS
from outbreak.monsters import MONSTERS, Drowned, Undertow
from outbreak.player import Player
from outbreak.skills import SKILLS
from outbreak.storage import Saves


def route(area, start, mark):
    target = tuple(area.find(mark))
    queue = deque([(tuple(start), [])])
    visited = {tuple(start)}
    while queue:
        position, moves = queue.popleft()
        if position == target:
            return moves
        x, y = position
        for command, (dx, dy) in DIRECTIONS.items():
            next_step = (x + dx, y + dy)
            if next_step not in visited and area.tile(next_step) != "#":
                visited.add(next_step)
                queue.append((next_step, moves + [command]))
    raise AssertionError(f"{mark} is unreachable in {area.name}")


class CampaignTest(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "accounts.json"
        self.saves = Saves(self.path)
        self.addCleanup(self.saves.close)
        self.output = io.StringIO()
        output_redirect = redirect_stdout(self.output)
        output_redirect.__enter__()
        self.addCleanup(output_redirect.__exit__, None, None, None)

    def test_accounts_validate_and_isolate_progress(self):
        with self.assertRaises(ValueError):
            self.saves.register("bad name", "123456")
        with self.assertRaises(ValueError):
            self.saves.register("Robin", "123")
        self.saves.register("Robin", "123456")
        with self.assertRaises(ValueError):
            self.saves.register("robin", "abcdef")
        with self.assertRaises(ValueError):
            self.saves.login("Robin", "incorrect")
        self.saves.register("Kestrel", "123456")
        player = self.saves.login("ROBIN", "123456")
        player.gold += 30
        self.saves.save(player)
        self.assertEqual(self.saves.login("Robin", "123456").gold, 46)
        self.assertEqual(self.saves.login("Kestrel", "123456").gold, 16)
        record = json.loads(self.path.read_text())["accounts"]["1"]
        self.assertNotIn("123456", record.values())

    def test_real_menu_register_login_save_quit(self):
        with patch("builtins.input", side_effect=["bad", "r", "Robin", "l", "Robin",
                                                   "invalid", "w", "d", "save", "quit"]):
            with patch("outbreak.game.getpass", return_value="123456"):
                main(self.path)
        self.assertIn("Account created", self.output.getvalue())
        self.assertIn("blocks the way", self.output.getvalue())
        self.assertIn("Unknown command", self.output.getvalue())
        self.assertEqual(self.saves.login("Robin", "123456").position, [2, 1])

    def test_campaign_using_terminal_commands(self):
        self.saves.register("Robin", "123456")
        player = self.saves.login("Robin", "123456")
        game = Game(self.saves, player)
        commands = deque()
        fights = []

        # Use the same input prompts a human sees. The combat adapter chooses
        # legal commands from current HP, supplies and cooldowns.
        original_run = Fight.run

        def run_fight(fight):
            fights.append(fight.monster.name)

            def combat_input(prompt):
                if player.hp < 38:
                    if player.inventory.get("tonic"):
                        return "tonic"
                    if "firstaid" in player.skills and ready(fight, "firstaid"):
                        return "skill firstaid"
                    if player.inventory.get("bandage"):
                        return "bandage"
                if "precision" in player.skills and ready(fight, "precision") and player.inventory.get("ammo"):
                    return "skill precision"
                if "rush" in player.skills and ready(fight, "rush"):
                    return "skill rush"
                return "shoot" if player.inventory.get("ammo") else "strike"

            with patch("builtins.input", side_effect=combat_input):
                return original_run(fight)

        def ready(fight, skill):
            return fight.turn >= fight.ready_on.get(skill, 0)

        def travel(area_key, start, *stops):
            area = AREAS[area_key]
            for mark, action in stops:
                commands.extend(route(area, start, mark))
                commands.extend(action)
                start = area.find(mark)

        travel("station", [1, 1], ("m", ["e"]), ("o", ["shop", "buy ammo"]),
               ("Z", []), ("D", []), ("t", ["e"]), ("m", ["e", "e"]), ("H", ["e"]))
        travel("hospital", AREAS["hospital"].find("S"), ("i", ["e"]), ("O", []),
               ("C", ["e"]), ("i", ["e", "e"]), ("R", ["e"]),
               ("V", []), ("l", ["e"]), ("L", ["e"]))
        travel("lab", AREAS["lab"].find("H"), ("P", []), ("B", ["status", "journal", "quit"]))

        with patch.object(Fight, "run", run_fight):
            with patch("builtins.input", side_effect=lambda prompt: commands.popleft()):
                self.assertEqual(game.run(), "quit")

        self.assertFalse(commands)
        self.assertEqual(player.stage, 4)
        self.assertGreater(player.hp, 0)
        self.assertGreater(player.level, 1)
        self.assertEqual(set(player.skills), set(SKILLS))
        self.assertEqual(player.side_quests, {"courier": "Complete", "medicine": "Complete"})
        self.assertEqual(set(fights), {cls.name for cls in MONSTERS.values()})
        self.assertEqual(len(fights), len(MONSTERS))
        self.assertIn("VICTORY", self.output.getvalue())
        with Saves(self.path).db as reopened:
            stored = reopened.table("accounts").all()[0]["player"]
            self.assertEqual(stored, player.snapshot())

    def test_defeat_keeps_checkpoint_and_boss_cannot_be_fled(self):
        self.saves.register("Robin", "123456")
        player = self.saves.login("Robin", "123456")
        player.area, player.position, player.stage, player.hp = "lab", [10, 1], 3, 1
        self.saves.save(player)
        with patch("builtins.input", side_effect=["d", "flee", "strike"]):
            self.assertEqual(Game(self.saves, player).run(), "logout")
        self.assertIn("hatch slammed shut", self.output.getvalue())
        restored = self.saves.login("Robin", "123456")
        self.assertEqual(restored.hp, 1)
        self.assertEqual(restored.position, [10, 1])
        self.assertEqual(restored.stage, 3)

    def test_skill_cooldown_and_failed_actions(self):
        player = Player("Robin", skills=["precision"])
        fight = Fight(player, Undertow())
        self.assertTrue(fight.action("skill precision")[1])
        self.assertFalse(fight.action("skill precision")[1])
        self.assertFalse(fight.action("skill rush")[1])
        self.assertFalse(fight.action("tonic")[1])
        self.assertEqual(player.inventory["ammo"], 6)
        fight.turn = 3
        self.assertFalse(fight.action("skill precision")[1])
        fight.turn = 4
        self.assertTrue(fight.action("skill precision")[1])
        player.inventory.clear()
        self.assertFalse(fight.action("shoot")[1])
        self.assertTrue(fight.action("strike")[1])

    def test_locked_door_and_shop_validation(self):
        player = Player("Robin", position=AREAS["station"].find("H"))
        game = Game(self.saves, player)
        game.command("e")
        self.assertEqual(player.area, "station")
        game.command("buy ammo")
        self.assertEqual(player.gold, 16)
        player.position = AREAS["station"].find("o")
        game.command("buy tonic")
        game.command("buy bad-item")
        self.assertEqual(player.gold, 16)
        game.command("buy ammo")
        self.assertEqual(player.gold, 12)
        self.assertEqual(player.inventory["ammo"], 8)

    def test_flee_does_not_reward_or_move(self):
        player = Player("Robin", position=[3, 5])
        # The clerk is at (4, 5).
        self.assertEqual(ENCOUNTERS[AREAS["station"].tile([4, 5])], "drowned")
        with patch("builtins.input", side_effect=["shoot", "flee"]):
            Game(self.saves, player).command("d")
        self.assertEqual(player.position, [3, 5])
        self.assertEqual(player.inventory["ammo"], 6)
        self.assertEqual(player.gold, 16)
        self.assertEqual(player.hp, 80 - Drowned.damage)
        self.assertEqual(player.cleared, [])


if __name__ == "__main__":
    unittest.main()
