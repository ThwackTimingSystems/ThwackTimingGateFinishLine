import serial
import threading
import time
import random
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import crc8
from bitstring import BitArray, BitStream


racerTimes = {}

delay = 0

RTT_RESPONSE_PACKET = bytes([2 236]) # 00000010 11101100 

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
hasher = crc8.crc8()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input

while True:
    if ser.inWaiting()>0:
        packet = parsePacket()
        if packet["type"] == 0:
            startRacer()
        if packet["type"] == 1:
            ser.write(RTT_RESPONSE_PACKET)
        if packet["type"] == 3:
            delay = packet["data"]

    if GPIO.input(12) == GPIO.LOW:
        finishRacer()
            

def startRacer
    racerTimes.append(time.time())
    print("")
    print("-----------------------------------")
    print('Racer On Course')
    print("-----------------------------------")
    print("")

def finishRacer()
    finishTime = int((time.time() - racerTimes[0]) * 1000) / 1000.0)
    racerTimes.pop(0)
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
    
    data = BitArray(ser.read(length))
    CRC8 = BitArray(ser.read(1))

    #recompute CRC and mark packet as error if both CRCs don't match
    if length == 0: 
        hasher.update(header.bin)
    else
        hasher.update(int(str(header.bin) + str(data.bin))
    if CRC8.hex != hasher.hexdigest():
        return {"type": "error"}

    if packetType==0 or packetType==1:
        return {"type": packetType}
    else if packetType==3:
        return {
            "type": packetType,
            "data": data.bin
        }


#type numbers
#1 - start
#2 - round trip calculation start
#3 - round trip calculation ack
#4 - round trip calculation report



GPIO.cleanup() # Clean up