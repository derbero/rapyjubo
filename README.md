<h1>raspberryPythonJukeBox (rapyjubo)</h1>
<br>
I wanted to build a musicbox that when powered on could read RFID cards to play music. This music should either be local music or Spotify or a web radio station...
a music juke box project with a headless Rasperry Pi
Shopping card:
usb sound card
...


configuration:
alsa / sound related things:

List USB devices:
$ lsusb
Bus 001 Device 004: ID ffff:0035
Bus 001 Device 006: ID 0d8c:0014 C-Media Electronics, Inc.
Bus 001 Device 005: ID 0424:7800 Standard Microsystems Corp.
Bus 001 Device 003: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 002: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

Check whether the sound cards are found
$ cat /proc/asound/cards
 0 [Device         ]: USB-Audio - USB Audio Device
                      C-Media Electronics Inc. USB Audio Device at usb-3f980000.usb-1.1.2, full speed
 1 [ALSA           ]: bcm2835_alsa - bcm2835 ALSA
                      bcm2835 ALSA


The first entry in the list is the RFID reader: vendor: ffff; 
$ sudo nano /etc/modprobe.d/alsa-base.conf:
options snd_usb_audio index=0
options snd_bcm2835 index=1

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

    

projects I came from:


Making it a service:
<br>[Unit]
Description=My Jukebox Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/rapyjubo/jukeBoxDaemon3.py > /home/pi/rapyjubo/jukeBoxDaemon.log 2>&1

[Install]
WantedBy=multi-user.target


References:
