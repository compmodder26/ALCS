###################################################################################
#
# ALCS.py
#
# This program is used to control a pressure sensor, that when
# pressed, will turn a light on.  This is a working small scale prototype of
# a sensor that can be used to signal a car to stop when it has
# reached the correct distance inside of its garage, to be able to close
# the garage door.
#
# A - Automatic
# L - Light
# C - Car
# S - Stopper
#
# Authors - Natalie Helm and Brian Helm
# Natalie's contributions are within the Main Program block and where otherwise
# noted.
#
####################################################################################

import RPi.GPIO as GPIO # Library that allows us to talk with the GPIO pins of the Raspberry Pi
import time # Library that allows us to pause the program (in the case where we want to leave the light on for a certain amount of time or make it blink)

# set up user friendly names for the GPIO pins we are working with
LIGHT = 18 # Pin number we are going to control the light with
ADCCLOCK = 23 # Pin number connected to the ADC (Analog to Digital Converter) Clock
ADCMOSI = 24 # Pin number connected to the ADC MOSI
ADCMISO = 25 # Pin number connected to the ADC MISO
ADCCS = 12 # Pin Number connected to the ADC CS
ADCCHANNEL = 0 # Channel number that the pressure sensor is connected to of the ADC (0 - 7)

# set up GPIO (General Purpose Input/Output)
GPIO.setwarnings(False) # we don't want to see any warnings
GPIO.setmode(GPIO.BCM) # set how the numbers of the pins are interpreted (system or bcm)

# set up the pin modes
GPIO.setup(LIGHT, GPIO.OUT) # we tell the raspberry pi that we want to use this pin to output signal to the light (sending a signal out)
GPIO.setup(ADCCLOCK, GPIO.OUT) # we tell the raspberry pi that we want to use this pin to output signal to the Clock pin on the ADC (sending a signal out)
GPIO.setup(ADCMOSI, GPIO.OUT) # we tell the raspberry pi that we want to use this pin to output signal to the MOSI pin on the ADC (sending a signal out)
GPIO.setup(ADCMISO, GPIO.IN) # we tell the raspberry pi that we want to use this pin to receive information from the MISO pin on the ADC (receiving a signal)
GPIO.setup(ADCCS, GPIO.OUT) # we tell the raspberry pi that we want to use this pin to output signal to the CS pin on the ADC (sending a signal out)



# Function: cleanup()
#
# Will be called at program end to do any necessary cleanup
def cleanup():
	GPIO.cleanup() # Cleans up any instructions we've given the Raspberry Pi about the pins we've been using

# Function: getPressureSensorValue()
#
# Will give the current value that the pressure sensor is reading.
# Values range from 0 (nothing on the sensor) to 1023 (maximum weight the sensor can read)
def getPressureSensorValue():
        GPIO.output(ADCCS, True)      # bring CS high
 
        GPIO.output(ADCCLOCK, False)  # start clock low
        GPIO.output(ADCCS, False)     # bring CS low
 
        commandout = ADCCHANNEL
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(ADCMOSI, True)
                else:
                        GPIO.output(ADCMOSI, False)
                commandout <<= 1
                GPIO.output(ADCCLOCK, True)
                GPIO.output(ADCCLOCK, False)
 
        pressureReading = 0

        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(ADCCLOCK, True)
                GPIO.output(ADCCLOCK, False)
                pressureReading <<= 1
                if (GPIO.input(ADCMISO)):
                        pressureReading |= 0x1
 
        GPIO.output(ADCCS, True)
        
        pressureReading >>= 1       # first bit is 'null' so drop it
        return pressureReading

# Function: lightOn()
#
# When called, this will tell the raspberry pi to turn on the pin that controls the light
# Which will make the light come on
def lightOn():
	GPIO.output(LIGHT, True) # True means that we want to turn it on

# Function: lightOff()
#
# When called, this will tell the raspberry pi to turn off the pin that controls the light
# Which will make the light turn off
def lightOff():
	GPIO.output(LIGHT, False) # False means that we want to turn it off

# Function: Blinky
#
# Makes the light blink for a specified number of seconds
#
# Created by Natalie with the aid of Brian
# Brian made the logic to make it blink for a specific amount of time
# Natalie included the code to turn the light on and off and to have it stay on
# or off for a specific amount of time (everything within the while loop)
def Blinky(secs):
	start = time.time()

	# loop until the difference between the current time reading and the start time reading is >= the number of seconds given
	while (time.time() - start < secs):
		lightOn()
		time.sleep(0.1)
		lightOff()
		time.sleep(0.1)
		
try:
#####################################################
# Natalie's Main Program
#####################################################
	Blinky(10)
#####################################################
# END Natalie's Main Program
#####################################################
except KeyboardInterrupt as e: # handle being interruped by the keyboard (Ctrl-c)
	cleanup()
except Exception as e: # any problem we encounter will result in us cleaning up and exiting
	cleanup()

# catch all cleanup() call
cleanup()
