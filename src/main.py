import os
import time
from datetime import datetime
import random
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import json
from bitstring import BitArray, BitStream
from Adafruit_LED_Backpack import SevenSegment

racerTimes = []

delay = 0

RTT_RESPONSE_PACKET = bytes([2, 236]) # 00000010 11101100 

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input    

display = SevenSegment.SevenSegment()
display.begin()

def startRacer(racerId):
    racerTimes.append([racerId, time.time()])
    print("")
    print("-----------------------------------")
    print('Racer ' + racerId + ' On Course')
    print("-----------------------------------")
    print("")

def finishRacer():
    finishTime = int(((time.time() - racerTimes[0][1]) * 1000) / 1000.0)
    finishTime = finishTime + delay/1000
    if(len(str(finishTime).split(".")) == 1):
        finishTime = float(finishTime) + float(random.randint(1, 11))/10)
    racerId = racerTimes[0][0]
    racerTimes.pop(0)

    racerName = idToName(racerId)

    minute = datetime.now().time().minute
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    
    result = {
        "racerID": racerId, 
        #"racerName": racerName, 
        #"runDuration": float(finishTime + float(random.randint(1, 11))/10), 
        "runDuration": float(finishTime),
        "startTime": str(datetime.now().time().hour) + ":" + minute
    }
    writeResult(result)

    formattedFinishTime = floatToDigits(finishTime)
    #print to 7-seg display
    display.clear
    display.set_digit(0, formattedFinishTime[0])
    display.set_digit(1, formattedFinishTime[1])
    display.set_digit(2, formattedFinishTime[2])
    display.set_digit(3, formattedFinishTime[3])
    display.write_display()

    print("")
    print("-----------------------------------")
    print("FINISH TIME")
    print(str(finishTime) + " seconds")
    print("-----------------------------------")
    print("")

    lastFinishStamp = time.time()
    displayActive = true

def parsePacket():
    #read header
    serialRaw = [ord(c) for c in ser.read()]
    header = BitStream(uint=serialRaw[0], length=8)

    #parse header
    length = header.read('uint:4')
    packetType = header.read('uint:4')

    #read and parse body
    serialRaw = [ord(c) for c in ser.read(length)]
    body = BitStream(uint=serialRaw[0], length=8)
    data = body.read('uint:8')

    #read and parse footer
    serialRaw = [ord(c) for c in ser.read(1)]
    footer = BitStream(uint=serialRaw[0], length=8)
    checkSum = footer.read('uint:8')
    
    #recompute checksum and mark packet as error if both checksums don't match
    if (calculateCheckSum(length, 4) + calculateCheckSum(packetType, 4) + calculateCheckSum(data, 8)) != checkSum:
        print("bad checksum")
        return {"type": "error"}

    return outVal {
        "type": packetType,
        "data": data
    }

    # debug
    # print("length " + str(length))
    # print("type " + str(packetType))
    # print("data " + str(data))
    # print("checksum  " + str(checkSum))

def calculateCheckSum(input, n):
    tot = 0
    for i in range(n):
        tot += (input>>i) & 1
    return tot

def writeResult(result):
    fname = os.path.expanduser("~/Desktop/finishLine/ThwackTimingGateServer/data/results.json")

    with open(fname, mode='r') as feedsjson:
        currentResults = json.load(feedsjson)

    currentResults.append(result)

    with open(fname, mode='w') as f:
        f.write(json.dumps(currentResults, indent=4))

# def idToName(id):
#     fname = os.path.expanduser("~/Desktop/finishLine/ThwackTimingGateServer/data/table.json")

#     with open(fname, mode='r') as idTable:
#         conversionTable = json.load(idTable)

#     racerName = conversionTable[0][str(id)]

#     return racerName

#takes in float and returns tens place, ones place, hyphen, tenths place in an array
def floatToDigits(num):
    numParts = str(num).split(".")
    outAry = ["F", "F", "F", "F"]

    if (len(numParts[0]) > 1):
        outAry[0] = numParts[0][-2]
    else:
        outAry[0] = "0"

    if (len(numParts[0][-1]) > 0):
        outAry[1] = numParts[0][-1]
    else:
        outAry[0] = "0"

    outAry[2] = "-"

    if(len(numParts) > 1 and len(numParts[1]) > 0):
        outAry[3] = numParts[1][0]
    else:
        outAry[3] = "0"

    return outAry

while True:
    if ser.inWaiting()>0:
        packet = parsePacket()
        if packet["type"] == 0: 
            startRacer(packet["data"])
        if packet["type"] == 1:
            ser.write(RTT_RESPONSE_PACKET)
        if packet["type"] == 3:
            delay = packet["data"]
            print("new delay: " + delay)

    if GPIO.input(12) == GPIO.LOW:
        finishRacer()
        time.sleep(.5)

    if(displayActive and lastFinishStamp-time.time()>10)
        display.clear()
        display.write_display()
        displayActive = false

    

GPIO.cleanup() # Clean up
