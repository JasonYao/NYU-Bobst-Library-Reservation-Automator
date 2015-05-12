#!/usr/bin/env python3
__author__ = 'Jason Yao'

# Majour imports
import sys
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Package dependent imports
import settings

# Modularizes our code via a main method
def main():
    browser = webdriver.Firefox()
    browser.get('https://login.library.nyu.edu/pds?func=load-login&institute=NYU&calling_system=https:login.library.nyu.edu&url=https%3A%2F%2Frooms.library.nyu.edu%2Fvalidate%3Freturn_url%3Dhttps%253A%252F%252Frooms.library.nyu.edu%252F%26https%3A%2F%2Flogin.library.nyu.edu_action%3Dnew%26https%3A%2F%2Flogin.library.nyu.edu_controller%3Duser_sessions')
    browser.find_element_by_class_name('btn').click()

    # Fills in login information
    username = browser.find_element_by_name('netid')
    password = browser.find_element_by_name('password')
    login = browser.find_element_by_class_name('uppercase rounded')

    # Signs into bobst reserve with the username and password
    username.send_keys(settings.overallUsername)
    password.send_keys(settings.overallPassword)
    login.click()

    # Fills in the date wanted
    currentDate = datetime.date.strftime("%m/%d/%y")
    reservationDate = str(currentDate + datetime.timedelta(days = settings.offsetDays))
    dateWanted = browser.find_element_by_name('reservation[which_date]')
    dateWanted.send_keys(reservationDate)

    # Logic to see how many friend's emails are available
    size = len(settings.friends)

    #TODO note: Will need to wrap the entire thing in a for-loop, and get passwords from 1/2 the people at least

    return

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
  main()
