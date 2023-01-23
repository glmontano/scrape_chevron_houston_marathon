from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime as dt
import csv
import time

######################## User Parameters ########################

YEAR = 2023

# Update to the location of your chrome driver
CHROME_DRIVER_PATH = r'C:\Users\gloui\Desktop\chromedriver\chromedriver_109.exe'

#################################################################

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

URL = f'https://track.rtrt.me/e/HOU-{YEAR}'
CSV_FILE_NAME = f'houston_marathon_{YEAR}.csv'

XPATH_ALL_FINISHERS_LIST = '//tr[@data-course="marathon"]'
XPATH_IFRAME = '//iframe[@name="rtframe"]'
XPATH_CONTESTANT_NUMBER = '//span[@class="x_res_count"]'
XPATH_ATHLETE_PLACE = '//div[@class="eventfontColors s-corner-all f_bld place_num"]'
XPATH_ATHLETE_NAME = '//span[@class="only_on_big uline loadleaderlink"]'
XPATH_ATHLETE_TIME = '//td[@class="lbtime nowrap "]'
XPATH_ATHLETE_GENDER = '//td[@class="eventfontColors lbname"]'
XPATH_PARTICIPATION_BUTTON = '//button[@class="btn btn-primary participantbtn"]'
XPATH_TOP_FINISHERS_BUTTON = '//div[@data-page="leaderboard"]'
XPATH_NEXT_PAGE_BUTTON = '//i[@class="x_prevnext icon-right cpoint"]'


def scrape_chevron_houston_marathon_data():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False
    chrome_options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
        driver.get(URL)

        # The trick is that everything is in an iframe! Go into the iframe and continue
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, XPATH_IFRAME)))
        iframe = driver.find_elements(By.XPATH, XPATH_IFRAME)
        driver.switch_to.frame(iframe[0])

        # Click participation button
        participation_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, XPATH_PARTICIPATION_BUTTON)))
        participation_button.click()

        # Click on Top Finishers
        top_finishers_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, XPATH_TOP_FINISHERS_BUTTON)))
        top_finishers_button.click()

        # Get Total Contestants
        page_contestant_numbers = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, XPATH_CONTESTANT_NUMBER)))
        total_contestants = int(page_contestant_numbers.text.split(' ')[-1].replace(',', ''))
        page_start_place = int(page_contestant_numbers.text.split(' ')[0].split('-')[0])
        page_end_place = int(page_contestant_numbers.text.split(' ')[0].split('-')[-1])

        # Begin to go through contestants; write data to CSV file
        with open(CSV_FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['place', 'name', 'time', 'gender'])

            # Loop through all pages!
            while page_end_place <= total_contestants:

                # Grab all results
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, XPATH_ALL_FINISHERS_LIST)))

                athlete_names = driver.find_elements(By.XPATH, XPATH_ATHLETE_NAME)
                athlete_places = driver.find_elements(By.XPATH, XPATH_ATHLETE_PLACE)
                athlete_times = driver.find_elements(By.XPATH, XPATH_ATHLETE_TIME)
                athlete_genders = driver.find_elements(By.XPATH, XPATH_ATHLETE_GENDER)

                # Capture the results into a CSV file!
                if athlete_names:
                    for j in range(0, len(athlete_names)):
                        try:
                            athlete_name = athlete_names[j].text
                        except (IndexError, ValueError):
                            athlete_name = 'N/A'
                        # print('Name:', athlete_name)
                        try:
                            athlete_place = athlete_places[j].text
                        except (IndexError, ValueError):
                            athlete_place = 'N/A'
                        # print('Place:', athlete_place)
                        try:
                            athlete_time = athlete_times[j].text
                        except (IndexError, ValueError):
                            athlete_time = 'N/A'
                        # print('Time:', athlete_time)
                        try:
                            athlete_gender = athlete_genders[j].text.split('\n')[-1].split(' ')[1].split('-')[0]
                        except (IndexError, ValueError):
                            athlete_gender = 'N/A'
                        # print('Gender:', athlete_gender)
                        # print('=============')
                        writer.writerow([athlete_place, athlete_name, athlete_time, athlete_gender])

                # Go to next page
                button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, XPATH_NEXT_PAGE_BUTTON)))
                button.click()
                
                # Get new page contestant numbers, and only continue if the new page's start is 10 more than the previous end
                while page_start_place != page_end_place + 1:
                    time.sleep(1) 
                    page_contestant_numbers = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, XPATH_CONTESTANT_NUMBER)))
                    page_start_place = int(page_contestant_numbers.text.split(' ')[0].split('-')[0])

                page_end_place = int(page_contestant_numbers.text.split(' ')[0].split('-')[-1])

    except Exception as e:
        print(e)
        print('Error')

    driver.close()

scrape_chevron_houston_marathon_data()
