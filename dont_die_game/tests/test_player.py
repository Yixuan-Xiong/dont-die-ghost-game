# Ask Chatgpt help me write the test

import unittest
from dont_die_game.player import Player

class TestPlayer(unittest.TestCase):
    # Unit tests for the Player class in the Don't Die game
    def test_initial_status(self):
        # Test that a new player has correct default values
        player = Player("Tester")
        self.assertEqual(player.health, 100)
        self.assertEqual(player.sanity, 100)
        self.assertEqual(player.fear, 0)
        self.assertTrue(player.alive)

    def test_take_damage(self):
        # Test that taking damage correctly reduces stats
        player = Player("Tester")
        player.take_damage(20, 30, 10)
        self.assertEqual(player.health, 80)
        self.assertEqual(player.sanity, 70)
        self.assertEqual(player.fear, 10)

    def test_reset(self):
        # Test that resetting the player restores all stats
        player = Player("Tester")
        player.take_damage(20, 30, 10)
        player.reset()
        self.assertEqual(player.health, 100)
        self.assertEqual(player.sanity, 100)
        self.assertEqual(player.fear, 0)
        self.assertTrue(player.alive)
