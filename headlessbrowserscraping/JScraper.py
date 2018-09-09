# @author Jake Runyan
# @desc A "Jscraper" web scraper ADT that runs a selenium instance headless or headed to drive chrome or firefox.

import json
import selenium
from selenium.webdriver.firefox.options import Options
from selenium import webdriver   
import sqlite3
import sys

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

class JScraperException(Exception):
    pass

class JScraper:
    #private
    __currencyTypes = None
    __targets = None
    __connection = None
    __webdriver = None

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
                        ''' (currency text, date timestamp, median_price real, hi_price real, hi_price_site text, lo_price real, lo_price_site text)''')
            except sqlite3.OperationalError:
                pass
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
    #public
    def __init__(self, jsonfile="directory.json", 
                    dtbfile="./databases/jscraper.db", 
                    logfile="log.txt",
                    browser_type="firefox",
                    browser_driverpath="./browserdrivers/geckodriver",
                    browser_isheadless=True):
        self.__initTargets(jsonfile)
        self.__initDatabase(dtbfile)
        self.__initWebdriver(browser_type, browser_driverpath, browser_isheadless)

    def scrape(self, currency="ALL", iterations=1 ,num_attempts=10):
        for i in range(iterations):
            if currency == "ALL":
                for currency_tkr in self.__currencyTypes:
                    currency_valueset = []
                    for target in self.__targets:
                        if target.ticker == currency_tkr:
                            finished_scraping = False
                            num_reattempts = num_attempts
                            while not finished_scraping:
                                print("\t Attempting " + str(target.url) + "...")
                                try:
                                    print("\tScraping " + str(target.url) + "...")
                                    self.__webdriver.get(target.url)
                                    value_element = self.__webdriver.find_element_by_xpath(target.xpath)
                                    value_str = value_element.text
                                    if value_str == "" or value_str == None:
                                        print("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                                        num_reattempts = num_reattempts-1
                                        if num_reattempts > 0:
                                            finished_scraping = False
                                        else:
                                            print("\tFailed to parse a string from the webpage. Continuing...")
                                            value = -1.0 #error value, most likely never used
                                            finished_scraping = True #loop control, dont mean anything
                                    else:
                                        #Regex will recognize strings with a decimal or integer number, with or without commas denoting thousands.
                                        value = float(re.search("[0-9,]+\.[0-9]+|[0-9,]+", value_str).group(0).replace(",", ""))
                                        BTC_PRICES.append(value)
                                        print("\tSuccess. Found BTC price " + str(value) + ".")
                                        finished_scraping = True
                                except selenium.common.exceptions.NoSuchElementException:
                                    print("\tFailed to parse a string from the webpage. Retrying... (" + str(num_reattempts) + " attempts left)")
                                    num_reattempts = num_reattempts-1
                                    if num_reattempts > 0:
                                        finished_scraping = False
                                    else:
                                        print("\tFailed to parse a string from the webpage. Continuing...")
                                        value = -1.0 #error value, most likely never used
                                        finished_scraping = True #loop control, dont mean anything
                                except:
                                    print("\tError: Connection to " + str(target.url) + " failed. Skipping it for now.")
                                    finished_scraping = True

            else: #scrape one specific currency's sources
                pass

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
print(scpr)
scpr.scrape()