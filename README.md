# iAltar
New implementation of artDisplay project
### git the source code
`cd $HOME/GitProjects;git clone git@github.com:sibosop/iAltar.git`
### update the os use apt-get since apt tends to screw up terminal screens
* `sudo apt-get update`
* `sudo apt-get upgrade`

###### If you get stuck on wolfram
* `sudo apt-get purge wolfram-engine`
* `sudo apt-get upgrade`

### setup env
* `cd $HOME/GitProjects/iAltar/setup`
* `cat README.md`
* log out, log back in

### fix the fstab
* `cd $ialtar`
* `sudo cp fstab /etc/fstab`

### make sure the syslog rotation is daily not weekly
check the log file daily since the directory is now smaller, change weekly to daily
keep only two days
sudo vi /etc/logrotate.conf

### get rid of user messages log which are redundant
`sudo cp $HOME/GitProjects/iAltar/rsyslog.conf /etc/rsyslog.conf`
### remove or setup network
`sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`
### update the support packages (fix swap)
* `cd $ialtar`
* `./packageSetup.sh`

### Crontab entry the redirects to syslog
* `MAILTO=""`
* `@reboot sleep 10; /home/pi/GitProjects/iAltar/config/asoundConfig.py -c /home/pi/GitProjects/iAltar/config/ProArts.json 2>&1 | logger -t asoundConfig`

* `@reboot sleep 20 ; /home/pi/GitProjects/iAltar/iAltar/iAltarWrap.sh -c /home/pi/GitProjects/iAltar/config/ProArts.json 2>&1 | logger -t iAltarWrap`




### sound setup info
Setting up usb speakers/mic has the unfortunate feature of assigning usb 'cards' at random during bootup. This will need to be fixed automagically but until that happens:
* `cat /proc/asound/cards`
This will list the 'cards'. This is assuming you are using the adafruint usb mic/speakers recommended by google
* USB-Audio - USB PnP Sound Device - microphone card
* USB-Audio - USB2.0 Device - speaker card
Once you have the card numbers you edit this file:
* `cp ~/GitProjects/AssAi/asoundrc.template ~/.asoundrc`
* `vi ~/.asoundrc`
Change the `pcm: hw:<cardno>,1` to have the proper numbers for the mic and speaker.

Linux uses ALSA for its audio:
* speaker-test 
  * `speaker-test -c2`
* arecord
  * `arecord --format=S16_LE --duration=5 --rate=16k --file-type=raw out.raw`
* aplay
  * `aplay --format=S16_LE --rate=16k out.raw`
* alsamixer (gui) or amixer (command line)
  * amixer -c 2 cset numid=3,name='PCM Playback Volume' 100
* aplay --format=S16_LE --rate=44100  audio3.raw
