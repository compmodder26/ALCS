###################################################################################
#
# ALCS.py
#
# This program is used to control a pressure sensor, that when
# pressed, will turn a light on.  This is a working prototype of a sensor
# that can be used (when at full scale) to signal a car to stop when it has
# reached the correct distance inside of its garage, to be able to close
# the garage door.
#
# A - Automatic
# L - Light
# C - Car
# S - Stopper
#
# Authors - Natalie Helm and Brian Helm
#
####################################################################################

import RPi.GPIO as GPIO # Library that allows us to talk with the GPIO pins of the Raspberry Pi
import time # Library that allows us to pause the program (in the case where we want to leave the light on for a certain amount of time)

# Pin number we are going to control the light with
LIGHT = 18

# set up GPIO
GPIO.setwarnings(False) # we don't want to see any warnings
GPIO.setmode(GPIO.BCM) # set how the numbers of the pins are interpreted (system or bcm)

# set up the light controlling pin
GPIO.setup(LIGHT, GPIO.OUT) # we tell the raspberry pi that we want to use this pin for output (sending a signal out)

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


#####################################################
# Main Program
#####################################################



#####################################################
# END Main Program
#####################################################

# We should always call this at the end of our program, if we are working with GPIO.  
# That cleans up any instructions we've given the Pi about the pins we've been using
GPIO.cleanup()
