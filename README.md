<h1>raspberryPythonJukeBox (rapyjubo)</h1>
<br>
I wanted to build a musicbox that when powered on could read RFID cards to play music. This music should either be local music or Spotify or a web radio station...
a music juke box project with a headless Rasperry Pi coded in Python.
<br>Shopping card:
<br>usb sound card
<br>...


<h2>configuration:</h2>
<h3>alsa / sound related things:</h3>
<br>
<p>List USB devices:</p>
The first entry in the list is the RFID reader: vendor: ffff; product: 0035
Second entry is the sound card: vendor: 0d8c; product: 0014 
<br>
<code>
$ lsusb
<ul>Bus 001 Device 004: ID ffff:0035</ul>
<ul>Bus 001 Device 006: ID 0d8c:0014 C-Media Electronics, Inc.</ul>
<ul>Bus 001 Device 005: ID 0424:7800 Standard Microsystems Corp.</ul>
<ul>Bus 001 Device 003: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub</ul>
<ul>Bus 001 Device 002: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub</ul>
<ul>Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub</ul>
</code>

make the USB sound card index=0
$ sudo nano /etc/modprobe.d/alsa-base.conf: (changed in phoniebox, too)
options snd_usb_audio index=0
options snd_bcm2835 index=1

Check whether the sound cards are found:
$ cat /proc/asound/cards
 0 [Device         ]: USB-Audio - USB Audio Device
                      C-Media Electronics Inc. USB Audio Device at usb-3f980000.usb-1.1.2, full speed
 1 [ALSA           ]: bcm2835_alsa - bcm2835 ALSA
                      bcm2835 ALSA

The 0 is the USB sound card index I set a little earlier
$ sudo nano /etc/asound.conf (changed in phoniebox, too)
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


<h3>Mopidy</h3>



<h3>pigpiod</h3>




<h2>Making it a service:</h2>
create a file and call it jukeboxdaemon.service.
Into that file copy and paste this:
<code>
<br>[Unit]
<br>Description=My Jukebox Service
<br>After=multi-user.target
<br>
<br>[Service]
<br>Type=idle
<br>ExecStart=/usr/bin/python /home/pi/rapyjubo/jukeBoxDaemon3.py > /home/pi/rapyjubo/jukeBoxDaemon.log 2>&1
<br>
<br>[Install]
<br>WantedBy=multi-user.target
</code>
<br>
Now move that file to /lib/systemd/system/jukeboxdaemon.service.
Set permisson to 644:
<code>
<br>$ sudo chmod 644 /lib/systemd/system/sample.service</br>
</code>
Now the unit file has been defined we can tell systemd to start it during the boot sequence :
<code>
<br>$ sudo systemctl daemon-reload</br>
<br>$ sudo systemctl enable jukeboxdaemon.service</br>
</code>
Reboot the Pi and your custom service should run:
sudo reboot
<br>Start / stop / status service 
<code>
<br>$ sudo systemctl start jukeboxdaemon.service
<br>$ sudo systemctl stop jukeboxdaemon.service
<br>$ sudo systemctl status jukeboxdaemon.service
</code>






kleine Helfer
Prozesse mit USer anzeigen 
> ps aux

<h2>Inspiring projects:</h2>
https://blog.mwiedemeyer.de/post/2017/Musikbox-fur-Kind-2/
http://www.linux-community.de/ausgaben/linuxuser/2013/07/raspberry-pi-zur-miniatur-musikzentrale-ausbauen/

<h2>References:</h2>
https://raspberrypi.stackexchange.com/questions/5475/usb-sound-card-found-but-no-output
https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
https://github.com/Fuzzwah/xbmc-rfid-music