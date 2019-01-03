# iAltar
New implementation of artDisplay project

### Crontab entry the redirects to syslog
`sleep 20; /home/pi/GitProjects/iAltar/iAltar/iAltarWrap.sh 2>&1 | logger -t iAltarWrap`
