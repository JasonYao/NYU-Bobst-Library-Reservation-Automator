__author__ = 'Jason Yao'

# Majour imports
import datetime

# Web driver imports
# Common imports
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Support imports
from selenium.webdriver.support import select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Package dependent imports
import settings

# Error Handling imports
from bin import ValidationError

# Function to turn an into into their string form
def toMonth(someMonth):
    try:
        returnMonth = ''
        if someMonth == '01':
            returnMonth = 'January'
        elif someMonth == '02':
            returnMonth = 'February'
        elif someMonth == '03':
            returnMonth = 'March'
        elif someMonth == '04':
            returnMonth = 'April'
        elif someMonth == '05':
            returnMonth = 'May'
        elif someMonth == '06':
            returnMonth = 'June'
        elif someMonth == '07':
            returnMonth = 'July'
        elif someMonth == '08':
            returnMonth = 'August'
        elif someMonth == '09':
            returnMonth = 'September'
        elif someMonth == '10':
            returnMonth = 'October'
        elif someMonth == '11':
            returnMonth = 'November'
        elif someMonth == '12':
            returnMonth = 'December'
        else:
            raise Exception(someMonth)
        return returnMonth
    except Exception as e:
        print('The month did not parse correctly')
        exit(1)

# Modularizes our code via a main method
def main():
    # Fills in the date wanted, only generated once
    currentDate = datetime.date.today()
    reservationDate = currentDate + datetime.timedelta(days = settings.offsetDays)
    reservationYear = reservationDate.strftime("%Y") # Date in string form for easy comparison
    reservationMonth = toMonth(reservationDate.strftime('%m')) # Month in string form for easy comparison
    reservationDay = reservationDate.strftime("%d")

    # Builds a browser connection
    browser = webdriver.Firefox()
    print("Browser is now open")

    for i in range(0, len(settings.loginArray)):
        try:
            print('user number ' + str(i) + ' status: starting')
            browser.get(
                'https://login.library.nyu.edu/pds?func=load-login&institute=NYU&calling_system=https:login.library.nyu'
                '.edu&url=https%3A%2F%2Frooms.library.nyu.edu%2Fvalidate%3Freturn_url%3Dhttps%253A%252F%252Frooms.'
                'library.nyu.edu%252F%26https%3A%2F%2Flogin.library.nyu.edu_action%3Dnew%26https%3A%2F%2Flogin.'
                'library.nyu.edu_controller%3Duser_sessions')

            browser.find_element_by_xpath("//div[@id='shibboleth']/p[1]/a").click()

            # Fills in login information
            username = browser.find_element_by_xpath("//form[@id='login']/input[1]")
            password = browser.find_element_by_xpath("//form[@id='login']/input[2]")

            # Signs into bobst reserve with the username and password
            username.send_keys(settings.loginArray[i].username)
            password.send_keys(settings.loginArray[i].password)
            browser.find_element_by_xpath("//form[@id='login']/input[3]").click()

            if browser.current_url == "https://shibboleth.nyu.edu/idp/Authn/UserPassword":
                raise ValidationError.ValidationError("User had invalid login: " + str(i))

            ##### START OF FUCKING AROUND WITH THE DATEPICKER #####
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//form[@class='form-horizontal']"))
            )
            datePicker = browser.find_element_by_xpath(
                "//form[@class='form-horizontal']/div[@class='well well-sm']"
                "/div[@class='form-group has-feedback']/div[@class='col-sm-6']/input[1]"
            ).click()

            # Checks the month and year
            datePickerYear = browser.find_element_by_xpath(
                "//div[@id='ui-datepicker-div']/div[@class='ui-datepicker-group ui-datepicker-group-first']/"
                "div[@class='ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-left']/"
                "div[@class='ui-datepicker-title']/span[@class='ui-datepicker-year']"
            )
            datePickerYear = datePickerYear.text
            datePickerMonth = browser.find_element_by_xpath(
                "//div[@id='ui-datepicker-div']/div[@class='ui-datepicker-group ui-datepicker-group-first']/"
                "div[@class='ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-left']/"
                "div[@class='ui-datepicker-title']/span[@class='ui-datepicker-month']"
            )
            datePickerMonth = datePickerMonth.text

            # Alters year
            while (datePickerYear != reservationYear):
                # Right clicks the month until it is correct year
                browser.find_element_by_class_name("ui-icon-circle-triangle-e").click()

                # Updates the date picker year
                datePickerYear = browser.find_element_by_xpath(
                    "//div[@id='ui-datepicker-div']/div[@class='ui-datepicker-group ui-datepicker-group-first']/"
                    "div[@class='ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-left']/"
                    "div[@class='ui-datepicker-title']/span[@class='ui-datepicker-year']"
                )
                datePickerYear = datePickerYear.text

            # Alters month
            while datePickerMonth != reservationMonth:
                # Right clicks the month until it is correct month
                browser.find_element_by_class_name("ui-icon-circle-triangle-e").click()

                # Updates the date picker month
                datePickerMonth = browser.find_element_by_xpath(
                    "//div[@id='ui-datepicker-div']/div[@class='ui-datepicker-group ui-datepicker-group-first']/"
                    "div[@class='ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-left']/"
                    "div[@class='ui-datepicker-title']/span[@class='ui-datepicker-month']"
                )
                datePickerMonth = datePickerMonth.text

            # At this, point, we are on the correct year & month. Selects the date below
            browser.find_element_by_link_text(reservationDay).click()
            ##### END OF FUCKING AROUND WITH THE DATEPICKER #####

            # Finds the time
            timeStart = i*2
            startMorning = True

            if (timeStart >= 12) & (timeStart < 24):
                startMorning = False
                timeStart -= 12

            if timeStart == 0:
                timeStart = 12

            # Selects the start time
            select.Select(browser.find_element_by_css_selector("select#reservation_hour")
                          ).select_by_value(str(timeStart))

            select.Select(browser.find_element_by_css_selector("select#reservation_minute")
                          ).select_by_value("0")

            # Selects AM/PM
            if startMorning:
                select.Select(browser.find_element_by_css_selector("select#reservation_ampm")).select_by_value('am')
            else:
                select.Select(browser.find_element_by_css_selector("select#reservation_ampm")).select_by_value('pm')

            # Selects the time length
            select.Select(browser.find_element_by_css_selector("select#reservation_how_long")
                          ).select_by_value('120')

            # Clicks the button
            browser.find_element_by_css_selector("button#generate_grid").click()

            # Utilize a wait
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//form[@id='new_reservation']"))
            )

            # Fills in the description of the booking
            description = browser.find_element_by_id("reservation_title")
            description.send_keys(settings.description)

            # Fills in the duplicate email for the booking
            duplicateCC = browser.find_element_by_id("reservation_cc")
            duplicateCC.send_keys(settings.loginArray[i].emailDuplicate)

            # Selects the row
            roomText = "Bobst " + settings.floorNumber + "-" + settings.roomNumber
            divFind = browser.find_element_by_xpath('//div[contains(text(), "' + roomText + '")]')

            # We have the row now, we click the appropriate place
            divFind.find_element_by_xpath(
                "../../td[@class='timeslot timeslot_available timeslot_preferred timeslot_preferred_first']").click()

            # Submits
            browser.find_element_by_xpath("//button[@class='btn btn-lg btn-primary']").click()

            print('user number ' + str(i) + ' status: done')

            # Logout
            browser.get('https://rooms.library.nyu.edu/logout')

        except GeneratorExit:
            return
        except ValidationError as ex:
            print(ex)
        except WebDriverException as ex1:
            print("Failed on user number: " + str(i))
            print(ex1)
        except Exception as ex2:
            print(ex2)

    # Close browser connection
    browser.close()
    return

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()
