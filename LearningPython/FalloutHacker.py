import tkinter as tk
from collections import Counter
from collections import OrderedDict
import os
import re

list = []
guess = ''
reguess = True
prevGuesses = []
errString = []
curPanel = None
spec = os.environ['TEMP'] + "\\FalloutHack.last"


def main(E):
    global list    
    global curPanel
    curPanel.update_idletasks()
    str = E.get().strip()
    curPanel.destroy()

    list = ListFromString(str)
    if CheckInput():
        SaveEntry(str)
    GuessThePassword()
    global reguess
    reguess = False
    _GetLikeness()

def mainPanel():
    offset = 0
    panel = tk.Tk()
    global curPanel
    curPanel = panel
    inPanel = tk.Frame(panel)
    inPanel.pack()
    tk.Label(inPanel, text="Input options:  ").pack( side = "left")
    E1 = tk.Entry(inPanel, bd =5, width = 100)
    E1.bind('<Return>', (lambda event: main(E1)))
    E1.pack(side = "right", fill = "x")
    
    tk.Button(panel, text="Reload last", command = lambda: LoadLast(E1)).pack(side = "left")
    tk.Button(panel, text="Hack!", command = lambda: main(E1), height=2, width=4).pack(side = "right")
    panel.mainloop()


def _GetLikeness():
    likeness = 0
    global guess
    global list
    panel = tk.Tk()
    top = tk.Frame(panel)
    guessText = ("Guess is: %s" %guess)
    tk.Label(top,text=guessText).pack()
    top.pack(side="top",expand=1,fill=tk.BOTH)
    
    defColor = top.cget("background")

    mid=tk.Frame(panel)
    mid.pack()

    btnMinH = 2
    btnMinW = 4

    maxLen = len(max(list, key=len)) + btnMinW
    if len(list) > 1:
        tk.Label(top, text="Enter Likeness:  ").pack(side = tk.LEFT)
        i = 0
        for item in list:
            it = tk.Frame(mid)
            it.pack(expand = 1, fill = tk.BOTH)
            col = "red" if item == guess else defColor
            tk.Button(it, text=item, command = lambda arg=item:EvalListByLikeness(arg,guess,panel), bg=col, width = maxLen, height= btnMinH).grid(row=i, column=0, sticky="WE")
            tk.Button(it, text="0", command = lambda: EvalListByLikeness(0,guess,panel), width= btnMinW, height= btnMinH).grid(row=i, column=1, columnspan=1)
            tk.Button(it, text="1", command = lambda: EvalListByLikeness(1,guess,panel), width= btnMinW, height= btnMinH).grid(row=i, column=2, columnspan=1)
            tk.Button(it, text="2", command = lambda: EvalListByLikeness(2,guess,panel), width= btnMinW, height= btnMinH).grid(row=i, column=3, columnspan=1)
            tk.Button(it, text="3", command = lambda: EvalListByLikeness(3,guess,panel), width= btnMinW, height= btnMinH).grid(row=i, column=4, columnspan=1)
            i += 1

    bot = tk.Frame(panel)
    bot.pack(side="right")
    tk.Button(bot, text = "Exit", command = ExitHack, height=btnMinH + 1, width=btnMinW+2).pack(side="right")
    panel.protocol("WM_DELETE_WINDOW", ExitHack)
    panel.mainloop()

    global reguess
    if reguess:
        GuessThePassword()

def ExitHack():
    print ("Exit requested")
    exit()

def ListFromString(string):
    list = re.split(';|,|\\*|\\n|\\s',string)
    list = [x.upper() for x in list]
    return list

def GuessThePassword():
    global list
    global guess
    global reguess
    from collections import defaultdict
    while True:
        ranking = defaultdict(dict)
        #print ("List is: %s" %list)
        for str in list:
            ind = 0
            for i,c in enumerate(str):
                ranking[str][ind] = 0
                for cmp in list:
                    val = 0
                    if cmp == str:
                        pass
                    if c==cmp[i]:
                        val = 1
                    val += ranking[str][ind]
                    ranking[str][ind] = val
                ind+=1


        for item in ranking.items():
            val = 0
            for v in item[1].items():
                val += v[1]
            ranking[item[0]]['rank']=val  
            #print ("Value for %s is %s" %(item[0],val))

        s = sorted(ranking.items(), key=lambda y: y[1]['rank'], reverse=True)
        guess = s[0][0]
        if len(list) == 1:
            #print ("No more options...Answer is: %s" %guess)
            guess = "Final: %s" %guess
        #print ("Guess is: %s" %guess)
        reguess = False
        _GetLikeness()

def EvalListByLikeness(likeness,guess,p):
    p.destroy()
    print ("Processing list...likeness:%s" %likeness)
    global list
    global prevGuesses

    try:
        likeness = int(likeness)
    except ValueError:
        likeness = likeness.upper()
        print ("Setting %s as DUD" %likeness)
        list = [x for x in list if x != likeness]
        return list

    prevGuesses.append([guess,likeness])
    #print ("Prev: %s" %prevGuesses)
    tmplist = []
    for str in list:
        guessMatch = 0
        for prevGuess in prevGuesses:
            if str == prevGuess[0]:
                continue
            val = 0
            for i,c in enumerate(str):
                if c==prevGuess[0][i]:
                    val += 1
            if val == prevGuess[1]:
                guessMatch += 1
            #print "Checking %s against %s (%s)" %(str,prevGuess,val)
        if guessMatch == len(prevGuesses):
            tmplist.append(str)
    if len(tmplist) == 0:
        print ("Bad likeness. Must be one of the following:")
        print (list)
        return list
    #print tmplist
    reguess = True
    list = tmplist

def CheckInput():
    global list
    global errString
    errors = 0
    if len(list) < 4:
        errString.append("INPUT ERROR: Too few entries found in list: %s" %list)
        errors+=1
    modeItem = Counter(list)
    mode = modeItem.most_common(1)
    mode = len(mode[0][0])
    lenLast=0
    for item in list:
        if len(item) < mode:
            errors += 1
            errString.append("LENGTH ERROR: Item %s too short." %item)
        elif len(item) < lenLast and lenLast != 0:
            errors += 1
            errString.append("LENGTH ERROR: Item %s didn't match last entry." %item)
        lenLast = len(item)
    if errors != 0:
        ErrorHandler()
    else:
        return True

def ErrorHandler():
    global errString
    global curPanel
    #curPanel.destroy()
    panel = tk.Tk()
    top = tk.Frame(panel)
    top.pack()
    for err in errString:
        tk.Label(top,text=err).pack(side = "bottom", anchor = "w")

    bot = tk.Frame(panel)
    bot.pack(side = "bottom")
    tk.Button(bot, text="Exit", command = exit).pack(side = "right")
    panel.mainloop()

def LoadLast(E):
    global spec
    try:
        with open(spec) as data:
            lines = data.readlines()
            try:
                lastStr = lines[-1].rstrip()
                E.insert(0,lastStr)
            except:
                pass
    except:
        print ("No data...")

def SaveEntry(line):
    global spec
    with open(spec,'a+') as data:
        lines = data.readlines()
        try:
            last_line = lines[-1].rstrip()
        except:
            last_line = None
        if line not in lines:
            data.write(line + "\n")

mainPanel()
