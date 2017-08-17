import sys
from enum import IntEnum
def main():
    codes = "0001 0010 0100 1000 0011 0111 1111111111111111111111111111111".split()
    for code in codes:
        print ("{} = {:,}".format(code, ConvertBinary(code)))

    types = [Foo.type.LINE, Foo.type.POLYGON, Foo.type.TEXT]
    typeVal = 0
    for x in types:
        typeVal = typeVal | x
    print (typeVal, ":",bin(typeVal))
    test = 0
    print ("Test:", test)
    test = test | 1
    print ("Test:", test)
    test = test | 3
    print ("Test:", test)

class Foo():
    class type(IntEnum):
        '''
        Enum that stores the possible datatyes for a selection.
        '''
        ALL = 0
        LINE = 1
        POLYGON = 2
        TEXT = 4
        TEXT3D = 8
        ARROW = 16
        DIMENSIONLINE = 32
        DIMENSIONRADIUS = 64
        DIMENSIONARC = 128
        DIMENSIONANGLE = 256
        IMPLIEDPOLYGON = 512

def ConvertBinary(bits):
    val = 0
    mult = 1
    for bit in reversed(bits):
        val += int(bit) * mult
        mult *= 2
    return val

if __name__ == '__main__':
    main()