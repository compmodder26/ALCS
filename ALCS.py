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
import Adafruit_MCP3008 as ADC # Library that allows us to easily talk to the MCP3008 ADC (Analog to Digital Converter)

# set up user friendly names for the GPIO pins we are working with
LIGHT = 18 # Pin number we are going to control the light with
ADCCLOCK = 23 # Pin number connected to the ADC (Analog to Digital Converter) Clock
ADCMOSI = 24 # Pin number connected to the ADC MOSI
ADCMISO = 25 # Pin number connected to the ADC MISO
ADCCS = 12 # Pin Number connected to the ADC CS
ADCCHANNEL = 0 # Channel number of the ADC that the pressure sensor is connected to (0 - 7)

# set up GPIO (General Purpose Input/Output)
GPIO.setwarnings(False) # we don't want to see any warnings
GPIO.setmode(GPIO.BCM) # set how the numbers of the pins are interpreted (system or bcm)

# set up the pin modes
GPIO.setup(LIGHT, GPIO.OUT) # we tell the raspberry pi that we want to use this pin to output signal to the light (sending a signal out)

# Set up ADC Reader
adcReader = ADC.MCP3008(clk=ADCCLOCK, cs=ADCCS, miso=ADCMISO, mosi=ADCMOSI)

# Function: cleanup()
#
# Will be called at program end to do any necessary cleanup
def cleanup():
	GPIO.cleanup() # Cleans up any instructions we've given the Raspberry Pi about the pins we've been using

# Function: getPressureSensorValue()
#
# Will give the current value that the pressure sensor is reading.
# Values range from 0 (nothing on the sensor) to 1023 (maximum pressure)
def getPressureSensorValue():
	return adcReader.read_adc(ADCCHANNEL)

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

# Function: Blinky()
#
# Makes the light blink for a specified number of seconds
#
# Created by Natalie with the help of Brian
# Brian made the logic to make it run for a specific amount of time
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
	Blinky(5)
#####################################################
# END Natalie's Main Program
#####################################################
except KeyboardInterrupt as e: # handle being interruped by the keyboard (Ctrl-c)
	cleanup()
except Exception as e: # any problem we encounter will result in us cleaning up and exiting
	cleanup()

# catch all cleanup() call
cleanup()
