from src.particles import Particle
import unittest


class ParticleTest(unittest.TestCase):

    def test_particle_constructor(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        p = Particle(1, 5, 5, 2, world)
        self.assertEqual(p.alive, True, 'The particle should start being alive')
        self.assertEqual(p.neighbors, [], 'At the beginning the neighbors list is empty')
        self.assertEqual(p.despair, 0, 'At the beginning the despair should be 0')
        self.assertEqual(p.id, 1, 'The ID should be equal to the parameter')

    def test_fill_affinity_list(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        p = Particle(1, 5, 5, 2, world)
        p.fill_affinity_list(5)
        self.assertEqual(len(p.neighbors), 5, 'It should have the affinity with the 5 neighbors')
        for i in p.neighbors:
            minus_1 = i == -1
            neutral_range = 60 >= i >= 40
            self.assertTrue(minus_1 or neutral_range, 'At the beginning the affinity list hast to be -1 or '
                                                      'between 40 and 60')

    def test_update_despair(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        p = Particle(1, 5, 5, 2, world)
        p.update_despair()
        self.assertIsInstance(p.despair, int)
        self.assertGreater(p.despair, 0)

    def test_calculate_neighborhood(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        p = Particle(1, 5, 5, 2, world, 1, 1)
        neighborhood_1 = p.calculate_neighborhood(1)
        self.assertEqual(len(neighborhood_1), 8, 'With diameter = 1 and no neighbors cells in the boundaries, the total'
                                                 'neighborhood cells are 9')
        neighborhood_2 = p.calculate_neighborhood(2)
        self.assertEqual(len(neighborhood_2), 15, 'With diameter = 2 and neighbors cells in the boundaries, the total'
                                                  'neighborhood cells are 15')
        p_2 = Particle(1, 5, 5, 2, world, 2, 2)
        neighborhood_p2 = p_2.calculate_neighborhood(2)
        self.assertEqual(len(neighborhood_p2), 24, 'With diameter = 2 and no neighbors cells in the boundaries, '
                                                   'the total neighborhood cells are 24')
        p_3 = Particle(1, 5, 5, 2, world, 4, 4)
        neighborhood_p3 = p_3.calculate_neighborhood(2)
        self.assertEqual(len(neighborhood_p3), 8, 'With diameter = 2 and many neighbors cells in the boundaries, '
                                                  'the total neighborhood cells are 8')

    def test_move(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        p = Particle(1, 5, 5, 2, world, 1, 1)
        p.move(world, 2)
        self.assertIsNot([p.x, p.y], [1, 1], 'Because world just have one particle, then '
                                             'the coordinates should change')
        world_2 = [[9 for _ in range(5)] for _ in range(5)]
        p_1 = Particle(1, 5, 5, 2, world_2, 1, 1)
        p_1.move(world_2, 2)
        self.assertEqual([p_1.x, p_1.y], [1, 1], 'Because world does not have free spaces, then the particle stays'
                                                 'in the same cell')

    def test_calculate_near_neighbors(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        world[0][0] = 2
        world[0][1] = 5
        p = Particle(1, 5, 5, 2, world, 1, 1)
        neighbors = p.calculate_near_neighbors(world)
        self.assertEqual(len(neighbors), 2, 'The world has 2 neighbors near the particle')
        neighbors.sort()
        self.assertEqual(neighbors, [2, 5])

    def test_average_affinity(self):
        world = [[-1 for _ in range(5)] for _ in range(5)]
        p = Particle(1, 5, 5, 2, world, 1, 1)
        p.fill_affinity_list(5)
        affinity_list = p.neighbors
        af_average = 0
        total = 0
        for affinity in affinity_list:
            if affinity > 0:
                af_average += affinity
                total += 1
        self.assertEqual(p.affinity_avg(), af_average / total)
