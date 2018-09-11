# @author Jake Runyan
# @desc A "Jscraper" web scraper ADT that runs a selenium instance headless or headed to drive chrome or firefox.

import datetime
import json
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import ticker
import re
import selenium
from selenium.webdriver.firefox.options import Options
from selenium import webdriver   
import sqlite3
import sys

#target class encapsulating crypto type, url, and xpath to value
class Target:
    ticker = ""
    url = ""
    xpath = ""
    def __init__(self, ttik, turl, tpath):
        self.ticker = ttik
        self.url = turl
        self.xpath = tpath
    def __str__(self):
        return ("{" + str(self.ticker) + " | " + str(self.url) + " | " + str(self.xpath) + "}")

#exception type for creating a special exception with a string
class JScraperException(Exception):
    pass

class JScraper:
    #private
    __currencyTypes = None
    __targets = None
    __connection = None
    __webdriver = None
    __log = None

    def __initTargets(self, file): #load scrape locations from json as array of Targets
        data = None
        self.__targets = []
        self.__currencyTypes = []
        try:
            with open(file, "r") as jsonfile:
                data = json.load(jsonfile)
            for currency in data:
                self.__currencyTypes.append(currency)
                for entry in data[currency]:
                    self.__targets.append(Target(currency, entry["url"], entry["xpath"]))
        except(IOError):
            raise JScraperException("Specified JSON file " + str(file) + " does not exist.")

    def __initDatabase(self, dtbfile):
        #requires targets to be loaded so currencyTypes exists.
        connection = sqlite3.connect(dtbfile)
        for currency in self.__currencyTypes:
            tablename = currency + "prices"
            try:
                connection.execute('''CREATE TABLE ''' + str(tablename) + 
                        ''' (currency text, date timestamp, median_price real, median_price_site text, hi_price real, hi_price_site text, lo_price real, lo_price_site text)''')
                self.__makeLogEntry(str(tablename) + " table was created.\n")
            except sqlite3.OperationalError:
                self.__makeLogEntry(str(tablename) + " table verified.\n")
        self.__connection = connection

    def __initWebdriver(self, browser_type, browser_driverpath, browser_isheadless):
        if browser_type == "firefox":
            ffox_options = Options()
            if browser_isheadless:
                ffox_options.add_argument("--headless")
            self.__webdriver = webdriver.Firefox(firefox_options=ffox_options, executable_path=browser_driverpath)
        else: #default to chrome
            chrome_options = webdriver.ChromeOptions()
            if browser_isheadless:
                chrome_options.add_argument("--headless")
            self.__webdriver = webdriver.Chrome(browser_driverpath, chrome_options=chrome_options)
        self.__webdriver.set_page_load_timeout(30)

    def __initLog(self):
        try:
            self.__log = open("log.txt", 'w')
        except:
            self.__log = None

    def __makeLogEntry(self, entry):
        if not(self.__log == None):
            self.__log.write(entry)

    def __renderProgressBar(self, x, y, width):
        msg = "\rJScraper progress: ["
        barsize = round(width * (x / y))
        for a in range(barsize):
            msg = msg + "="
        for a in range(barsize,width):
            msg = msg + " "
        msg = msg + "] " + str(x) + "\\" + str(y)
        sys.stdout.write(msg)
        pass

    #public
    #default constructor, with a few configurable options
    def __init__(self, jsonfile="directory.json", 
                    dtbfile="./databases/jscraper.db", 
                    logfile="log.txt",
                    browser_type="firefox",
                    browser_driverpath="./browserdrivers/geckodriver",
                    browser_isheadless=True):
        self.__initTargets(jsonfile)
        self.__initDatabase(dtbfile)
        self.__initWebdriver(browser_type, browser_driverpath, browser_isheadless)
        self.__initLog()

    #deconstructor used to close things the program was using
    #it's generally not recommended to do this in Python
    #invoked when all references are deleted or del keyword used
    def __del__(self):
        self.__currencyTypes = None
        self.__targets = None
        self.__webdriver.quit()
        self.__connection.close()
        if not(self.__log == None):
            self.__log.close()

    #scrapes data from all targets, returns a dictionary containing scraped values sorted by ticker
    #NOTE: uses a regex to parse strings so needs modification for non-numerics
    def scrape(self, currency="ALL", iterations=1 ,num_attempts=10):
        results = {}
        for i in range(iterations):
            completed = 0
            self.__renderProgressBar(completed, len(self.__targets), 20)
            for currency_tkr in self.__currencyTypes:
                if(currency_tkr == currency or currency == "ALL"):
                    currency_valueset = []
                    for target in self.__targets:
                        if target.ticker == currency_tkr:
                            finished_scraping = False
                            num_reattempts = num_attempts
                            while not finished_scraping:
                                self.__makeLogEntry("\t Attempting " + str(target.url) + "...\n")
                                try:
                                    self.__makeLogEntry("\tScraping " + str(target.url) + "...\n")
                                    self.__webdriver.get(target.url)
                                    value_element = self.__webdriver.find_element_by_xpath(target.xpath)
                                    value_str = value_element.text
                                    if value_str == "" or value_str == None:
                                        self.__makeLogEntry("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)\n")
                                        num_reattempts = num_reattempts-1
                                        if num_reattempts > 0:
                                            finished_scraping = False
                                        else:
                                            self.__makeLogEntry("\tFailed to parse a string from the webpage. Continuing...\n")
                                            value = -1.0
                                            finished_scraping = True
                                    else:
                                        value = float(re.search("[0-9,]+\.[0-9]+|[0-9,]+", value_str).group(0).replace(",", ""))
                                        currency_valueset.append((value, target.url))
                                        self.__makeLogEntry("\tSuccess. Found BTC price " + str(value) + ".\n")
                                        finished_scraping = True
                                except selenium.common.exceptions.NoSuchElementException:
                                    self.__makeLogEntry("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)\n")
                                    num_reattempts = num_reattempts-1
                                    if num_reattempts > 0:
                                        finished_scraping = False
                                    else:
                                        self.__makeLogEntry("\tFailed to parse a string from the webpage. Continuing...\n")
                                        value = -1.0
                                        finished_scraping = True
                                except selenium.common.exceptions.TimeoutException:
                                    self.__makeLogEntry("\tConnection failed after 30 seconds... (" + str(num_reattempts) + " attempts left)\n")
                                    num_reattempts = num_reattempts-1
                                    if num_reattempts > 0:
                                        finished_scraping = False
                                    else:
                                        self.__makeLogEntry("\tFailed to parse a string from the webpage. Continuing...\n")
                                        value = -1.0
                                        finished_scraping = True

                                except:
                                    self.__makeLogEntry("\tError: Connection to " + str(target.url) + " failed. Skipping it for now.\n")
                                    finished_scraping = True
                            completed = completed + 1
                            self.__renderProgressBar(completed, len(self.__targets), 20)
                    self.__makeLogEntry("Scraped " + currency_tkr + " To get values: " + str(currency_valueset) + "\n")
                    results[currency_tkr] = currency_valueset
        sys.stdout.write("\n") #for the progress bar
        return results

    #recieves data as array of (value, url) pairs and records it into the database
    def recordData(self, data):
        if not(data == None) and len(data) > 0:
            for currency_type in data:
                data_list = data[currency_type]
                data_list_inorder = sorted(data_list)
                median_price = -1.0
                median_price_site = None
                lo_price = data_list_inorder[0][0]
                lo_price_site = data_list_inorder[0][1]
                hi_price = data_list_inorder[len(data_list_inorder)-1][0]
                hi_price_site = data_list_inorder[len(data_list_inorder)-1][1]
                while len(data_list_inorder) > 2:
                    del data_list_inorder[0]
                    del data_list_inorder[len(data_list_inorder)-1]
                if len(data_list_inorder) == 2:
                    median_price = (data_list_inorder[0][0] + data_list_inorder[1][0]) / 2.0
                    median_price_site = data_list_inorder[1][1]
                else: #is 1
                    median_price = data_list_inorder[0][0]
                    median_price_site = data_list_inorder[0][1]
                self.__makeLogEntry("For " + str(currency_type) + "  low price: " + str(lo_price) + " at " + str(lo_price_site) + "  median price: " + str(median_price) + " at " + str(median_price_site) + "  hi price: " + str(hi_price) + " at " + str(hi_price_site) + "\n")
                tablename = currency_type + "prices"
                # try:
                prepstmt = "INSERT INTO " + str(tablename) + " VALUES ('" + str(currency_type) + "','"  + str(datetime.datetime.utcnow()) + "'," + str(median_price) + ",'" + str(median_price_site) + "'," + str(hi_price) + ",'" + str(hi_price_site) + "',"  + str(lo_price) + ",'" + str(lo_price_site) + "')" 
                self.__connection.execute(prepstmt)
                self.__connection.commit()
                # except:
                #     print("AN ERROR WAS HANDLED DURING DATABASE ENTRY")

    #requires a connection to be defined
    def renderGraph(self, currency="ALL", mode="MEDIAN"):
        for curr in self.__currencyTypes:
            if(curr == currency or currency == "ALL"):
                dates = []
                medians = []
                hi_vals = []
                lo_vals = []
                itor = 1
                tablename = curr + "prices"
                for row in self.__connection.execute("SELECT * FROM " + str(tablename) + " ORDER BY date DESC"):
                    dates.insert(0,row[1])
                    medians.insert(0,row[2])
                    hi_vals.insert(0,row[4])
                    lo_vals.insert(0,row[6])
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

    def printTargets(self):
        for target in self.__targets:
            print(target)

    def getTargets(self):
        return self.__targets

    def printCurrencies(self):
        print(self.getCurrencies())

    def getCurrencies(self):
        return self.__currencyTypes

scpr = JScraper(browser_isheadless=False)
# results = scpr.scrape()
# scpr.recordData(results)
scpr.renderGraph()
del scpr