"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Che Mullins

AI Usage: This code was developed with assistance from ChatGPT for structure, logic debugging, and syntax improvements. All functional and algorithmic elements were reviewed and refined by me to ensure correctness and understanding.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

# character_manager.py

def create_character(name, character_class):
   
    if character_class == "Warrior":
        max_health = 150
        strength = 20
        magic = 5
    elif character_class == "Mage":
        max_health = 80
        strength = 5
        magic = 20
    elif character_class == "Rogue":
        max_health = 100
        strength = 15
        magic = 10
    elif character_class == "Cleric":
        max_health = 110
        strength = 10
        magic = 15
    else:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    # Ensure all required keys are present
    return {
        "name": name,              # Character name (passed parameter)
        "class": character_class,  # Character class (passed parameter)
        "level": 1,                # Default level
        "health": max_health,      # Set health
        "max_health": max_health,  # Set max health
        "strength": strength,      # Set strength
        "magic": magic,            # Set magic power
        "experience": 0,           # Set initial experience (this is where KeyError happens)
        "gold": 50,                # Default gold value
        "inventory": [],           # Default empty inventory
        "active_quests": [],       # Default empty active quests
        "completed_quests": []     # Default empty completed quests
    }


    
def save_character(character, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    save_path = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(save_path, 'w') as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True
    except (PermissionError, IOError) as e:
        raise e

def load_character(character_name, save_directory="data/save_games"):
    save_path = os.path.join(save_directory, f"{character_name}_save.txt")
    
    if not os.path.exists(save_path):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    
    try:
        character = {}
        with open(save_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split(": ")
                if key == "INVENTORY" or key == "ACTIVE_QUESTS" or key == "COMPLETED_QUESTS":
                    character[key] = value.split(',')
                else:
                    character[key] = value
        # Convert relevant fields to proper types
        character['level'] = int(character['level'])
        character['health'] = int(character['health'])
        character['max_health'] = int(character['max_health'])
        character['strength'] = int(character['strength'])
        character['magic'] = int(character['magic'])
        character['experience'] = int(character['experience'])
        character['gold'] = int(character['gold'])
        return character
    except Exception as e:
        raise SaveFileCorruptedError(f"Error loading file '{character_name}_save.txt': {e}")

def list_saved_characters(save_directory="data/save_games"):
     if not os.path.exists(save_directory):
        return []
    
     saved_files = os.listdir(save_directory)

     return [file.split('_save.txt')[0] for file in saved_files if file.endswith('_save.txt')]

def delete_character(character_name, save_directory="data/save_games"):
    save_path = os.path.join(save_directory, f"{character_name}_save.txt")
    
    if not os.path.exists(save_path):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    
    os.remove(save_path)
    return True
    
# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character['health'] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain experience.")
    
    character['experience'] += xp_amount
    
    while character['experience'] >= character['level'] * 100:
        character['level'] += 1
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        character['experience'] -= character['level'] * 100
        character['health'] = character['max_health']
        print(f"{character['name']} leveled up to level {character['level']}!")

def add_gold(character, amount):
    if character['gold'] + amount < 0:
        raise ValueError(f"{character['name']} does not have enough gold.")
    
    character['gold'] += amount
    return character['gold']

def heal_character(character, amount):
    actual_heal = min(amount, character['max_health'] - character['health'])
    character['health'] += actual_heal
    return actual_heal

def is_character_dead(character):
    return character['health'] <= 0
    
def revive_character(character):
    if character['health'] > 0:
        return False

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required_fields = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list
    }
    
    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
        
        if not isinstance(character[field], expected_type):
            raise InvalidSaveDataError(f"Invalid type for field: {field}. Expected {expected_type.__name__}, got {type(character[field]).__name__}")
    
    return True
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

