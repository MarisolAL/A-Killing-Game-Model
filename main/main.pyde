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
    if tablero.fase == 0:
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
    if tablero.fase == 1:
        for i in range(len(malla)):
            for j in range(len(malla[i])):
                if malla[i][j] != -1:
                    #Hay un jugador
                    if malla[i][j] == tablero.asesino : 
                        fill(color(155,10,10)) 
                    elif malla[i][j] == tablero.asesinado:
                        fill(color(155,155,10))
                    else:
                        fill(color(100,50,100))
                else:
                    fill(color(0,0,0))
                #Dibujamos los cuadrados
                rect(i*tam_cuadro, j*tam_cuadro, tam_cuadro, tam_cuadro)
    with open("desesp_1jug.txt", "a") as txt:
        txt.write(str(tablero.jugadores[7].desesperacion) + ", ")
    des_sum = 0
    for i in tablero.jugadores:
        des_sum += i.desesperacion
    with open("desesp_sis.txt", "a") as txt:
        txt.write(str(des_sum) + ", ")
    prom = 0
    for i in tablero.jugadores:
        vec = filter((lambda x: True if x >=0 else False),i.vecinos)
        s = sum(vec)
        prom += s/len(vec)
    with open("afinidad.txt", "a") as txt:
        txt.write(str(prom/len(tablero.jugadores)) + ", ")
    #for i in range(len(tablero.jugadores)):
        #print(tablero.jugadores[i].vecinos, tablero.jugadores[i].desesperacion)
    #print("----------------------")
    
    #print(tablero.jugadores[7].desesperacion,end=',')
    tablero.mueve_jugadores()
    tablero.run()
    iteraciones += 1
