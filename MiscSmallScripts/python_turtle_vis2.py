from turtle import *
from math import sin,cos
setup()
title("turtle test")
clear()

#INTRODUCE PROCEDURES   
def square(length):
    down()
    for i in range(4):
        forward(length)
        right(90)

def circ(radius):
    THETA = 0
    STEPS = 100
    OrigX = 0
    OrigY = 0
    for i in range(STEPS):
        down()
        if THETA > 2*pi:
            break
        x = (OrigX + radius*cos(THETA))
        y = (OrigY + radius*sin(THETA))
        goto(x,y)
        if i == 1:
            clear()
        THETA += (2*pi)/STEPS
    up()

circ(20)
done()

#HAVE STUDENTS PREDICT WHAT THIS WILL DRAW
#for i in range(50):
#    up()
#    left(90)
#    forward(25)
#    square(i)

#NOW HAVE THE STUDENTS WRITE CODE TO DRAW
#A SQUARE 'TUNNEL' (I.E. CONCENTRIC SQUARES
#GETTING SMALLER AND SMALLER).

#AFTER THAT, MAKE THE TUNNEL ROTATE BY HAVING
#EACH SUCCESSIVE SQUARE TILTED
