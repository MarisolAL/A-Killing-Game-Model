from __future__ import print_function
from particulas import Particula
from tablero import Tablero

colores = [color(219,179,174),color(202,236,248),color(172,95,131),color(71,79,58),color(78,120,151),color(252,234,227),color(129,13,23),color(165,59,76),color(252,251,249),color(60,48,60),color(189,189,189),color(53,84,87),color(112,106,83),color(244,192,215),color(157,201,108),color(78,85,140),color(115,179,142),color(251,202,170),color(85,84,54),color(183,150,171)]
tablero = Tablero(20,20,20)
iteraciones = 0
fase_act = 0

def fase_0(malla,tam_cuadro,incentivo):
    for i in range(len(malla)):
            for j in range(len(malla[i])):
                if malla[i][j] != -1:
                    #Hay un jugador
                    if incentivo: 
                        a = (250/20)*tablero.jugadores[malla[i][j]].desesperacion
                        fill(color(a+5,10,10)) 
                    else:
                        a = colores[malla[i][j]%len(colores)]
                        fill(a)
                else:
                    stroke(0,0,0)
                    fill(color(0,0,0))
                #Dibujamos los cuadrados
                rect(i*tam_cuadro, j*tam_cuadro, tam_cuadro, tam_cuadro)

def fase_1(malla,tam_cuadro):
    for i in range(len(malla)):
            for j in range(len(malla[i])):
                if malla[i][j] != -1:
                    #Hay un jugador
                    if malla[i][j] == tablero.asesino : 
                        fill(color(155,10,10)) 
                    #elif malla[i][j] == tablero.asesinado:
                     #   fill(color(155,155,10))
                    else:
                        fill(color(100,50,100))
                else:
                    fill(color(0,0,0))
                #Dibujamos los cuadrados
                rect(i*tam_cuadro, j*tam_cuadro, tam_cuadro, tam_cuadro)
    fill(color(155,155,10))
    rect(tablero.x_vic*tam_cuadro, tablero.y_vic*tam_cuadro, tam_cuadro, tam_cuadro)
                
def fase_2(malla,tam_cuadro):
    a = colores[tablero.asesino%len(colores)]
    for i in range(len(malla)):
        for j in range(len(malla[i])):
            if malla[i][j] != -1:
                #Hay un jugador
                if malla[i][j] == tablero.asesino : 
                    fill(color(155,10,10)) 
                else:
                    if tablero.jugadores[malla[i][j]].sospechoso != -1:
                        fill(a)
                    else:
                        fill(color(100,150,200))
            else:
                fill(color(0,0,0))
            #Dibujamos los cuadrados
            rect(i*tam_cuadro, j*tam_cuadro, tam_cuadro, tam_cuadro)
    fill(color(155,155,10))
    rect(tablero.x_vic*tam_cuadro, tablero.y_vic*tam_cuadro, tam_cuadro, tam_cuadro)
                
def setup():
    '''Hacer aqui todos los preparativos'''
    size(800,800)
    stroke(50)
    background(0,0,0)
    frameRate(5)
    
def draw():
    '''Dibujar y actualizar del sistema '''
    global iteraciones
    global fase_act
    incentivo = False
    if iteraciones%30 == 0:
        tablero.desespera()
        incentivo = True
    tam_cuadro = 800/20
    malla = tablero.tablero
    if tablero.fase == 0:
        fase_0(malla,tam_cuadro,incentivo)
    if tablero.fase == 1:
        fase_1(malla,tam_cuadro)
    if tablero.fase == 2:
        fase_2(malla,tam_cuadro)
    if tablero.fase == 0:            
        pass
        #print(max(map((lambda x: x.desesperacion),tablero.jugadores)))
    with open("desesp_1jug.txt", "a") as txt:
        txt.write(str(tablero.jugadores[7].desesperacion) + ",")
    des_sum = 0
    for i in tablero.jugadores:
        des_sum += i.desesperacion
    with open("desesp_sis.txt", "a") as txt:
        txt.write(str(des_sum) + ",")
    prom = 0
    jugadores_vivos = 0
    for i in tablero.jugadores:
        vec = filter((lambda x: True if x >=0 else False),i.vecinos)
        s = sum(vec)
        prom += s/len(vec)
        if i.vivo:
            jugadores_vivos += 1
    with open("afinidad.txt", "a") as txt:
        txt.write(str(prom/len(tablero.jugadores)) + ",")
    with open("no_jugadores.txt", "a") as txt:
        txt.write(str(jugadores_vivos) + ",")
    if fase_act != tablero.fase:
        #Hubo cambio de fase
        print(iteraciones,end=", ")
        fase_act = tablero.fase
    #for i in range(len(tablero.jugadores)):
        #print(tablero.jugadores[i].vecinos, tablero.jugadores[i].desesperacion)
    #print("----------------------")
    
    #print(tablero.jugadores[7].desesperacion,end=',')
    
    tablero.run()
    iteraciones += 1
