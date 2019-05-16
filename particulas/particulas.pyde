import random

class Particula:
    
    def __init__(self, id, x_max, y_max, tam_vecindad, malla=None,x0=None, y0=None):
        self.id = id # Esto nos ayudara para saber cual es la posicion de cada uno
        # en los arreglos de los vecinos 
        self.x = x0 if x != None else random.randint(0,x_max)
        self.y = y0 if y != None else random.randint(0,y_max)
        self.x_max = x_max
        self.y_max = y_max
        self.vecinos = [] # Vecinos de la particula, esta lista tendra la afinidad con cada uno
        self.desesperacion = 0
        self.sospechoso = None
        self.tam_vecindad = tam_vecindad # Radio de la vecindad de vision
        if malla:
            malla[self.x, self.y] = id
        
    def llena_vecinos(self, total_vecinos):
        '''
        Funcion que llena la lista de vecinos de la particula, todas
        las particulas tienen un arreglo donde en la posicion i el valor
        en el mismo significa el nivel de afinidad de la particula actual
        con la particula i. En la posicion correspondiente a la particula
        pondremos un -1. Los valores iniciales son aleatorios y del 4 al 6
        para que se mantengan en un estado en el que pueden interactuar.
        '''
        vecinos = [0]*total_vecinos
        for i in range(0, total_vecinos):
            vecinos[i] = random.randint(4,6)
        vecinos[self.id] = -1    
        self.vecinos = vecinos
        
    def obten_vecindad(self, diametro=1):
        '''Nota, esta funcion solo sirve por ahora
        con diametro 1
        '''
        vecindad = []
        x_m = self.x_max
        y_m = self.y_max
        for i in range(0,diametro + 1):
            v1 = [(self.x + 1 + i)% x_m , (self.y + i)%y_m] #N
            v2 = [(self.x - 1 + i)% x_m , (self.y + i)%y_m] #S
            v3 = [(self.x + 1+ i)% x_m , (self.y + 1 + i)% y_m] #NE
            v4 = [(self.x + 1 + i)% x_m , (self.y - 1 + i)% y_m] #NO
            v5 = [(self.x - 1 + i)% x_m , (self.y + 1 + i)% y_m] #SE
            v6 = [(self.x - 1 + i)% x_m , (self.y - 1 + i)% y_m] #SO
            v7 = [(self.x + i)% x_m  , (self.y + 1 + i)% y_m] #E
            v8 = [(self.x + i)% x_m  , (self.y - 1 + i)% y_m] #O
            vecindad.append(v1,v2,v3,v4,v5,v6,v7,v8)
        return vecindad
        
    def mueve(self, malla):
        '''
        Funcion que mueve las posiciones de la particula de forma aleatoria.
        La malla es el tablero donde estan 
        ocurriendo las interacciones.
        '''
        # Numero Direccion
        #    1       N
        #    2       NE
        #    3       E
        #    4       SE
        #    5       S
        #    6       SO
        #    7       O
        #    8       NO
        acomodado = False
        celdas_posibles = self.obten_vecindad()
        posicion = celdas_posibles[random.randint(0,len(celdas_posibles))]
        iteracion = 0
        while not acomodado and celdas_posibles:        
            if malla[posicion[0],posicion[1]]==0:
                #Esta vacia
                malla[posicion[0],posicion[1]] = self.id
                malla[self.x,self.y] = 0 #Cambiamos los valores de la malla
                self.x = posicion[0]
                self.y = posicion[1]
                acomodado = True
            else:
                celdas_posibles.remove(posicion)
                posicion = celdas_posibles[random.randint(0,len(celdas_posibles))]
        # Si no hay celdas disponibles, el agente no se mueve
        
        def desespera(self):
            # Esta funcion se invoca cuando hay un estimulador de desesperacion
            cantidad = random.randint(1,2)
            self.desespera += cantidad
            
        def vecinos_cercanos(self, malla):
            '''
            Funcion que devuelve los vecinos cercanos al agente en cuestion.
            jugadores es la lista que contiene a todos los agentes y sus caracteristicas
            '''
            vecindad = self.obten_vecindad()
            vecinos = []
            for i in vecindad:
                if malla[i[0],i[1]] != 0:
                    # Guardamos lo que corresponde con el id del vecino
                    vecinos.append(malla[i[0],i[1]])
            return vecinos
