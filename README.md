# NYU-Bobst-Library-Reservation-Automator
An automator written in Python to automatically book the largest available room, can be paired with cron to run daily

## Description
This script is for the use of automatically reserving rooms in bobst library.

## Usage

    1.) First you'll need to move and edit the settings file
```
mv example.settings.py settings.py
nano settings.py
```
    2.) Simply use ./AutoReserve.py to run the program.

    OPTIONAL:
    To set up daily automatic reservations, it's best to use your own server that's online 24 hours. I will be using [Phi Kappa Sigma's](skullhouse.nyc)
    webserver since the reservations will nominally be for the use of fraternity members.
    TODO


## The Explaination
NYU's Library system may be robust and have annoying features that can make it difficult to automate,
but there are some exploits that we can use.

    1.) The fact that for sanitation purposes, they do not actually get rid of duplicates, i.e.
        JasonYao@nyu.edu and JasonYao+1@nyu.edu are counted as separate when dealing with emails.
        What this means: we can exploit this so that the number of friends required to automate are
        lower, enabling us to simply use 1 person and their duplicate email for each 2-hour block.
    2.) The fact that we can utilize web drivers such as with [Selenium](https://selenium-python.readthedocs.org/) that can help us with
        automation.

Utilizing these two facets, this simplifies the amount of work required is much less negligable. We first will create a new User class per person,
with a .name, .password and .email attribute.

In the settings file, we will thus create a list of Users, and simply automate the task of logging in, selecting the time/room, and filling out all the forms

## Licensing
This software is released under the GNU GPL 2.0 License as described in the [License file](LICENSE).
