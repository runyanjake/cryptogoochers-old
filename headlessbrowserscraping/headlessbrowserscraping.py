# https://github.com/runyanjake/cryptogoochers/headlesschrometesting/headlesschrome.py
# @Author Jake Runyan
# Testing of headless chrome to scrape cryptocoin data and store it in a database, generating a nice graph as output.
# Running this script performs one complete scrape of relevant data (enough to fully populate a database row), generates a graph and exits.
# It is designed to be called on a timetable for continuous data acquisition.
#

import datetime
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import ticker
import os
import optparse
import plotly
import plotly.graph_objs as go
import re
import requests
import sqlite3
import sys
import time
import selenium
from selenium.webdriver.firefox.options import Options
from selenium import webdriver   

class SiteAndXPath:
    ticker = ""
    site = ""
    xpath = ""
    def __init__(self, sticker, spsite, spxpath):
        self.ticker = sticker
        self.site = spsite
        self.xpath = spxpath

#note that cloudflare and other ddos-stoppers messes with the success rate of this program
BTC_SOURCES = [ 
                #### ---- B T C / B I T C O I N ---- ####
                #Overview numbers
                # SiteAndXPath("BTC", "https://www.coindesk.com/price/", "//span[@class='data']"), #this site takes forever
                SiteAndXPath("BTC", "https://cointelegraph.com/bitcoin-price-index", "//div[@class='value text-nowrap']"),
                SiteAndXPath("BTC", "https://coinmarketcap.com/currencies/bitcoin/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/coinbaseUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/bitstampUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/krakenUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/itbitUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/coinsbankUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/wexUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/lakeUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/cexUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/getbtcUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/localbtcUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/btcalphaUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/okcoinUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/bitbayUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://bitcoincharts.com/markets/bitkonanUSD.html", "//div[@id='market_summary']/child::div/child::p/child::span"),
                SiteAndXPath("BTC", "https://coinranking.com/coin/bitcoin-btc", "//span[@class='price__price']"),
                
                #### ---- E T H / E T H E R E U M ---- ####
                #Overview numbers
                SiteAndXPath("ETH", "https://coinmarketcap.com/currencies/ethereum/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("ETH", "https://coinranking.com/coin/ethereum-eth", "//span[@class='price__price']"),
                
                #### ---- X R P / R I P P L E ---- ####
                #Overview numbers
                SiteAndXPath("XRP", "https://coinmarketcap.com/currencies/ripple/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("XRP", "https://coinranking.com/coin/xrp-xrp", "//span[@class='price__price']"),
                
                #### ---- E O S ---- ####
                #Overview numbers
                SiteAndXPath("EOS", "https://coinmarketcap.com/currencies/eos/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("EOS", "https://coinranking.com/coin/eos-eos", "//span[@class='price__price']"),
                
                #### ---- X L M / S T E L L A R ---- ####
                #Overview numbers
                SiteAndXPath("XLM", "https://coinmarketcap.com/currencies/stellar/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("XLM", "https://coinranking.com/coin/stellar-xlm", "//span[@class='price__price']"),
                
                #### ---- L T C / L I T E C O I N ---- ####
                #Overview numbers
                SiteAndXPath("LTC", "https://coinmarketcap.com/currencies/litecoin/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("LTC", "https://coinranking.com/coin/litecoin-ltc", "//span[@class='price__price']"),
                
                #### ---- A D A / C A R D O N O ---- ####
                #Overview numbers
                SiteAndXPath("ADA", "https://coinmarketcap.com/currencies/cardano/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("ADA", "https://coinranking.com/coin/cardano-ada", "//span[@class='price__price']"),
                
                #### ---- M I O T A / I O T A ---- ####
                #Overview numbers
                SiteAndXPath("MIOTA", "https://coinmarketcap.com/currencies/iota/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("MIOTA", "https://coinranking.com/coin/iota-iot", "//span[@class='price__price']"),
                
                #### ---- T R X / T R O N ---- ####
                #Overview numbers
                SiteAndXPath("TRX", "https://coinmarketcap.com/currencies/tron/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("TRX", "https://coinranking.com/coin/tron-trx", "//span[@class='price__price']"),
                
                #### ---- U S D T / T E T H E R---- ####
                #Overview numbers
                SiteAndXPath("USDT", "https://coinmarketcap.com/currencies/tether/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("USDT", "https://coinranking.com/coin/tether-usdt", "//span[@class='price__price']"),
                
                #### ---- X M R / M O N E R O ---- ####
                #Overview numbers
                SiteAndXPath("XMR", "https://coinmarketcap.com/currencies/monero/", "//span[@class='h2 text-semi-bold details-panel-item--price__value']"),
                #Market Values
                SiteAndXPath("XMR", "https://coinranking.com/coin/monero-xmr", "//span[@class='price__price']")
                ]

#program defaults
DEF_CURRENCY = "BTC"
DEF_ITERATIONS = 10000
DEF_WAIT_TIME = 900
DEF_BROWSER = "firefox"

#main loop execution
def main():
    #Cmd line validation & setup
    optionParser = optparse.OptionParser()
    optionParser.add_option("--browser",
                        dest="browser",
                        type="string",
                        help="""Which browser to ghost drive.
                                Choices are 'chrome' or 'firefox'. Default=%s""" 
                                % DEF_BROWSER,
                        default=DEF_BROWSER)
    optionParser.add_option("--currency",
                        dest="currency",
                        type="string",
                        help="""Set the currency to update for. Default=%s""" 
                                % DEF_CURRENCY,
                        default=DEF_CURRENCY)
    optionParser.add_option("--iterations",
                        dest="iterations",
                        type="int",
                        help="""Number of iterations to run for. Default=%d""" 
                                % DEF_ITERATIONS,
                        default=DEF_ITERATIONS)
    optionParser.add_option("--wait_time",
                        dest="wait_time",
                        type="int",
                        help="""Time (seconds) to wait between scraping runs. Default=%d""" 
                                % DEF_WAIT_TIME,
                        default=DEF_WAIT_TIME)
    (options, args) = optionParser.parse_args()

    # Database creation/connection
    print("Performing database setup...")
    connection = sqlite3.connect('databases/cryptogoochers.db')
    tablename = options.currency + "prices"
    try:
        connection.execute('''CREATE TABLE ''' + str(tablename) + 
                ''' (currency text, date timestamp, median_price real, hi_price real, hi_price_site text, lo_price real, lo_price_site text)''')
        print(str(tablename) + " table was created.")
    except sqlite3.OperationalError:
        print(str(tablename) + " table verified.")
    print("Done.")

    driver = None
    if options.browser == 'firefox':
        PATH_TO_FIREFOX = "./browserdrivers/geckodriver"
        ffox_options = Options()
        #options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=ffox_options, executable_path=PATH_TO_FIREFOX)
    else:
        PATH_TO_CHROMEDRIVER = './browserdrivers/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER, chrome_options=chrome_options)  # Chrome driver, using the chromedriver file in PATH_TO_CHROMEDRIVER, if not specified will search path.
    

    for itor in range(0, options.iterations):
        scrape_and_store(options, tablename, connection, driver, itor, options.iterations)
        extendgraph(connection, tablename)
        time.sleep(options.wait_time) #sleep some amount of time before scraping again
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

def scrape_and_store(options, tablename, connection, driver, cur_scrape, max_scrapes):
    print("Scraping iteration " + str(cur_scrape+1) + "/" + str(max_scrapes) + ":")
    BTC_PRICES = []
    #Scraping Prices
    for itor in range(0, len(BTC_SOURCES)):
        if BTC_SOURCES[itor].ticker == options.currency:
            finished_scraping = False
            num_reattempts = 10
            while not finished_scraping:
                try:
                    print("\tScraping " + str(BTC_SOURCES[itor].site) + "...")
                    driver.get(BTC_SOURCES[itor].site)
                    btc_value_element = driver.find_element_by_xpath(BTC_SOURCES[itor].xpath)
                    btc_value_str = btc_value_element.text
                    if btc_value_str == "" or btc_value_str == None:
                        print("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                        num_reattempts = num_reattempts-1
                        if num_reattempts > 0:
                            finished_scraping = False
                        else:
                            print("\tFailed to parse a string from the webpage. Continuing...")
                            btc_value = -1.0 #error value, most likely never used
                            finished_scraping = True #loop control, dont mean anything
                    else:
                        #Regex will recognize strings with a decimal or integer number, with or without commas denoting thousands.
                        btc_value = float(re.search("[0-9,]+\.[0-9]+|[0-9,]+", btc_value_str).group(0).replace(",", ""))
                        BTC_PRICES.append(btc_value)
                        print("\tSuccess. Found BTC price " + str(btc_value) + ".")
                        finished_scraping = True
                except selenium.common.exceptions.NoSuchElementException:
                    print("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                    num_reattempts = num_reattempts-1
                    if num_reattempts > 0:
                        finished_scraping = False
                    else:
                        print("\tFailed to parse a string from the webpage. Continuing...")
                        btc_value = -1.0 #error value, most likely never used
                        finished_scraping = True #loop control, dont mean anything
                except:
                    print("\tError: Connection to " + str(BTC_SOURCES[itor].site) + " failed. Skipping it for now.")
                    finished_scraping = True
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
    print("\n\tScraped " + str(len(BTC_PRICES)) + " websites for data points). If more than 0, will perform database insert.")
    print("\tMedian Price: " + str(medianprice))
    print("\tHigh Price: " + str(hiprice) + " from " + str(hiprice_site))
    print("\tLow Price: " + str(loprice) + " from " + str(loprice_site) + "\n")
    if len(BTC_PRICES) > 0:
        #Perform insertion into database
        prepstmt = "INSERT INTO " + str(tablename) + " VALUES ('" + str(options.currency) + "','"  + str(now) + "'," + str(medianprice) + "," + str(hiprice) + ",'" + str(hiprice_site) + "',"  + str(loprice) + ",'" + str(loprice_site) + "')" 
        connection.execute(prepstmt)
        connection.commit()

def extendgraph(connection, tablename):
    print("Creating a Graph...")
    dates = []
    medians = []
    hi_vals = []
    lo_vals = []
    itor = 1
    for row in connection.execute("SELECT * FROM " + str(tablename) + " ORDER BY date DESC"):
        dates.insert(0,row[1])
        medians.insert(0,row[2])
        hi_vals.insert(0,row[3])
        lo_vals.insert(0,row[5])
        itor = itor + 1

    print("NUMBER OF DATABASE ITEMS GRABBED: " + str(len(dates)))

    pricingfilepath = "output/" + tablename
    medianfilepath = pricingfilepath +  "_median"

    #hopefully controlls the number of ticks on the x axis
    xticks = ticker.MaxNLocator(20)

    fig1, ax = plt.subplots( nrows=1, ncols=1)  # create figure & 1 axis
    ax.plot(dates, medians, label="Median")
    ax.xaxis.set_major_locator(xticks) #set number of ticks on plot
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=270) #rotate labels
    plt.tight_layout() #make room for lablels
    fig1.savefig(medianfilepath+'.png', dpi=1000)   # save the figure to file
    plt.close(fig1)

    fig2, ax = plt.subplots( nrows=1, ncols=1)  # create figure & 1 axis
    ax.plot(dates, medians, label="Median")
    ax.plot(dates, hi_vals, label="High Value")
    ax.plot(dates, lo_vals, label="Low Value")
    ax.xaxis.set_major_locator(xticks) #set number of ticks on plot
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=270) #rotate labels
    plt.tight_layout() #make room for lablels
    fig2.savefig(pricingfilepath+'.png', dpi=1000)   # save the figure to file
    plt.close(fig2)

    print("Done.")

def extendgraph_plotly(connection, tablename):
    #plotly setup
    print("Establishing connection to plotly...")
    plotly.tools.set_credentials_file(username='cryptogoochers', api_key='eH5qdbtfFBm78btw82io')
    plotly.tools.set_config_file(world_readable=True, sharing='public')
    print("Done.")

    print("Creating a Graph...")
    dates = []
    medians = []
    hi_vals = []
    lo_vals = []
    for row in connection.execute("SELECT * FROM " + str(tablename) + " ORDER BY date DESC"):
        dates.append(row[1])
        medians.append(row[2])
        hi_vals.append(row[3])
        lo_vals.append(row[5])

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
    pricingfile = tablename
    medianfile = tablename + "_median"
    try:
        btc_pricing_url = plotly.plotly.plot(data, filename=pricingfile, auto_open=False)
        btc_median_trace_url = plotly.plotly.plot([median_trace], filename=medianfile, auto_open=False)
    except: 
        print("\tERROR: Plotly denied the request to update plot. Skipping plot update for now.")


    print("Done.")

#main loop execution
if __name__ == "__main__": main()
