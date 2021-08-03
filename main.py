"""
File: main.py
--------------------
This is a web automation tool to check if there are reservations available for any resort on the ikon pass
website, and alerts the user if reservations are available on the selected dates.
"""

#### Additions to make #####
# Add dynamic resort option
# Add dynamic date options
# Figure out how to share this as an .exe file
#############################

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class Concierge:

    def __init__(self):
        """
        Constructs the Ikon Concierge class

        """
        self.path = "C:\Program Files (x86)\Google\Chrome\chromedriver.exe"
        self.website = "https://account.ikonpass.com/en/login"
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.website)
        self.driver.implicitly_wait(10)
        time.sleep(1)

    def quit_driver(self):
        """ Closes the driver """
        self.driver.quit()


    def accept_cookies(self):
        """ This function accepts the cookies in the Ikon pass website """

        # For some reason we need to click on the button twice, waiting one second in between
        cookies = self.driver.find_element_by_class_name("cc-compliance")

        # Setting up action chains
        actions = ActionChains(self.driver)
        actions.click(cookies)
        actions.pause(1)
        actions.click(cookies)
        actions.perform()

        return

    def login(self, username, password):
        """ This function inputs user's credentials to log into the Ikon pass website

        username: Ikon pass email
        password: Ikon pass password
        """
        # Filling in username and password fields
        time.sleep(2)
        username_field = self.driver.find_element_by_id("email")
        username_field.send_keys(username)
        password_field = self.driver.find_element_by_id("sign-in-password")
        password_field.send_keys(password)

        # Logging in
        log_in = self.driver.find_element_by_css_selector(".primary")
        log_in.click()

        time.sleep(2)

        return

    def go_to_resort(self, resort):
        """ This functions goes from the landing page after logging in to the reservation page for the desired resort

        resort: Desired resort to check ## CURRENTLY ONLY WORKS FOR JACKSON HOLE ##
        """
        time.sleep(5)
        # Accessing the "Make a Reservation" page
        reservation_ele = self.driver.find_element_by_css_selector(".coqxua")
        reservation_ele.click()

        # If people have favorites, then this will be section-1 instead of section-0
        # This is poorly coded, we would need to look for the Jackson Hole tag and then go up to the parents
        resort = self.driver.find_element_by_id("react-autowhatever-resort-picker-section-0-item-3")
        resort.click()

        continue_button = self.driver.find_element_by_css_selector("#root > div > div > main > section.sc-pBolk.bLdbNO > div > div.amp-card.sc-qYFre.hyLEUz > div.sc-pBwqG.hsfcA-d > div.sc-pIuOK.kfwIKW > button")
        continue_button.click()

        time.sleep(1)

        return

    def obtain_dates(self):
        """ This function obtains the HTML for current month and uses the parse_dates function to obtain
        a dictionary with date availability

        returns: Dictionary with date availability
        """
        time.sleep(1)

        # Going to next month
        # next_month = self.driver.find_element_by_css_selector("#root > div > div > main > section.sc-pBolk.bLdbNO > div > div.amp-card.sc-pRrxg.OYQvJ > div.sc-pZOOJ.iFmuIW > div.sc-pZpxQ.kynict > div:nth-child(1) > div.DayPicker.sc-pIVsU.fBycfn > div > div.sc-pcHDm.cSajLG > div.sc-ptCms.fzKffT > button:nth-child(3) > span > span > i")
        # next_month.click()

        # Checking availability of dates
        time.sleep(1)
        dates_source = self.driver.page_source

        # Parsing dates
        dates = self.parse_dates(dates_source)

        return dates

    def parse_dates(self, source_code):
        """ Parses monthly source code to determine which dates are unavailable, available, or already reserved
        by the user. Uses BeautifulSoup to parse through the HTML.

        Args:
            source_code: HTML source code for current month

        Returns:
            Dictionary with each date and corresponding availability
        """
        soup = BeautifulSoup(source_code, "html.parser")
        tags = soup.find("div", "DayPicker-Body")

        # Creating dictionary in which we'll store availability
        master_dates = dict()

        # Going week by week

        # Looking at the direct contents of the HTML
        for week in tags.contents:
            # Going into the children of each week (parses out each day)
            for child in week.children:
                # Including only days that are active for the month
                if child['aria-disabled'] == "false":

                    # Obtaining day and list with all classes
                    day = child['aria-label']
                    class_list = child['class']

                    # Checking classes to see if day is available, unavailable or already reserved
                    if 'DayPicker-Day--unavailable' in class_list:
                        master_dates[day] = 'unavailable'
                    elif 'DayPicker-Day--confirmed' in class_list:
                        master_dates[day] = 'confirmed'
                    else:
                        master_dates[day] = 'available'

        return master_dates

    def select_date(self, dates, day):
        """ Given a specific day, verifies if the day is available. If it is, the day is confirmed. If it is not,
        the user receives a message stating the date availability.

        Args:
            dates_dict (dict): dictionary with date availability
            day (str): date to check, must be formatted as "Mon MMM DD YYYY"

        Returns:
            availability: 'available', 'unavailable', 'already reserved' message
        """
        # Building CSS selector
        selector = f'[aria-label="{day}"]'

        # Checking if requested day is available
        if dates[day] == 'available':
            select_day = self.driver.find_element_by_css_selector(selector)
            select_day.click()

            save_button = self.driver.find_element_by_css_selector("#root > div > div > main > section.sc-fzqyOu.ijDjOa > div > div.amp-card.sc-prRJy.gqNvjh > div.sc-qQjAt.kHbQih > div.sc-pByoR.YJVtY > div:nth-child(2) > div > div.sc-pCOsa.eakatQ > button.sc-AxjAm.jxPclZ.sc-pAArZ.lkoEyq")
            save_button.click()

        return dates[day]

    def confirm_reservation(self):
        """
        Once dates have been selected in the reservation page, this function confirms these reservations
        """
        # Click on the "Review my reservations button"
        time.sleep(2)
        review_reservations = self.driver.find_element_by_css_selector("#root > div > div > main > section.sc-fzqyOu.ijDjOa > div > div.amp-card.sc-prRJy.gqNvjh > div.sc-qQjAt.kHbQih > div.sc-qWPci.fYvXyK > button")
        review_reservations.click()

        time.sleep(2)

        # Confirm that I have read terms and conditions
        conditions = self.driver.find_element_by_css_selector("#root > div > div > main > section.sc-fzqyOu.ijDjOa > div > div.amp-card.sc-prRJy.gqNvjh > div.sc-qQjAt.kHbQih > div > div.sc-pAMbm.bWxMRp > label > input")
        conditions.click()
        time.sleep(1)

        # Confirm reservations
        confirm = self.driver.find_element_by_css_selector("#root > div > div > main > section.sc-fzqyOu.ijDjOa > div > div.amp-card.sc-prRJy.gqNvjh > div.sc-qQjAt.kHbQih > div > div.sc-qQkIG.edTdYL > button")
        confirm.click()

        time.sleep(5)

        return


    def explicit_wait(self, selector, method, wait):
        """ Waits for the condition to be met in order to execute the command. If the selector is not found,
        close the program.

        Args:
            Selector: Selector used to find HTML element
            Method: Method to select the HTML tag (ID, class, css_selector, etc.)
            Wait: Time to wait until element is found before shutting the program down

        Return:
            Element: Selenium element
        """
        try:
            element = WebDriverWait(self.driver, wait).until(
                EC.presence_of_element_located((By.eval(method), selector))
            )
        except:
            self.quit_driver()

        return element


def main(days, resort, username, password):

    # Initialize class and use methods to navigate to desired dates
    concierge = Concierge()
    concierge.accept_cookies()
    concierge.login(username, password)
    concierge.go_to_resort(resort)
    dates = concierge.obtain_dates()

    # Create a set to save if any date is available
    selection_result = set()

    # Check if dates are available. If they are, select them
    for day in days:
        day_is_available = concierge.select_date(dates, day)
        selection_result.add(day_is_available)
        print(day, day_is_available)

    # If dates are available, confirm the reservation.
    # Else, if all dates are confirmed, then send message that the program is complete and stop it from running
    # Else, close the driver and keep trying
    if 'available' in selection_result:
        concierge.confirm_reservation()
        result = 'Incomplete'
    elif len(selection_result)==1 and 'confirmed' in selection_result:
        print("Program is complete")
        result = 'Complete'
    else:
        print("Dates are unavailable")
        result = 'Incomplete'

    time.sleep(1)

    concierge.quit_driver()

    return result

if __name__ == '__main__':
    main()