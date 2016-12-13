import random
board = [['*' for i in range(3)] for j in range(3)]
mode = 2

def PrintBoard(board):
    length = len(board)
    printLn = '   '
    for i in range(1,length+1):
        printLn += ' %s' %i
    printLn += "\n   " + '-' * 6 + "\n"
    for i in range(1,length+1):
        printLn += ' %s|' %i
        for spot in board[i-1]:
            printLn += ' %s' %spot
        printLn += "\n"
    print (printLn)

def askmove(piece):
    global mode
    global nMoves
    while True:
        try:
            if mode == 1:
                x,y = map(int, input('\nEnter move for %s> ' %piece))
                #print ("Input %s/%s" %(x,y))
            else:
                x,y = random.randrange(1,4), random.randrange(1,4)

            if board[x-1][y-1] == '*':
                board[x-1][y-1] = piece
            else:
                continue
        except (ValueError, IndexError):
            pass
        else:
            break
    print ("----------")
    PrintBoard(board)
    nMoves +=1
    if ([piece] * 3 in board or
        (piece,) * 3 in zip(*board) or
        all(board[i][i] == piece for i in range(3)) or
        all(board[i][2-i] == piece for i in range(3))):
        print(piece, 'wins.')
    elif all(p!='*' for row in board for p in row):
        print('Tie.')
    else:
        return True
    

mode = int(input("Select play mode: 1v1 (1) or Auto(2) >"))
if (mode == 1):
   print ("Enter moves as YX(Vert/Horiz) values:")
   PrintBoard(board)
nMoves = 0
while askmove('X') and askmove('O'):
    pass

print ("Result in %s moves" %nMoves)

print ("Result in %s moves" %nMoves)
