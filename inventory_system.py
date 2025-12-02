"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Che Mullins

AI Usage: This code was developed with assistance from ChatGPT for structure, logic debugging, and syntax improvements. All functional and algorithmic elements were reviewed and refined by myself to ensure correctness and understanding.

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")
    character['inventory'].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character['inventory']

def count_item(character, item_id):
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character['inventory'])

def clear_inventory(character):
    removed_items = character['inventory']
    character['inventory'] = []
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    
    # Retrieve the item from the item_data dictionary
    item = item_data.get(item_id)
    if item is None or item['type'] != 'consumable':
        raise InvalidItemTypeError(f"Item {item_id} is not a consumable")
    
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    stat_name, value = item['effect'].split(":")
    value = int(value)  # Ensure the value is an integer
    
    # Apply effect to character
    apply_stat_effect(character, stat_name, value)
    
    # Remove the item from inventory after use
    character['inventory'].remove(item_id)
    
    return f"Used {item_id}, {stat_name} increased by {value}."

def equip_weapon(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    
    item = item_data.get(item_id)
    if item is None or item['type'] != 'weapon':
        raise InvalidItemTypeError(f"Item {item_id} is not a weapon")
    
   
    if 'equipped_weapon' in character:
        unequip_weapon(character)
    
    effect = item['effect']
    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, value)
    character['equipped_weapon'] = item_id
    character['inventory'].remove(item_id)
    return f"Weapon {item_id} equipped."

def equip_armor(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    
    item = item_data.get(item_id)
    if item is None or item['type'] != 'armor':
        raise InvalidItemTypeError(f"Item {item_id} is not armor")
    
    # Unequip current armor if any
    if 'equipped_armor' in character:
        unequip_armor(character)
    
    # Equip new armor
    effect = item['effect']
    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, value)
    character['equipped_armor'] = item_id
    character['inventory'].remove(item_id)
    return f"Armor {item_id} equipped."

def unequip_weapon(character):
    if 'equipped_weapon' not in character:
        return None
    
    weapon_id = character['equipped_weapon']
    item_data = get_item_data(weapon_id)
    effect = item_data[weapon_id]['effect']
    stat_name, value = parse_item_effect(effect)
    
    # Remove weapon stat effect
    apply_stat_effect(character, stat_name, -value)
    
    # Add weapon back to inventory
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")
    
    character['inventory'].append(weapon_id)
    del character['equipped_weapon']
    return weapon_id


def unequip_armor(character):
    if 'equipped_armor' not in character:
        return None
    
    armor_id = character['equipped_armor']
    item_data = get_item_data(armor_id)
    effect = item_data[armor_id]['effect']
    stat_name, value = parse_item_effect(effect)
    
    
    apply_stat_effect(character, stat_name, -value)
    
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")
    
    character['inventory'].append(armor_id)
    del character['equipped_armor']
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    
    item_data = {
        "expensive_item": {'cost': 100, 'type': 'consumable', 'effect': 'health:50'},
        "health_potion": {'cost': 25, 'type': 'consumable', 'effect': 'health:20'},
        "iron_sword": {'cost': 150, 'type': 'weapon', 'effect': 'strength:5'}
    }

    
    if item_id not in item_data:
        raise ItemNotFoundError(f"Item {item_id} not found in item data")

    item = item_data[item_id]  # Retrieve the item from item_data using item_id
    
    
    if character['gold'] < item['cost']:
        raise InsufficientResourcesError("Not enough gold!")

    
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")

    character['gold'] -= item['cost']
    
    add_item_to_inventory(character, item_id)
    
    return True

def sell_item(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    
    item = item_data.get(item_id)  # Retrieve item from item_data
    if item is None:
        raise ItemNotFoundError(f"Item {item_id} not found in item data")
    
    # Calculate sell price (half of the cost)
    sell_price = item['cost'] // 2
    
    # Remove item from inventory
    character['inventory'].remove(item_id)
    
    # Add gold to character
    character['gold'] += sell_price
    
    return sell_price
# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    stat_name, value = effect_string.split(":")
    return stat_name, int(value)

def apply_stat_effect(character, stat_name, value):
    if stat_name not in character:
        raise ValueError(f"Invalid stat {stat_name}")
    
    if stat_name == "health":
        new_health = character['health'] + value
        if new_health > character['max_health']:
            character['health'] = character['max_health']
        else:
            character['health'] = new_health
    else:
        character[stat_name] += value

def display_inventory(character, item_data_dict):
    inventory_summary = {}
    for item_id in character['inventory']:
        item_name = item_data_dict[item_id]['name']
        inventory_summary[item_name] = inventory_summary.get(item_name, 0) + 1

    for item_name, count in inventory_summary.items():
        print(f"{item_name}: {count}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

