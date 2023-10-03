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
    ended: bool
        Boolean that indicates if the game has finished
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
        self.players = []
        self.phase = 0
        self.killer = -1
        self.victim = -1
        self.corpse_x = -1
        self.corpse_y = -1
        self.time_left = 35
        self.ended = False
        for i in range(players_amount):
            self.players.append(Particle(i, x_size, y_size, vision_size, self.board))  # TODO: check
            self.players[i].fill_affinity_list(players_amount)

    def alive_players(self):
        """
        Method that filters the players list and returns the list of alive players only.
        Returns
        -------
        list
            The list of players currently alive
        """
        alive_players = filter(lambda player: player.alive, self.players)
        return alive_players

    def update_affinity_boundaries(self):
        """
        Function that updates the affinity level limits of the players
        """
        alive_p = self.alive_players()
        for i in range(len(alive_p)):
            vec = alive_p[i].neighbors
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
        alive_p = self.alive_players()
        for player in alive_p:
            # Available neighbors
            neighbors = filter((lambda x: True if x >= 0 else False), player.neighbors)
            if len(neighbors) < 2:
                print(player.neighbors)
            # Calculate the average of the interactions
            average_affinity = sum(neighbors) / len(neighbors)
            if average_affinity > 50:
                cant = random.randint(0, 2)
                player.despair -= cant
            if player.despair < 0:
                player.despair = 0

    def suspicion_propagation(self, player_1, player_2):  # TODO Model the case of the killer interaction
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
        if player_1.suspect == -1:
            player_1.suspect = player_2.suspect if do_player1_trust else -1
        if player_2.suspect == -1:
            player_2.suspect = player_1.suspect if do_player2_trust else -1

    def players_interaction(self, player_1, player_2):
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
        neighborhoods = []
        for player in self.players:
            if player.alive:
                n_player_i = player.calculate_near_neighbors(self.board)
                player_id = player.id
                neighborhoods.append(n_player_i)
                neighborhoods[player_id] = filter((lambda x: True if self.players[x].alive else False),
                                                  neighborhoods[player_id])
            else:
                neighborhoods.append([])
        # We delete the duplicates
        for i in range(len(neighborhoods)):
            neighborhood_i = neighborhoods[i]
            for j in range(len(neighborhood_i)):
                neighbor = neighborhood_i[j]
                if i in neighborhoods[neighbor] or not self.players[i].alive:
                    neighborhoods[neighbor].remove(i)
        for i in range(len(neighborhoods)):
            if neighborhoods[i]:
                for j in range(len(neighborhoods[i])):
                    player_1 = self.players[i]
                    player_2 = self.players[neighborhoods[i][j]]
                    if self.phase == 0:
                        self.players_interaction(player_1, player_2)
                    if self.phase == 2:
                        self.suspicion_propagation(player_1, player_2)
        self.update_affinity_boundaries()
        self.update_despair()

    def has_murder(self):
        """
        Function that verifies if a murder happened
        """
        alive_p = self.alive_players()
        players = alive_p[:]
        random.shuffle(players)
        for player in players:
            if player.despair >= 20:
                self.phase = 1
                self.killer = player.id
                break

    def increase_despair(self):
        """
        Function that increases the despair of all the living players
        """
        alive_p = self.alive_players()
        for player in alive_p:
            player.update_despair()

    def decrease_despair(self):
        """
        Function that decreases the despair of all the living players
        """
        alive_p = self.alive_players()
        for player in alive_p:
            player.decrease_despair()

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

    def commit_murder(self, killer, victim):
        """
        Function that models a murder in the game.

        Parameters
        ----------
        killer: Particle
            Particle that will have the role of killer
        victim: Particle
            The particle that will have the role of victim
        """
        self.corpse_x = victim.x
        self.corpse_y = victim.y
        self.board[victim.x][victim.y] = -1
        self.killer = killer.id
        victim.die()
        victim_id = victim.id
        self.victim = victim_id
        alive_p = self.alive_players()
        for player in alive_p:
            player.neighbors[victim_id] = -1
            player.suspect = -1
        # There will always be a key witness that will see the crime
        near_players = alive_p[:]
        near_players.remove(self.players[killer.id])
        near_players.sort(key=self.distance_from_murder)  # Gets the nearest player
        self.players[near_players[0].id].suspect = killer.id
        self.increase_despair()

    def search_victim(self):  # TODO Move to particle?
        """
        Function that takes the closest neighbor of the killer and kills it.
        """
        # Reachable neighbors
        neighborhoods = self.players[self.killer].calculate_near_neighbors(self.board)
        if neighborhoods:
            random.shuffle(neighborhoods)
            killer_p = self.players[self.killer]
            victim_p = self.players[neighborhoods[0]]
            self.commit_murder(killer_p, victim_p)
            self.phase = 2

    def move_players(self):
        """
        Move alive players in the board
        """
        alive_p = self.alive_players()
        for player in alive_p:
            player.move(self.board)

    def despair_average(self):
        """
        Method that calculates the average of despair in the system.

        Returns
        -------
        float
            The despair average of the players
        """
        alive_p = self.alive_players()
        despair_average = 0
        for player in alive_p:
            despair_average += player.despair
        return despair_average / len(alive_p)

    def players_affinity_average(self):
        """
        Method that calculates the affinity average in the system.

        Returns
        -------
        float
            The affinity average of the players
        """
        alive_p = self.alive_players()
        affinity_avg = 0
        for player in alive_p:
            affinity_avg += player.affinity_avg()
        return affinity_avg / len(alive_p)

    def run(self, with_incentive=True):  # TODO Verify
        """
        Models the rules in the game, takes into consideration each game phase
        """
        if not self.ended:
            self.interact()
            if self.phase == 0:
                is_there_incentive = random.randint(0, 20)
                if is_there_incentive == 0 and with_incentive:
                    self.increase_despair()
                self.has_murder()
            if self.phase == 1:
                self.search_victim()
            if self.phase == 2: # TODO At the end decrease a little bit the despair
                if self.time_left < 0:
                    # Calculate the verdict
                    alive_players = self.alive_players()
                    right_votes = len(filter((lambda x: True if x.suspect == self.killer else False), alive_players))
                    if right_votes > len(alive_players) / 2:
                        print("WIN CASE")
                        killer = self.players[self.killer]
                        self.board[killer.x][killer.y] = -1
                        self.players[self.killer].die()
                        for i in self.players:
                            if i.alive:
                                i.neighbors[self.killer] = -1
                                i.suspect = -1
                        self.board[self.corpse_x][self.corpse_y] = -1
                    else:
                        print("---- The players lose the game! ----")
                        for player in alive_players:
                            if player.id != self.killer:
                                self.board[player.x][player.y] = -1
                                player.die()
                        self.ended = True
                    alive_players = self.alive_players()
                    if len(alive_players) <= 2:
                        print("---- The game has ended! ----")
                        self.ended = True
                    else:
                        self.corpse_x = -1
                        self.corpse_y = -1
                        self.time_left = 35
                        self.killer = -1
                        self.victim = -1
                        self.decrease_despair()
                        self.phase = 0
                else:
                    self.time_left -= 1
            self.move_players()
