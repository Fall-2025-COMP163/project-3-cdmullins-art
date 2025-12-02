"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Che Mullins

AI Usage: AI assisted with several key aspects of the project, mostly guiding the inheritance and method overriding process. 
It also helped refine the game flow, particularly in structuring the main menu, game loop, and handling user inputs effectively. AI played a role in error handling, ensuring that invalid inputs were managed gracefully, and in organizing game data loading and saving. 
Through these contributions, AI helped streamline the development process, ensuring the game ran smoothly and provided a seamless user experience.

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest_data = quest_data_dict[quest_id]
    
    # Check if character's level meets the required level for the quest
    if character['level'] < quest_data['required_level']:
        raise InsufficientLevelError(f"{character['name']} does not meet the level requirement for '{quest_id}'.")

    # Check if the quest has a prerequisite and if it has been completed
    if quest_data['prerequisite'] != 'NONE' and quest_data['prerequisite'] not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' requires completing '{quest_data['prerequisite']}' first.")

    # Accept the quest and add to active_quests
    character['active_quests'].append(quest_id)
    print(f"Quest '{quest_id}' accepted by {character['name']}.")
def complete_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    quest_data = quest_data_dict[quest_id]
    
    # Remove from active quests and add to completed quests
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    
    # Grant rewards
    character['xp'] += quest_data['reward_xp']
    character['gold'] += quest_data['reward_gold']
    
    # Return reward summary
    return {
        'reward_xp': quest_data['reward_xp'],
        'reward_gold': quest_data['reward_gold']
    }


def abandon_quest(character, quest_id):
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    character['active_quests'].remove(quest_id)
    print(f"Quest '{quest_id}' abandoned.")
    return True

def get_active_quests(character, quest_data_dict):
    active_quests_data = []
    for quest_id in character['active_quests']:
        if quest_id in quest_data_dict:
            active_quests_data.append(quest_data_dict[quest_id])
    return active_quests_data

def get_completed_quests(character, quest_data_dict):
   completed_quests_data = []
   for quest_id in character['completed_quests']:
       if quest_id in quest_data_dict:
          completed_quests_data.append(quest_data_dict[quest_id])
   return completed_quests_data

def get_available_quests(character, quest_data_dict):
    available_quests = []
    for quest_id, quest_data in quest_data_dict.items():
        if quest_data['required_level'] <= character['level'] and \
           quest_data.get('prerequisite', 'NONE') in character['completed_quests'] and \
           quest_id not in character['active_quests'] and \
           quest_id not in character['completed_quests']:
            available_quests.append(quest_data)
    return available_quests


# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character['completed_quests']

def is_quest_active(character, quest_id):
    return quest_id in character['active_quests']

def can_accept_quest(character, quest_id, quest_data_dict):
    try:
        accept_quest(character, quest_id, quest_data_dict)
        return True
    except (QuestNotFoundError, InsufficientLevelError, QuestRequirementsNotMetError, QuestAlreadyCompletedError):
        return False
        
def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest_data = quest_data_dict[quest_id]
    prerequisite_chain = [quest_id]
    
    while quest_data.get('prerequisite', 'NONE') != 'NONE':
        prerequisite_id = quest_data['prerequisite']
        if prerequisite_id not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite quest '{prerequisite_id}' not found.")
        prerequisite_chain.insert(0, prerequisite_id)
        quest_data = quest_data_dict[prerequisite_id]
    
    return prerequisite_chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total_quests = len(quest_data_dict)
    completed_quests = len(character['completed_quests'])
    return (completed_quests / total_quests) * 100 if total_quests > 0 else 0
    
def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = sum(quest_data_dict[quest_id]['reward_xp'] for quest_id in character['completed_quests'] if quest_id in quest_data_dict)
    total_gold = sum(quest_data_dict[quest_id]['reward_gold'] for quest_id in character['completed_quests'] if quest_id in quest_data_dict)
    return {'total_xp': total_xp, 'total_gold': total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [quest_data for quest_id, quest_data in quest_data_dict.items() if min_level <= quest_data['required_level'] <= max_level]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data.get('prerequisite', 'NONE')}")
    print(f"Rewards: XP = {quest_data['reward_xp']}, Gold = {quest_data['reward_gold']}")


def display_quest_list(quest_list):
    for quest_data in quest_list:
        print(f"{quest_data['title']} - Level {quest_data['required_level']} - XP: {quest_data['reward_xp']} Gold: {quest_data['reward_gold']}")
         
def display_character_quest_progress(character, quest_data_dict):
    active_count = len(character['active_quests'])
    completed_count = len(character['completed_quests'])
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print(f"\nQuest Progress for {character['name']}:")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {completion_percentage:.2f}%")
    print(f"Total XP Earned: {total_rewards['total_xp']}")
    print(f"Total Gold Earned: {total_rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for quest_id, quest_data in quest_data_dict.items():
        prerequisite = quest_data.get('prerequisite', 'NONE')
        
        if prerequisite != 'NONE':
            
            if prerequisite not in quest_data_dict:
                raise QuestNotFoundError(f"Prerequisite quest '{prerequisite}' not found for quest '{quest_id}'.")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

