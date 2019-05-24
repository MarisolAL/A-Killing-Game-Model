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
                #print(vecindades[vecino],i)
                vecindades[vecino].remove(i)
        for i in range(len(vecindades)):
            if vecindades[i]!= []:
                for j in range(len(vecindades[i])):
                    jugador_1 = self.jugadores[i]
                    jugador_2 = self.jugadores[vecindades[i][j]]
                    self.interactua(jugador_1, jugador_2)
        
        
    def interactua(self, jugador_1, jugador_2):
        '''
        Funcion que aplica las reglas de interaccion
        recibe las particulas que representan los jugadores
        '''
        af1 = False
        af2 = False
        if jugador_1.vecinos[jugador_2.id]>=5:
            #Si la afinidad es positiva
            af1 = True
        if jugador_2.vecinos[jugador_1.id]>=5:
            af2 = True
        if af1 and af2:
            #Ambas interacciones son positivas
            jugador_1.vecinos[jugador_2.id] +=1
            jugador_2.vecinos[jugador_1.id] +=1 
            jugador_1.desesperacion -=1
            jugador_2.desesperacion -= 1
        elif af1 and not af2:
            # El vecino con afinidad positiva la disminuye y el que 
            #tiene afinidad negativa la aumenta
            jugador_1.vecinos[jugador_2.id] -=1
            jugador_2.vecinos[jugador_1.id] +=1
        elif af2:
            jugador_1.vecinos[jugador_2.id] +=1
            jugador_2.vecinos[jugador_1.id] -=1
            
        else:
            if random.uniform(0,1)<= 0.7:
                #Ambos vecinos disminuyen la afinidad con el otro con una probabilidad de 0.7
                jugador_1.vecinos[jugador_2.id] -=1
                jugador_2.vecinos[jugador_1.id] -=1
            else:
                jugador_1.vecinos[jugador_2.id] +=1
                jugador_2.vecinos[jugador_1.id] +=1
        #Ajustamos los valores a los rangos
        if jugador_1.vecinos[jugador_2.id] > 10: jugador_1.vecinos[jugador_2.id] = 10
        if jugador_2.vecinos[jugador_1.id] > 10: jugador_2.vecinos[jugador_1.id] = 10
        if jugador_1.vecinos[jugador_2.id] < 0: jugador_1.vecinos[jugador_2.id] = 0
        if jugador_2.vecinos[jugador_1.id] < 0: jugador_2.vecinos[jugador_1.id] = 0
        if jugador_1.desesperacion <0 : jugador_1.desesperacion = 0
        if jugador_2.desesperacion <0 : jugador_2.desesperacion = 0
        if jugador_1.desesperacion >10 : jugador_1.desesperacion = 10
        if jugador_2.desesperacion >10 : jugador_2.desesperacion = 10
        
    def mueve_jugadores(self):
        for i in range(len(self.jugadores)):
            self.jugadores[i].mueve(self.tablero)
