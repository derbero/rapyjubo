<h1>raspberryPythonJukeBox (rapyjubo)</h1>
<br>
I wanted to build a musicbox that when powered on could read RFID cards to play music. This music should either be local music or Spotify or a web radio station...
a music juke box project with a headless Rasperry Pi
Shopping card:
usb sound card
...


<h2>configuration:</h2>
<h3>alsa / sound related things:</h3>

List USB devices:
The first entry in the list is the RFID reader: vendor: ffff; product: 0035
Second entry is the sound card: vendor: 0d8c; product: 0014 
$ lsusb
Bus 001 Device 004: ID ffff:0035
Bus 001 Device 006: ID 0d8c:0014 C-Media Electronics, Inc.
Bus 001 Device 005: ID 0424:7800 Standard Microsystems Corp.
Bus 001 Device 003: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 002: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

make the USB sound card index=0
$ sudo nano /etc/modprobe.d/alsa-base.conf:
options snd_usb_audio index=0
options snd_bcm2835 index=1

Check whether the sound cards are found:
$ cat /proc/asound/cards
 0 [Device         ]: USB-Audio - USB Audio Device
                      C-Media Electronics Inc. USB Audio Device at usb-3f980000.usb-1.1.2, full speed
 1 [ALSA           ]: bcm2835_alsa - bcm2835 ALSA
                      bcm2835 ALSA

The 0 is the USB sound card index I set a little earlier
$ sudo nano /etc/asound.conf
defaults.pcm.!card 0
defaults.ctl.!card 0

$ aplay -l
card 0: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 7/7
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
card 1: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

Test the sound (will output a noise from left to right and back):
$ speaker-test -c2


    
<h3>RFID reader</h3>
The RFID reader is tricky to get input from as it behaves like a keyboard entering the number and <Enter>. Running in headless mode I had to do this to get the input to the shell.

Set up a udev rule to grant only this user access to your RFID reader:
$ sudo nano /etc/udev/rules.d/80-rfid.rules
SUBSYSTEMS=="usb" ATTRS{idVendor}=="ffff" ATTRS{idProduct}=="0035"  MODE:="0660" SYMLINK+="RFID" OWNER="pi"



projects I came from:
https://blog.mwiedemeyer.de/post/2017/Musikbox-fur-Kind-2/
http://www.linux-community.de/ausgaben/linuxuser/2013/07/raspberry-pi-zur-miniatur-musikzentrale-ausbauen/




Making it a service:
<br>[Unit]
Description=My Jukebox Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/rapyjubo/jukeBoxDaemon3.py > /home/pi/rapyjubo/jukeBoxDaemon.log 2>&1

[Install]
WantedBy=multi-user.target

Start / stop / status service 
$ sudo systemctl start jukeboxdaemon.service
$ sudo systemctl stop jukeboxdaemon.service
$ sudo systemctl status jukeboxdaemon.service

References:
https://raspberrypi.stackexchange.com/questions/5475/usb-sound-card-found-but-no-output
https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
https://github.com/Fuzzwah/xbmc-rfid-music