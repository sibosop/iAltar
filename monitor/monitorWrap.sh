#!/bin/bash

while true; do
  args=""
  for i in $@
  do
    args="$args $i "
  done
  export PYTHONUNBUFFERED=true
  /home/pi/GitProjects/iAltar/monitor/monitor.py $args
  rc=$?
  case $rc in
    3) echo doing poweroff; sudo poweroff
    ;;
    4) echo doing reboot; sudo reboot
    ;;
    5) echo doing stop; exit 0
    ;;
    *)
    ;;
  esac
done
