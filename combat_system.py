"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Che Mullins

AI Usage: This code was developed with assistance from ChatGPT for structure, logic debugging, and syntax improvements. All functional and algorithmic elements were reviewed and refined by myself to ensure correctness and understanding.


Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    if enemy_type == "goblin":
        return {'name': 'Goblin', 'health': 50, 'max_health': 50, 'strength': 8, 'magic': 2, 'xp_reward': 25, 'gold_reward': 10}
    elif enemy_type == "orc":
        return {'name': 'Orc', 'health': 80, 'max_health': 80, 'strength': 12, 'magic': 5, 'xp_reward': 50, 'gold_reward': 25}
    elif enemy_type == "dragon":
        return {'name': 'Dragon', 'health': 200, 'max_health': 200, 'strength': 25, 'magic': 15, 'xp_reward': 200, 'gold_reward': 100}
    else:
        raise InvalidTargetError(f"Invalid enemy type: {enemy_type}")

def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0
    
    def start_battle(self):
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is already dead!")
        
        while self.character['health'] > 0 and self.enemy['health'] > 0:
            self.turn_counter += 1
            if self.turn_counter % 2 == 0:
                self.enemy_turn()
            else:
                self.player_turn()
            
            self.check_battle_end()

        winner = 'player' if self.enemy['health'] <= 0 else 'enemy'
        xp = self.enemy['xp_reward'] if winner == 'player' else 0
        gold = self.enemy['gold_reward'] if winner == 'player' else 0
        return {'winner': winner, 'xp_gained': xp, 'gold_gained': gold}

    
    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        print("\nYour Turn!")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        choice = input("Choose an action: ")
        if choice == "1":
            self.basic_attack()
        elif choice == "2":
            use_special_ability(self.character, self.enemy)
        elif choice == "3":
            if self.attempt_escape():
                self.combat_active = False
                print("You escaped the battle!")
        else:
            print("Invalid choice!")

    
    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        print(f"\n{self.enemy['name']} attacks!")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} dealt {damage} damage!")

    
    def calculate_damage(self, attacker, defender):
        damage = max(1, attacker['strength'] - (defender['strength'] // 4))
        return damage

    
    def apply_damage(self, target, damage):
        target['health'] = max(0, target['health'] - damage)
        display_combat_stats(self.character, self.enemy)

    
    def check_battle_end(self):
        if self.enemy['health'] <= 0:
            print(f"\n{self.enemy['name']} has been defeated!")
            self.combat_active = False
            return 'player'
        elif self.character['health'] <= 0:
            print("\nYou have been defeated!")
            self.combat_active = False
            return 'enemy'
        return None
    
    def attempt_escape(self):
        escape_success = random.choice([True, False])
        if escape_success:
            print("You successfully escaped the battle!")
        else:
            print("Escape attempt failed!")
        return escape_success
        
# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    if character['class'] == 'Warrior':
        warrior_power_strike(character, enemy)
    elif character['class'] == 'Mage':
        mage_fireball(character, enemy)
    elif character['class'] == 'Rogue':
        rogue_critical_strike(character, enemy)
    elif character['class'] == 'Cleric':
        cleric_heal(character)
    else:
        print("Unknown class ability.")

def warrior_power_strike(character, enemy):
    damage = 2 * character['strength']
    enemy['health'] -= damage
    display_battle_log(f"Warrior Power Strike! You dealt {damage} damage.")


def mage_fireball(character, enemy):
    damage = 2 * character['magic']
    enemy['health'] -= damage
    display_battle_log(f"Mage Fireball! You dealt {damage} damage.")


def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        damage = 3 * character['strength']
        enemy['health'] -= damage
        display_battle_log(f"Rogue Critical Strike! You dealt {damage} damage.")
    else:
        display_battle_log("Rogue Critical Strike failed!")


def cleric_heal(character):
    heal_amount = 30
    character['health'] = min(character['health'] + heal_amount, character['max_health'])
    display_battle_log(f"Cleric Heal! You restored {heal_amount} health.")

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    if character['health'] > 0 and not character.get('in_battle', False):
        return True
    return False

def get_victory_rewards(enemy):
     rewards = {
        'xp': enemy.get('xp_reward', 0),  # Default to 0 if no xp_reward key exists
        'gold': enemy.get('gold_reward', 0)  # Default to 0 if no gold_reward key exists
     }

     return rewards

def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    print(f">>> {message}")
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

