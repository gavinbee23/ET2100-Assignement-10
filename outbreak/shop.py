from .items import ITEMS


def show_shop(player):
    print(f"Gold: {player.gold}")
    for key, item in ITEMS.items():
        print(f"  buy {key:<8} {item.price:>2} gold  {item.name}. {item.description}.")


def buy(player, key):
    if key not in ITEMS:
        return "Unknown item. Type shop to see the catalog."
    item = ITEMS[key]
    if player.gold < item.price:
        return f"You need {item.price} gold."
    player.gold -= item.price
    player.add(key)
    return f"Purchased {item.name} for {item.price} gold."
