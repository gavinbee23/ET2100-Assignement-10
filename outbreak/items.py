from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    price: int
    description: str


ITEMS = {
    "ammo": Item("Cartridge", 4, "One pistol shot"),
    "bandage": Item("Dressing", 9, "Restores up to 25 HP"),
    "tonic": Item("Field injector", 17, "Restores up to 50 HP"),
}
HEALING = {"bandage": 25, "tonic": 50}


def heal_with_item(player, key):
    if key not in HEALING or player.inventory.get(key, 0) < 1:
        return "You don't have that healing item.", False
    if player.hp == player.max_hp:
        return "You're already at full health.", False
    player.remove(key)
    restored = player.heal(HEALING[key])
    return f"Used {ITEMS[key].name}. Restored {restored} HP.", True


def inventory_text(player):
    return ", ".join(
        f"{ITEMS[key].name} x{quantity}"
        for key, quantity in sorted(player.inventory.items()) if quantity
    ) or "Empty"
