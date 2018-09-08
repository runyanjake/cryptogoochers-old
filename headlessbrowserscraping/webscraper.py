# @author Jake Runyan
# @desc A "Jscraper" web scraper ADT that runs a selenium instance headless or headed to drive chrome or firefox.

import json

class Target:
    site = ""
    xpath = ""
    def __init__(self, turl, tpath):
        self.url = turl
        self.xpath = tpath
    def __str__(self):
        return ("{" + str(self.url) + ": " + str(self.xpath) + "}")

class Jscraper:
    #private
    def __loadTargets(self, file):
        print("load targets")
        #load scrape locations from json as array of Targets
        data = None
        self.BTC_SOURCES = []
        with open("directory.json", "r") as jsonfile:
            data = json.load(jsonfile)
        for currency in data:
            for entry in data[currency]:
                self.BTC_SOURCES.append(Target(entry["url"], entry["xpath"]))

    #public
    def __init__(self):
        self.__loadTargets("directory.json")
        self.printSources()
    def printSources(self):
        for source in self.BTC_SOURCES:
            print(source)
        pass
    def scrape(self):
        pass

scpr = Jscraper()