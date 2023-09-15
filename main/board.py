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
