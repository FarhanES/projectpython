"""
LEGENDS OF THE FORGOTTEN REALM
Python Major Project Assignment
A command-line turn-based RPG built using Python 3.x.

Run: python legends_of_the_forgotten_realm.py

This is a single-file implementation using only the Python standard library.
Save data is written to legends_save.json in the same folder.
"""

import json
import os
import random
import time

SAVE_FILE = "legends_save.json"
MAX_LEVEL = 100

# ---------------------------------------------------------------------------
# DATA: weapon rarity, weapons, armor, potions, enemies, bosses, and regions
# ---------------------------------------------------------------------------

RARITY = {
    "Common":     {"multiplier": 1.0, "crit": 0,  "drop": 50.0},
    "Uncommon":   {"multiplier": 1.1, "crit": 2,  "drop": 25.0},
    "Rare":       {"multiplier": 1.3, "crit": 5,  "drop": 15.0},
    "Super Rare": {"multiplier": 1.5, "crit": 8,  "drop": 6.0},
    "Epic":       {"multiplier": 1.8, "crit": 12, "drop": 3.0},
    "Mythical":   {"multiplier": 2.2, "crit": 18, "drop": 0.9},
    "Legendary":  {"multiplier": 2.8, "crit": 25, "drop": 0.1},
}
RARITY_ORDER = list(RARITY)

WEAPONS = [
    {"name": "Wooden Sword", "rank": "Common", "damage": 5, "price": 40, "level": 1},
    {"name": "Rusty Axe", "rank": "Common", "damage": 6, "price": 45, "level": 1},
    {"name": "Training Bow", "rank": "Common", "damage": 5, "price": 42, "level": 1},
    {"name": "Bronze Dagger", "rank": "Common", "damage": 7, "price": 55, "level": 2},
    {"name": "Iron Sword", "rank": "Rare", "damage": 14, "price": 180, "level": 8},
    {"name": "Steel Axe", "rank": "Rare", "damage": 16, "price": 210, "level": 10},
    {"name": "Long Bow", "rank": "Rare", "damage": 13, "price": 190, "level": 8},
    {"name": "Silver Spear", "rank": "Uncommon", "damage": 10, "price": 100, "level": 5},
    {"name": "Crystal Blade", "rank": "Super Rare", "damage": 24, "price": 420, "level": 16},
    {"name": "Shadow Dagger", "rank": "Super Rare", "damage": 25, "price": 450, "level": 18},
    {"name": "Lightning Bow", "rank": "Super Rare", "damage": 23, "price": 430, "level": 16},
    {"name": "Flame Sword", "rank": "Epic", "damage": 34, "price": 800, "level": 25},
    {"name": "Ice Spear", "rank": "Epic", "damage": 32, "price": 780, "level": 25},
    {"name": "Thunder Hammer", "rank": "Epic", "damage": 38, "price": 900, "level": 28},
    {"name": "Phoenix Blade", "rank": "Mythical", "damage": 50, "price": 1600, "level": 40},
    {"name": "Demon Slayer", "rank": "Mythical", "damage": 55, "price": 1800, "level": 45},
    {"name": "Celestial Staff", "rank": "Mythical", "damage": 52, "price": 1750, "level": 42},
    {"name": "Dragon King's Sword", "rank": "Legendary", "damage": 75, "price": 3500, "level": 60},
    {"name": "Blade of Eternity", "rank": "Legendary", "damage": 82, "price": 4000, "level": 70},
    {"name": "Bow of the Gods", "rank": "Legendary", "damage": 78, "price": 3800, "level": 65},
    {"name": "Void Reaver", "rank": "Legendary", "damage": 90, "price": 5000, "level": 80},
]

