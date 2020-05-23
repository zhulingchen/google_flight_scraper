"""
Google Flight Scraper

Author: Lingchen Zhu
"""

import os
import re
import argparse
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart



def ticket_chooser(type):
    try:
        ticket_type_menu = browser.find_element_by_xpath("//span[@class='gws-flights-form__menu-button-icon']")
        ticket_type_menu.click()
        ticket_type = browser.find_element_by_xpath("//span[text()='{:s}']".format(type))
        ticket_type.click()
        time.sleep(1)
    except Exception as e:
        pass


def depart_airport_chooser(depart_airport_name):
    depart_airport = browser.find_element_by_xpath("//div[@class='flt-input gws-flights-form__input-container gws-flights__flex-box gws-flights-form__airport-input gws-flights-form__swapper-right']")
    depart_airport.click()
    time.sleep(1)
    depart_airport = browser.find_element_by_xpath("//input[@placeholder='Where from?']")
    depart_airport.clear()
    depart_airport.send_keys(depart_airport_name)
    time.sleep(1)
    first_item = browser.find_element_by_xpath("//span[@class='fsapp-option-city-name']")
    first_item.click()


def arrival_airport_chooser(arrival_airport_name):
    arrival_airport = browser.find_element_by_xpath("//div[@class='flt-input gws-flights-form__input-container gws-flights__flex-box gws-flights-form__airport-input gws-flights-form__empty gws-flights-form__swapper-left']")
    arrival_airport.click()
    time.sleep(1)
    arrival_airport = browser.find_element_by_xpath("//input[@placeholder='Where to?']")
    arrival_airport.clear()
    time.sleep(1)
    arrival_airport.send_keys(arrival_airport_name)
    time.sleep(1)
    first_item = browser.find_element_by_xpath("//span[@class='fsapp-option-city-name']")
    first_item.click()


def date_chooser(depart_date, return_date=None):
    depart_date = datetime.strptime(depart_date, '%Y-%m-%d')
    date = browser.find_element_by_xpath("//div[@class='gws-flights__flex-filler gws-flights__ellipsize gws-flights-form__input-target']")
    date.click()
    time.sleep(1)
    date = browser.find_element_by_xpath("//input[@placeholder='Departure date']")
    date.send_keys(Keys.CONTROL + 'a')
    date.send_keys(Keys.DELETE)
    time.sleep(1)
    date.send_keys('{:d}/{:d}/{:d}'.format(depart_date.month, depart_date.day, depart_date.year))
    date.send_keys(Keys.ENTER)
    time.sleep(1)
    if return_date:
        return_date = datetime.strptime(return_date, '%Y-%m-%d')
        date = browser.find_element_by_xpath("//input[@placeholder='Return date']")
        date.send_keys(Keys.CONTROL + 'a')
        date.send_keys(Keys.DELETE)
        time.sleep(1)
        date.send_keys('{:d}/{:d}/{:d}'.format(return_date.month, return_date.day, return_date.year))
        date.send_keys(Keys.ENTER)
        time.sleep(1)
    date = browser.find_element_by_xpath("//g-raised-button[@data-flt-ve='done']")
    date.click()
    time.sleep(5)


def search():
    more_results = browser.find_element_by_xpath("//a[@class='gws-flights-results__dominated-link']")
    more_results.click()
    time.sleep(15)


def compile(save_filename=None):
    itinerary = browser.find_elements_by_xpath("//div[contains(@class, 'gws-flights-results__itinerary-card-summary')]")
    # collect itinerary data
    data = [[None] * 10 for _ in range(len(itinerary))]
    for i, itin in enumerate(itinerary):
        itin_info = itin.text.split('\n')
        data[i][0] = itin_info[0].split('–')[0].strip()
        data[i][1] = itin_info[0].split('–')[1].strip()
        if re.compile('[0-9]+h [0-9]+m').match(itin_info[2]):  # no extra carrier exists, insert a blank
            itin_info.insert(2, '')
        for j, itin_item in enumerate(itin_info[1:]):
            data[i][j+2] = itin_item
    # create a data frame
    columns = ['depart time', 'arrival time', 'carrier', 'extra carrier', 'duration', 'airports (from-to)', 'stops', 'layover', 'price', 'round trip']
    df = pd.DataFrame(data, columns=columns)
    # save the data frame
    save_filename_ext = os.path.splitext(save_filename)[1][1:]
    if save_filename_ext in ['xls', 'xlsx']:
        df.to_excel(save_filename, index=False)
    elif save_filename_ext == 'csv':
        df.to_csv(save_filename, index=False)
    else:
        raise NotImplementedError



if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('airports', metavar='airports', type=str.upper, nargs=2, help='depart and arrival airports')
    parser.add_argument('dates', metavar='dates', type=str, nargs='+', help='depart and return dates')
    parser.add_argument('-l', '--checklist', type=str.lower, help="where the job will run")
    args = parser.parse_args()
    depart_airport, arrival_airport = args.airports
    is_roundtrip = True if len(args.dates) > 1 else False
    depart_date = args.dates[0]
    return_date = args.dates[1] if len(args.dates) > 1 else None

    # use ChromeDriver
    driver = os.path.normpath('./chromedriver.exe')
    browser = webdriver.Chrome(executable_path=driver)

    # jump to the google flight website
    link = 'https://www.google.com/flights'
    browser.get(link)

    # search flights with the given inputs
    if not is_roundtrip:
        ticket_chooser('One way')
    depart_airport_chooser(depart_airport)
    arrival_airport_chooser(arrival_airport)
    date_chooser(depart_date=depart_date, return_date=return_date)
    search()

    # compile and save results
    save_filename = './result_{:s}-{:s}_{:s}'.format(depart_airport, arrival_airport, depart_date)
    if is_roundtrip:
        save_filename += '-{:s}'.format(return_date)
    save_filename += '_created_on_{:d}-{:d}-{:d}_{:d}h{:d}m{:d}s'.format(datetime.now().year, datetime.now().month, datetime.now().day,
                                                                         datetime.now().hour, datetime.now().minute, datetime.now().second)
    save_filename += '.xls'
    save_filename = os.path.normpath(save_filename)
    compile(save_filename)
    print('Google Flight search results are saved as {:s}'.format(save_filename))

    # quit the browser
    browser.quit()

