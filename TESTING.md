# Testing and midterm demo

## Run the automated checks

From the extracted project folder:

```powershell
uv sync
uv run python -m compileall -q main.py outbreak tests
uv run python -m unittest discover -s tests -v
```

Expect seven passing tests. They use temporary save files. The campaign test feeds movement and combat commands into the game loops to defeat all six monsters, finish both side quests, learn all three skills, and compare the saved victory with the live player state. Other tests cover the startup menu, account isolation, blocked movement, purchases, combat cooldowns, retreat, and defeat recovery.

## Manual walkthrough (spoilers)

Use `map` to plan a route through the corridors. Step onto a symbol and press `e` to interact. Threats engage when you step onto their square.

1. **Station.** Register and log in. From the start, try `w` to see the wall warning, then enter `d` three times and `e` to learn Precision Shot from Mara. For Oren's shop, enter `s`, `s`, `a`, `a`, then `shop` and `buy ammo`. Type `status` to see the change.
2. **Lost Courier.** Find Tavi (`t`) in the bottom corridor. Defeat the Sluice Hound (`D`), talk to Tavi, then return to Mara to collect your reward. You can defeat the hound on the way to Tavi and escort them on your first conversation.
3. **Hospital.** From the station's bottom corridor, follow the east passage up to `H` and use it. Talk to Inez (`i`) for First Aid and the Cold Chain quest. Find the sealed case (`C`) on the lower west side and return it to Inez. You can spend a field injector during combat with `tonic`.
4. **Open the lab.** Find the relay (`R`) along the hospital's upper corridor. Take it to Lin (`l`) on the lower east side for access to `L` and the Adrenaline Rush skill. The west end of the case corridor leads down to the route toward Lin.
5. **Win.** In the lab, follow the west passage down and across the lower corridor, then head up to `B`. Heal before entering if your HP is low. Use `skill precision` when ready, `skill rush` to reduce a counterattack, and healing as needed. The Undertow hits harder once it loses half its HP. After victory, check `journal`, log out, then log back in to verify the ending and your loot are saved.

## Rehearse for the midterm

- Start with a new demo account. Show the intro, an invalid command, wall collision, Mara teaching Precision Shot, and a purchase from Oren. Log out and log back in to demonstrate persistence.
- For the final-boss demo, prepare a second account one tile away from `B` with ammunition and healing items. Play the fight live and show the completed journal. Use the automated campaign test to demonstrate both side quests if class time is short.
- Open `outbreak/monsters.py`. Explain how `Hound` inherits from `Monster` and overrides `attack()`, then delegates to the base behavior on its normal turns.
- Open `outbreak/skills.py` and `outbreak/combat.py`. Explain how the fight calls a subclass's `activate()` and records the next eligible turn. A skill with a two-turn cooldown used on turn 1 becomes available on turn 4.
- Trace a movement command from `Game.command()` through `Game.move()` to the map lookup. Then trace a successful action from `Player.snapshot()` to the TinyDB update in `Saves.save()`.
- Be ready to modify one small value live, such as the Hound's lunge damage, and explain which part of the game will change. Restore it and rerun the tests before submitting.
