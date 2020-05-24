"""
Google Flight Scraper

My own scraper for Google Flights search and result compilation written in Python.
It is designed for my personal and convenient use only, not for any commercial purposes.

Author: Lingchen Zhu (zhulingchen@gmail.com)
Copyright (c) 2020

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software with the rights of use, copy,
modify, and distribute, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. no commercial use

2. must keep the author's name (Lingchen Zhu) in the copyright notice

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import re
import argparse
import time
import numpy as np
import pandas as pd
from collections import namedtuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.mime.multipart import MIMEMultipart



def ticket_chooser(type):
    ticket_type_menu = browser.find_element_by_xpath("//span[@class='gws-flights-form__menu-button-icon']")
    ticket_type_menu.click()
    ticket_type = browser.find_element_by_xpath("//span[text()='{:s}']".format(type))
    ticket_type.click()
    time.sleep(1)


def depart_airport_chooser(depart_airport_name):
    depart_airport = browser.find_element_by_xpath("//div[@class='flt-input gws-flights-form__input-container gws-flights__flex-box gws-flights-form__airport-input gws-flights-form__swapper-right']")
    depart_airport.click()
    time.sleep(1)
    depart_airport = browser.find_element_by_xpath("//input[@placeholder='Where from?']")
    depart_airport.clear()
    time.sleep(1)
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


def search_more():
    more_results = browser.find_element_by_xpath("//a[@class='gws-flights-results__dominated-link']")
    more_results.click()
    time.sleep(15)


def compile(flight_number=False, carriers=None):
    itinerary = browser.find_elements_by_xpath("//li[contains(@class, 'gws-flights-results__result-item')]")
    # collect itinerary data
    colnames = ['depart time', 'arrival time', 'carrier', 'extra carrier', 'duration', 'airports (from-to)', 'stops', 'layover', 'price', 'round trip']
    if flight_number:
        colnames += ['flight number']
    data = []
    for itin in itinerary:
        itin_info = itin.text.split('\n')
        if re.compile('[0-9]+h [0-9]+m').match(itin_info[2]):  # no extra carrier exists, insert a blank
            itin_info.insert(2, '')
        if carriers and all(c not in itin_info[1].lower() for c in carriers) and all(c not in itin_info[2].lower() for c in carriers):
            continue
        data.append([None] * len(colnames))
        data[-1][0] = itin_info[0].split('–')[0].strip()
        data[-1][1] = itin_info[0].split('–')[1].strip()
        for j, itin_item in enumerate(itin_info[1:]):
            data[-1][j+2] = itin_item
        if flight_number:
            # expand details
            # browser.execute_script("arguments[0].scrollIntoView(false);", itin)
            # actions.move_to_element(itin).perform()  # move to the element otherwise click() will throw Exception: element click intercepted
            expand = itin.find_element_by_xpath(".//div[@aria-label='Show details']")
            actions.move_to_element(expand).perform()  # move to the element otherwise click() will throw Exception: element click intercepted
            expand.click()
            time.sleep(1)
            itin_detail = itin.find_element_by_xpath(".//div[@class='gws-flights-widgets-expandablecard__body']")
            flight_number_info = itin_detail.find_elements_by_xpath(".//div[@class='gws-flights-results__other-leg-info gws-flights__flex-box gws-flights__align-center']")
            flight_number_info = ','.join(n.text.split('\n')[-1] for n in flight_number_info)
            data[-1][-1] = flight_number_info
            # hide details
            # browser.execute_script("arguments[0].scrollIntoView(false);", itin)
            # actions.move_to_element(itin).perform()  # move to the element otherwise click() will throw Exception: element click intercepted
            hide = itin.find_element_by_xpath(".//div[@aria-label='Hide details']")
            actions.move_to_element(hide).perform()  # move to the element otherwise click() will throw Exception: element click intercepted
            hide.click()
            time.sleep(1)
            # hide the current itinerary to save time for scrolling
            # browser.execute_script("arguments[0].style.visibility='hidden';", itin)
    # create a data frame and return
    return pd.DataFrame(data, columns=colnames)



if __name__ == '__main__':
    # print copyright
    print('====================================================================================================')
    print("Welcome to use the scraper for Google Flights search and result compilation.\n")
    print("Author: Lingchen Zhu (zhulingchen@gmail.com)")
    print("Copyright (c) 2020\n")
    print('THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
    print('====================================================================================================')

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--airports', metavar='AIRPORT', type=str.upper, nargs=2, help='depart and arrival airports')
    parser.add_argument('-d', '--dates', metavar='YYYY-MM-DD', type=str, nargs='+', help='depart and return dates (one date for one way or two dates for round-trip)')
    parser.add_argument('-l', '--checklist', metavar='FILE', type=str.lower, help='checklist file (a .csv or an Excel file) including many airports and dates')
    parser.add_argument('-n', '--flight-number', action='store_true', help="get the flight number")
    parser.add_argument('-c', '--carriers', metavar='CARRIER', type=str.lower, nargs='*', help="filter specific carriers")
    args = parser.parse_args()
    colnames = ['depart_airport', 'arrival_airport', 'depart_date', 'return_date']
    dialog = namedtuple("Dialog", field_names=colnames)

    if args.checklist:
        checklist_filename = os.path.normpath(args.checklist)
        checklist_filename_ext = os.path.splitext(checklist_filename)[1][1:]
        if checklist_filename_ext == 'csv':
            checklist = pd.read_csv(checklist_filename, names=colnames, header=None)
            checklist['return_date'] = [None if pd.isnull(d) else d for d in checklist['return_date']]
        elif checklist_filename_ext in ['xls', 'xlsx']:
            checklist = pd.read_excel(checklist_filename, names=colnames, header=None)
            checklist['depart_date'] = [str(d.date()) for d in checklist['depart_date']]
            checklist['return_date'] = [None if pd.isnull(d) else str(d.date()) for d in checklist['return_date']]
        else:
            raise NotImplementedError
        checklist = checklist.values
        inputlist = []
        for item in checklist:
            inputlist.append(dialog(**{k: v for k, v in zip(colnames, item)}))
    elif args.airports:
        if args.dates:
            inputlist = [dialog(args.airports[0], args.airports[1], args.dates[0], args.dates[1] if len(args.dates) > 1 else None)]
        else:  # use today's date if no -d/--dates arguments is given
            inputlist = [dialog(args.airports[0], args.airports[1], str(datetime.now().date()), None)]
    else:
        raise ValueError('Either explicit airports and date(s) or a checklist of airports and date(s) must be given.')

    # use ChromeDriver
    driver = os.path.normpath('./chromedriver.exe')
    browser = webdriver.Chrome(executable_path=driver)
    actions = ActionChains(browser)

    # search and compile results
    for item in inputlist:
        # print search dialog information
        info = 'Searching and compiling flights from {:s} to {:s}, leaving on {:s}'.format(item.depart_airport, item.arrival_airport, item.depart_date)
        if item.return_date:
            info += ', returning on {:s}'.format(item.return_date)
        print(info)

        try:
            # jump to the google flight website
            link = 'https://www.google.com/flights'
            browser.get(link)

            # search flights with the given inputs
            if not item.return_date:
                ticket_chooser('One way')
            depart_airport_chooser(item.depart_airport)
            arrival_airport_chooser(item.arrival_airport)
            date_chooser(depart_date=item.depart_date, return_date=item.return_date)
            search_more()  # click "XXX more flights"
            df = compile(flight_number=args.flight_number, carriers=args.carriers)  # compile results as a pandas DataFrame
        except Exception as e:
            print('Search failed')
            continue

        # prepare the save filename
        save_filename = './result_{:s}-{:s}_{:s}'.format(item.depart_airport, item.arrival_airport, item.depart_date)
        if item.return_date:
            save_filename += '-{:s}'.format(item.return_date)
        save_filename += '_created_on_{:d}-{:d}-{:d}_{:d}h{:d}m{:d}s'.format(datetime.now().year, datetime.now().month, datetime.now().day,
                                                                             datetime.now().hour, datetime.now().minute, datetime.now().second)
        save_filename += '.xls'
        save_filename = os.path.normpath(save_filename)

        # save the pandas DataFrame as an Excel file
        save_filename_ext = os.path.splitext(save_filename)[1][1:]
        if save_filename_ext in ['xls', 'xlsx']:
            df.to_excel(save_filename, index=False)
        elif save_filename_ext == 'csv':
            df.to_csv(save_filename, index=False)
        else:
            raise NotImplementedError

        print('Google Flight search results are saved as {:s}'.format(save_filename))

    # quit the browser
    browser.quit()