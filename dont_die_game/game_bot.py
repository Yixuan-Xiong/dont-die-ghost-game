import random
import json
from dont_die_game.constants import ghost_types, evidence_tool_map, tools
from dont_die_game.utils.keywords_extractor import extract_keywords

# Ask Chatgpt load initial values from config.json
# Get the current directory path
import os

current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

# GameBot class
class GameBot:
    # Define the GameBot
    def __init__(self, name):
        self.greetings = ["Hi", "Hello", "Hey", "Howdy", "Yo", "What's up"]
        self.name = name
        self.current_ghost = None
        self.collected_evidence_by_tool = []
        self.round_count = 0  
        self.attack_level = 1  
        self.active = True  
    
    # Set random greeting
    def introduce(self, player_name):
        greeting = random.choice(self.greetings)
        print(f"\n{self.name}: {greeting} {player_name}! My name is {self.name}. Please be safe and don't die!")
    
    # Explain the game rules
    def explain_rules(self):
        print("\nGAME RULES:")
        rules = [
            "1. Identify the ghost haunting the location by collecting evidence.",
            "2. There are 6 ghost types, each requiring 3 specific pieces of evidence for identification.",
            "3. Use 7 different investigative tools to gather evidence. Each tool is effective for specific types of evidence.",
            "4. Once you think you know the ghost type, make a guess. If you're wrong, the ghost will attack!",
            "5. The ghost becomes more aggressive over time. Every 5 rounds, it attacks, reducing your health, sanity, and increasing your fear.",
            "6. You can ask for hints, but it will increase your fear and decrease your sanity.",
        ]
        for rule in rules:
            print(rule)
        input("\n[Press Enter to continue...]")

    def start_game(self):
        # Randomly select a ghost type
        ghost_list = list(ghost_types.keys())
        ghost_index = random.randint(0, len(ghost_list) - 1)
        self.current_ghost = ghost_list[ghost_index]
        self.selected_evidence = ghost_types[self.current_ghost]

        # Reset evidence collection
        self.collected_evidence_by_tool = []
        # Reset round count
        self.round_count = 0
        self.attack_level = 1
        self.active = True

        print(f"\n{self.name}: OMG! There's a ghost in this place. Be careful!")
        # Display ghost ASCII Art
        self.show_ghost_art(self.current_ghost)
    
    # Ghost ASCII Art
    def show_ghost_art(self, ghost_type):
        arts = {
            "Spirit": r"""
               .-"      "-.
              /            \
             |,  .-.  .-.  ,|
             | )(_o/  \o_)( |
             |/     /\     \|
             (_     ^^     _)
              \__|IIIIII|__/
               | \IIIIII/ |
               \          /
                 --------
            """,
            "Banshee": r"""
               .-"      "-.
              /    .--.    \
             |   ( o  o )   |
             |    \ -- /    |
              \    '--'    /
               '--.____.--'
                 /      \
                (        )
                 \______/
            """,
            "Yokai": r"""
               .-"       "-.
              /   \          /
             |     O        O|
             |       .-----. |
              \     /     /  /
               '-.__|    |_.' 
            """,
            "Thaye": r"""
              .-'         '-.
             /    .----.     \
            |   ( o  o )      |
            |    \ -- /       |
             \     '--'      /
              '-._________.-'
            """,
            "Demon": r"""
                ,     ,
               (o     o)
                \ (X) /
                 \___/
                .-'   '-.
               /         \
              /___________\
            """,
            "Yurei": r"""
               .-"       "-.
              /             \
             |   O       O   |
             |      (_)      |
              \     ___     /
               '-._______.-'
            """
        }
        print(arts[ghost_type])

    def detect_keywords(self, user_input):
        # Define action keywords
        extracted_keywords = extract_keywords(user_input)
        keywords_map = {
            "tool": ["tool", "use tool", "tools", "use", "find"],
            "evidence": ["review", "check", "see", "have","evidence"],
            "guess": ["guess", "make a guess", "guessing", "identify ghost", "know"],
            "all ghosts": ["all ghosts", "ghost list", "ghosts", "requirements", "show ghosts", "ghost types", "need"],
            "hint": ["hints", "help", "clue", "hint"],
            "status": ["status", "health", "sanity", "fear", "check status"],
            "quit": ["quit", "exit", "leave", "stop", "end"],
        }

        # Check for matching actions
        for action in keywords_map.keys():
            for keyword in keywords_map[action]:
                for extracted in extracted_keywords:
                    if keyword in extracted:
                        return action
        
        # If no action matches, return None
        return None
    
    # Use tool
    def use_tool(self, tool):
        tool_lower = tool.lower()
        valid_tools_lower = []
        for t in tools:
            valid_tools_lower.append(t.lower())
        if tool_lower not in valid_tools_lower:
            print("\nInvalid tool. Here are the valid tools you can use:")
            for t in tools:
                print(f"  - {t}")
            return
        
        #  Find the original tool name
        name_tool = None
        index = 0
        while index < len(valid_tools_lower):
            if valid_tools_lower[index] == tool_lower:
                name_tool = tools[index]
                break
            index += 1   # Ask gpt to help me
        
        # Find possible evidence for the tool
        possible_evidence = []
        for evidence, tool_name in evidence_tool_map.items():
            if tool_name.lower() == tool_lower:
                possible_evidence.append(evidence)

        effective = random.choice([True, False])
        if effective == True:
            found_evidence = []
            for evidence in possible_evidence:
                if evidence in self.selected_evidence:
                    found_evidence.append(evidence)
            
            # Reply (reandom)
            if len(found_evidence) > 0:
                evidence_found = random.choice(found_evidence)
                if evidence_found not in self.collected_evidence_by_tool:
                    self.collected_evidence_by_tool.append(evidence_found)
                    print(f"\n{self.name}: Using the {name_tool}, you discovered '{evidence_found}'! Great work!")
                else:
                    print(f"\n{self.name}: The {name_tool} worked, but you've already found '{evidence_found}'.")
            else:
                print(f"\n{self.name}: The {name_tool} is working fine, but no relevant evidence was found.")
        else:
            print(f"\n{self.name}: The {name_tool} didn't reveal any evidence this time. Let's try another tools")
    
    # Give hints
    def give_hint(self, player, player_name):
        remaining_evidence = []
        # Only hints at evidence not found
        for evidence in self.selected_evidence:
            if evidence not in self.collected_evidence_by_tool:
                remaining_evidence.append(evidence)

        if len(remaining_evidence) > 0:
            hint = random.choice(remaining_evidence)
            print(f"\n{self.name}: {player_name}, maybe we should focus on tools that can detect '{hint}'?")
        else:
            print(f"\n{self.name}: {player_name}, we have already collected all possible evidence. Time to make a guess!")
        
        # Setup hints' damage
        player.fear += 5
        player.sanity -= 3
        print(f"\n*** Using hints makes you uneasy. You lose 3 sanity and gain 5 fear! ***")
    
    # Check the attack(each 5 round)
    def check_round_attack(self, player):
        if not self.active:
            return
        # Print round
        self.round_count += 1
        print(f"\n\033[1mROUND {self.round_count}\033[0m")  # Bold
        # Each 5 round get attack
        if self.round_count % config["attack_interval"] == 0:
            print(f"\n*** It's the {self.round_count}th round! Watch out for attacks! ***")
            self.ghost_attack(player)
    
    # Set the damage of the ghost's attack (initial increase)
    def ghost_attack(self, player):
        damage = config["damage_base"] + (self.attack_level * config["damage_increase_per_level"])
        sanity_loss = config["sanity_loss_base"] + (self.attack_level * config["sanity_loss_increase"])
        fear_increase = config["fear_increase_base"] + self.attack_level
        self.attack_level += 1
        print(f"\n{self.name}: The ghost attacked us!")
        player.take_damage(damage, sanity_loss, fear_increase)
    
    # Review evidence
    def review_evidence(self, player_name):
        if len(self.collected_evidence_by_tool) > 0:
            evidence_str = ""
            for evidence in self.collected_evidence_by_tool:
                if evidence_str == "":
                    evidence_str = evidence
                else:
                    evidence_str += ", " + evidence  # Ask gpt to help me

            print(f"{self.name}: {player_name}, Evidence found with tools: {evidence_str}.")
        else:
            print(f"{self.name}: {player_name}, No evidence has been found with tools yet.")
    
    # Show all the type of ghosts
    def show_all_ghosts(self):
        print(f"\n{self.name}: Here's the evidence required for each ghost:")
        for ghost in ghost_types.keys():
            evidence_list = ghost_types[ghost]
            tools_used = []

            for evidence in evidence_list:
                tools_used.append(evidence_tool_map[evidence])
            
            # list all the type
            evidence_str = ""
            for evidence in evidence_list:
                if evidence_str == "":
                    evidence_str = evidence
                else:
                    evidence_str += ", " + evidence  

            tools_str = ""
            for tool in tools_used:
                if tools_str == "":
                    tools_str = tool
                else:
                    tools_str += ", " + tool

            print(f"  - {ghost}: {evidence_str} (Tools: {tools_str})")  # Ask gpt to help me

    # Check the answer
    def check_guess(self, guess, player):
        guess_lower = guess.lower()
        valid_ghosts_lower = []
        for ghost in ghost_types.keys():
            valid_ghosts_lower.append(ghost.lower())

        if guess_lower not in valid_ghosts_lower:
            print("\nI can't understand. Here are the valid ghosts you can guess:")
            for ghost in ghost_types.keys():
                print(f"  - {ghost}")
            return False
        
        #  Find the original tool name
        name_ghost = None
        index = 0
        while index < len(valid_ghosts_lower):
            if valid_ghosts_lower[index] == guess_lower:
                ghost_list = list(ghost_types.keys())
                name_ghost = ghost_list[index]
                break
            index += 1 

        if name_ghost == self.current_ghost:
            print(f"\n{self.name}: Incredible! You correctly identified the ghost as {name_ghost}. Well done, {player.name}!")
            self.active = False
            return True
        else:
            print(f"\n{self.name}: No! The ghost is angry that you called it a {name_ghost}. It attacks!")
            # Set wrong answer damge
            player.take_damage(30, 10, 5)
            return False
    
    def end_game(self):
        self.active = False
