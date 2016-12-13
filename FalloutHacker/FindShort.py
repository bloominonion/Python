import re
import pprint
from collections import Counter


def main():
    while(True):
        string = "RECYCLING FAVORABLE WASTELORD HUMANKIND ELABORATE ATTACKERS ADVERTISE AUTHORITY BEAUTIFUL DESERTERS FEARFULLY GYMNASIUM"
        list = re.split(';|,|\\*|\\n|\\s',string)
        list = [x.upper() for x in list]

        True if CheckInput(list) else False

        quit()



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