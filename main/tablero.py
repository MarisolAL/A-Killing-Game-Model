#from __future__ import division
import random
from particulas import Particula 

class Tablero:
    
    def __init__(self, tam_x, tam_y, numero_jugadores, rango_vision = 2):
        self.x_m = tam_x
        self.y_m = tam_y
        self.tablero = [[-1 for x in range(tam_x)] for y in range(tam_y)]
        self.jugadores = [None]*numero_jugadores
        for i in range(numero_jugadores):
            # Creamos a los jugadores, dentro del constructor ponemos en las 
            #celdas ocupadas el id del vecino correspondiente
            self.jugadores[i] = Particula(i,tam_x, tam_y, rango_vision, self.tablero)
            self.jugadores[i].llena_vecinos(numero_jugadores)
            
    def interactuar(self):
        '''
        Funcion que se dedica de verificar las interacciones entre los agentes
        y guardarlas.
        '''
        vecindades = [None]*len(self.jugadores)
        for i in range(len(self.jugadores)):
            vecindades[i] = self.jugadores[i].vecinos_cercanos(self.tablero)
        # Eliminamos los duplicados
        for i in range(len(vecindades)):
            vecindad_de_i = vecindades[i]
            for j in range(len(vecindad_de_i)):
                vecino = vecindad_de_i[j]
                vecindades[vecino].remove(i)
        for i in range(len(vecindades)):
            if vecindades[i]!= []:
                for j in range(len(vecindades[i])):
                    jugador_1 = self.jugadores[i]
                    jugador_2 = self.jugadores[vecindades[i][j]]
                    self.interactua(jugador_1, jugador_2)
        self.ajusta_afinidad()
        self.ajusta_desesperacion()
        
        
    def interactua(self, jugador_1, jugador_2):
        '''
        Funcion que aplica las reglas de interaccion
        recibe las particulas que representan los jugadores
        '''
        af1 = False
        af2 = False
        if jugador_1.vecinos[jugador_2.id]>=50:
            #Si la afinidad es positiva
            af1 = True
        if jugador_2.vecinos[jugador_1.id]>=50:
            af2 = True
        if af1 and af2:
            #Ambas interacciones son positivas, sumamos dos a cada afinidad
            jugador_1.vecinos[jugador_2.id] +=3
            jugador_2.vecinos[jugador_1.id] +=3 
        elif af1 and not af2:
            # El vecino con afinidad positiva se mantiene
            # y el que tiene afinidad negativa la aumenta
            jugador_2.vecinos[jugador_1.id] +=5
            jugador_1.vecinos[jugador_2.id] -=5
        elif af2:
            jugador_2.vecinos[jugador_1.id] -=5
            jugador_1.vecinos[jugador_2.id] +=5
        else:
            jugador_1.vecinos[jugador_2.id] -=1
            jugador_2.vecinos[jugador_1.id] -=1
        
    def ajusta_afinidad(self):
        '''Funcion que normaliza las afinidades'''
        for i in range(len(self.jugadores)):
            self.jugadores[i].vecinos = map((lambda x: x),self.jugadores[i].vecinos) 
    
                
                
    
    def ajusta_desesperacion(self):
        '''Funcion que mueve los niveles de desesperacion
        dada la afinidad'''
        pass    
    
    def mueve_jugadores(self):
        for i in range(len(self.jugadores)):
            self.jugadores[i].mueve(self.tablero)
            
    def desespera(self):
        for i in self.jugadores:
            i.desespera()
