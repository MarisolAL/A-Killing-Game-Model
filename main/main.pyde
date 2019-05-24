from particulas import Particula
from tablero import Tablero

tablero = Tablero(20,20,10)

def setup():
    '''Hacer aqui todos los preparativos'''
    size(100,100)
    stroke(50)
    background(0,0,0,0)
    frameRate(2)
    
def draw():
    '''Dibujar y actualizaciones del sistema '''
    tam_cuadro = 100/20
    malla = tablero.tablero
    for i in range(len(malla)):
        for j in range(len(malla[i])):
            if malla[i][j] != -1:
                #Hay un jugador
                fill(color(0,210,100))
            else:
                fill(color(0,0,0))
            #Dibujamos los cuadrados
            rect(i*tam_cuadro, j*tam_cuadro, tam_cuadro, tam_cuadro)
    tablero.mueve_jugadores()
