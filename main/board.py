import random
import math
from particles import Particle


class Board:
    """
    Class that models the board where the particles (agents) interact.

    Attributes
    ----------
    x_m: int
        Maximum x coordinate
    y_m: int
        Maximum y coordinate # TODO: check using tuples
    board: list
        Array with all the available cells
    players: list
        List of particles that represent the game players
    phase: int
        Status of the game, 0 for interaction, 1 for murder, 2 for judgement
    killer: int
        ID of the killer in the current phase
    victim: int
        ID of the victim in the current phase
    corpse_x: int
        x coordinate of the corpse in the current phase
    corpse_y: int
        y coordinate of the corpse in the current phase
    time_left: int
        Time left for a judgement
    murder: tuple
        Tuple that has the killer and the victim of the current murder
    """

    def __init__(self, x_size, y_size, players_amount, vision_size=2):
        """
        Board class constructor
        Parameters
        ----------
        x_size: int
            Maximum x coordinate
        y_size: int
            Maximum y coordinate
        players_amount: int
            Total amount of players
        vision_size: int
            Vision size of each player (particle)
        """
        self.x_m = x_size
        self.y_m = y_size
        self.board = [[-1 for x in range(x_size)] for y in range(y_size)]
        self.players = [None] * players_amount
        self.phase = 0
        self.killer = -1
        self.victim = -1
        self.corpse_x = -1
        self.corpse_y = -1
        self.time_left = 35
        for i in range(players_amount):
            self.players[i] = Particle(i, x_size, y_size, vision_size, self.board)  # TODO: check
            self.players[i].fill_affinity_list(players_amount)

    def update_affinity(self):
        """
        Function that updates the affinity level limits of the players
        """
        for i in range(len(self.players)):
            vec = self.players[i].neighbors
            for v in range(len(vec)):
                if vec[v] > 100:
                    vec[v] = 100
                if vec[v] < 0 and v != -1:
                    vec[v] = 0

    def update_despair(self):
        """
        Function that updates the despair level of the players, the function takes into consideration the
        affinity levels of the player.
        """
        for i in self.players:
            # Available neighbors
            neighbors = filter((lambda x: True if x > 0 else False), i.neighbors)
            # Calculate the average of the interactions
            s = sum(neighbors) / len(neighbors)
            if s > 50:
                cant = random.randint(0, 2)
                i.despair -= cant
            if i.despair < 0:
                i.despair = 0

    def suspicion_propagation(self, player_1, player_2):
        """
        Function that spreads suspicions according to the affinity level.
        Parameters
        ----------
        player_1: Particle
            Player that will interact
        player_2: Particle
            Player that will interact
        """
        do_player1_trust = True if player_1.neighbors[player_2.id] >= 40 else False
        do_player2_trust = True if player_2.neighbors[player_1.id] >= 40 else False
        if player_1.suspicious == -1:
            player_1.suspicious = player_2.suspicious if do_player1_trust else -1
        if player_2.suspicious == -1:
            player_2.suspicious = player_1.suspicious if do_player2_trust else -1

    def players_interaction(self, player_1, player_2):  # TODO: Use switch?
        """
        Function that updates the affinity between two players using the rules of the game.
        Parameters
        ----------
        player_1: Particle
            Player that will interact
        player_2: Particle
            Player that will interact
        """
        affinity_p1 = False
        affinity_p2 = False
        if player_1.neighbors[player_2.id] >= 50:
            # If the affinity is positive
            affinity_p1 = True
        if player_2.neighbors[player_1.id] >= 50:
            affinity_p2 = True
        if affinity_p1 and affinity_p2:
            # If both affinities are positive, then we add 2 to each affinity
            player_1.neighbors[player_2.id] += 3
            player_2.neighbors[player_1.id] += 3
        elif affinity_p1 and not affinity_p2:
            # The neighbor with positive affinity keeps it and the negative one increases the negativity
            player_2.neighbors[player_1.id] += 5
            player_1.neighbors[player_2.id] -= 5
        elif affinity_p2:
            player_2.neighbors[player_1.id] -= 5
            player_1.neighbors[player_2.id] += 5
        else:
            player_1.neighbors[player_2.id] -= 1
            player_2.neighbors[player_1.id] -= 1

    def interact(self):
        """
        Function that verifies and saves the interaction between the players
        """
        neighborhoods = [None] * len(self.players)
        for i in range(len(self.players)):
            if self.players[i].alive:
                neighborhoods[i] = self.players[i].calculate_near_neighbors(self.board)
                neighborhoods[i] = filter((lambda x: True if self.players[x].alive else False), neighborhoods[i])
            else:
                neighborhoods[i] = []
        # We delete the duplicates
        for i in range(len(neighborhoods)):
            neighborhood_i = neighborhoods[i]
            for j in range(len(neighborhood_i)):
                neighbor = neighborhood_i[j]
                if i in neighborhoods[neighbor] or not self.players[i].alive:
                    neighborhoods[neighbor].remove(i)
        for i in range(len(neighborhoods)):
            if neighborhoods[i] != []:
                for j in range(len(neighborhoods[i])):
                    player_1 = self.players[i]
                    player_2 = self.players[neighborhoods[i][j]]
                    if self.phase == 0:
                        self.players_interaction(player_1, player_2)
                    if self.phase == 2:
                        self.suspicion_propagation(player_1, player_2)
        self.update_affinity()
        self.update_despair()

    def has_murder(self):
        """
        Function that verifies if a murder happened
        """
        players = self.players[:]
        random.shuffle(players)
        for i in players:
            if i.alive:
                if i.despair >= 20:
                    self.phase = 1
                    self.killer = i.id
                    break

    def increase_despair(self):
        """
        Function that increases the despair of all the living players
        """
        for i in self.players:
            if i.alive:
                i.despair()

    def distance_from_murder(self, player):
        """
        Function that calculates the distance from the player to the current murder. For death players, the distance
        is the maximum one.
        Parameters
        ----------
        player: Particle
            Player that will be used to check the distance
        Returns
        -------
        float
            The distance from the player to the current murder
        """
        killer = self.players[self.killer]
        killer_x = killer.x
        killer_y = killer.y
        if player.alive:
            dis = math.sqrt((killer_x - player.x) ** 2 + (killer_y - player.y) ** 2)
            return dis
        else:
            return self.x_m

    def murder(self, killer, victim):
        """
        Function that models a murder in the game
        Parameters
        ----------
        killer: Particle
            Particle that will have the role of killer
        victim: Particle
            Particle that will have the role of victim
        """
        self.corpse_x = victim.x
        self.corpse_y = victim.y
        self.board[victim.x][victim.y] = -1
        victim.die()
        victim_id = victim.id
        self.victim = victim_id
        for i in self.players:
            if i.alive:
                i.neighbors[id] = -1
                i.suspicious = -1
        # There will always be a key witness that will see the crime
        near_players = self.players[:]
        near_players.remove(self.players[self.killer])
        near_players.remove(self.players[self.victim])
        near_players.sort(key=self.distance_from_murder)  # Gets the nearest player
        self.players[near_players[0].id].suspicious = self.killer
        self.increase_despair()

    def search_victim(self):  # TODO Move to particle?, check what happens when there is not close neighbor
        """
        Function that takes the closest neighbor of the killer and kills it.
        """
        # Reachable neighbors
        neighborhoods = self.players[self.killer].calculate_near_neighbors(self.board)
        if neighborhoods:
            random.shuffle(neighborhoods)
            self.murder(self.players[self.killer], self.players[neighborhoods[0]])
            self.phase = 2

    def move_players(self):
        """
        Move the alive players in the board
        """
        for i in range(len(self.players)):
            if self.players[i].alive:
                self.players[i].move(self.board)

    def run(self):
        """
        Models the rules in the game, takes into consideration each game phase
        """
        self.interact()
        if self.phase == 0:
            self.has_murder()
        if self.phase == 1:
            self.search_victim()
        if self.phase == 2:
            # TODO Check that when move again to phase 0, delete the corpse from the board
            if self.time_left < 0:
                # Calculate the verdict
                right_votes = len(filter((lambda x: True if x.suspicious == self.killer else False), self.players))
                alive_players = len(filter((lambda x: True if x.alive else False), self.players))
                if right_votes > alive_players / 2:  # TODO Model when the players fail (else)
                    self.players[self.killer].die()
                    for i in self.players:
                        if i.alive:
                            i.neighbors[self.killer] = -1
                            i.suspicious = -1
                for i in range(self.x_m):
                    for j in range(self.y_m):
                        if self.board[i][j] == self.victim:
                            self.board[i][j] = -1
                        if self.board[i][j] == self.killer:
                            self.board[i][j] = -1
                self.corpse_x = -1
                self.corpse_y = -1
                self.time_left = 35
                self.killer = -1
                self.victim = -1
                self.phase = 0
            else:
                self.time_left -= 1

        self.move_players()
