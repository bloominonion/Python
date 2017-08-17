import csv
import matplotlib.pyplot as plt
from itertools import zip_longest

# Reads a csv file and plots the points in it. 
# Lines can be split by either a blank line or a
# coloring/line type can be applied. 
# The format for coloring/lines is:
#     "color,linetype"
#     ** All formatting is based on matplotlib styles and colors
#        ('--' = dashed line, etc)

def main():
    csvFile = "debugPolys.csv"

    lines = []
    thisLine = init2dList()
    colors = []
    lType = []
    with open(csvFile,"r") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            vals = []
            try:
                vals = [float(x) for x in row]
            except:
                pass
            if len(vals) < 2:
                if (len(thisLine[0]) > 1 and len(thisLine[1]) > 0):
                    thisLine[0].append(thisLine[0][0])
                    thisLine[1].append(thisLine[1][0])
                    lines.append(thisLine)
                    thisLine = init2dList()
                l = len(row)
                if l == 0:
                    colors.append(None)
                    lType.append(None)
                if l == 1:
                    vals = row[0].split(",")
                    if len(vals) > 1:
                        colors.append(vals[0])
                        lType.append(vals[1])
            else:
                thisLine[0].append(float(row[0]))
                thisLine[1].append(float(row[1]))
        
    index = 0
    for line, lnType, color in zip_longest(lines, lType, colors):
        if color is None:
            color = "black"

        if lnType is None:
            lnType = "--"
            
        plt.plot(line[0],line[1], color=color, linestyle=lnType, linewidth=4)
        index += 1

    plt.show()

def init2dList():
    return  [[] for i in range(2)]

def OldLines():
    pass
    # orig = [
    # 2.05,3.01,
    # 2.29,3.71,
    # 3.39,4.07,
    # 4.57,4.16,
    # 4.66,3.65,
    # 3.8,3.61,
    # 3.22,3.35,
    # 2.85,3.01,
    # 2.05,3.01,
    # 'break','',
    # 2.15,2.23,
    # 2.18,2.46,
    # 2.64,2.6,
    # 2.97,2.63,
    # 3.2,2.5,
    # 3.06,2.35,
    # 2.71,2.28,
    # 2.54,2.11,
    # 2.15,2.23,
    # 'break','',
    # 3.62,2.95,
    # 3.9,3.16,
    # 4.61,3.26,
    # 4.69,3.1,
    # 4.58,2.85,
    # 4,2.71,
    # 3.62,2.95,
    # 'break','']

    # polyx = []
    # polyy = []
    # for i in range(0,len(orig),2):
    #     if orig[i] == 'break':
    #         plt.plot(polyx,polyy,'k-')
    #         polyx = []
    #         polyy = [] 
    #     else:
    #         polyx.append(orig[i])
    #         polyy.append(orig[i+1])

def ExampleFile():
    return """"red,--"
5,2
5,1
0,1
0,2

1,2
2,6
"blue,--"
5,4
5,3
0,3
0,4
"grey,--"
2.05,3.01
2.29,3.71
3.39,4.07
4.57,4.16
4.66,3.65
3.8,3.61,
3.22,3.35
2.85,3.01
2.05,3.01"""

if __name__ == '__main__':
    main()