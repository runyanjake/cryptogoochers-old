# @author Jake Runyan
# @desc A hypothetical trader that unit tests a variety of VectorSpaces' new APIs to see if using those as margins to trade is worth it.

import ccxt 
from JScraper import JScraper # https://github.com/runyanjake/JScraper
import json
import sys

#exception type for creating a special exception with a string
class PortfolioException(Exception):
    pass

class Portfolio:
    #private
    __filepath = None
    __cashpool_amt = None
    __portfolio_id = None
    __portfolio_owner = None
    __portfolio = {}

    #public
    #default constructor FOR EXISTING PORTFOLIO
    #if wanting a blank new portfolio, use the static method Portfolio.generatePortfolio(...)
    def __init__(self, path_to_file):
        file = None
        try:
            file = open(path_to_file)
        except(Exception):
            raise PortfolioException("Portfolio file not found: " + str(path_to_file))
        data = json.load(file)
        tmp = data["cashpool_amt"]
        if tmp == None:
            raise PortfolioException("Corrupted portfolio file: No cashpool amount for " + str(path_to_file))
        self.__cashpool_amt = tmp
        tmp = data["portfolio_id"]
        if tmp == None:
            raise PortfolioException("Corrupted portfolio file: No ID for " + str(path_to_file))
        self.__portfolio_id = tmp
        tmp = data["portfolio_owner"]
        if tmp == None:
            raise PortfolioException("Corrupted portfolio file: No Owner for " + str(path_to_file))
        self.__portfolio_owner = tmp
        tmp = data["portfolio"]
        if tmp == None:
            raise PortfolioException("Corrupted portfolio file: No Portfolio for " + str(path_to_file))
        for entry in tmp:
            self.__portfolio[entry] = tmp[entry]
            # for item in entry:
            #     self.__portfolio[item] = entry[item]
        self.__filepath = path_to_file

    @staticmethod
    #Creates new instance of portfolio, as a JSON file. this DOES NOT create a PF instance
    #ID must be number, owner must be string, portfolio must be dictionary of string : number pairs denoting ticker : amount relation
    #portfolio id is mainly a semantic identifier, the filename of the portfolio is the important thing.
    def generatePortfolio(path, portfolioID, portfolioOwner, portfolio, cashpool_amount):
        data = {}
        data["cashpool_amt"] = cashpool_amount
        data["portfolio"] = portfolio
        data["portfolio_id"] = portfolioID
        data['portfolio_owner'] = portfolioOwner
        try:
            open(path)
            raise PortfolioException("A portfolio with this name exists. Portfolios will not overwrite other portfolios.")
        except(IOError):
            file = open(path, "w+")
            json.dump(data, file, indent=4)
            pass
    
    #tostring
    def __str__(self):
        mystr = ""
        mystr = mystr + "Portfolio #" + str(self.__portfolio_id) + " at " + str(self.__filepath) + ", owned by " + str(self.__portfolio_owner) + " containing {"
        first = True
        for entry in self.__portfolio:
            if first:
                mystr = mystr + "(" + str(entry) + ", " + str(self.__portfolio[entry]) + ")"
                first = False
            else:
                mystr = mystr + ", (" + str(entry) + ", " + str(self.__portfolio[entry]) + ")"
        mystr = mystr + "} with an idle cashpool amount of " + str(self.__cashpool_amt) + ".\n"
        return mystr

    #uses JScraper to retrive current values and compute worth of portfolio
    #CALCULATED BY MEDIAN AMOUNT
    def worth(self):
        if self.__portfolio is None:
            raise PortfolioException("Corrupted portfolio: No Portfolio")
        else:
            #TODO: make JScraper able to report latest price and use it to calculate data
            scpr = JScraper()
            total = 0.0
            for ticker in self.__portfolio:
                price_per_share = scpr.retrieveMedians(curr=ticker)[0]
                total = total + price_per_share * self.__portfolio[ticker]
            return total

    #returns the amount of each coin held by the portfolio.
    def amount(self, ticker):
        if ticker in self.__portfolio:
            return self.__portfolio[ticker]
        else:
            return -1

    #Saves this portfolio to disk
    def save(self):
        data = {}
        data['cashpool_amt'] = self.__cashpool_amt
        data["portfolio"] = self.__portfolio
        data["portfolio_id"] = self.__portfolio_id
        data['portfolio_owner'] = self.__portfolio_owner
        file = open(self.__filepath, "w+")
        json.dump(data, file, indent=4)

    #purchase some amount of a specified currency
    def purchase(self, ticker, amt):
        #TODO: checkout ccxt https://github.com/ccxt/ccxt for selling to a bunch of markets
        #determine best market, connect to it
        #CALCULATED BY MEDIAN AMOUNT
        scpr = JScraper()
        price_per_share = scpr.retrieveMedians(curr=ticker)[0]
        #facilitate trade
        if(price_per_share * amt > self.__cashpool_amt):
            raise PortfolioException("Not enough in cashpool to purchase " + str(amt) + " of " + str(ticker) + ".")
        if ticker in self.__portfolio:
            self.__portfolio[ticker] = self.__portfolio[ticker] + amt
        else:
            self.__portfolio[ticker] = amt
        self.__cashpool_amt = self.__cashpool_amt - (amt * price_per_share)
        #update hardcopy portfolio

    #sell some amount of a specified currency
    def sell(self, ticker, amt):
        #TODO: checkout ccxt https://github.com/ccxt/ccxt for selling to a bunch of markets
        #determine best market, connect to it
        #CALCULATED BY MEDIAN AMOUNT
        scpr = JScraper()
        price_per_share = scpr.retrieveMedians(curr=ticker)[0]
        #facilitate trade
        if ticker in self.__portfolio:
            if amt > self.__portfolio[ticker]:
                raise PortfolioException("Portfolio does not contain that amount of " + str(ticker) + ".")
            self.__portfolio[ticker] = self.__portfolio[ticker] - amt
            self.__cashpool_amt = self.__cashpool_amt + (amt * price_per_share)
        else:
            raise PortfolioException("Portfolio does not contain any coins of the type " + str(ticker) + ".")
        #update hardcopy portfolio

#main imethod, unit testing
if __name__ == "__main__":
    p = Portfolio("portfolio.pf")
    # Portfolio.generatePortfolio("./port.pf", 11111, "Jake Runyan", {"BTC" : 9000, "ETH" : 200}, 100)
    # p2 = Portfolio("./port.pf")

    # print("Testing 3 bad cases....")
    # try:
    #     p.purchase("BTC", 100000000)
    # except(PortfolioException):
    #     print("Exception caught successfully.")
    # try:
    #     p.sell("BTC", 10000000)
    # except(PortfolioException):
    #     print("Exception caught successfully.")
    # try:
    #     p.sell("NONEXISTANT", 1)
    # except(PortfolioException):
    #     print("Exception caught successfully.")

    print(p)
    print("Total Worth: " + str(p.worth()))
    p.purchase("BTC", 0.01)
    print(p)
    print("Total Worth: " + str(p.worth()))
    print("BTC " + str(p.amount("BTC")))
    p.save()