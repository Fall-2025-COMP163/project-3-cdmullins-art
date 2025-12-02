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

item_data = {
    "health_potion": {
        'cost': 25,
        'type': 'consumable',  # Marked as consumable
        'effect': 'health:20'  # Effect: increases health by 20
    },
    "iron_sword": {
        'cost': 150,
        'type': 'weapon',  # Marked as weapon (non-consumable)
        'effect': 'strength:5'  # Effect: increases strength by 5
    },
    "expensive_item": {
        'cost': 100,
        'type': 'consumable',  # Marked as consumable
        'effect': 'health:50'  # Effect: increases health by 50
    },
    # Add weapon1 if it's a valid item
    "weapon1": {
        'cost': 50,
        'type': 'weapon',  # Marked as weapon
        'effect': 'strength:3'  # Effect: increases strength by 3
    }
}

def use_item(character, item_id, item_data):
    # Check if the item is in the inventory
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    
    # Get the item data from the global item_data dictionary
    item = item_data.get(item_id)

    if item is None:
        raise ItemNotFoundError(f"Item {item_id} not found in item data")

    # If item is consumable, apply effect and remove it from inventory
    if item['type'] == 'consumable':
        effect = item['effect']
        # Example: Apply health effect (this can be extended for other stats)
        if "health:" in effect:
            health_increase = int(effect.split(":")[1])
            character['health'] += health_increase
            character['health'] = min(character['health'], character['max_health'])  # Ensure health doesn't exceed max_health
        character['inventory'].remove(item_id)
        return f"Used {item_id}, health increased by {health_increase}."

    # If item is a weapon, just equip it (no consumable effect)
    elif item['type'] == 'weapon':
        # Equip the weapon (you could extend this logic to modify character stats)
        return f"Equipped {item_id} (Strength increased by {item['effect'].split(':')[1]})"
    
    # Handle invalid item type
    else:
        raise InvalidItemTypeError(f"Item {item_id} is not consumable or weapon.")

# Test Example
character = {'health': 80, 'inventory': ['weapon1'], 'max_health': 100, 'strength': 10}
result = use_item(character, 'weapon1', item_data)
print(result)
    
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

