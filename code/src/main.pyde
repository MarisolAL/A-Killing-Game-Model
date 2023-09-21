from __future__ import print_function
from particles import Particle
from board import Board

colors = [color(219,179,174),
           color(202,236,248),
           color(172,95,131),
           color(71,79,58),
           color(78,120,151),
           color(252,234,227),
           color(129,13,23),
           color(165,59,76),
           color(252,251,249),
           color(60,48,60),
           color(189,189,189),
           color(53,84,87),
           color(112,106,83),
           color(244,192,215),
           color(157,201,108),
           color(78,85,140),
           color(115,179,142),
           color(251,202,170),
           color(85,84,54),
           color(183,150,171)]
board = Board(20,20,20)
iterations = 0
actual_phase = 0

def phase_0(board_array, square_size, incentive):
    """
    Method that models the phase 0 (interaction)
    """
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                if incentive:
                    a = (250/20)*board.players[board_array[i][j]].despair
                    fill(color(a+5,10,10))
                else:
                    a = colors[board_array[i][j]%len(colors)]
                    fill(a)
            else:
                stroke(0,0,0)
                fill(color(0,0,0))
            # Draw the rectangle
            rect(i*square_size, j*square_size, square_size, square_size)

def phase_1(board_array, square_size):
    """
    Method that models the phase 1 (searching murder)
    """
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                if board_array[i][j] == board.killer:
                    fill(color(155,10,10)) 
                    #elif board_array[i][j] == board.victim: # TODO Check
                     #   fill(color(155,155,10))
                else:
                    fill(color(100,50,100))
            else:
                fill(color(0,0,0))
            # Draw the rectangle
            rect(i*square_size, j*square_size, square_size, square_size)
    fill(color(155,155,10))
    rect(board.corpse_x * square_size, board.corpse_y * square_size, 
         square_size, square_size)
                
def phase_2(board_array, square_size):
    """
    Method that models the phase 2 (murder)
    """
    a = colors[board.killer%len(colors)]
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                if board_array[i][j] == board.killer:
                    fill(color(155,10,10)) 
                else:
                    if board.players[board_array[i][j]].suspicious != -1:
                        fill(a)
                    else:
                        fill(color(100,150,200))
            else:
                fill(color(0,0,0))
            # Draw the rectangle
            rect(i*square_size, j*square_size, square_size, square_size)
    fill(color(155,155,10))
    rect(board.corpse_x * square_size, board.corpse_y * square_size, 
         square_size, square_size)
                
def setup(): 
    size(200,200)
    stroke(50)
    background(0,0,0)
    frameRate(5)
    
def draw():
    '''Draw and update the system ''' 
    global iterations # TODO Move to a file
    global actual_phase
    incentive = False
    if iterations%30 == 0:
        board.increase_despair()
        print("increase")
        incentive = True
    square_size = 200/20
    board_array = board.board
    if board.phase == 0:
        phase_0(board_array,square_size,incentive)
    if board.phase == 1:
        phase_1(board_array,square_size)
    if board.phase == 2:
        phase_2(board_array,square_size)
    if board.phase == 0:
        pass
        #print(max(map((lambda x: x.despair),board.players)))
    with open("despair_1jug.txt", "a") as txt:
        txt.write(str(board.players[7].despair) + ",")
    despair_total = 0
    for i in board.players:
        despair_total += i.despair
    with open("despair_sis.txt", "a") as txt:
        txt.write(str(despair_total) + ",")
    average = 0
    alive_players = 0
    for i in board.players:
        vec = filter((lambda x: True if x >=0 else False),i.neighbors)
        s = sum(vec)
        average += s/len(vec)
        if i.alive:
            alive_players += 1
    with open("affinity.txt", "a") as txt:
        txt.write(str(average/len(board.players)) + ",")
    with open("n_players.txt", "a") as txt:
        txt.write(str(alive_players) + ",")
    if actual_phase != board.phase:
        # There was a phase change
        print(iterations, end=", ")
        actual_phase = board.phase
    #for i in range(len(board.players)):
        #print(board.players[i].neighbors, board.players[i].despair)
    #print("----------------------")
    
    #print(board.players[7].despair,end=',')
    
    board.run()
    iterations += 1
