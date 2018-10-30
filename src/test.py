from bitstring import BitArray, BitStream
import Leaderboard
import json
import os
from datetime import datetime

print(str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute))

def calculateCheckSum(input):
    tot = 0
    for i in range(8):
        tot += (input>>i) & 1
    return tot

print(calculateCheckSum(0))
print(calculateCheckSum(4))
print(calculateCheckSum(8))
print(calculateCheckSum(9))

