from __future__ import print_function
from particles import Particle
from board import Board

colors = [color(255,0,255),
           color(153,102,203),
           color(70,130,180),
           color(199,234,70),
           color(78,120,151), 
           color(217,221,220),
           color(80,151,164), 
           color(249,135,197), 
           color(207,152,26),
           color(252,226,5), 
           color(255,166,201),
           color(254,91,172), 
           color(131,153,107), 
           color(161,173,231), 
           color(244,161,136), 
           color(45,97,205), 
           color(183,163,173), 
           color(201,142,81), 
           color(85,84,54),
           color(183,150,171)]

board = Board(20,20,20)
iterations = 0
actual_phase = 0
board_px_size = 500
board_size = 20

def phase_0(board_array, square_size, incentive):
    """
    Function that models the phase 0 (interaction)
    """
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                player_id = board_array[i][j]
                if incentive:
                    despair_color = (250/20) * board.players[player_id].despair
                    fill(color(despair_color + 5, 20, 10))
                else:
                    player_color = colors[player_id % len(colors)]
                    fill(player_color)
            else:
                stroke(0,0,0)
                fill(color(0,0,0))
            # Draw the circle
            circle(i*square_size, j*square_size, square_size)

def phase_1(board_array, square_size):
    """
    Function that models the phase 1 (searching murder)
    """
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                if board_array[i][j] == board.killer:
                    fill(color(155,10,10))  
                else:
                    fill(color(100,50,100))
            else:
                fill(color(0,0,0))
            # Draw the circle
            circle(i*square_size, j*square_size, square_size) 
    fill(color(155,155,10))
    circle(board.corpse_x * square_size, board.corpse_y * square_size, 
         square_size)
                
def phase_2(board_array, square_size):
    """
    Function that models the phase 2 (murder)
    """
    a = colors[board.killer%len(colors)]
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                player_id = board_array[i][j]
                if player_id == board.killer:
                    fill(color(155,10,10)) 
                else:
                    if board.players[player_id].suspect != -1:
                        fill(a)
                    else:
                        fill(color(255,204,229))
            else:
                fill(color(0,0,0))
            # Draw the circle
            circle(i*square_size, j*square_size, square_size)
    corpse_x = board.corpse_x * square_size
    corpse_y = board.corpse_y * square_size
    fill(color(155,155,10)) 
    circle(corpse_x, corpse_y, square_size)

                
def setup(): 
    size(board_px_size, board_px_size)
    stroke(50)
    background(0,0,0)
    frameRate(5)

"""
def statistics():
    with open("despair_1jug.txt", "a") as txt:
        txt.write(str(board.players[7].despair) + ",")
    with open("affinity.txt", "a") as txt:
        txt.write(str(average/len(board.players)) + ",")
    with open("n_players.txt", "a") as txt:
        txt.write(str(alive_players) + ",")
    if actual_phase != board.phase:
        # There was a phase change
        print(iterations, end=", ")
        actual_phase = board.phase
        
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
            
    #for i in range(len(board.players)):
        #print(board.players[i].neighbors, board.players[i].despair)
    #print("----------------------")
    
    #print(board.players[7].despair,end=',')
"""
        
        
        
def draw():
    '''Draw and update the system ''' 
    global iterations # TODO Move to a file
    global actual_phase
    incentive = False
    if iterations%30 == 0:
        board.increase_despair() 
        incentive = True
    square_size = board_px_size/ board_size
    board_array = board.board
    if board.phase == 0:
        phase_0(board_array, square_size, incentive)
    if board.phase == 1:
        phase_1(board_array, square_size)
    if board.phase == 2:
        phase_2(board_array, square_size) 
        
    board.run()
    iterations += 1
