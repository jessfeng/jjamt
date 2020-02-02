#!/usr/bin/env python
#---------------------------------------------------
#
#	This is a program for Passive Buzzer Module
#		It will play simple songs.
#	You could try to make songs by youselves!
# 
#		Passive buzzer 			   Pi 
#			VCC ----------------- 3.3V
#			GND ------------------ GND
#			SIG ---------------- Pin 11
#
#---------------------------------------------------

import RPi.GPIO as GPIO
import time
import logging
import threading

BuzzerList = [11, 12]
LED = [20,21]

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes

song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
			1, 1, 1, 1, 1, 1, 3, 1, 
			1, 3, 1, 1, 1, 1, 1, 1, 
			1, 2, 1, 1, 1, 1, 1, 1, 
			1, 1, 3	]

song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]

beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
			1, 1, 2, 2, 1, 1, 3, 1, 
			1, 2, 2, 1, 1, 2, 2, 1, 
			1, 2, 2, 1, 1, 3 ]

buzz_left = None 
buzz_right = None
global led_on, buzzer_on

class Buzzer():
	def __init__(self):
		super().__init__()
		self.setup()
		global led_on, buzzer_on
		led_on = False	
		buzzer_on = False

	def playLeftBuzzer(self):
		print ('\n    Playing left buzzer...')
		self.playBuzzer(BuzzerList[0])
	
	def playRightBuzzer(self):
		print ('\n    Playing right buzzer...')
		self.playBuzzer(BuzzerList[1])

	def playBuzzer(self, buzzer):
		global buzzer_on
		buzzer_on = True
		start_time = time.time()
		while buzzer_on:
			GPIO.output(buzzer,GPIO.HIGH)
			print("beeep")
			GPIO.output(buzzer,GPIO.LOW)
			print("noooo")
			time.sleep(0.1)
			end_time = time.time()
			if (end_time - start_time > 2):
				 buzzer_on = False
				
	def closeBuzzer(self):
		global buzzer_on
		buzzer_on = False

	
	def lightLeftLED(self):
		a=0
		self.dc = 50
		self.p.ChangeDutyCycle(self.dc)
		
		global led_on
		led_on = True
		start_time = time.time()
		while led_on:
			a +=1
			if ( a == 5):
				self.freq += 5
				self.p.ChangeFrequency(self.freq)
			time.sleep(1)
			# print(freq)
			end_time = time.time()
			if (end_time - start_time > 1): 
				led_on = False
				self.dc = 0
				self.p.ChangeDutyCycle(self.dc)
	
	def closeLED(self):		
		global led_on
		led_on = False
	
	def setup(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)		# Numbers GPIOs by physical location
		GPIO.setup(BuzzerList[0], GPIO.OUT)	# Set pins' mode is output
		GPIO.setup(BuzzerList[1], GPIO.OUT)	# Set pins' mode is output
		# global buzz_left, buzz_right			# Assign a global variable to replace GPIO.PWM 
		# buzz_left = GPIO.PWM(BuzzerList[0], 440)	# 440 is initial frequency.
		# buzz_right = GPIO.PWM(BuzzerList[1], 10)	# 440 is initial frequency.
		# buzz_left.start(50)					# Start Buzzer pin with 50% duty ration
		# buzz_right.start(50)					# Start Buzzer pin with 50% duty ration
		
		# LED
		GPIO.setup(LED[0], GPIO.OUT)  # Set GPIO pin 12 to output mode.
		self.freq = 10
		self.p = GPIO.PWM(LED[0], self.freq)   # Initialize PWM on pwmPin 40Hz frequency

		# main loop of program   
		self.dc = 0
		self.p.start(self.dc)                      # Start PWM with 0% duty cycle                         

	def loop(self):
		while True:
			print ('\n    Playing song 1...')
			for i in range(1, len(song_1)):		# Play song 1
				buzz_left.ChangeFrequency(song_1[i])	# Change the frequency along the song note
				time.sleep(buzz_left[i] * 0.5)		# delay a note for beat * 0.5s
			time.sleep(1)						# Wait a second for next song.

			print ('\n\n    Playing song 2...')
			for i in range(1, len(song_2)):     # Play song 1
				buzz_left.ChangeFrequency(song_2[i]) # Change the frequency along the song note
				time.sleep(buzz_left[i] * 0.5)     # delay a note for beat * 0.5s
	
	def execute(self, command):
		global buzzer_on, led_on
		if (command == "playLeftBuzzer" and buzzer_on == False):
			t1 = threading.Thread(target=self.playLeftBuzzer, args=())
			t1.start()
		elif (command == "playRightBuzzer" and buzzer_on == False):
			t2 = threading.Thread(target=self.playRightBuzzer, args=())
			t2.start()
		elif (command == "lightLeftLED" and led_on == False):
			t3 = threading.Thread(target=self.lightLeftLED, args=())
			t3.start()
		# elif (command == "lightRightLED" and led_on == False):
			# t1 = threading.Thread(target=self.lightRightLED, args=())
			# t1.start()
		else:
			print("Buzzer is on")

	def destory(self):
		# global buzz_left, buzz_right
		# buzz_left.stop()					# Stop the buzzer
		# buzz_right.stop()					# Stop the buzzer
		# GPIO.output(Buzzer[0], 1)		# Set Buzzer pin to High
		# GPIO.output(Buzzer[1], 1)		# Set Buzzer pin to High
		# GPIO.output(LED[1], 1)		# Set Buzzer pin to High
		# GPIO.output(LED[1], 1)		# Set Buzzer pin to High
		GPIO.cleanup()				# Release resource
	
	def __del__(self):
		self.destory()


if __name__ == '__main__':		# Program start from here
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
						datefmt="%H:%M:%S")
						
	buzzer = Buzzer()
	# buzzer.playLeftBuzzer()

	t1 = threading.Thread(target=buzzer.playRightBuzzer, args=())
	logging.info("Main    : before running playLeftBuzzer")
	t1.start()
	logging.info("Main    : wait for the playLeftBuzzer to finish")
	# x.join()
	logging.info("Main    : all done")
	
	t2 = threading.Thread(target=buzzer.lightLeftLED, args=())
	t2.start()
	
	
	time.sleep(5)
	# t3 = threading.Thread(target=buzzer.closeLED, args=())
	# t3.start()
	# t4 = threading.Thread(target=buzzer.closeBuzzer, args=())
	# t4.start()

