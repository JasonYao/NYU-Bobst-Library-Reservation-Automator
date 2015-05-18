#!/bin/bash -e

#write out current crontab
crontab -l > tempCron

#echo new cron into cron file
echo "00 1 * * * ~/projects/NYU-Bobst-Library-Reservation-Automator/time.sh" >> tempCron

#install new cron file
crontab tempCron
rm tempCron
