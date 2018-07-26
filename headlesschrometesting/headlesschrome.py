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

class SiteAndXPath:
    site = ""
    xpath = ""
    def __init__(self, spsite, spxpath):
        self.site = spsite
        self.xpath = spxpath

BTC_SOURCES = [ #Bitcoin Overview numbers
                SiteAndXPath("https://www.coindesk.com/price/", "//span[@class='data']"),
                SiteAndXPath("https://cointelegraph.com/bitcoin-price-index", "//div[@class='value text-nowrap']"),
                #Bitcoin Trading Site numbers (recent trades)
                SiteAndXPath("https://bitcoincharts.com/markets/coinbaseUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/bitstampUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/krakenUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/itbitUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/coinsbankUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/wexUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/lakeUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/cexUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/getbtcUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/localbtcUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/btcalphaUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/okcoinUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/bitbayUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("https://bitcoincharts.com/markets/bitkonanUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span")]
BTC_PRICES = []


#Testing Code
def test():
    testing = 2
    driver.get(BTC_SOURCES[testing].site)
    btc_value_element = driver.find_element_by_xpath(BTC_SOURCES[testing].xpath)
    btc_value_str = btc_value_element.text
    print("Element: " + str(btc_value_element))
    print("Text: " + str(btc_value_str))
    exit(-1)


#main loop execution
def main():
    #Database creation/connection
    print("Performing database setup...")
    connection = sqlite3.connect('databases/cryptogoochers.db')
    try:
        print("No database exists. Creating a new one.")
        connection.execute('''CREATE TABLE BTCprices
                (date text, median_price real, hi_price real, hi_price_site text, lo_price real, lo_price_site text)''')
    except sqlite3.OperationalError:
        print("BTCprices table verified.")
    print("Done.")

    PATH_TO_CHROMEDRIVER = './chromedriver/chromedriver'
    driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)  # Chrome driver, using the chromedriver file in PATH_TO_CHROMEDRIVER, if not specified will search path.

    scrape_and_store(connection, driver)

    driver.quit()


def scrape_and_store(connection, driver):
    #Scraping Prices
    for itor in range(0, len(BTC_SOURCES)):
        succeeded_scraping = False
        num_reattempts = 10
        while not succeeded_scraping:
            print("Scraping " + str(BTC_SOURCES[itor].site) + "...")
            driver.get(BTC_SOURCES[itor].site)
            btc_value_element = driver.find_element_by_xpath(BTC_SOURCES[itor].xpath)
            btc_value_str = btc_value_element.text
            if btc_value_str == "" or btc_value_str == None:
                print("Failed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                num_reattempts = num_reattempts-1
                if num_reattempts > 0:
                    succeeded_scraping = False
                else:
                    print("Failed to parse a string from the webpage. Continuing...")
                    btc_value = -1.0 #error value, most likely never used
                    succeeded_scraping = True #loop control, dont mean anything
            else:
                #Regex will recognize strings with a decimal or integer number, with or without commas denoting thousands.
                btc_value = float(re.search("[0-9,]+\.[0-9]+|[0-9,]+", btc_value_str).group(0).replace(",", ""))
                BTC_PRICES.append(btc_value)
                print("Success. Found BTC price " + str(btc_value) + ".")
                succeeded_scraping = True
    #Doing some math with the prices.
    btc_prices_copy = []
    for price in BTC_PRICES:
        btc_prices_copy.append(price)
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
    print("\nPrices scraped: " + str(BTC_PRICES) + " (" + str(len(BTC_PRICES)) + " scraped data points).")
    print("Median Price: " + str(medianprice))
    print("High Price: " + str(hiprice) + " from " + str(hiprice_site))
    print("Low Price: " + str(loprice) + " from " + str(loprice_site) + "\n")
    #Perform insertion into database
    prepstmt = "INSERT INTO BTCprices VALUES ('" + str(now) + "'," + str(medianprice) + "," + str(hiprice) + ",'" + str(hiprice_site) + "',"  + str(loprice) + ",'" + str(loprice_site) + "')" 
    connection.execute(prepstmt)
    connection.commit()
    connection.close()


#main loop execution
if __name__ == "__main__": main()