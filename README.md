Smoock
======

Smoock is a little python script to wake up smoothly ;-)

It randomly chooses a file from a given path, and reproduces it increasing the volume.

In order to close the program (and mute the sound) you will have to solve a "mathematic challenge". Unless you solve it, the music will stay rockin'!!!

Installation instructions
=========================

1) Just place the script wherever you want (keep in mind the path!), let's assume /home/chema/smoock/ as path, so the absolute path to the script is: /home/chema/smoock/smoock.py

2) Create a directory called "sounds" within the main path: "/home/chema/smoock/sounds/"

3) Copy the sounds you want to listen when you wake up into the path above

	$ ls -1 /home/chema/smoock/sounds/
	sound1.mp3
	sound2.mp3
	sound3.wav
	sound4.ogg


4) Edit the script "smoock.py" and set the new path: PLPATH = '/home/chema/smoock/sounds'


5) Edit the script "smoock.py" and set the new challenge path:

	CHALLENGE_FILE='/path/to/your/daily/challenge'
	WAKEUP_FILE='/path/to/your/challenge/response'


6) Edit the script "smoock.py" and modify your mixer settings


OPTIONAL: You might also want to change the settings about delays,increments,etc.


*** IMPORTANT NOTE 1 ***
You must to add the script to your crontab (or another daemon like cron)

Example: 0 7 * * 1-5 /usr/bin/python /path/to/smoock.py


*** IMPORTANT NOTE 2 ***

Make sure your system date is correct! For this task you can add another crontab entry like follows:


0 5 * * * /usr/sbin/ntpdate your.favourite.ntp.server


Have fun!!
