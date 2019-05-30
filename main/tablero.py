#from __future__ import division
import random
from particulas import Particula 

class Tablero:
    
    def __init__(self, tam_x, tam_y, numero_jugadores, rango_vision = 2):
        self.x_m = tam_x
        self.y_m = tam_y
        self.tablero = [[-1 for x in range(tam_x)] for y in range(tam_y)]
        self.jugadores = [None]*numero_jugadores
        self.fase = 0 # Fase 0 = interaccion, Fase 1 = Asesinato, Fase 2 = juicio
        self.asesino = -1 # Id del que va a asesinar
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
            vec = self.jugadores[i].vecinos
            for v in range(len(vec)):
                if vec[v] > 100:
                    vec[v] = 100
                if vec[v]<0 and v!=-1:
                    vec[v]=0
    
                
                
    
    def ajusta_desesperacion(self):
        '''Funcion que mueve los niveles de desesperacion
        dada la afinidad'''
        for i in self.jugadores:
            # Vecinos validos
            vecinos = filter((lambda x: True if x >0 else False),i.vecinos)
            # Obtenemos el promedio de las interacciones
            s = sum(vecinos)/len(vecinos)
            if s>50:
                cant = random.randint(0,2)
                i.desesperacion -=  cant
            if i.desesperacion < 0: i.desesperacion = 0
        
    
    def mueve_jugadores(self):
        for i in range(len(self.jugadores)):
            self.jugadores[i].mueve(self.tablero)
            
    def desespera(self):
        for i in self.jugadores:
            i.desespera()
            
    def check_asesinato(self):
        '''Funcion que revisa si se lleva a cabo un asesinato'''
        jugadores = self.jugadores[:]
        random.shuffle(jugadores)
        for i in jugadores:
            if i.desesperacion >= 20:
                self.fase = 1
                self.asesino = i.id
