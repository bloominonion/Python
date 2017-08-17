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
groups = "a b c d".split()
items = "1 2 3 4".split()

nGrps = len(groups)
nItems = len(items)
for i in range(nGrps):
    groupPct = float(i/nGrps)
    for j in range(nItems):
        itemPct = float(j/nItems)
        pctComplete = (1.0/nGrps) * itemPct + groupPct
        print ("Processing: {}::{} -- {}".format(i,j, pctComplete) )