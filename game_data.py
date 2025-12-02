"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Che Mullins

AI Usage: This code was developed with assistance from ChatGPT for structure, logic debugging, and syntax improvements. All functional and algorithmic elements were reviewed and refined by myself to ensure correctness and understanding.


This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    quests = {}
    try:
        with open(filename, "r") as file:
            quest_data = file.read().strip().split("\n\n")  # Separate quests by blank lines
            for quest_block in quest_data:
                lines = quest_block.splitlines()
                try:
                    quest = parse_quest_block(lines)
                    quests[quest['quest_id']] = quest
                except InvalidDataFormatError as e:
                    raise InvalidDataFormatError(f"Error parsing quest block in {filename}: {e}")
    except FileNotFoundError:
        raise MissingDataFileError(f"{filename} not found.")
    except Exception as e:
        raise CorruptedDataError(f"Error loading {filename}: {str(e)}")
    
    return quests

def load_items(filename="data/items.txt"):
    items = {}
    try:
        with open(filename, "r") as file:
            item_data = file.read().strip().split("\n\n")  # Separate items by blank lines
            for item_block in item_data:
                lines = item_block.splitlines()
                item = parse_item_block(lines)
                items[item['item_id']] = item
    except FileNotFoundError:
        raise MissingDataFileError(f"{filename} not found.")
    except Exception as e:
        raise CorruptedDataError(f"Error loading {filename}: {str(e)}")
    
    return items
    
def validate_quest_data(quest_dict):
    required_fields = ['quest_id', 'title', 'description', 'reward_xp', 'reward_gold', 'required_level', 'prerequisite']
    
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    # Validate reward_xp, reward_gold, required_level to be integers
    for field in ['reward_xp', 'reward_gold', 'required_level']:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Invalid type for {field}: Expected integer")

    # Validate prerequisite is a valid quest_id or "NONE"
    if quest_dict['prerequisite'] != "NONE" and not isinstance(quest_dict['prerequisite'], str):
        raise InvalidDataFormatError(f"Invalid prerequisite value: {quest_dict['prerequisite']}")
    
    return True
def validate_item_data(item_dict):
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    valid_types = ['weapon', 'armor', 'consumable']
    
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}. Must be one of {valid_types}")

    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError(f"Invalid cost value: {item_dict['cost']}. Expected integer")
    
    try:
        stat_name, value = item_dict['effect'].split(":")
        int(value)  # Check that value can be converted to an integer
    except ValueError:
        raise InvalidDataFormatError(f"Invalid effect format: {item_dict['effect']}. Expected 'stat_name:value'")
    
    return True

def create_default_data_files():
    try:
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists("data/quests.txt"):
            with open("data/quests.txt", "w") as file:
                file.write("QUEST_ID: quest_001\nTITLE: Slay the Dragon\nDESCRIPTION: Defeat the dragon terrorizing the village\nREWARD_XP: 100\nREWARD_GOLD: 50\nREQUIRED_LEVEL: 1\nPREREQUISITE: NONE\n")
  
        if not os.path.exists("data/items.txt"):
            with open("data/items.txt", "w") as file:
                file.write("ITEM_ID: health_potion\nNAME: Health Potion\nTYPE: consumable\nEFFECT: health:50\nCOST: 10\nDESCRIPTION: Restores 50 health.\n")
        
    except Exception as e:
        raise CorruptedDataError(f"Error creating data files: {str(e)}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    quest_data = {}
    for line in lines:
        line = line.strip()  # Remove any leading/trailing spaces
        if ": " not in line:
            continue  # Skip lines that don't have the expected ": " delimiter

        try:
            key, value = line.split(": ", 1)
            if key == "QUEST_ID":
                quest_data['quest_id'] = value
            elif key == "TITLE":
                quest_data['title'] = value
            elif key == "DESCRIPTION":
                quest_data['description'] = value
            elif key == "REWARD_XP":
                quest_data['reward_xp'] = int(value)
            elif key == "REWARD_GOLD":
                quest_data['reward_gold'] = int(value)
            elif key == "REQUIRED_LEVEL":
                quest_data['required_level'] = int(value)
            elif key == "PREREQUISITE":
                quest_data['prerequisite'] = value
        except ValueError:
            raise InvalidDataFormatError(f"Invalid format in quest block: {line}")
    
    return quest_data

def parse_item_block(lines):
    item_data = {}
    for line in lines:
        try:
            key, value = line.split(": ", 1)
            if key == "ITEM_ID":
                item_data['item_id'] = value
            elif key == "NAME":
                item_data['name'] = value
            elif key == "TYPE":
                item_data['type'] = value
            elif key == "EFFECT":
                item_data['effect'] = value
            elif key == "COST":
                item_data['cost'] = int(value)
            elif key == "DESCRIPTION":
                item_data['description'] = value
        except ValueError:
            raise InvalidDataFormatError(f"Invalid format in item block: {line}")
    
    return item_data

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

