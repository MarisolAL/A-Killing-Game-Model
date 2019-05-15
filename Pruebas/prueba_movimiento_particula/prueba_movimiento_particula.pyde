import random

malla = [[0 for x in range(100)] for y in range(100)]
vecino_feo = [70,90]
vecino_bueno = [30,10]
velocidad_inicial = [random.uniform(0,1), random.uniform(0,1)]


def act_velocidad(velocidad_act, vecino_bueno, vecino_feo, x,w=0.1, f=0.2, b=0.2):
    vel = [0]*len(velocidad_act)
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    for i in range(2):
        f1 = w*velocidad_act[i]
        f2 = r1*b*(vecino_bueno[i]-x[i])
        f3 = r2*f*(vecino_feo[i]-x[i])
        vel[i] = f1+f2-f3
    return vel

def act_x(x, velocidad):
    x_a = [0]*len(x)
    for i in range(len(x)):
        val = (int)(x[i]+velocidad[i])
        if val>=100:
            val = 0
        if val < 0:
            val = 99 
        x_a[i] = val
    return x_a

x = [0,0]
vel = act_velocidad(velocidad_inicial,vecino_bueno,vecino_feo,x)

def setup():
    size(700,700)
    background(0,0,0)
    frameRate(1)
    
def draw():
    global x
    global vel
    background(0,0,0)
    fill(127, 0, 0)
    rect(vecino_feo[0]*7,vecino_feo[1]*7, 7,7)
    fill(0,100,255)
    rect(vecino_bueno[0]*7,vecino_bueno[1]*7,7,7)
    fill(255,100,100)
    rect(x[0]*7,x[1]*7,7,7)
    vel = act_velocidad(vel,vecino_bueno,vecino_feo,x)
    x = act_x(x,vel)
    
