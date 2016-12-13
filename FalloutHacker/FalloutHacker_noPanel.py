import re
import pprint
from collections import Counter

def main():
    while(True):
        #string = raw_input('Enter the options:')
        #if string == '':
        #    print ("No string entered...")
        #    break
        string = "BEGAN PARTS WHITE WORTH BASED BROKE WHILE GUIDE WHOSE GROWN RAISE RAZOR"
        list = re.split(';|,|\\*|\\n|\\s',string)
        list = [x.upper() for x in list]

        # Validate input list
        True if CheckInput(list) else False
        #print list
        if not GuessThePassword(list):
            break

def GuessThePassword(list):
    from collections import defaultdict
    prevGuesses = []
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

        s = sorted(ranking.iteritems(), key=lambda (x, y): y['rank'], reverse=True)
        guess = s[0][0]
        if len(list) == 1:
            print ("No more options...Answer is: %s" %guess)
            return False;
        print ("Guess is: %s" %guess)

        try:
            likeness = raw_input('Likeness >> ')
        except SyntaxError:
            likeness = None
        if likeness == None or likeness == '':
            print ("No likeness value entered...we got it!")
            return False

        try:
            likeness = int(likeness)
        except ValueError:
            likeness = likeness.upper()
            print ("Setting %s as DUD" %likeness)
            list = [x for x in list if x != likeness]
            return False

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
            print list
            return False
        #print tmplist
        list = tmplist

def CheckInput(list):
        errors = 0
        if list < 4:
            print ("ERROR: Too few entries found in list: %s" %list)
            return False
        modeItem = Counter(list)
        mode = modeItem.most_common(1)
        mode = len(mode[0][0])
        for item in list:
            if len(item) < mode:
                errors += 1
                print("Error on %s" %item)
        if errors != 0:
            return False
        else:
            return True

main()