ARMORS = [
    {"name": "Cloth Tunic", "rank": "Common", "defense": 3, "hp": 10, "mana": 5, "crit_resist": 0, "price": 35, "level": 1},
    {"name": "Leather Vest", "rank": "Common", "defense": 5, "hp": 15, "mana": 0, "crit_resist": 1, "price": 55, "level": 2},
    {"name": "Bronze Guard", "rank": "Uncommon", "defense": 8, "hp": 25, "mana": 5, "crit_resist": 2, "price": 110, "level": 5},
    {"name": "Iron Armor", "rank": "Rare", "defense": 12, "hp": 35, "mana": 5, "crit_resist": 3, "price": 220, "level": 10},
    {"name": "Ranger Mantle", "rank": "Rare", "defense": 10, "hp": 25, "mana": 10, "crit_resist": 4, "price": 230, "level": 10},
    {"name": "Crystal Plate", "rank": "Super Rare", "defense": 18, "hp": 55, "mana": 20, "crit_resist": 6, "price": 480, "level": 18},
    {"name": "Shadow Suit", "rank": "Super Rare", "defense": 16, "hp": 40, "mana": 25, "crit_resist": 8, "price": 500, "level": 20},
    {"name": "Flameguard Armor", "rank": "Epic", "defense": 25, "hp": 80, "mana": 20, "crit_resist": 10, "price": 850, "level": 28},
    {"name": "Frostweave Robe", "rank": "Epic", "defense": 22, "hp": 60, "mana": 45, "crit_resist": 9, "price": 880, "level": 28},
    {"name": "Phoenix Mail", "rank": "Mythical", "defense": 34, "hp": 120, "mana": 50, "crit_resist": 14, "price": 1700, "level": 42},
    {"name": "Demon King's Shell", "rank": "Mythical", "defense": 40, "hp": 140, "mana": 35, "crit_resist": 18, "price": 1950, "level": 48},
    {"name": "Celestial Aegis", "rank": "Legendary", "defense": 55, "hp": 200, "mana": 80, "crit_resist": 25, "price": 3900, "level": 65},
    {"name": "Eternity Plate", "rank": "Legendary", "defense": 62, "hp": 230, "mana": 70, "crit_resist": 30, "price": 4500, "level": 75},
]

POTIONS = {
    "Small Health Potion": {"type": "health", "hp": 50, "mana": 0, "price": 25},
    "Medium Health Potion": {"type": "health", "hp": 100, "mana": 0, "price": 50},
    "Large Health Potion": {"type": "health", "hp": 250, "mana": 0, "price": 100},
    "Giant Health Potion": {"type": "health", "hp": 500, "mana": 0, "price": 180},
    "Ultimate Health Potion": {"type": "health", "hp": -1, "mana": 0, "price": 350},
    "Small Mana Potion": {"type": "mana", "hp": 0, "mana": 30, "price": 25},
    "Medium Mana Potion": {"type": "mana", "hp": 0, "mana": 75, "price": 50},
    "Large Mana Potion": {"type": "mana", "hp": 0, "mana": 150, "price": 100},
    "Giant Mana Potion": {"type": "mana", "hp": 0, "mana": 300, "price": 180},
    "Ultimate Mana Potion": {"type": "mana", "hp": 0, "mana": -1, "price": 350},
    "Healing Draught": {"type": "mixed", "hp": 100, "mana": 30, "price": 90},
    "Elixir of Balance": {"type": "mixed", "hp": 150, "mana": 75, "price": 160},
    "Royal Elixir": {"type": "mixed", "hp": 300, "mana": 150, "price": 300},
    "Attack Tonic": {"type": "buff", "stat": "attack", "amount": 10, "turns": 3, "price": 90},
    "Iron Skin Tonic": {"type": "buff", "stat": "defense", "amount": 10, "turns": 3, "price": 90},
    "Focus Elixir": {"type": "buff", "stat": "crit", "amount": 10, "turns": 3, "price": 100},
    "Battle Brew": {"type": "mixed", "hp": 80, "mana": 50, "price": 120},
}

REGIONS = [
    "Village", "Forest", "Cave", "Desert", "Ruins",
    "Castle", "Volcano", "Frozen Mountain", "Sky Temple", "Demon Realm"
]
BOSSES = {
    10: "Goblin King", 20: "Forest Guardian", 30: "Ancient Golem",
    40: "Vampire Lord", 50: "Dragon Rider", 60: "Demon General",
    70: "Ice Titan", 80: "Shadow Emperor", 90: "Celestial Dragon",
    100: "Ancient Demon King"
}
ENEMY_NAMES = [
    "Goblin", "Wolf", "Slime", "Zombie", "Skeleton",
    "Orc", "Bandit", "Troll", "Dark Archer", "Giant Spider",
    "Vampire", "Werewolf", "Necromancer", "Ice Golem", "Fire Demon",
    "Sand Raider", "Scorpion Beast", "Ruins Keeper", "Cursed Knight", "Stone Wraith",
    "Castle Guard", "Blood Witch", "Lava Hound", "Ash Giant", "Frost Wolf",
    "Ice Witch", "Sky Harpy", "Storm Drake", "Void Stalker", "Demon Scout"
]

