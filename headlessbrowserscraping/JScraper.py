# @author Jake Runyan
# @desc A "Jscraper" web scraper ADT that runs a selenium instance headless or headed to drive chrome or firefox.

import json
import sqlite3
import sys

class Target:
    ticker = ""
    site = ""
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
    __currencyTypes = []
    __targets = None
    __connection = None

    def __initTargets(self, file): #load scrape locations from json as array of Targets
        data = None
        self.__targets = []
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

    #public
    def __init__(self, jsonfile="directory.json", dtbfile="./databases/jscraper.db", logfile="log.txt"):
        self.__initTargets(jsonfile)
        self.__initDatabase(dtbfile)

    def printTargets(self):
        for target in self.__targets:
            print(target)

    def printCurrencies(self):
        sys.stdout.write("Currencies: {")
        first = True
        for currency in self.__currencyTypes:
            if first:
                sys.stdout.write(currency)
                first = False
            else:
                sys.stdout.write(", " + currency)
        sys.stdout.write("}\n")

    def scrape(self):
        pass

scpr = JScraper()
scpr.printCurrencies()
scpr.printTargets()