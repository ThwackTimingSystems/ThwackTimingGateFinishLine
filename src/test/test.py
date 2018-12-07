from bitstring import BitArray, BitStream

import json
import os
from datetime import datetime

def testFunc(id):
    fname = os.path.expanduser("~/Desktop/developer/Projects/ThwackRepos/ThwackTimingGateFinishLine/src/test/test2.json")
    with open(fname, mode='r') as idTable:
        conversionTable = json.load(idTable)

    racerName = conversionTable[str(id)]

    return racerName

print("1: " + testFunc("1"))
print("2: " + testFunc("2"))
print("3: " + testFunc("3"))
print("4: " + testFunc("4"))
