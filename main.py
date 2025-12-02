"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Che Mullins

AI Usage: AI assisted with several key aspects of the project, mostly guiding the inheritance and method overriding process.
It also helped refine the game flow, particularly in structuring the main menu, game loop, and handling user inputs effectively. AI played a role in error handling, ensuring that invalid inputs were managed gracefully, and in organizing game data loading and saving.
Through these contributions, AI helped streamline the development process, ensuring the game ran smoothly and provided a seamless user experience.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    print("\nMain Menu:")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    choice = input("Choose an option: ")
    try:
        choice = int(choice)
        if choice in [1, 2, 3]:
            return choice
        else:
            print("Invalid choice. Please choose between 1-3.")
            return main_menu()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return main_menu()
        
def new_game():
     global current_character
    
     name = input("Enter your character's name: ")
     character_class = input("Choose your class (Warrior, Mage, Rogue, Cleric): ")
    
     try:
         current_character = character_manager.create_character(name, character_class)
         print(f"{current_character.name} the {current_character.character_class} has been created!")
         game_loop()  # Start the game loop
     except InvalidCharacterClassError:
         print(f"Error: '{character_class}' is not a valid class. Please try again.")
         new_game()


def load_game():
    global current_character

    saved_characters = ["Character1", "Character2"]  
    
    print("Saved characters:")
    for idx, char in enumerate(saved_characters, 1):
        print(f"{idx}. {char}")
    
    try:
        choice = int(input("Choose a character to load: "))
        current_character = character_manager.load_character(saved_characters[choice-1])
        print(f"{current_character.name} has been loaded.")
        game_loop()  # Start the game loop
    except (ValueError, IndexError):
        print("Invalid choice.")
        load_game()

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            break
        else:
            print("Invalid choice, please select 1-6.")

def game_menu():
    print("\nGame Menu:")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    choice = input("Choose an option: ")
    try:
        choice = int(choice)
        if 1 <= choice <= 6:
            return choice
        else:
            print("Invalid choice. Please choose between 1-6.")
            return game_menu()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return game_menu()

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    print(f"\nCharacter Stats for {current_character.name}:")
    print(f"Class: {current_character.character_class}")
    print(f"Health: {current_character.health}")
    print(f"Strength: {current_character.strength}")
    print(f"Magic: {current_character.magic}")
    print(f"Level: {current_character.level}")
    print(f"XP: {current_character.xp}")


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    print(f"\n{current_character.name}'s Inventory:")
    print("Inventory: Sword, Shield, Potion")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    print("\nQuest Menu:")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest")
    print("7. Back")

def explore():
    """Find and fight random enemies"""
    global current_character
    print(f"\n{current_character.name} is exploring...")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    print(f"\n{current_character.name} is at the shop...")
   

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    try:
        character_manager.save_character(current_character)
        print(f"{current_character.name} has been saved!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    try:
        game_data.load_quests()
        game_data.load_items()
        print("Game data loaded successfully!")
    except Exception as e:
        print(f"Error loading game data: {e}")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    print(f"{current_character.name} has died!")
    choice = input("Do you want to revive for 100 gold? (yes/no): ").lower()
    if choice == "yes":
        if current_character.gold >= 100:
            current_character.gold -= 100
            current_character.health = 100
            print(f"{current_character.name} has been revived!")
        else:
            print("Not enough gold!")
    else:
        print("Game over!")
        game_running = False


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

