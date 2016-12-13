from turtle import *
setup()
title("turtle test")
clear()

#DRAW A SQUARE
down()        #pen down
forward(50)   #move forward 50 units
right(90)     #turn right 90 degrees
forward(50)
right(90)
forward(50)
right(90)
forward(50)

#INTRODUCE ITERATION TO SIMPLIFY SQUARE CODE
clear()
for i in range(4):
    forward(50)
    right(90)

#INTRODUCE PROCEDURES   
def square(length):
    down()
    for i in range(4):
        forward(length)
        right(90)

#HAVE STUDENTS PREDICT WHAT THIS WILL DRAW
for i in range(50):
    up()
    left(90)
    forward(25)
    square(i)

#NOW HAVE THE STUDENTS WRITE CODE TO DRAW
#A SQUARE 'TUNNEL' (I.E. CONCENTRIC SQUARES
#GETTING SMALLER AND SMALLER).

#AFTER THAT, MAKE THE TUNNEL ROTATE BY HAVING
#EACH SUCCESSIVE SQUARE TILTED