# iAltar
New implementation of artDisplay project

### Crontab entry the redirects to syslog
`@reboot sleep 20; /home/pi/GitProjects/iAltar/iAltar/iAltarWrap.sh 2>&1 | logger -t iAltarWrap`

### make sure the syslog rotation is daily not weekly
check the log file daily since the directory is now smaller, change weekly to daily
keep only two days
sudo vi /etc/logrotate.conf
