import serial
import time
import random
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

END = '!'
START_SEQ = ['s', 't', 'a', 'r', 't']
QUIT_SEQ = ['q', 'u', 'i', 't']
incoming = []
onCourse = False

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input

while True:
    if not onCourse:
        incoming.append(ser.read())
        while incoming[len(incoming) - 1] != END:
            incoming.append(ser.read())
        del incoming[len(incoming) - 1]
        
        if incoming == START_SEQ:
            startTime = time.time()
            onCourse = True
            print("")
            print("-----------------------------------")
            print('Racer On Course')
            print("-----------------------------------")
            print("")
        if incoming == QUIT_SEQ:
            break
    else:
        if GPIO.input(12) == GPIO.LOW:
            print("")
            print("")
            print("")
            print("-----------------------------------")
            print("FINISH TIME")
            print(str(int((time.time() - startTime) * 1000) / 1000.0) + " seconds")
            print("-----------------------------------")
            onCourse = False
            incoming = []

GPIO.cleanup() # Clean up
