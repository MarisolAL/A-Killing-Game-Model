import random
import numpy


vecino_feo = [50,100]
vecino_bueno = [100,0]
velocidad_inicial = [random.uniform(0,1), random.uniform(0,1)]

def act_velocidad(velocidad_act, vecino_bueno, vecino_feo, x,w=0.5, f=0.3, b=0.2):
    vel = [0]*len(velocidad_act)
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    for i in range(len(velocidad_act)):
        f1 = w*velocidad_act[i]
        f2 = r1*b*(vecino_bueno[i]-x[i])
        f3 = r2*f*(vecino_feo[i]-x[i])
        vel[i] = f1+f2-f3
    return vel

def act_x(x, velocidad):
    velocidad = numpy.asarray(velocidad)
    x_a = [0]*len(x)
    for i in range(len(x)):
        val = (int)(x[i]+velocidad[i])
        x_a[i] = val if val>0 else 0
    return x_a

x = [0,0]
vel = act_velocidad(velocidad_inicial,vecino_bueno,vecino_feo,x)
for i in range(0,10):
    print(x,vel)
    vel = act_velocidad(vel,vecino_bueno,vecino_feo,x)
    x = act_x(x,vel)
