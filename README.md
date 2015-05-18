# NYU-Bobst-Library-Reservation-Automator
An automator written in Python to automatically book the room that you want, can be run daily automatically with cron

## Description
This script is for the use of automatically reserving rooms in bobst library.

## Usage
1.) Make a project directory to keep this out of your way
```
[If on OSX]: cd ~/Documents/
[If on Ubuntu]: cd ~

mkdir projects
cd projects
git clone https://github.com/JasonYao/NYU-Bobst-Library-Reservation-Automator.git
```

2.) First you'll need to move and edit the settings file

```
cd NYU-Bobst-Library-Reservation-Automator
mv example.settings.py settings.py
nano settings.py
```
Edit the settings.py file with all the settings (they're pretty self-explainatory), and save by 

```
CTRL + x
y
```

3.) Now you'll need to have your .csv file on hand - build a google docs that asks for a person's username
and password (since it's the most efficient way), and save export the Google form as `userLogins.csv`. If you
don't want to use the .csv format, just manually edit the `settings.py` file.

4.) Simply use `./run.sh` to check and download dependencies if required, and build a localized virtual environment automatically.

OPTIONAL:
To set up daily automatic reservations, it's best to use your own server that's online 24 hours. I will be using [Phi Kappa Sigma's](https://skullhouse.nyc)
webserver since the reservations will nominally be for the use of fraternity members.

5.) run ` ./time ` to have your server/computer run the program every x time. You'll have to manually edit the file to
change the time between jobs, please don't be an ass and set it to every 1 seconds, that'll just wreck your computer,
and I absolve myself of any liability for your stupidity.

NOTE: Only run `./time` ONCE, this will add the job to run every day at 1am by default.

## The Explaination
NYU's Library system makes it annoying for students because each student is limited to one booking every 24 hours.
This script is meant to help alleviate the issue, by having it done automatically for you.

More notably, there is a quirk (read: exploits) of the current system that can help us with these bookings.

1.) The fact that for sanitation purposes, the library system does not actually get rid
	of duplicates, i.e. `JasonYao@nyu.edu` and `JasonYao+1@nyu.edu` are counted as separate
	when dealing with emails. What this means: we can exploit this so that the number of
	friends required to book a room sequentially are lower, enabling us to simply use 1
	person and their duplicate email for each 2-hour block.

2.) The fact that we can utilize web drivers such as with [Selenium](https://selenium-python.readthedocs.org) that can
	help us with automation when dealing with web elements.

Utilizing these two axioms, this simplifies the amount of work required to be much less than we'd normally need.

We first will create a new User class per person, with a .name, .password and .email attribute. Each User will be made to login, and book the room
that was specified in the [settings](settings.py) file.

In the settings file, we will thus create a list of Users, and simply automate the task of logging in, selecting the time/room,
filling out all forms required.

This script follows a naive approach, and will simply book rooms in order of time (i.e. from 0000 -> 0200 etc.).

TODO
Add an array of best times, and have it implement the best time for the number of users.

## Licensing
This software is released under the GNU GPL 2.0 License as described in the [License file](LICENSE).
