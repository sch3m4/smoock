#!/usr/bin/env python
#
# IMPORTANT: Do not forget to add the crontab entry: 0 7 * * 1-5 /usr/bin/python /path/to/smoock.py
#
# Written by Chema Garcia (aka sch3m4)
#
# Date: 04/2013
# Project URL: http://github.com/sch3m4/smoock 
# Contact info:
#	Blog......: http://safetybits.net
#	Repos.....: http://github.com/sch3m4
#	Twitter...: http://twitter.com/sch3m4
#	Mail......: chema@safetybits.net
#

import os
import sys
import time
import signal
import random
import threading
import subprocess

AOUTPUT='oss' # mplayer audo output (alsa,pulseaudio,oss,etc.)
MIXER='/usr/bin/ossmix' # audio mixer tool
MIXER_STR='vmix0-outvol' # string to master audio device
MPLAYER='/usr/bin/mplayer' # path to mplayer binary
PLPATH='/home/chema/smoock/sounds/' # path containing the audio files to randomly choose the one to be reproduced

MIN_VOL=10 # min. volume value
MAX_VOL=25 # max. volume value
DELTA=0.5 # volume increment
DELAY=3 # volume increment's delay

PID=None # main child process PID (mplayer)

OPNUM=2 # amount of operations for the challenge
RAND_MIN=1 # min. random value ("mathematic challenge")
RAND_MAX=10 # max. random value ("mathematic challenge")

CHALLENGE_FILE='/home/chema/challenge' # file to write the challenge
CHALLENGE=None # challenge string
CHALLENGESOL=None # challenge solution
CHALLENGE_SOLVED = False # is the challenge solver?
WAKEUP_FILE='/home/chema/solution' # file containing the solution (created by user)


def play_file(path):
	"""
	Reproduces the file given in "path" by using mplayer
	"""
	global PID
	with open(os.devnull,"w") as fnull:
		res = subprocess.Popen([MPLAYER,'-ao',AOUTPUT,path],stdout = fnull, stderr = fnull)
		PID = res.pid

def set_vol(val):
	"""
	Sets the volume to value "val" by using the given mixer (MIXER)
	"""
	with open(os.devnull,"w") as fnull:
		res = subprocess.Popen([MIXER,MIXER_STR,val],stdout = fnull, stderr = fnull)
		os.waitpid(res.pid)

def create_challenge():
	"""
	Function to create a random "mathematic challenge"
	"""
	global CHALLENGE
	global CHALLENGESOL

	op = ['+','-','*','/']
	values = []
	# randomly choose OPNUM operators
	operators = random.sample(op,OPNUM)
	# randomly choose the values
	for i in range(0,OPNUM):
		values.append( str(random.randint(RAND_MIN,RAND_MAX)) )
	# create the string
	result = []
	result.append(values[0])
	for i in range(0,OPNUM):
		result.append(operators[i])
		result.append(values[i])
	# gets the string
	CHALLENGE = " ".join(result)
	# gets the result value (I'll not do it by implementing binary trees ;) )
	CHALLENGESOL = str(eval(CHALLENGE)) # I know you like it :)

	# creates the file
	file = open(CHALLENGE_FILE,"w")				
	file.write(CHALLENGE + "\n" )
	file.close()			


def smooth_clock():
	"""
	Function to choose the file from the "playlist" and reproduce it
	"""
	
	# chooses the file
	file = PLPATH + '/' + random.sample(os.listdir(PLPATH),1)[0]

	while CHALLENGE_SOLVED is False:
		# sets the initial volume value
		curvol = MIN_VOL
		set_vol(str(curvol))
		# plays the file
		play_file(file)
		# smooth effect to increase the volume
		while curvol < MAX_VOL and CHALLENGE_SOLVED is False:
			time.sleep(DELAY)
			curvol += DELTA
			set_vol(str(curvol))

		while CHALLENGE_SOLVED is False:
			# waits for mplayer to finish
			os.waitpid(PID,3)

	# once the challenge has been solved...
	os.kill(PID,signal.SIGKILL)

def check_challenge():
	"""
	Checks the challenge
	"""
	global CHALLENGE_SOLVED

	while CHALLENGE_SOLVED == False:
		try:
			file = open(WAKEUP_FILE,"r")
		except:
			time.sleep(1)
			continue

		resp = file.readline().strip()
		file.close()

		if resp == CHALLENGESOL:
			CHALLENGE_SOLVED = True
			print "Challenge Solved!"
		else:
			print "Incorrect challenge solution!"
			time.sleep(5)


if __name__ == "__main__":

	# creates the "mathematic challenge"
	create_challenge()
	# let's play
	thread = threading.Thread(target = smooth_clock )
	thread.start()
	# checks the challenge response
	check_challenge()
	# waits for the thread
	thread.join()

	# removes the files
	os.remove(CHALLENGE_FILE)
	os.remove(WAKEUP_FILE)

	sys.exit(0);

