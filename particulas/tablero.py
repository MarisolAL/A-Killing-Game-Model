import random
import particulas 

class Tablero:
    
    def __init__(self, tam_x, tam_y, numero_jugadores, rango_vision = 2):
        self.x_m = tam_x
        self.y_m = tam_y
        self.tablero = [[0 for x in range(tam_x)] for y in range(tam_y)]
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
            for i in range(len(self.jugadores)):
                vecinos_de_i = vecindades[i]
                for j in vecinos_de_i:
                    # Verificamos la lista de vecinos de cada jugador
                    if vecindades[vecinos_de_i[j]] != -1:
                        interactua(self.jugadores[i].id,self.jugadores[vecinos_de_i[j].id])
                    vecindades[vecinos_de_i[j]] = -1
        
        def interactua(jugador_1, jugador_2):
            '''
            Funcion que aplica las reglas de interaccion
            '''
    
