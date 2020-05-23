"""
Google Flight Scraper

Author: Lingchen Zhu
"""

import os
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
    df = pd.DataFrame()
    itinerary = browser.find_elements_by_xpath("//div[contains(@class, 'gws-flights-results__itinerary-card-summary')]")
    for i, itin in enumerate(itinerary):
        itin_info = itin.text.split('\n')
        if len(itin_info) == 7:  # no extra carrier exists, insert a blank
            itin_info.insert(2, '')
        df.loc[i, 'depart time'] = itin_info[0].split('–')[0].strip()
        df.loc[i, 'arrival time'] = itin_info[0].split('–')[1].strip()
        df.loc[i, 'carrier'] = itin_info[1]
        df.loc[i, 'extra carrier'] = itin_info[2]
        df.loc[i, 'duration'] = itin_info[3]
        df.loc[i, 'airports (from-to)'] = itin_info[4]
        df.loc[i, 'stops'] = itin_info[5]
        df.loc[i, 'layover'] = itin_info[6]
        df.loc[i, 'price'] = itin_info[7]
    save_filename_ext = os.path.splitext(save_filename)[1][1:]
    if save_filename_ext in ['xls', 'xlsx']:
        df.to_excel(save_filename)
    elif save_filename_ext == 'csv':
        df.to_csv(save_filename)
    else:
        raise NotImplementedError



if __name__ == '__main__':
    # use ChromeDriver
    driver = os.path.normpath('./chromedriver.exe')
    browser = webdriver.Chrome(executable_path=driver)

    # jump to the google flight website
    link = 'https://www.google.com/flights'
    browser.get(link)

    # search flights with the given inputs
    is_roundtrip = False
    if not is_roundtrip:
        ticket_chooser('One way')
    depart_airport_chooser('NYC')
    arrival_airport_chooser('SHA')
    if is_roundtrip:
        depart_date = '2020-10-01'
        return_date = '2020-12-01'
        date_chooser(depart_date=depart_date, return_date=return_date)
    else:
        depart_date = '2020-10-01'
        date_chooser(depart_date=depart_date)
    search()

    # compile and save results
    save_filename = os.path.normpath('./result.xls')
    compile(save_filename)

    # quit the browser
    browser.quit()

