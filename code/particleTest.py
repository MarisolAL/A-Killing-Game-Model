from src.particles import Particle
import unittest


class ParticleTest(unittest.TestCase):

    def test_particle_constructor(self):
        world = [[-1 for x in range(5)] for y in range(5)]
        p = Particle(1, 5, 5, 2, world)
        self.assertEqual(p.alive, True, 'The particle should start being alive')
        self.assertEqual(p.neighbors, [], 'At the beginning the neighbors list is empty')
        self.assertEqual(p.despair, 0, 'At the beginning the despair should be 0')
        self.assertEqual(p.id, 1, 'The ID should be equal to the parameter')

    def test_fill_affinity_list(self):
        world = [[-1 for x in range(5)] for y in range(5)]
        p = Particle(1, 5, 5, 2, world)
        p.fill_affinity_list(5)
        self.assertEqual(len(p.neighbors), 5, 'It should have the affinity with the 5 neighbors')
        for i in p.neighbors:
            minus_1 = i == -1
            neutral_range = 60 >= i >= 40
            self.assertTrue(minus_1 or neutral_range, 'At the beginning the affinity list hast to be -1 or '
                                                      'between 40 and 60')

    def test_update_despair(self):
        world = [[-1 for x in range(5)] for y in range(5)]
        p = Particle(1, 5, 5, 2, world)
        p.update_despair()
        self.assertIsInstance(p.despair, int)
        self.assertGreater(p.despair, 0)
