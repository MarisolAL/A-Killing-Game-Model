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
        self.assertEqual(b.murder, None)
        for player in b.players:
            self.assertIsInstance(player, Particle)
        self.assertEqual(len(b.players), 3)

    

    
