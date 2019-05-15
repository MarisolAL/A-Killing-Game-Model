import random

class Particula:
    
    def __init__(self, x_max, y_max, tam_vecindad, x0=None, y0=None):
        self.x = x0 if x != None else random.randint(0,x_max)
        self.y = y0 if y != None else random.randint(0,y_max)
        self.x_max = x_max
        self.y_max = y_max
        self.vecinos = [] # Vecinos de la particula, esta lista tendra la afinidad con cada uno
        self.velocidad = [random.uniform(0,1), random.uniform(0,1)] #Velocidad en x y y
        self.desesperacion = 0
        self.sospechoso = None
        self.tam_vecindad = tam_vecindad # Radio de la vecindad
        
    def llena_vecinos(self, total_vecinos, indice_propio):
        '''
        Funcion que llena la lista de vecinos de la particula, todas
        las particulas tienen un arreglo donde en la posicion i el valor
        en el mismo significa el nivel de afinidad de la particula actual
        con la particula i. En la posicion correspondiente a la particula
        pondremos un -1. Los valores iniciales son aleatorios y del 1 al 10.
        '''
        vecinos = [0]*total_vecinos
        for i in range(0, total_vecinos):
            vecinos[i] = random.randint(0,10)
        vecinos[indice_propio] = -1    
        self.vecinos = vecinos
        
    def mueve(self):
        '''
        Funcion que mueve las posiciones de la particula dado los vecinos que le 
        caen bien y un momentum aleatorio.
        '''
        
