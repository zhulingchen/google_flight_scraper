import os
import time
import datetime
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
    depart_month, depart_day, depart_year = depart_date
    date = browser.find_element_by_xpath("//div[@class='gws-flights__flex-filler gws-flights__ellipsize gws-flights-form__input-target']")
    date.click()
    time.sleep(1)
    date = browser.find_element_by_xpath("//input[@placeholder='Departure date']")
    date.send_keys(Keys.CONTROL + 'a')
    date.send_keys(Keys.DELETE)
    time.sleep(1)
    date.send_keys('{:d}/{:d}/{:d}'.format(depart_month, depart_day, depart_year))
    date.send_keys(Keys.ENTER)
    time.sleep(1)
    if return_date:
        return_month, return_day, return_year = return_date
        date = browser.find_element_by_xpath("//input[@placeholder='Return date']")
        date.send_keys(Keys.CONTROL + 'a')
        date.send_keys(Keys.DELETE)
        time.sleep(1)
        date.send_keys('{:d}/{:d}/{:d}'.format(return_month, return_day, return_year))
        date.send_keys(Keys.ENTER)
        time.sleep(1)
    date = browser.find_element_by_xpath("//g-raised-button[@data-flt-ve='done']")
    date.click()


def search():
    more_results = browser.find_element_by_xpath("//a[@class='gws-flights-results__dominated-link']")
    more_results.click()
    time.sleep(10)


def compile():
    pass



if __name__ == '__main__':
    driver = os.path.normpath('./chromedriver.exe')
    browser = webdriver.Chrome(executable_path=driver)

    link = 'https://www.google.com/flights'
    browser.get(link)

    is_roundtrip = False
    if not is_roundtrip:
        ticket_chooser('One way')
    depart_airport_chooser('NYC')
    arrival_airport_chooser('SHA')
    if is_roundtrip:
        date_chooser(depart_date=(10, 1, 2020), return_date=(12, 1, 2020))
    else:
        date_chooser(depart_date=(10, 1, 2020))
    search()
    compile()

