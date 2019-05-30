from __future__ import print_function
from particulas import Particula
from tablero import Tablero

tablero = Tablero(20,20,20)
iteraciones = 0

def setup():
    '''Hacer aqui todos los preparativos'''
    size(200,200)
    stroke(50)
    background(0,0,0,0)
    frameRate(3)
    
def draw():
    '''Dibujar y actualizar del sistema '''
    global iteraciones
    incentivo = False
    if iteraciones%30 == 0:
        tablero.desespera()
        incentivo = True
    tam_cuadro = 200/20
    malla = tablero.tablero
    for i in range(len(malla)):
        for j in range(len(malla[i])):
            if malla[i][j] != -1:
                #Hay un jugador
                if incentivo: 
                    a = (250/20)*tablero.jugadores[malla[i][j]].desesperacion
                    fill(color(a+5,10,10)) 
                else:
                    fill(color(0,210,100))
            else:
                fill(color(0,0,0))
            #Dibujamos los cuadrados
            rect(i*tam_cuadro, j*tam_cuadro, tam_cuadro, tam_cuadro)
    #for i in range(len(tablero.jugadores)):
        #print(tablero.jugadores[i].vecinos, tablero.jugadores[i].desesperacion)
    #print("----------------------")
    
    print(tablero.jugadores[7].desesperacion)
    tablero.mueve_jugadores()
    tablero.interactuar()
    iteraciones += 1
