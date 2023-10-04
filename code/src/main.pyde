from __future__ import print_function
from particles import Particle
from board import Board

colors = [color(0,255,128),
          color(0, 255, 255),
          color(0,128,255),
          color(127,0,255),
          color(255,0,255), 
          color(255,0,127),
          color(255,51,153),  
          color(153,51,255), 
          color(51,255,255), 
          color(51,255,153),  
          color(102,255,178), 
          color(102,255,255), 
          color(102,178,255), 
          color(102,102,255), 
          color(178, 102, 255), 
          color(255, 102, 255),
          color(255, 102, 178),
          color(51, 51, 255),
          color(153, 255, 153),
          color(153, 255, 204)]

board = Board(20,20,20,3)
iterations = 0
actual_phase = 0
board_px_size = 500
board_size = 20

def phase_0(board_array, circle_size, incentive):
    """
    Function that models the phase 0 (interaction)
    """
    r = circle_size/2
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
                circle(i*circle_size + r, j*circle_size + r, circle_size) 

def phase_1(board_array, circle_size):
    """
    Function that models the phase 1 (searching murder)
    """
    r = circle_size/2
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                if board_array[i][j] == board.killer:
                    fill(color(155,10,10))  
                else:
                    fill(color(100,50,100))
                circle(i*circle_size + r, j*circle_size + r, circle_size)          
                
def phase_2(board_array, circle_size):
    """
    Function that models the phase 2 (murder)
    """ 
    r = circle_size/2
    corpse_x = board.corpse_x * circle_size
    corpse_y = board.corpse_y * circle_size
    fill(color(155,155,10)) 
    #circle(corpse_x + r, corpse_y + r, circle_size)
    triangle(corpse_x, corpse_y + circle_size,
             corpse_x + r, corpse_y,
             corpse_x + circle_size, corpse_y + circle_size)
    killer_color = colors[board.killer%len(colors)]
    for i in range(len(board_array)):
        for j in range(len(board_array[i])):
            if board_array[i][j] != -1:
                # There is a player
                player_id = board_array[i][j]
                if player_id == board.killer:
                    fill(color(155,10,10)) 
                else:
                    if board.players[player_id].suspect != -1:
                        fill(killer_color)
                    else:
                        fill(color(255,204,229))
                circle(i*circle_size + r, j*circle_size + r, circle_size) 
            
def show_basic_stats(board, iterations):
    fill(245, 243, 240)
    rect(0, 500, 500, 700, 8, 8, 0, 0)
    fill(45, 98, 152)
    textSize(16)
    textAlign(LEFT)
    iteration_str = ("Iteration: %i" % (iterations)) 
    phase_str = ("Actual phase: %i" % (board.phase))    
    text(iteration_str, 20, 520)
    text(phase_str, 20, 540)
    
    despair_avg = board.despair_average()
    despair_str = ("Average despair: %i" % (despair_avg)) 
    text(despair_str, 20, 560)
    
    af_avg = board.players_affinity_average() 
    af_str = ("Average affinity: %i" % (af_avg)) 
    text(af_str, 20, 580) 
    
    alive_players = board.alive_players()
    alive_p_str = ("Alive players: %i" % (len(alive_players)))
    text(alive_p_str, 20, 600) 
    
        
def setup(): 
    size(board_px_size, board_px_size + 110)
    stroke(50)
    background(0,0,0)
    frameRate(5) 
        
def draw():
    '''Draw and update the system '''  
    global iterations
    fill(0, 0, 0)
    square(0, 0, board_px_size)
    
    show_basic_stats(board, iterations) 
    
    incentive = False
    if iterations%30 == 0:
        board.increase_despair() 
        incentive = True
    circle_size = board_px_size/ board_size
    board_array = board.board
    if board.phase == 0:
        phase_0(board_array, circle_size, incentive)
    if board.phase == 1:
        killer = board.killer
        phase_str = ("The player %i is searching a victim" % (killer))
        text(phase_str, 200, 520) 
        phase_1(board_array, circle_size)
    if board.phase == 2:
        killer = board.killer
        victim = board.victim
        phase_str = ("The player %i killed the player %i" % (killer, victim))
        text(phase_str, 200, 520) 
        phase_2(board_array, circle_size)
    if board.ended: 
        fill(153, 0, 0)
        text("The game has ended", 200, 540) 
        
    
    board.run()
    iterations += 1
