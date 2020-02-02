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

class Buzzer():
	def __init__(self):
		super().__init__()
		self.setup()	

	def playLeftBuzzer(self):
		print ('\n    Playing left buzzer...')
		global buzz_left
		self.playBuzzer(buzz_left)
	
	def playRightBuzzer(self):
		print ('\n    Playing right buzzer...')
		global buzz_right
		self.playBuzzer(buzz_right)

	def playBuzzer(self, buzzer):
		for i in range(1, len(song_1)):		# Play song 1
			buzzer.ChangeFrequency(song_1[i])	# Change the frequency along the song note
			time.sleep(buzzer[i] * 0.5)		# delay a note for beat * 0.5s

	def setup(self):
		GPIO.setmode(GPIO.BCM)		# Numbers GPIOs by physical location
		GPIO.setup(Buzzer[0], GPIO.OUT)	# Set pins' mode is output
		GPIO.setup(Buzzer[1], GPIO.OUT)	# Set pins' mode is output
		global buzz_left, buzz_right			# Assign a global variable to replace GPIO.PWM 
		buzz_left = GPIO.PWM(Buzzer[0], 440)	# 440 is initial frequency.
		buzz_right = GPIO.PWM(Buzzer[1], 440)	# 440 is initial frequency.
		buzz_left.start(50)					# Start Buzzer pin with 50% duty ration
		buzz_right.start(50)					# Start Buzzer pin with 50% duty ration

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

	def destory(self):
		buzz_left.stop()					# Stop the buzzer
		buzz_right.stop()					# Stop the buzzer
		GPIO.output(Buzzer[0], 1)		# Set Buzzer pin to High
		GPIO.output(Buzzer[1], 1)		# Set Buzzer pin to High
		GPIO.cleanup()				# Release resource
	
	def __del__(self, name):
		self.destory()


if __name__ == '__main__':		# Program start from here
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
						datefmt="%H:%M:%S")
						
	buzzer = Buzzer()
	# buzzer.playLeftBuzzer()

	x = threading.Thread(target=buzzer.playLeftBuzzer, args=())
	logging.info("Main    : before running playLeftBuzzer")
	x.start()
	logging.info("Main    : wait for the playLeftBuzzer to finish")
	# x.join()
	logging.info("Main    : all done")

