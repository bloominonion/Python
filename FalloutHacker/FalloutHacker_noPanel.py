from collections import Counter, OrderedDict, defaultdict
import os
import re

reguess = True
prevGuesses = []
# Tests string ... answer is WORTH
#optStr = "BEGAN PARTS WHITE WORTH BASED BROKE WHILE GUIDE WHOSE GROWN RAISE RAZOR"
optStr = ""
spec = "FalloutHack.last"

def main():
    global optStr
    optStr = input("Enter options (space/comma/semicolon delimted) >>>")
    optList = ProcessInput(optStr)
    if optList:
        print ("Processing options: \n   %s" %optList)
        status = True
        while status:
            guess, status = GuessThePassword(optList)
            if status:
                likeness = input ("\nGuess is: %s\n   Enter likeness >>> " %guess)
                optList, status, msg = EvalListByLikeness(optList, likeness, guess)
                if not status:
                    print (msg)
            else:
                print ("\nNo more guesses...Answer is: %s" %guess)

def ProcessInput(string):
    optList = re.split(';|,|\\*|\\n|\\s',string)
    optList = [x.upper() for x in optList]
    if CheckInput(optList):
        SaveEntry(optList)
        return optList
    else:
        return False

def GuessThePassword(options):
    ranking = defaultdict(dict)
    for str in options:
        ind = 0
        for i,c in enumerate(str):
            ranking[str][ind] = 0
            for cmp in options:
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
    if len(options) == 1:
        #print ("No more options...Answer is: %s" %guess)
        return guess, False
    return guess, True


def EvalListByLikeness(optList, likeness,guess):
    print ("   Likeness: %s ... removing invalid options..." %likeness)

    if likeness == "":
        print ("Setting %s as DUD" %guess)
        optList = [x for x in optList if x != guess]
        return optList, True, ""
    else:
        try:
            likeness = int(likeness)
        except ValueError:
            likeness = likeness.upper()
            print ("Setting %s as DUD" %likeness)
            optList = [x for x in optList if x != likeness]
            return optList, True, ""

    prevGuesses.append([guess,likeness])
    #print ("Prev: %s" %prevGuesses)
    tmplist = []
    for option in optList:
        guessMatch = 0
        for prevGuess in prevGuesses:
            if option == prevGuess[0]:
                continue
            val = 0
            for i,c in enumerate(option):
                if c==prevGuess[0][i]:
                    val += 1
            if val == prevGuess[1]:
                guessMatch += 1
            #print "Checking %s against %s (%s)" %(option,prevGuess,val)
        if guessMatch == len(prevGuesses):
            tmplist.append(option)
    if len(tmplist) == 0:
        errMsg = "Bad likeness. Must be one of the following:\n %s" %optList
        return None, False, errMsg
    return tmplist, True, ""

def CheckInput(optList):
    errString = ""
    errors = 0
    if len(optList) < 4:
        errString += "INPUT ERROR: Too few entries found in list: %s\n" %optList
        errors+=1
    modeItem = Counter(optList)
    modeF = modeItem.most_common(1)
    mode = len(modeF[0][0])
    lenLast=0
    for item in optList:
        if len(item) < mode:
            errors += 1
            errString += "LENGTH ERROR: Item %s too short.\n" %item
        elif len(item) > mode:
            errors += 1
            errString += "LENGTH ERROR: Item %s too long.\n" %item
        elif len(item) < lenLast and lenLast != 0:
            errors += 1
            errString += "LENGTH ERROR: Item %s didn't match previous entry.\n" %item
        lenLast = len(item)
    if errors:
        print ("%s errors found" %errors)
        print (errString)
        return False
    else:
        return True

def LoadLast():
    global spec
    global optStr
    try:
        with open(spec) as data:
            lines = data.readlines()
            try:
                optStr = lines[-1].rstrip()
            except:
                pass
    except:
        print ("No data...")

def SaveEntry(inputStr):
    global spec
    entry = ' '.join(val for val in inputStr)
    if os.path.exists(spec):
        entry = entry.strip()
        with open(spec,'r+') as data:
            lines = data.read().splitlines()
            if lines:
                if entry not in lines:
                    data.seek(0,2)
                    data.write(entry + "\n")
    else:
        print ("Unable to open spec.")

if __name__ == '__main__':
    main()