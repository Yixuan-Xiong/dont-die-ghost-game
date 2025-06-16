import json

# Ask Chatgpt load initial values from config.json
# Get the current directory path
import os

current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

# Player class
class Player:
    # Initial data of player name, status, and survival status
    def __init__(self, name):
        self.name = name
        self.health = config["initial_health"]
        self.sanity = config["initial_sanity"]
        self.fear = 0
        self.alive = True
    
    # Reduce health & sanity and increase fear when the player takes damage
    def take_damage(self, amount, sanity_loss, fear_increase):
        self.health -= amount
        self.sanity -= sanity_loss
        self.fear += fear_increase
        print(f"\n*** You lose {amount} health, {sanity_loss} sanity, and gain {fear_increase} fear ***")
        if self.health <= 0 or self.sanity <= 0:
            self.alive = False

    # Resets the player’s status to their initial values, allowing them to start a new game.
    def reset(self):
        self.health = config["initial_health"]
        self.sanity = config["initial_sanity"]
        self.fear = 0
        self.alive = True
    
    # Displays the player’s current stats
    def show_status(self):
        print(f"\n{self.name}, here's your current status:")
        print(f"      Health: {self.health}")
        print(f"      Sanity: {self.sanity}")
        print(f"      Fear Level: {self.fear}")
        if self.alive == True:
            print("      Alive: Yes")
        else:
            print("      Alive: No")
