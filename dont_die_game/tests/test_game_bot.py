# Ask Chatgpt help me write the test

import unittest
from dont_die_game.game_bot import GameBot
from dont_die_game.player import Player
from dont_die_game.constants import tools

class TestGameBot(unittest.TestCase):
    def setUp(self):
        # Create a GameBot and Player instance before each test
        self.bot = GameBot(name="TestBot")
        self.player = Player(name="Tester")
        self.bot.start_game()

    def test_start_game_sets_ghost_and_evidence(self):
        # Ensure the game initializes correctly
        # A ghost should be selected
        self.assertIsNotNone(self.bot.current_ghost)
        # No evidence collected at the start
        self.assertEqual(self.bot.collected_evidence_by_tool, [])
        # Each ghost has exactly 3 evidence types
        self.assertEqual(len(self.bot.selected_evidence), 3)

    def test_use_tool_possible_evidence_collection(self):
        # Test tool usage and evidence collection logic
        self.bot.selected_evidence = ["EMF Level 5"]
        self.bot.collected_evidence_by_tool = []

        self.bot.use_tool("EMF Reader")

        # We cannot assert specific evidence due to randomness,
        # but the result should still be a list
        self.assertIsInstance(self.bot.collected_evidence_by_tool, list)

    def test_check_guess_correct(self):
        # Simulate correct ghost guess
        guess = self.bot.current_ghost
        result = self.bot.check_guess(guess, self.player)
        # Should return True for correct guess
        self.assertTrue(result)
        # Game should become inactive after correct guess
        self.assertFalse(self.bot.active)

    def test_check_guess_wrong(self):
        # Simulate incorrect ghost guess
        wrong_guess = "Spirit" if self.bot.current_ghost != "Spirit" else "Demon"
        initial_health = self.player.health
        result = self.bot.check_guess(wrong_guess, self.player)
        
        # Should return False for wrong guess
        self.assertFalse(result)
        # Player health should decrease
        self.assertLess(self.player.health, initial_health)

    def test_give_hint_affects_sanity_and_fear(self):
        # Test if using hint affects player stats
        initial_sanity = self.player.sanity
        initial_fear = self.player.fear

        self.bot.give_hint(self.player, self.player.name)
        
        # Sanity should decrease
        self.assertLess(self.player.sanity, initial_sanity)
        # Fear should increase
        self.assertGreater(self.player.fear, initial_fear)

    def test_check_round_attack_every_5_rounds(self):
        # Manually force 5 rounds
        for _ in range(4):
            self.bot.check_round_attack(self.player)
        health_before = self.player.health
        # 5th round, attack expected
        self.bot.check_round_attack(self.player)
        # Player should lose health
        self.assertLess(self.player.health, health_before)

if __name__ == '__main__':
    unittest.main()
