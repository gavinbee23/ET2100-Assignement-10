from .skills import teach

OBJECTIVES = (
    "Find Dispatcher Mara Venn at Ninth Ward station.",
    "Use H at the station to enter the hospital and find the relay (R).",
    "Bring the relay to Engineer Lin (l) in the hospital.",
    "Use L to enter the lab, then defeat the Undertow (B).",
    "Bellwether's flood siren is back on. Main quest complete.",
)


def journal(player):
    print(f"Main | {OBJECTIVES[player.stage]}")
    print("Lost Courier | " + player.side_quests.get("courier", "Unstarted"))
    print("Cold Chain | " + player.side_quests.get("medicine", "Unstarted"))


def talk(player, mark):
    if mark == "m" and player.stage == 0:
        player.stage = 1
        teach(player, "precision")
        print("Mara's badge unlocks the route to the hospital.")
    elif mark == "l" and player.stage == 2:
        player.stage = 3
        teach(player, "rush")
        print("Lin restores power to the lab's service hatch.")
    elif mark == "i":
        medicine(player)
    elif mark == "t":
        courier(player)
    elif mark == "m" and player.side_quests.get("courier") == "Escorted":
        print('Mara says, "Tavi made it to the radio room. I owe you."')
        player.side_quests["courier"] = "Complete"
        player.gold += 18
        player.add("ammo", 4)
        player.gain_xp(15)
        print("Lost Courier complete. +18 gold, 4 cartridges, 15 XP.")


def medicine(player):
    state = player.side_quests.get("medicine")
    teach(player, "firstaid")
    if state is None:
        player.side_quests["medicine"] = "Find the sealed case (C) in the far ward."
    elif state == "Case found":
        player.side_quests["medicine"] = "Complete"
        player.gold += 20
        player.add("tonic", 2)
        player.gain_xp(18)
        print("Cold Chain complete. +20 gold, 2 field injectors, 18 XP.")


def courier(player):
    if player.side_quests.get("courier") in ("Escorted", "Complete"):
        return
    if "station:hound" in player.cleared:
        player.side_quests["courier"] = "Escorted"
        print("Tavi runs to the radio room. Report back to Mara for your reward.")
    else:
        player.side_quests["courier"] = "Defeat the Sluice Hound (D), then return to Tavi."

