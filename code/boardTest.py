from src.board import Board
from src.particles import Particle
import unittest


class BoardTest(unittest.TestCase):

    def test_boardConstructor(self):
        b = Board(5, 5, 3)
        self.assertEqual([b.x_m, b.y_m], [5, 5])
        self.assertEqual(len(b.board), 5)
        self.assertEqual(len(b.board[0]), 5)
        self.assertEqual(b.killer, -1)
        self.assertEqual(b.victim, -1)
        self.assertEqual(b.phase, 0)
        self.assertEqual([b.corpse_x, b.corpse_y], [-1, -1])
        self.assertEqual(b.time_left, 35)
        self.assertEqual(b.ended, False)
        for player in b.players:
            self.assertIsInstance(player, Particle)
        self.assertEqual(len(b.players), 3)

    def test_alive_players(self):
        b = Board(5, 5, 3)
        player = b.players[0]
        player.die()
        alive_p = b.alive_players()
        self.assertEqual(len(alive_p), 2)

    def test_murder(self):
        b = Board(5, 5, 3)
        b.commit_murder(b.players[0], b.players[1])
        victim = b.players[1]
        killer = b.players[0]
        self.assertFalse(victim.alive)
        self.assertEqual(b.killer, killer.id)
        self.assertEqual(b.victim, victim.id)
