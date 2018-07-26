# https://github.com/runyanjake/cryptogoochers/headlesschrometesting/headlesschrome.py
# @Author Jake Runyan
# Testing of headless chrome to scrape cryptocoin data and store it in a database, generating a nice graph as output.
# Running this script performs one complete scrape of relevant data (enough to fully populate a database row), generates a graph and exits.
# It is designed to be called on a timetable for continuous data acquisition.
#

import datetime
import os
import plotly
import plotly.graph_objs as go
import re
import sqlite3
import sys
import time
import selenium
from selenium.webdriver.firefox.options import Options
from selenium import webdriver   

class SiteAndXPath:
    site = ""
    xpath = ""
    def __init__(self, spsite, spxpath):
        self.site = spsite
        self.xpath = spxpath

#note that cloudflare and other ddos-stoppers messes with the success rate of this program
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

#important constants for scraper behavior
SCRAPER_ITERATIONS = 10000
SCRAPER_WAIT_TIME = 900 #in seconds (15 mins > 96 updates a day, plotly limit for unpaid is 100)

#main loop execution
def main():
    # Database creation/connection
    print("Performing database setup...")
    connection = sqlite3.connect('databases/cryptogoochers.db')
    try:
        connection.execute('''CREATE TABLE BTCprices
                (date timestamp, median_price real, hi_price real, hi_price_site text, lo_price real, lo_price_site text)''')
    except sqlite3.OperationalError:
        print("BTCprices table verified.")
    print("Done.")

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="/Users/runyanjake/Desktop/Academia/CodingStuff/Repositories/cryptogoochers/headlessfirefoxtesting/firefoxdriver/geckodriver")

    for itor in range(0, SCRAPER_ITERATIONS):
        scrape_and_store(connection, driver, itor, SCRAPER_ITERATIONS)
        extendgraph(connection)
        time.sleep(SCRAPER_WAIT_TIME) #sleep some amount of time before scraping again
    driver.quit() #quit the webdriver
    connection.close() #close the connection

#Testing Code
def test():
    testing = 2
    driver.get(BTC_SOURCES[testing].site)
    btc_value_element = driver.find_element_by_xpath(BTC_SOURCES[testing].xpath)
    btc_value_str = btc_value_element.text
    print("Element: " + str(btc_value_element))
    print("Text: " + str(btc_value_str))
    exit(-1)

def scrape_and_store(connection, driver, cur_scrape, max_scrapes):
    print("Scraping iteration " + str(cur_scrape+1) + "/" + str(max_scrapes) + ":")
    BTC_PRICES = []
    #Scraping Prices
    for itor in range(0, len(BTC_SOURCES)):
        succeeded_scraping = False
        num_reattempts = 10
        while not succeeded_scraping:
            try:
                print("\tScraping " + str(BTC_SOURCES[itor].site) + "...")
                driver.get(BTC_SOURCES[itor].site)
                btc_value_element = driver.find_element_by_xpath(BTC_SOURCES[itor].xpath)
                btc_value_str = btc_value_element.text
                if btc_value_str == "" or btc_value_str == None:
                    print("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                    num_reattempts = num_reattempts-1
                    if num_reattempts > 0:
                        succeeded_scraping = False
                    else:
                        print("\tFailed to parse a string from the webpage. Continuing...")
                        btc_value = -1.0 #error value, most likely never used
                        succeeded_scraping = True #loop control, dont mean anything
                else:
                    #Regex will recognize strings with a decimal or integer number, with or without commas denoting thousands.
                    btc_value = float(re.search("[0-9,]+\.[0-9]+|[0-9,]+", btc_value_str).group(0).replace(",", ""))
                    BTC_PRICES.append(btc_value)
                    print("\tSuccess. Found BTC price " + str(btc_value) + ".")
                    succeeded_scraping = True
            except selenium.common.exceptions.NoSuchElementException:
                print("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                num_reattempts = num_reattempts-1
                if num_reattempts > 0:
                    succeeded_scraping = False
                else:
                    print("\tFailed to parse a string from the webpage. Continuing...")
                    btc_value = -1.0 #error value, most likely never used
                    succeeded_scraping = True #loop control, dont mean anything
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
    print("\n\tScraped " + str(len(BTC_PRICES)) + " websites for data points).")
    print("\tMedian Price: " + str(medianprice))
    print("\tHigh Price: " + str(hiprice) + " from " + str(hiprice_site))
    print("\tLow Price: " + str(loprice) + " from " + str(loprice_site) + "\n")
    #Perform insertion into database
    prepstmt = "INSERT INTO BTCprices VALUES ('" + str(now) + "'," + str(medianprice) + "," + str(hiprice) + ",'" + str(hiprice_site) + "',"  + str(loprice) + ",'" + str(loprice_site) + "')" 
    connection.execute(prepstmt)
    connection.commit()

def extendgraph(connection):
    print("Creating a Graph...")
    dates = []
    medians = []
    hi_vals = []
    lo_vals = []
    for row in connection.execute("SELECT * FROM BTCprices ORDER BY date DESC"):
        dates.append(row[0])
        medians.append(row[1])
        hi_vals.append(row[2])
        lo_vals.append(row[4])


    #plotly setup
    plotly.tools.set_credentials_file(username='cryptogoochers', api_key='eH5qdbtfFBm78btw82io')
    plotly.tools.set_config_file(world_readable=True, sharing='public')

    median_trace = go.Scatter(
        x=dates,
        y=medians
    )
    hi_trace = go.Scatter(
        x=dates,
        y=hi_vals
    )
    lo_trace = go.Scatter(
        x=dates,
        y=lo_vals
    )
    data = [median_trace, hi_trace, lo_trace]

    #upload the file
    try:
        btc_pricing_url = plotly.plotly.plot(data, filename="btc_pricing", auto_open=False)
        btc_median_trace_url = plotly.plotly.plot([median_trace], filename="btc_median_trace", auto_open=False)
    except: 
        print("Plotly denied the request to update plot. Skipping plot update for now.")


    print("Done.")

#main loop execution
if __name__ == "__main__": main()