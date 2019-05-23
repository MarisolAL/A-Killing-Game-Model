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
            
        def interactuar(self):
            '''
            Funcion que se dedica de verificar las interacciones entre los agentes
            y guardarlas.
            '''
            vecindades = [None]*len(self.jugadores)
            for i in range(len(self.jugadores)):
                vecindades[i] = self.jugadores[i].vecinos_cercanos()
            for i in range(len(vecindades)):
                vecindad_de_i = vecindades[i]
                for j in range(len(vecindad_de_i)):
                    # el vecino i ve a j
                    vecino = vecindad_de_i[j]
                    vecindad[vecino].remove(i)
                    

            #for i in range(len(self.jugadores)):
             #   vecinos_de_i = vecindades[i]
              #  for j in vecinos_de_i:
               #     # Verificamos la lista de vecinos de cada jugador
                #    if vecindades[vecinos_de_i[j]] != -1:
                 #       interactua(self.jugadores[i],self.jugadores[vecinos_de_i[j]])
                  #  vecindades[vecinos_de_i[j]] = -1
        
        def interactua(jugador_1, jugador_2):
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
                # Ambas interacciones son positivas
                jugador_1.vecinos[jugador_2.id] = (jugador_1.vecinos[jugador_2.id] + 1)%11
                jugador_2.vecinos[jugador_1.id] = (jugador_2.vecinos[jugador_1.id] + 1)%11
                jugador_1.desesperacion = (jugador_1.desesperacion -1)%11
                jugador_2.desesperacion = (jugador_2.desesperacion -1)%11
            elif af1 and not af2:
                # El vecino con afinidad positiva la disminuye y el que 
                # tiene afinidad negativa la aumenta
                jugador_1.vecinos[jugador_2.id] = (jugador_1.vecinos[jugador_2.id] - 1)%11
                jugador_2.vecinos[jugador_1.id] = (jugador_2.vecinos[jugador_1.id] + 1)%11
            elif af2:
                jugador_1.vecinos[jugador_2.id] = (jugador_1.vecinos[jugador_2.id] + 1)%11
                jugador_2.vecinos[jugador_1.id] = (jugador_2.vecinos[jugador_1.id] - 1)%11
            
            else:
                if random.uniform(0,1)<= 0.7:
                    #Ambos vecinos disminuyen la afinidad con el otro con una probabilidad de 0.7
                    jugador_1.vecinos[jugador_2.id] = (jugador_1.vecinos[jugador_2.id] - 1)%11
                    jugador_2.vecinos[jugador_1.id] = (jugador_2.vecinos[jugador_1.id] - 1)%11
                else:
                    jugador_1.vecinos[jugador_2.id] = (jugador_1.vecinos[jugador_2.id] + 1)%11
                    jugador_2.vecinos[jugador_1.id] = (jugador_2.vecinos[jugador_1.id] + 1)%11
    
tab = Tablero(20,20,15)
tab.interactuar()