CLASS_STATS = {
    "Warrior":  {"hp": 150, "mana": 45, "attack": 18, "defense": 14, "crit": 8},
    "Mage":     {"hp": 100, "mana": 120, "attack": 22, "defense": 6, "crit": 14},
    "Archer":   {"hp": 115, "mana": 75, "attack": 17, "defense": 10, "crit": 20},
    "Assassin": {"hp": 90, "mana": 70, "attack": 24, "defense": 6, "crit": 28},
}
SKILLS = {
    "Warrior": [("Slash", 8, 1.5), ("Shield Bash", 12, 1.8), ("Rage", 18, 2.2), ("Earthquake", 30, 3.0)],
    "Mage": [("Fireball", 10, 1.7), ("Ice Blast", 14, 2.0), ("Thunder Strike", 22, 2.6), ("Meteor", 35, 3.4)],
    "Archer": [("Multi Shot", 8, 1.5), ("Poison Arrow", 12, 1.9), ("Explosive Arrow", 20, 2.5), ("Sniper Shot", 32, 3.3)],
    "Assassin": [("Backstab", 8, 1.8), ("Smoke Bomb", 12, 1.7), ("Shadow Strike", 20, 2.6), ("Instant Kill", 35, 4.0)],
}

def line():
    print("=" * 62)

