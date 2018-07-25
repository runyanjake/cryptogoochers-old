# https://github.com/runyanjake/cryptogoochers/headlesschrometesting/headlesschrome.py
# @Author Jake Runyan
# Testing of headless chrome to scrape cryptocoin data and store it in a database, generating a nice graph as output.
# Running this script performs one complete scrape of relevant data (enough to fully populate a database row), generates a graph and exits.
# It is designed to be called on a timetable for continuous data acquisition.
#

import os 
import re
import sqlite3
import time
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys

PATH_TO_CHROMEDRIVER = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)  # Chrome driver, using the chromedriver file in PATH_TO_CHROMEDRIVER, if not specified will search path.

BTC_WEB_SOURCES = ['https://www.coindesk.com/price/',
                        'https://cointelegraph.com/bitcoin-price-index']
BTC_PRICE_XPATHS = ["//span[@class='data']",
                        "//div[@class='value text-nowrap']"]
BTC_PRICES = []

assert(len(BTC_WEB_SOURCES) == len(BTC_PRICE_XPATHS)) #the 2 correspond for links and scraping commands

#Scraping Prices
for itor in range(0, len(BTC_WEB_SOURCES)):
    succeeded_scraping = False
    num_reattempts = 10
    while not succeeded_scraping:
        print("Scraping " + str(BTC_WEB_SOURCES[itor]) + "...")
        driver.get(BTC_WEB_SOURCES[itor])
        btc_value_element = driver.find_element_by_xpath(BTC_PRICE_XPATHS[itor])
        btc_value_str = btc_value_element.text
        if btc_value_str == "":
            print("Failed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
            num_reattempts = num_reattempts-1
            if num_reattempts > 0:
                succeeded_scraping = False
            else:
                print("Failed to parse a string from the webpage. Continuing...")
                btc_value = -1.0 #error value, most likely never used
                succeeded_scraping = True #loop control, dont mean anything
        else:
            btc_value = float(re.search("[0-9,]+\.[0-9]+", btc_value_str).group(0).replace(",", ""))
            BTC_PRICES.append(btc_value)
            print("Found BTC price " + str(btc_value))
            succeeded_scraping = True
            print("Done.")

#Storing Prices
if len(BTC_PRICES) > 0

driver.quit()