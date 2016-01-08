from visual import *
from math import sin, cos


scene.title = "Projectile Motion!!"
scene.x = 0
scene.y = 0
scene.width = 1500
scene.height = 600
scene.center = (100,10,0)
scene.autoscaling = 1

ANGLE = 50
InitVel = 35

# Set acceleration in each direction (m/s^2)
XAccel = 0
YAccel = -9.8
ZAccel = 0

# Initial positions for each direction
X0 = 0
Y0 = 0
Z0 = 0

BallRadius = 2


Ball = sphere(pos=vector(X0, Y0, Z0),radius=(BallRadius), make_trail = true)
GROUND = box(pos=vector(100,-1,0),size=(200,2,50))

Dt = 0.01 # Time interval for drawing

BallVector = vector(InitVel*cos(ANGLE*pi/180), InitVel*sin(ANGLE*pi/180),0)
Fgrav = vector(0,YAccel*Dt,0)

Scaling=3
arrow(pos=Ball.pos, axis=BallVector/Scaling, shaftwidth=1)
DIR = arrow(pos=Ball.pos, axis=BallVector/(Scaling), shaftwidth=0.2, color=(1,0,0))

FINISHED = 0
TIME = 0
while not FINISHED:
    TIME += Dt
    rate(60)
    BallVector = BallVector+Fgrav
    Ball.pos += BallVector*Dt
    DIR.pos = Ball.pos
    DIR.axis = BallVector/(Scaling)
    if ((TIME - int(TIME)) > 0.99):
        print "TIME: ", str(int(TIME))
        print "POS : ", Ball.pos
        arrow(pos=Ball.pos, axis=(BallVector/Scaling), shaftwidth=1)
    if Ball.y < (BallRadius/2) and TIME > 0.5:
        print "Position: ", Ball.pos
        print "Time:     ", str(TIME)
        FINISHED = 1
        