def ask_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt).strip())
            if low <= value <= high:
                return value
            print(f"Enter a number from {low} to {high}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_from_list(prompt, items):
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    return items[ask_int(prompt, 1, len(items)) - 1]

def make_item_copy(item):
    return dict(item)

def create_player():
    line()
    print("CHARACTER CREATION")
    name = input("Enter Player Name: ").strip() or "Hero"
    player_class = choose_from_list("Choose your class: ", list(CLASS_STATS))
    base = CLASS_STATS[player_class]
    starter_weapon = make_item_copy(WEAPONS[0])
    starter_armor = make_item_copy(ARMORS[0])
    return {
        "name": name, "class": player_class, "level": 1, "exp": 0,
        "hp": base["hp"], "max_hp": base["hp"], "mana": base["mana"], "max_mana": base["mana"],
        "attack": base["attack"], "defense": base["defense"], "crit": base["crit"],
        "crit_damage": 2.0, "gold": 120, "weapon": starter_weapon, "armor": starter_armor,
        "potions": {"Small Health Potion": 2, "Small Mana Potion": 1},
        "inventory": [], "bosses_defeated": [], "enemies_defeated": 0,
        "weapons_collected": [starter_weapon["name"]], "rare_items_found": [],
        "unlocked_region": 0, "buffs": {}, "play_start": time.time(), "final_score": 0
    }

def armor_bonus(player, key):
    return player["armor"].get(key, 0) if player.get("armor") else 0

def total_attack(player):
    buff = player.get("buffs", {}).get("attack", {})
    return player["attack"] + player["weapon"]["damage"] + buff.get("amount", 0)

def total_defense(player):
    buff = player.get("buffs", {}).get("defense", {})
    return player["defense"] + armor_bonus(player, "defense") + buff.get("amount", 0)

def total_crit(player):
    buff = player.get("buffs", {}).get("crit", {})
    return min(90, player["crit"] + RARITY[player["weapon"]["rank"]]["crit"] + buff.get("amount", 0))

def show_stats(player):
    line()
    print(f"{player['name']} the {player['class']} | Level {player['level']}")
    print(f"HP: {player['hp']}/{player['max_hp'] + armor_bonus(player, 'hp')}  "
          f"Mana: {player['mana']}/{player['max_mana'] + armor_bonus(player, 'mana')}")
    print(f"Attack: {total_attack(player)} | Defense: {total_defense(player)} | Critical chance: {total_crit(player)}%")
    print(f"EXP: {player['exp']} | Gold: {player['gold']}")
    print(f"Weapon: {player['weapon']['name']} ({player['weapon']['rank']})")
    print(f"Armor: {player['armor']['name']} ({player['armor']['rank']})")
    print(f"Enemies defeated: {player['enemies_defeated']} | Bosses defeated: {len(player['bosses_defeated'])}/10")
    line()

def exp_to_next(level):
    return 100 + level * 35

def level_up(player):
    while player["level"] < MAX_LEVEL and player["exp"] >= exp_to_next(player["level"]):
        player["exp"] -= exp_to_next(player["level"])
        player["level"] += 1
        player["max_hp"] += 18
        player["max_mana"] += 10
        player["attack"] += 3
        player["defense"] += 2
        player["hp"] = player["max_hp"] + armor_bonus(player, "hp")
        player["mana"] = player["max_mana"] + armor_bonus(player, "mana")
        print(f"\nLEVEL UP! You are now level {player['level']}. Your stats have increased.")
        if player["level"] % 5 == 0:
            print("Milestone reached: a new class skill/passive bonus is unlocked!")
            player["crit"] = min(60, player["crit"] + 2)
        if player["level"] % 10 == 0:
            print(f"Boss gate reached: defeat {BOSSES[player['level']]} to unlock the next region.")
    if player["level"] >= MAX_LEVEL:
        player["exp"] = 0

def get_enemy(player, boss=False):
    level = player["level"]
    if boss:
        boss_name = BOSSES.get(level, "Ancient Demon King")
        multiplier = 4.2
        name = boss_name
    else:
        max_index = min(len(ENEMY_NAMES) - 1, max(4, (level - 1) // 3))
        name = random.choice(ENEMY_NAMES[:max_index + 1])
        multiplier = 1.0
    hp = int((45 + level * 15) * multiplier)
    attack = int((8 + level * 2.3) * (1.65 if boss else 1.0))
    defense = int((2 + level * 0.65) * (1.4 if boss else 1.0))
    return {"name": name, "hp": hp, "max_hp": hp, "attack": attack, "defense": defense,
            "boss": boss, "turn": 0}

def enemy_drop(player):
    gold = random.randint(12, 30) + player["level"] * 3
    player["gold"] += gold
    print(f"You found {gold} gold.")
    if random.random() < 0.45:
        potion = random.choice(list(POTIONS))
        player["potions"][potion] = player["potions"].get(potion, 0) + 1
        print(f"Loot drop: {potion}!")
    if random.random() < 0.22:
        item = make_item_copy(random.choice(WEAPONS + ARMORS))
        player["inventory"].append(item)
        print(f"Loot drop: {item['name']} ({item['rank']})!")
        if item["name"] not in player["weapons_collected"] and "damage" in item:
            player["weapons_collected"].append(item["name"])
        if item["rank"] in ("Rare", "Super Rare", "Epic", "Mythical", "Legendary"):
            player["rare_items_found"].append(item["name"])
    player["exp"] += 45 + player["level"] * 12
    player["enemies_defeated"] += 1
    level_up(player)

def use_potion(player):
    available = [name for name, count in player["potions"].items() if count > 0]
    if not available:
        print("You have no potions.")
        return False
    print("Potions:")
    for i, name in enumerate(available, 1):
        print(f"{i}. {name} x{player['potions'][name]} ({POTIONS[name]['type']})")
    print("0. Cancel")
    choice = ask_int("Choose a potion: ", 0, len(available))
    if choice == 0:
        return False
    name = available[choice - 1]
    potion = POTIONS[name]
    player["potions"][name] -= 1
    if potion["type"] in ("health", "mixed"):
        amount = player["max_hp"] + armor_bonus(player, "hp") if potion.get("hp") == -1 else potion.get("hp", 0)
        player["hp"] = min(player["max_hp"] + armor_bonus(player, "hp"), player["hp"] + amount)
    if potion["type"] in ("mana", "mixed"):
        amount = player["max_mana"] + armor_bonus(player, "mana") if potion.get("mana") == -1 else potion.get("mana", 0)
        player["mana"] = min(player["max_mana"] + armor_bonus(player, "mana"), player["mana"] + amount)
    if potion["type"] == "buff":
        player["buffs"][potion["stat"]] = {"amount": potion["amount"], "turns": potion["turns"]}
        print(f"{potion['stat'].title()} increased by {potion['amount']} for {potion['turns']} turns.")
    print(f"Used {name}.")
    return True

def use_skill(player, enemy):
    skills = SKILLS[player["class"]]
    unlocked = min(len(skills), 1 + (player["level"] - 1) // 5)
    usable = skills[:unlocked]
    print("Skills:")
    for i, (name, cost, mult) in enumerate(usable, 1):
        print(f"{i}. {name} | Mana {cost} | Damage x{mult}")
    print("0. Cancel")
    choice = ask_int("Choose a skill: ", 0, len(usable))
    if choice == 0:
        return False
    name, cost, multiplier = usable[choice - 1]
    if player["mana"] < cost:
        print("Not enough mana.")
        return False
    player["mana"] -= cost
    damage = max(1, int(total_attack(player) * multiplier) - enemy["defense"])
    if name == "Instant Kill" and random.random() < 0.04:
        damage = enemy["hp"]
        print("INSTANT KILL!")
    enemy["hp"] -= damage
    print(f"{name}! You dealt {damage} damage.")
    return True

def player_attack(player, enemy):
    damage = max(1, total_attack(player) - enemy["defense"] + random.randint(-3, 5))
    if random.randint(1, 100) <= total_crit(player):
        damage = int(damage * player["crit_damage"])
        print("CRITICAL HIT!")
    enemy["hp"] -= damage
    print(f"You dealt {damage} damage to {enemy['name']}.")

def enemy_turn(player, enemy, defending):
    if enemy["hp"] <= 0:
        return
    enemy["turn"] += 1
    if enemy["boss"] and enemy["turn"] % 3 == 0:
        damage = int(enemy["attack"] * 1.8)
        print(f"{enemy['name']} uses a devastating special attack!")
    else:
        damage = enemy["attack"] + random.randint(-3, 4)
    damage = max(1, damage - total_defense(player) // 3)
    if defending:
        damage = max(1, damage // 2)
        print("Your defense reduces the incoming damage by 50%.")
    player["hp"] -= damage
    print(f"{enemy['name']} hits you for {damage} damage.")
    if enemy["boss"] and enemy["hp"] < enemy["max_hp"] // 3 and random.random() < 0.25:
        heal = int(enemy["max_hp"] * 0.08)
        enemy["hp"] = min(enemy["max_hp"], enemy["hp"] + heal)
        print(f"{enemy['name']} heals for {heal} HP!")

def tick_buffs(player):
    for stat in list(player.get("buffs", {})):
        player["buffs"][stat]["turns"] -= 1
        if player["buffs"][stat]["turns"] <= 0:
            del player["buffs"][stat]
            print(f"A {stat} buff has worn off.")

def battle(player, enemy):
    line()
    print(("BOSS BATTLE: " if enemy["boss"] else "ENCOUNTER: ") + enemy["name"])
    print(f"Enemy HP: {enemy['hp']} | Attack: {enemy['attack']} | Defense: {enemy['defense']}")
    defending = False
    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYour HP {player['hp']} | Mana {player['mana']} || {enemy['name']} HP {max(0, enemy['hp'])}")
        print("1 Attack  2 Skills  3 Heal/Use Potion  4 Defend  5 Inventory  6 Stats  7 Run")
        action = ask_int("Your action: ", 1, 7)
        acted = True
        defending = False
        if action == 1:
            player_attack(player, enemy)
        elif action == 2:
            acted = use_skill(player, enemy)
        elif action == 3:
            acted = use_potion(player)
        elif action == 4:
            defending = True
            print("You brace yourself for the next attack.")
        elif action == 5:
            show_inventory(player)
            acted = False
        elif action == 6:
            show_stats(player)
            acted = False
        elif action == 7:
            if enemy["boss"]:
                print("You cannot flee from a boss battle!")
                acted = False
            elif random.random() < 0.65:
                print("You escaped from the encounter.")
                return "escaped"
            else:
                print("You failed to escape!")
        if acted and enemy["hp"] > 0:
            enemy_turn(player, enemy, defending)
            tick_buffs(player)
    if player["hp"] <= 0:
        print("\nGAME OVER — your hero has fallen.")
        return "dead"
    print(f"\nVictory! You defeated {enemy['name']}.")
    if enemy["boss"]:
        if enemy["name"] not in player["bosses_defeated"]:
            player["bosses_defeated"].append(enemy["name"])
        player["gold"] += 200 + player["level"] * 10
        reward = make_item_copy(random.choice([x for x in WEAPONS + ARMORS if RARITY[x["rank"]]["drop"] <= 15]))
        player["inventory"].append(reward)
        print(f"Boss reward: {reward['rank']} {reward['name']} (guaranteed Rare-or-better).")
        if "damage" in reward:
            player["weapons_collected"].append(reward["name"])
        player["rare_items_found"].append(reward["name"])
    enemy_drop(player)
    return "won"

def show_inventory(player):
    line()
    print("INVENTORY")
    if not player["inventory"]:
        print("Your bag is empty.")
    else:
        for i, item in enumerate(player["inventory"], 1):
            if "damage" in item:
                detail = f"Weapon | {item['rank']} | Damage {item['damage']} | Level {item['level']}"
            else:
                detail = f"Armor | {item['rank']} | Defense +{item['defense']} | Level {item['level']}"
            print(f"{i}. {item['name']} — {detail}")
    print("Potions:")
    for name, count in player["potions"].items():
        if count:
            print(f" - {name}: {count}")
    print("Actions: 1 Equip item | 2 Drop item | 3 Sell item | 4 Use potion | 0 Back")
    choice = ask_int("Choose action: ", 0, 4)
    if choice == 0:
        return
    if choice == 4:
        use_potion(player)
        return
    if not player["inventory"]:
        print("No equipment items available.")
        return
    idx = ask_int("Item number: ", 1, len(player["inventory"])) - 1
    item = player["inventory"][idx]
    if choice == 1:
        if player["level"] < item["level"]:
            print(f"You need level {item['level']} to equip this item.")
            return
        if "damage" in item:
            player["weapon"] = item
            print(f"Equipped {item['name']}.")
        else:
            player["armor"] = item
            print(f"Equipped {item['name']}.")
    elif choice == 2:
        removed = player["inventory"].pop(idx)
        print(f"Dropped {removed['name']}.")
    elif choice == 3:
        removed = player["inventory"].pop(idx)
        price = int(removed["price"] * 0.45)
        player["gold"] += price
        print(f"Sold {removed['name']} for {price} gold.")

def shop(player):
    while True:
        line()
        print(f"VILLAGE SHOP — Gold: {player['gold']}")
        print("1 Buy weapons  2 Buy armor  3 Buy potions  4 Sell inventory item  0 Exit")
        choice = ask_int("Choose: ", 0, 4)
        if choice == 0:
            return
        if choice in (1, 2):
            stock = WEAPONS if choice == 1 else ARMORS
            available = [x for x in stock if x["level"] <= player["level"]]
            for i, item in enumerate(available, 1):
                extra = f"Damage {item['damage']}" if "damage" in item else f"Defense {item['defense']}"
                print(f"{i}. {item['name']} [{item['rank']}] — {extra}, {item['price']} gold")
            print("0. Back")
            idx = ask_int("Buy which item? ", 0, len(available))
            if idx:
                item = available[idx - 1]
                if player["gold"] < item["price"]:
                    print("Not enough gold.")
                else:
                    player["gold"] -= item["price"]
                    player["inventory"].append(make_item_copy(item))
                    print(f"Purchased {item['name']}.")
        elif choice == 3:
            names = list(POTIONS)
            for i, name in enumerate(names, 1):
                print(f"{i}. {name} — {POTIONS[name]['price']} gold")
            idx = ask_int("Buy which potion? (0 to back): ", 0, len(names))
            if idx:
                name = names[idx - 1]
                count = ask_int("Quantity: ", 1, 20)
                total = POTIONS[name]["price"] * count
                if player["gold"] >= total:
                    player["gold"] -= total
                    player["potions"][name] = player["potions"].get(name, 0) + count
                    print(f"Purchased {count} x {name}.")
                else:
                    print("Not enough gold.")
        elif choice == 4:
            if not player["inventory"]:
                print("Nothing to sell.")
            else:
                for i, item in enumerate(player["inventory"], 1):
                    print(f"{i}. {item['name']} — sell for {int(item['price'] * .45)} gold")
                idx = ask_int("Sell which item? (0 to back): ", 0, len(player["inventory"]))
                if idx:
                    item = player["inventory"].pop(idx - 1)
                    gain = int(item["price"] * .45)
                    player["gold"] += gain
                    print(f"Sold {item['name']} for {gain} gold.")

def save_game(player):
    data = dict(player)
    data.pop("play_start", None)
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Game saved to {SAVE_FILE}.")
    except OSError as error:
        print(f"Could not save game: {error}")

def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            player = json.load(file)
        player["play_start"] = time.time()
        player.setdefault("buffs", {})
        print("Save loaded successfully.")
        return player
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print(f"No valid save found ({error}).")
        return None

def instructions():
    line()
    print("HOW TO PLAY")
    print("- Create a hero and select Warrior, Mage, Archer, or Assassin.")
    print("- Fight enemies to earn EXP, gold, potions, and equipment.")
    print("- Use skills by spending mana; stronger skills unlock every 5 levels.")
    print("- Defend to reduce the next incoming attack by 50%.")
    print("- Visit the shop to buy equipment and potions.")
    print("- Every 10 levels, defeat the region boss before progressing.")
    print("- Save from the main menu. The save file uses JSON.")
    print("- Reach level 100 and defeat the Ancient Demon King to win.")
    print("World: " + " -> ".join(REGIONS))
    input("Press Enter to return to the menu...")

def victory_screen(player):
    elapsed = max(0, int(time.time() - player.get("play_start", time.time())))
    minutes, seconds = divmod(elapsed, 60)
    player["final_score"] = player["level"] * 100 + player["gold"] + player["enemies_defeated"] * 20
    line()
    print("                 VICTORY — ELDORIA IS FREE!")
    line()
    print(f"Player Name: {player['name']}")
    print(f"Final Level: {player['level']}")
    print(f"Total Gold: {player['gold']}")
    print(f"Bosses Defeated: {len(player['bosses_defeated'])}")
    print(f"Enemies Defeated: {player['enemies_defeated']}")
    print(f"Weapons Collected: {len(set(player['weapons_collected']))}")
    print(f"Rare Items Found: {len(player['rare_items_found'])}")
    print(f"Total Play Time: {minutes}m {seconds}s")
    print(f"Final Score: {player['final_score']}")
    print('"A hero is not measured by the sword they carry, but by the code that forges it."')
    line()

def explore(player):
    if player["level"] >= 10 and player["level"] % 10 == 0:
        boss_name = BOSSES[player["level"]]
        if boss_name not in player["bosses_defeated"]:
            print(f"\nA powerful boss blocks your path: {boss_name}!")
            result = battle(player, get_enemy(player, boss=True))
            if result == "dead":
                return False
            if result == "won":
                player["unlocked_region"] = min(9, player["level"] // 10)
            return True
    region_index = min(9, (player["level"] - 1) // 10)
    print(f"\nYou travel through {REGIONS[region_index]}...")
    enemy = get_enemy(player)
    result = battle(player, enemy)
    return result != "dead"

def game_loop(player):
    while True:
        if player["hp"] <= 0:
            print("\nGAME OVER")
            print("1 Retry from saved game  2 Load Save  3 Exit")
            choice = ask_int("Choose: ", 1, 3)
            if choice == 1:
                player["hp"] = max(1, (player["max_hp"] + armor_bonus(player, "hp")) // 2)
                player["mana"] = player["max_mana"] + armor_bonus(player, "mana")
            elif choice == 2:
                loaded = load_game()
                if loaded:
                    player = loaded
            else:
                return
        if player["level"] >= 100 and BOSSES[100] in player["bosses_defeated"]:
            victory_screen(player)
            return
        line()
        print(f"LEGENDS OF THE FORGOTTEN REALM — {player['name']} | Level {player['level']}")
        print("1 Explore / Fight  2 Inventory  3 Shop  4 View Stats  5 Save Game  6 Main Menu")
        choice = ask_int("Choose an action: ", 1, 6)
        if choice == 1:
            if player["level"] % 10 == 0 and player["level"] in BOSSES and BOSSES[player["level"]] not in player["bosses_defeated"]:
                print(f"Boss gate: {BOSSES[player['level']]}. Prepare before entering!")
            alive = explore(player)
            if not alive:
                player["hp"] = 0
        elif choice == 2:
            show_inventory(player)
        elif choice == 3:
            shop(player)
        elif choice == 4:
            show_stats(player)
        elif choice == 5:
            save_game(player)
        elif choice == 6:
            return

def main():
    random.seed()
    while True:
        line()
        print("        LEGENDS OF THE FORGOTTEN REALM")
        print("     A Command-Line Turn-Based RPG in Python")
        line()
        print("1. New Game")
        print("2. Continue")
        print("3. Instructions")
        print("4. Exit")
        choice = ask_int("Select an option: ", 1, 4)
        if choice == 1:
            player = create_player()
            game_loop(player)
        elif choice == 2:
            player = load_game()
            if player:
                game_loop(player)
        elif choice == 3:
            instructions()
        else:
            print("Thank you for playing. Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame closed safely. Save before exiting next time.")
