import serial
import threading
import time
import random
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import crc8
import json
from bitstring import BitArray, BitStream
from datetime import datetime


racerTimes = []

delay = 0

RTT_RESPONSE_PACKET = bytes([2, 236]) # 00000010 11101100 

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input

while True:
    if ser.inWaiting()>0:
        packet = parsePacket() #
        if packet["type"] == 0: 
            startRacer(packet.data)
        if packet["type"] == 1:
            ser.write(RTT_RESPONSE_PACKET)
        if packet["type"] == 3:
            delay = packet["data"]

    if GPIO.input(12) == GPIO.LOW:
        finishRacer()
            

def startRacer(racerId):
    racerTimes.append((racerId, time.time()))
    print("")
    print("-----------------------------------")
    print('Racer On Course')
    print("-----------------------------------")
    print("")

def finishRacer():
    finishTime = int((time.time() - racerTimes[0][1]) * 1000) / 1000.0)
    racerId = racerTimes[0][0]
    racerTimes.pop(0)

    result = {
        "racerID": racerID, 
        "racerName": "Name Not Assigned", 
        "runDuration": finishTime, 
        "startTime": str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute)
    }
    addResult(result)

    print("")
    print("-----------------------------------")
    print("FINISH TIME")
    print(str(finishTime) + " seconds")
    print("-----------------------------------")
    print("")

def parsePacket(packet):
    header = BitArray(ser.read(1))
    length = header.read(uint:4)
    packetType = header.read(uint:4)

    print(header)
    print(length)
    print(packetType)


    data = BitArray(ser.read(length))
    CRC8 = BitArray(ser.read(1))

    #recompute CRC and mark packet as error if both CRCs don't match
    if length == 0: 
        packetTop = header.int
    else
        packetTop = int(str(header.int) + str(data.int))
    if calcualteCheckSum(packetTop) != hasher.hexdigest():
        return {"type": "error"}
    
    return {
        "type": packetType,
        "data": data.bin
    }

def addResult(result):
    fname = "test.json"

    with open(fname) as feedsjson:
        currentResults = json.load(json.load)

    currentResults.append(result)

    with open(fname, mode='w') as f:
        f.write(json.dumps(currentResults))

def calculateCheckSum(input):
    tot = 0
    for i in range(8):
        tot += (input>>i) & 1
    return tot

GPIO.cleanup() # Clean up
