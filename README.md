# iAltar
New implementation of artDisplay project

### Crontab entry the redirects to syslog
`@reboot sleep 20; /home/pi/GitProjects/iAltar/iAltar/iAltarWrap.sh 2>&1 | logger -t iAltarWrap`
