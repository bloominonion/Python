# Simple script for calculating and reporting the 
# progress percentage of a multi part process.
# e.g.
# group a
#    item 1
#    item 2
#    item 3
#    item 4
# group b
#    item 1
# ...

import timeit
def main():
    nRuns = 50
    runTime1 = timeit.timeit(splitgroups, number=nRuns)
    runTime2 = timeit.timeit(countfirst, number=nRuns)
    print ("T1  :", runTime1)
    print ("T2  :", runTime2)
    print ("Diff:", runTime1-runTime2)

def splitgroups():
    groups = "a b c d".split()
    items = "1 2 3 4".split()
    nGrps = len(groups)
    nItems = len(items)
    for i in range(nGrps):
        groupPct = float(i/nGrps)
        for j in range(nItems):
            itemPct = float(j/nItems)
            pctComplete = (1.0/nGrps) * itemPct + groupPct
            # print ("Processing: {}::{} -- {}".format(i,j, pctComplete) )

def countfirst():
    groups = "a b c d".split()
    items = "1 2 3 4".split()
    total = 0
    for i in range(len(groups)):
        total += len(items)

    i = 0
    for x in range(len(groups)):
        for y in range(len(items)):
            # print ("Processing: {}::{} -- {}".format(x, y, (i/total)) )
            i += 1

if __name__ == '__main__':
    main()