# https://github.com/runyanjake/cryptogoochers/headlesschrometesting/headlesschrome.py
# @Author Jake Runyan
# Testing of headless chrome to scrape cryptocoin data and store it in a database, generating a nice graph as output.
# Running this script performs one complete scrape of relevant data (enough to fully populate a database row), generates a graph and exits.
# It is designed to be called on a timetable for continuous data acquisition.
#

import datetime
import os 
import re
import sqlite3
import time
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys

PATH_TO_CHROMEDRIVER = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)  # Chrome driver, using the chromedriver file in PATH_TO_CHROMEDRIVER, if not specified will search path.

class SiteAndXPath:
    site = ""
    xpath = ""
    def __init__(self, spsite, spxpath):
        self.site = spsite
        self.xpath = spxpath


# BTC_WEB_SOURCES = ['https://www.coindesk.com/price/',
#                         'https://cointelegraph.com/bitcoin-price-index']
# BTC_PRICE_XPATHS = ["//span[@class='data']",
#                         "//div[@class='value text-nowrap']"]
# assert(len(BTC_WEB_SOURCES) == len(BTC_PRICE_XPATHS)) #the 2 correspond for links and scraping commands

BTC_SOURCES = [SiteAndXPath("https://www.coindesk.com/price/", "//span[@class='data']"),
                SiteAndXPath("https://cointelegraph.com/bitcoin-price-index", "//div[@class='value text-nowrap']")]
BTC_PRICES = []


#Scraping Prices
for itor in range(0, len(BTC_SOURCES)):
    succeeded_scraping = False
    num_reattempts = 10
    while not succeeded_scraping:
        print("Scraping " + str(BTC_SOURCES[itor].site) + "...")
        driver.get(BTC_SOURCES[itor].site)
        btc_value_element = driver.find_element_by_xpath(BTC_SOURCES[itor].xpath)
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
btc_prices_copy = BTC_PRICES
now = datetime.datetime.utcnow()
medianprice = 0.0
hiprice = 0.0
hiprice_site = ""
loprice = 0.0
loprice_site = ""
if len(BTC_PRICES) > 0:
        #find high price and source
        valuehighest = btc_prices_copy[0] 
        indexhighest = 0
        index = 0
        for price in btc_prices_copy:
            if price > valuehighest:
                valuehighest = price
                indexhighest = index
            index = index + 1
        hiprice = btc_prices_copy[indexhighest]
        hiprice_site = BTC_SOURCES[indexhighest].site
        #find low price and source
        valuelowest = btc_prices_copy[0] 
        indexlowest = 0
        index = 0
        for price in btc_prices_copy:
            if price < valuelowest:
                valuelowest = price
                indexlowest = index
            index = index + 1
        loprice = btc_prices_copy[indexlowest]
        loprice_site = BTC_SOURCES[indexlowest].site
        #find median
        while len(btc_prices_copy) > 2: 
            valuelowest = btc_prices_copy[0]
            indexlowest = 0
            index = 0
            for price in btc_prices_copy:
                if price < valuelowest:
                    valuelowest = price
                    indexlowest = index
                index = index + 1
            del btc_prices_copy[indexlowest] #delete lowest price 
            valuehighest = btc_prices_copy[0] 
            indexhighest = 0
            index = 0
            for price in btc_prices_copy:
                if price > valuehighest:
                    valuehighest = price
                    indexhighest = index
                index = index + 1
            del btc_prices_copy[indexhighest] #delete highest price
        if len(btc_prices_copy) == 1:
            medianprice = btc_prices_copy[0]
        else:
            medianprice = (btc_prices_copy[0] + btc_prices_copy[1]) / 2.0

print("Prices scraped: " + str(BTC_PRICES))
print("Median Price: " + str(medianprice))
print("High Price: " + str(hiprice) + " from " + str(hiprice_site))
print("Low Price: " + str(loprice) + " from " + str(loprice_site))
        

driver.quit()