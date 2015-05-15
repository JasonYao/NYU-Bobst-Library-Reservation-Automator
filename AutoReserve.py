__author__ = 'Jason Yao'

# Majour imports
import datetime
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.support import select

# Package dependent imports
import settings
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

    # Builds a browser connection
    browser = webdriver.Firefox()
    print("Browser is now open")

    for i in range(0, len(settings.loginArray)):
        try:
            print('Attempting to register with user number: ' + str(i))
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


            #browser.close()
            print("Got to test point, exiting now")
            exit(0)

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
