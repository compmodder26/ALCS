#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008 as ADC

LIGHT   = 21
ADCCLK  = 18
ADCMISO = 23
ADCMOSI = 24
ADCCS   = 25
ADCCHAN = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT, GPIO.OUT)

adcReader = ADC.MCP3008(clk=ADCCLK, cs=ADCCS, miso=ADCMISO, mosi=ADCMOSI)

def cleanup():
	GPIO.cleanup()

def getPressureSensorValue():
	return adcReader.read_adc(ADCCHAN)

def lightOn():
	GPIO.output(LIGHT, True)

def lightOff():
	GPIO.output(LIGHT, False)

def Blinky(secs):
	start = time.time()

	while (time.time() - start < secs):
		lightOn()
		time.sleep(0.1)
		lightOff()
		time.sleep(0.1)
		
try:
	Blinky(5)

	lastvalue = 0
		
	while (True):
		pressurereading = getPressureSensorValue()

		if pressurereading > 450 and lastvalue < 450:
			Blinky(20)

		lastvalue = pressurereading
		time.sleep(0.1)
except KeyboardInterrupt as e:
	cleanup()
except Exception as e:
	cleanup()

cleanup()
