import random


class Particle:
    """
    Class that models a particle (agent) in the system.

    Attributes
    ----------
    id: int
        ID of the particle
    x: int
        Coordinate x of the particle
    y: int
        Coordinate y of the particle
    x_max: int
        Maximum coordinate x that the particle x value can have
    y_max: int
        Maximum coordinate y that the particle y value can have
    alive: bool
        Boolean that records the living state of the particle
    neighbors: list
        List of the particle's affinity with the neighbors
    despair: int
        Number that represents the despair or stress level of the particle
    suspect: int
        ID of the particle that the agent suspects committed the crime
    neighborhood_size: int
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
        self.suspect = None
        self.neighborhood_size = neighborhood_size  # Neighborhood vision size
        if world_array:
            world_array[self.x][self.y] = self.id

    def fill_affinity_list(self, neighbors_amount):
        """
        Function that fills the neighbors affinity list of a particle, every particle has in the position i
        the level of affinity with the particle i. On the position with itself the array will have a -1 and
        the affinity amount will randomly begin with numbers between 4 and 6 to make available the interaction.

        Parameters
        ----------
        neighbors_amount: int
            Total number of neighbors, including itself
        """
        neighbors = [0] * neighbors_amount
        for i in range(0, neighbors_amount):
            neighbors[i] = random.randint(40, 60)
        neighbors[self.id] = -1
        self.neighbors = neighbors

    def calculate_neighborhood(self, diameter=1):
        """
        Function that calculates the coordinates that belong to the particle neighborhood according to
        the diameter.

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
        x_min = self.x - diameter
        x_max = self.x + diameter + 1
        y_min = self.y - diameter
        y_max = self.y + diameter + 1
        if x_min < 0:
            x_min = 0
        if x_max > self.x_max:
            x_max = self.x_max
        if y_min < 0:
            y_min = 0
        if y_max > self.y_max:
            y_max = self.y_max
        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if [i, j] != [self.x, self.y]:
                    neighborhood.append([i, j])
        return neighborhood

    def move(self, world_array, diameter=1):
        """
        Function that randomly moves a particle into a new free space. `world_array` is the board
        where the interactions are happening, if there is no free space, then the particle stays in the same
        coordinate.
        Parameters
        ----------
        world_array: list
            Array with all the available spaces and the particles that represents the model of the world
        diameter: int
         Diameter used to calculate the available coordinates to move
        """
        position_settled = False
        posible_spaces = self.calculate_neighborhood(diameter)
        random.shuffle(posible_spaces)
        position = posible_spaces[0]
        while not position_settled and posible_spaces:
            if world_array[position[0]][position[1]] == -1:
                # The position is empty
                world_array[position[0]][position[1]] = self.id
                world_array[self.x][self.y] = -1
                self.x = position[0]
                self.y = position[1]
                position_settled = True
            else:
                posible_spaces.remove(position)
                if posible_spaces:
                    position = posible_spaces[0]

    def update_despair(self):
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
            All the neighbors ID's that are located in the neighborhood
        """
        neighborhood = self.calculate_neighborhood(self.neighborhood_size)
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
        self.suspect = None
