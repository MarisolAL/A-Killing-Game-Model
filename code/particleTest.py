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
