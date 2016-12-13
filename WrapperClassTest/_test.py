import ModTest as m

with m.multiAttrObj() as obj:
    print ("Attribute A:")
    for i in range(obj.nAttrA()):
       #print (obj.getAttrA(i))  # This version works
       print (obj.AttrA[i])      # This version fails

    #print ("\nAttribute B:")
    #for i in range(obj.nAttrB()):
    #   #print (obj.getAttrB(i))  # This version works
    #   print (obj.AttrB[i])      # This version fails