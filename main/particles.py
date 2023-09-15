import random


class Particle:
    """
    Class that models a particle (agent) in the system.

    Attributes
    ----------
    id: int
        ID of the particle
    x: Int
        Coordinate x of the particle
    y: Int
        Coordinate y of the particle
    x_max: Int
        Maximum coordinate x that the particle x value can have
    y_max: Int
        Maximum coordinate y that the particle y value can have
    alive: bool
        Boolean that records the living state of the particle
    neighbors: list
        List of the particle's affinity with the neighbors
    despair: Int
        Number that represents the despair or stress level of the particle
    suspicious:

    neighborhood_size: Int
        Size of the neighborhood vision
    """

    def __init__(self, p_id, x_max, y_max, neighborhood_size=1, world_array=None, x_0=None, y_0=None):
        """
        Particle class constructor

        Parameters
        ----------
        p_id: int
            Identifier of the particle
        x_max: int
            Maximum x coordinate
        y_max: int
            Minimum y coordinate
        neighborhood_size: int
            Size of the particle neighborhood_size
        world_array: list
            Array with all the available spaces and the particles that represents the model of the world
        x_0: int
            Initial x coordinate
        y_0: int
            Initial y coordinate
        """
        self.id = p_id  # This will help to check the position of each neighbor
        self.x = x_0 if x_0 is not None else random.randint(0, x_max - 1)
        self.y = y_0 if y_0 is not None else random.randint(0, y_max - 1)
        self.x_max = x_max
        self.y_max = y_max
        self.alive = True
        self.neighbors = []  # Neighbors of the particle, this list will have the affinity with each neighbor
        self.despair = 0
        self.suspicious = None
        self.neighborhood_size = neighborhood_size  # Neighborhood vision size
        if world_array:
            world_array[self.x][self.y] = id

    def fill_affinity_list(self, neighbors_amount):
        """
        Function that fills the neighbors affinity list of a particle, every particle has in the position i
        the level of affinity with the particle i. On the position with itself the array will have a -1 and
        the affinity amount will randomly begin with numbers between 4 and 6 to make available the interaction.

        Parameters
        ----------
        neighbors_amount: int
            Total number of neighbors
        """
        neighbors = [0] * neighbors_amount
        for i in range(0, neighbors_amount):
            neighbors[i] = random.randint(40, 60)
        neighbors[self.id] = -1
        self.neighbors = neighbors

    def calculate_neighborhood(self, diameter=1):  # TODO: For the moment only works with diameter = 1
        """
        Function that calculates the coordinates that belong to the particle neighborhood

        Parameters
        ----------
        diameter: int
         Diameter used to calculate the coordinates
        Returns
        -------
        list
            The coordinates that represent the neighborhood
        """
        neighborhood = []
        x_m = self.x_max
        y_m = self.y_max
        for i in range(0, diameter):
            v1 = [(self.x + 1 + i) % x_m, (self.y + i) % y_m]  # N
            v2 = [(self.x - 1 + i) % x_m, (self.y + i) % y_m]  # S
            v3 = [(self.x + 1 + i) % x_m, (self.y + 1 + i) % y_m]  # NE
            v4 = [(self.x + 1 + i) % x_m, (self.y - 1 + i) % y_m]  # NW
            v5 = [(self.x - 1 + i) % x_m, (self.y + 1 + i) % y_m]  # SE
            v6 = [(self.x - 1 + i) % x_m, (self.y - 1 + i) % y_m]  # SW
            v7 = [(self.x + i) % x_m, (self.y + 1 + i) % y_m]  # E
            v8 = [(self.x + i) % x_m, (self.y - 1 + i) % y_m]  # W
            neighborhood += [v1, v2, v3, v4, v5, v6, v7, v8]
        return neighborhood

    def move(self, world_array):
        """
        Function that randomly moves a particle into a new free space. `world_array` is the board
        where the interactions are happening.
        Parameters
        ----------
        world_array: list
            Array with all the available spaces and the particles that represents the model of the world
        """
        # Number Direction
        #    1       N
        #    2       NE
        #    3       E
        #    4       SE
        #    5       S
        #    6       SW
        #    7       W
        #    8       NW
        position_settled = False
        posible_spaces = self.calculate_neighborhood()
        position = posible_spaces[random.randint(0, len(posible_spaces) - 1)]
        iteration = 0
        while not position_settled and posible_spaces:
            if world_array[position[0]][position[1]] == -1:
                # The position is empty
                world_array[position[0]][position[1]] = self.id
                world_array[self.x][self.y] = -1  # Shuffle the values of `world_array`
                self.x = position[0]
                self.y = position[1]
                position_settled = True
            else:
                posible_spaces.remove(position)
                position = posible_spaces[random.randint(0, len(posible_spaces) - 1)]  # TODO: Check using shuffle

    def despair(self):
        """
        Function that modifies the `despair` level of a particle, this happens when there is an incentive. The
        maximum amount is 20.
        """
        amount = random.randint(1, 3)
        self.despair += amount
        if self.despair > 20:
            self.despair = 20

    def calculate_near_neighbors(self, world_array):
        """
        Function that calculates the near neighbors of the particle
        Parameters
        ----------
        world_array: list
            Array with all the available spaces and the particles that represents the model of the world
        Returns
        -------
        list
            All the neighbors in the neighborhood
        """
        neighborhood = self.calculate_neighborhood()
        neighbors = []
        for i in neighborhood:
            if world_array[i[0]][i[1]] != -1:
                # We save the position of the neighbor
                neighbors.append(world_array[i[0]][i[1]])
        return neighbors

    def die(self):
        """
        Function that models the death of a particle
        """
        self.alive = False
        self.x = -100
        self.y = -100
        self.despair = 0
        self.suspicious = None
