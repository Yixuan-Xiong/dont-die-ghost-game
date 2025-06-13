from dont_die_game.chatbot_base import ChatbotBase
from dont_die_game.player import Player
from dont_die_game.game_bot import GameBot
from dont_die_game.constants import ghost_types, tools

class MyChatbot(ChatbotBase):
    # Initial
    def __init__(self):
        super().__init__()
        self.conversation_is_active = True
        self.player = None
        self.game_bot = None
    
    # Start-greeting
    def greeting(self):
        print("Welcome to 'Don't Die'! Please be safe and catch the ghost!")
        self.player_setup()
    
    # Start-game 
    def player_setup(self):
        player_name = input("What is your name?\n> ")
        bot_name = input("What would you like to call me?\n> ")
        self.game_bot = GameBot(name=bot_name)
        self.player = Player(name=player_name)
        self.game_bot.introduce(player_name)
        self.game_bot.explain_rules()
        self.game_bot.start_game()
    
    # Respond for every choice
    def respond(self):
        while self.conversation_is_active:
            if not self.player.alive:
                print(f"\n{self.game_bot.name}: Unfortunately, you are dead. The game is over.")
                replay_response = self.ask_replay()
                if replay_response:
                    self.player.reset()
                    self.game_bot.start_game()
                else:
                    break
            
            # Show what you can do
            print("\nWhat would you like to do?")
            commands = [
                "Tool: Use a tool to search for evidence.",
                "Evidence: Review collected evidence.",
                "Guess: Guess the ghost type.",
                "All ghosts: View all ghost types and required evidence.",
                "Hint: Get a hint from your bot.",
                "Status: Check your current status.",
                "Quit: Quit the game."
            ]
            for command in commands:
                print(f"  - {command}")
            user_input = input("\n> ").strip().lower()
            
            # Detect key words
            action = self.game_bot.detect_keywords_rake(user_input)
            
            # Choose tool
            if action == "tool":
                # tool loop
                while True:
                    print("\nYou can use one of these tools:")
                    for tool in tools:
                        print(f"  - {tool}")
                    tool_choice = input("\nWhich tool would you like to use?\n> ").strip()

                    # valid tool choice
                    valid_tools_lower = []
                    for t in tools:
                        valid_tools_lower.append(t.lower())
                    
                    tool_choice_lower = tool_choice.lower()
                    if tool_choice_lower in valid_tools_lower:
                        self.game_bot.use_tool(tool_choice)
                        break
                    else:
                        print(f"\nInvalid tool. Please choose a valid tool from the list.")
            
            # Choose review
            elif action == "evidence":
                self.game_bot.review_evidence(self.player.name)
            
            # Choose guess
            elif action == "guess":
                print("\nHere are the valid ghosts you can guess:")
                for ghost in ghost_types.keys():
                    print(f"  - {ghost}")
                guess = input("\nWhich ghost do you think it is?\n> ").strip()
                    
                # Valid guess
                valid_ghosts_lower = []
                for ghost in ghost_types.keys():
                    valid_ghosts_lower.append(ghost.lower())
                    
                #guess the ghosts
                guess_lower = guess.lower()
                if guess_lower in valid_ghosts_lower:
                    guess_correct = self.game_bot.check_guess(guess, self.player)
                    if guess_correct:
                        replay_response = self.ask_replay()
                        if replay_response:
                            self.player.reset() 
                            self.game_bot.start_game()
                        else:
                            self.conversation_is_active = False
                            break
                    else:
                        break
                else:
                    print("\nInvalid guess. Please choose a valid ghost from the list.")

            # Choose all ghosts
            elif action == "all ghosts":
                self.game_bot.show_all_ghosts()
            
            # Choose hint
            elif action == "hint":
                self.game_bot.give_hint(self.player, self.player.name)
            
            # Choose status
            elif action == "status":
                self.player.show_status()
            
            # Choose quit
            elif action == "quit":
                self.conversation_is_active = False
                self.game_bot.end_game()
                break
            else:
                print(f"\n{self.game_bot.name}: I can't understand. Please try again.")

            self.game_bot.check_round_attack(self.player)
    
    def ask_replay(self):
        while True:
            replay = input(f"\n{self.game_bot.name}: Would you like to play another game? (yes/no)\n> ").strip().lower()
            if replay == "yes":
                return True
            elif replay == "no":
                return False
            else:
                print(f"\n{self.game_bot.name}: I don't understand. Please type 'yes' or 'no'.")

    # Ending
    def farewell(self):
        self.game_bot.end_game()
        print(f"\n{self.game_bot.name}: Thanks for playing 'Don't Die'. See you next time! Goodbye!") 
