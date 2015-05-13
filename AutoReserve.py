#!/usr/bin/env python3
__author__ = 'Jason Yao'

# Majour imports
import datetime
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.support import select

# Package dependent imports
import settings

# Function to turn an into into their string form
def toMonth(someMonth):
    try:
        returnMonth = ''
        if someMonth == 1:
            returnMonth = 'January'
        elif someMonth == 2:
            returnMonth = 'February'
        elif someMonth == 3:
            returnMonth = 'March'
        elif someMonth == 4:
            returnMonth = 'April'
        elif someMonth == 5:
            returnMonth = 'May'
        elif someMonth == 6:
            returnMonth = 'June'
        elif someMonth == 7:
            returnMonth = 'July'
        elif someMonth == 8:
            returnMonth = 'August'
        elif someMonth == 9:
            returnMonth = 'September'
        elif someMonth == 10:
            returnMonth = 'October'
        elif someMonth == 11:
            returnMonth = 'November'
        elif someMonth == 12:
            returnMonth = 'December'
        else:
            raise MonthError(someMonth)
        return returnMonth
    except MonthError as e:
        print('The month did not parse correctly: ' + e.value)
        exit(1)

# Modularizes our code via a main method
def main():
    # Fills in the date wanted, only generated once
    currentDate = datetime.date
    reservationDate = currentDate + datetime.timedelta(days = settings.offsetDays)
    reservationYear = reservationDate.strftime("%Y") # Date in string form for easy comparison
    reservationMonth = toMonth(reservationDate.strftime("%m")) # Month in string form for easy comparison

    # Builds a browser connection
    browser = webdriver.Firefox()

    for i in range(0, len(settings.loginArray)):
        try:
            browser.get(
                'https://login.library.nyu.edu/pds?func=load-login&institute=NYU&calling_system=https:login.library.nyu'
                '.edu&url=https%3A%2F%2Frooms.library.nyu.edu%2Fvalidate%3Freturn_url%3Dhttps%253A%252F%252Frooms.'
                'library.nyu.edu%252F%26https%3A%2F%2Flogin.library.nyu.edu_action%3Dnew%26https%3A%2F%2Flogin.'
                'library.nyu.edu_controller%3Duser_sessions')
            browser.find_element_by_class_name('btn').click()

            # Fills in login information
            username = browser.find_element_by_name('netid')
            password = browser.find_element_by_name('password')
            login = browser.find_element_by_class_name('uppercase rounded')

            # Signs into bobst reserve with the username and password
            username.send_keys(settings.loginArray[i].username)
            password.send_keys(settings.loginArray[i].password)
            login.click()

            ##### START OF FUCKING AROUND WITH THE DATEPICKER #####TODO HOLY SHIT BALLS THIS IS HARD WTF KIND OF RETARDED SHIT IS NYU UP TO
            datePicker = browser.find_element_by_xpath("//div[@id='ui-datepicker-div']").click()

            # Checks the month and year
            datePickerYear = browser.find_element_by_xpath("//div[@class='ui-datepicker-year']")
            datePickerYear = datePickerYear.text
            datePickerMonth = browser.find_element_by_xpath("//div[@class='ui-datepicker-month']")
            datePickerMonth = datePickerMonth.text

            # Alters year
            while (datePickerYear != reservationYear):
                # Right clicks the month until it is correct year
                browser.find_element_by_xpath("//a[@class='ui-datepicker-next ui-corner-all']").click()
                datePickerYear = browser.find_element_by_xpath("//div[@class='ui-datepicker-year']")
                datePickerYear = datePickerYear.text
            # Alters month
            while (datePickerMonth != reservationMonth):
                # Right clicks the month until it is correct month
                browser.find_element_by_xpath("//a[@class='ui-datepicker-next ui-corner-all']").click()
                datePickerMonth = browser.find_element_by_xpath("//div[@class='ui-datepicker-month']")
                datePickerMonth = datePickerMonth.text

            # At this, point, we are on the correct year & month. Selects the date below
            browser.find_element_by_xpath("//tbody/td[@class=' ']")
            browser.find_element_by_css_selector()
            ##### END OF FUCKING AROUND WITH THE DATEPICKER #####

            # Finds the time
            timeStart = i*2
            startMorning = True

            if (timeStart >= 12) & (timeStart < 24):
                startMorning = False
                timeStart -= 12

            # Deals with the time TODO Finish the part with the time clicking
            select(browser.find_element_by_css_selector("select#reservation_hour")).select_by_value(timeStart).click()

            select(browser.find_element_by_css_selector("select#reservation_minute")).select_by_value('0').click()

            # Selects AM/PM
            if startMorning:
                select(browser.find_element_by_css_selector("select#reservation_ampm")).select_by_value('am').click()
            else:
                select(browser.find_element_by_css_selector("select#reservation_ampm")).select_by_value('pm').click()

            # Selects the time length
            select(browser.find_element_by_css_selector("select#reservation_how_long")).select_by_value('120').click()

            # Clicks the button
            browser.find_element_by_css_selector("button#generate_grid").click()

            # Fills in the description of the booking
            description = browser.find_element_by_id("reservation_title")
            description.send_keys(settings.description)

            # Fills in the duplicate email for the booking
            duplicateCC = browser.find_element_by_id("reservation_cc")
            duplicateCC.send_keys(settings.loginArray[i].emailDuplicate)

            # Selects the room
            browser.find_element_by_xpath\
                ("//tbody/tr[3]/td[@class='timeslot timeslot_available timeslot_preferred timeslot_preferred_first']").click()

            # Submits
            browser.find_element_by_xpath("//button[@class='btn btn-lg btn-primary']").click()

            # Logout
            browser.get('https://rooms.library.nyu.edu/logout')

        except WebDriverException:
            print("Shit, something went wrong.")

    # Close browser connection
    browser.close()
    return

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()
