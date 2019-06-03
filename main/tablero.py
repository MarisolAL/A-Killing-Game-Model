import random
import math
from particulas import Particula 

class Tablero:
    
    def __init__(self, tam_x, tam_y, numero_jugadores, rango_vision = 2):
        self.x_m = tam_x
        self.y_m = tam_y
        self.tablero = [[-1 for x in range(tam_x)] for y in range(tam_y)]
        self.jugadores = [None]*numero_jugadores
        self.fase = 0 # Fase 0 = interaccion, Fase 1 = Asesinato, Fase 2 = juicio
        self.asesino = -1 # Id del que va a asesinar
        self.asesinado = -1
        self.testigo = -1
        self.x_vic = -1
        self.y_vic = -1
        self.tiempo_restante_juicio = 35
        for i in range(numero_jugadores):
            # Creamos a los jugadores, dentro del constructor ponemos en las 
            #celdas ocupadas el id del vecino correspondiente
            self.jugadores[i] = Particula(i,tam_x, tam_y, rango_vision, self.tablero)
            self.jugadores[i].llena_vecinos(numero_jugadores)
            
    def run(self):
        self.interactuar()       
        if self.fase == 0:   
            self.check_asesinato()
        if self.fase == 1:
            self.acecha_presa()
        if self.fase == 2:
            # Recordar al pasar a la fase 0 quitar del tablero al muerto
            if self.tiempo_restante_juicio < 0:
                # Hacemos veredicto
                votos_correctos = len(filter((lambda x: True if x.sospechoso == self.asesino else False),self.jugadores))
                jugadores_vivos = len(filter((lambda x: True if x.vivo else False),self.jugadores))
                if votos_correctos > jugadores_vivos/2:
                    print("CORRECTOOOOO")
                    self.jugadores[self.asesino].muere()
                    for i in self.jugadores:
                        if i.vivo:
                            i.vecinos[self.asesino] = -1
                            i.sospechoso = -1
                for i in range(self.x_m):
                    for j in range(self.y_m):
                        if self.tablero[i][j] == self.asesinado:
                            self.tablero[i][j] = -1
                        if self.tablero[i][j] == self.asesino:
                            self.tablero[i][j] = -1
                self.x_vic = -1
                self.y_vic = -1
                self.tiempo_restante_juicio = 35
                self.asesino = -1
                self.asesinado = -1
                self.fase = 0
            else:
                self.tiempo_restante_juicio -= 1
                    
        self.mueve_jugadores()
                  
    
    def interactuar(self):
        '''
        Funcion que se dedica de verificar las interacciones entre los agentes
        y guardarlas.
        '''
        vecindades = [None]*len(self.jugadores)
        for i in range(len(self.jugadores)):
            if self.jugadores[i].vivo:
                vecindades[i] = self.jugadores[i].vecinos_cercanos(self.tablero)
                vecindades[i] = filter((lambda x: True if self.jugadores[x].vivo else False),vecindades[i])
            else:
                vecindades[i] = []
        # Eliminamos los duplicados
        for i in range(len(vecindades)):
            vecindad_de_i = vecindades[i]
            for j in range(len(vecindad_de_i)):
                vecino = vecindad_de_i[j]
                if i in vecindades[vecino] or not self.jugadores[i].vivo:
                    vecindades[vecino].remove(i)
        for i in range(len(vecindades)):
            if vecindades[i]!= []:
                for j in range(len(vecindades[i])):
                    jugador_1 = self.jugadores[i]
                    jugador_2 = self.jugadores[vecindades[i][j]]
                    if self.fase == 0:
                        self.interactua(jugador_1, jugador_2)
                    if self.fase == 2:
                        self.propaga_culpable(jugador_1, jugador_2)
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
        '''Funcion que ajusta los limites de las afinidades'''
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
            if self.jugadores[i].vivo :
                self.jugadores[i].mueve(self.tablero)
            
    def desespera(self):
        for i in self.jugadores:
            if i.vivo:
                i.desespera()
            
    def check_asesinato(self):
        '''Funcion que revisa si se lleva a cabo un asesinato'''
        jugadores = self.jugadores[:]
        random.shuffle(jugadores)
        for i in jugadores:
            if i.vivo:
                if i.desesperacion >= 20:
                    self.fase = 1
                    self.asesino = i.id
                    break
            
    def acecha_presa(self):
        '''Funcion que toma un vecino contiguo al asesino
        y lo mata'''
        # Vecinos que posiblemente puede matar
        vecindades = self.jugadores[self.asesino].vecinos_cercanos(self.tablero)
        if vecindades != []:
            random.shuffle(vecindades)
            self.asesinato(self.jugadores[self.asesino], self.jugadores[vecindades[0]])
            self.fase = 2
        
    def distancia_del_asesinato(self,jugador):
        '''Funcion que calcula la distancia de un jugador al asesino en el 
        momento del asesinato'''
        asesino = self.jugadores[self.asesino]
        x_ases = asesino.x
        y_ases = asesino.y
        if jugador.vivo:
            dis = math.sqrt((x_ases - jugador.x)**2+ (y_ases - jugador.y)**2)
            return dis
        else:
            return self.x_m
            
    def asesinato(self, asesino, asesinado):
        '''Funcion que lleva a cabo el asesinato'''
        self.x_vic = asesinado.x
        self.y_vic = asesinado.y
        self.tablero[asesinado.x][asesinado.y] = -1
        asesinado.muere()
        id = asesinado.id
        self.asesinado = id
        for i in self.jugadores:
            if i.vivo:
                i.vecinos[id] = -1
                i.sospechoso = -1
        # Va a haber un testigo clave que es el que vera la situacion
        jugadores_cercanos = self.jugadores[:]
        jugadores_cercanos.remove(self.jugadores[self.asesino])
        jugadores_cercanos.remove(self.jugadores[self.asesinado])
        jugadores_cercanos.sort(key=self.distancia_del_asesinato)
        self.jugadores[jugadores_cercanos[0].id].sospechoso = self.asesino
        self.testigo = self.jugadores[jugadores_cercanos[0].id].id
        self.desespera()
    
    def propaga_culpable(self, jugador_1, jugador_2):
        '''Funcion que propaga al sospechoso de cada uno
        de acuerdo a la afinidad'''
        af_j1 = True if jugador_1.vecinos[jugador_2.id]>=40 else False
        af_j2 = True if jugador_2.vecinos[jugador_1.id]>=40 else False
        if jugador_1.sospechoso == -1:
            jugador_1.sospechoso = jugador_2.sospechoso if af_j1 else -1
        if jugador_2.sospechoso == -1:
            jugador_2.sospechoso = jugador_1.sospechoso if af_j2 else -1
        
