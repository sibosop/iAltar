# iAltar
New implementation of artDisplay project

### Crontab entry the redirects to syslog
`@reboot sleep 20; /home/pi/GitProjects/iAltar/iAltar/iAltarWrap.sh 2>&1 | logger -t iAltarWrap`
### for setups with alternate config files
`@reboot sleep 20 ; /home/pi/GitProjects/iAltar/iAltar/iAltarWrap.sh -c /home/pi/GitProjects/iAltar/config/ProArts.json 2>&1 | logger -t iAltarWrap`

### make sure the syslog rotation is daily not weekly
check the log file daily since the directory is now smaller, change weekly to daily
keep only two days
sudo vi /etc/logrotate.conf

### get rid of user messages log which are redondant
`sudo cp $HOME/GitProjects/iAltar/rsyslog.conf /etc/rsyslog.conf`

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
