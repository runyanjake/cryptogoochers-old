# @author Jake Runyan
# @desc A bot made from a JScraper and Portfolio, also a test grounds for new features

from JScraper import JScraper 
from Portfolio import Portfolio
import math
import sys
import time
import requests
import json

TIME_BETWEEN_ITERATIONS = 900 #15min

def dataScavenger(delay=TIME_BETWEEN_ITERATIONS, rendergraphs=False):
    scpr = JScraper(browser_type="chrome",browser_driverpath="./browserdrivers/chromedriver")
    while True:
        scpr.updateDirectory()
        data = scpr.scrape()
        scpr.recordData(data)
        if rendergraphs:
            scpr.renderGraph()
            scpr.renderALLGraph()
        time.sleep(delay) #sec

#buys cryptocurrencies whose last median was greater than the average of the last LOOKBACK_LENGTH medians
LOOKBACK_LENGTH = 10
def strategy1():
    print("Running Strategy 1.")
    scpr = JScraper(browser_type="chrome",browser_driverpath="./browserdrivers/chromedriver")
    p = Portfolio("portfolio_strat1.pf")
    myportfolio = p.getPortfolio()
    while True:
        # try to intelligently buy
        for curr in myportfolio:
            meds = scpr.retrieveMedians(curr=curr, max=LOOKBACK_LENGTH)
            if len(meds) < LOOKBACK_LENGTH:
                continue #Do nothing until 
            curr_median = meds[0]
            mean_of_median = 0
            for m in meds:
                mean_of_median = mean_of_median + m
            mean_of_median = mean_of_median / len(meds)
            print(str(curr) + ": MOst recent median: " + str(curr_median) + "  mean of median: " + str(mean_of_median))
            MAX_PERCENT_ALLOWANCE = .10
            if(mean_of_median < curr_median):
                purchase_amt = MAX_PERCENT_ALLOWANCE * p.getCashpool()
                purchase_price = curr_median
                shares = purchase_amt / purchase_price
                p.purchase(curr, shares)
                print("Buying " + str(shares) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(shares * purchase_price) + ").")
            elif(mean_of_median > curr_median):
                share_ct = p.amount(curr)
                if not(share_ct == -1 or share_ct <= 0.0):
                    sell_ct = MAX_PERCENT_ALLOWANCE * share_ct
                    purchase_price = curr_median
                    p.sell(curr, sell_ct)
                    print("Selling " + str(sell_ct) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(sell_ct * purchase_price) + ").")
            else: #if price constant, do nothing
                pass
        print(p)
        print("Total worth: " + str(p.getWorth()) + ".\n")
        time.sleep(TIME_BETWEEN_ITERATIONS) #sec

#performs strategy 1 on just bitcoin
def strategy2():
    print("Running Strategy 2.")
    scpr = JScraper(browser_type="chrome",browser_driverpath="./browserdrivers/chromedriver")
    p = Portfolio("portfolio_strat2.pf")
    myportfolio = p.getPortfolio()
    while True:
        # try to intelligently buy
        for curr in myportfolio:
            meds = scpr.retrieveMedians(curr=curr, max=LOOKBACK_LENGTH)
            if len(meds) < LOOKBACK_LENGTH:
                continue #Do nothing until 
            curr_median = meds[0]
            mean_of_median = 0
            for m in meds:
                mean_of_median = mean_of_median + m
            mean_of_median = mean_of_median / len(meds)
            print(str(curr) + ": MOst recent median: " + str(curr_median) + "  mean of median: " + str(mean_of_median))
            MAX_PERCENT_ALLOWANCE = .10
            if(mean_of_median < curr_median):
                purchase_amt = MAX_PERCENT_ALLOWANCE * p.getCashpool()
                purchase_price = curr_median
                shares = purchase_amt / purchase_price
                p.purchase(curr, shares)
                print("Buying " + str(shares) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(shares * purchase_price) + ").")
            elif(mean_of_median > curr_median):
                share_ct = p.amount(curr)
                if not(share_ct == -1 or share_ct <= 0.0):
                    sell_ct = MAX_PERCENT_ALLOWANCE * share_ct
                    purchase_price = curr_median
                    p.sell(curr, sell_ct)
                    print("Selling " + str(sell_ct) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(sell_ct * purchase_price) + ").")
            else: #if price constant, do nothing
                pass
        print(p)
        print("Total worth: " + str(p.getWorth()) + ".\n")
        time.sleep(TIME_BETWEEN_ITERATIONS) #sec

#uses significance to determine whether or not to buy.
def strategy3():
    lookback = 100
    print("Running Strategy 3.")
    scpr = JScraper(browser_type="chrome",browser_driverpath="./browserdrivers/chromedriver")
    p = Portfolio("portfolio_strat3.pf")
    myportfolio = p.getPortfolio()
    while True:
        # try to intelligently buy
        for curr in myportfolio:
            meds = scpr.retrieveMedians(curr=curr, max=lookback)
            if len(meds) < lookback:
                continue #Do nothing until 
            curr_median = meds[0]
            deviation_of_median = 0
            variance_of_median = 0
            mean_of_median = 0
            for m in meds:
                mean_of_median = mean_of_median + m
            mean_of_median = mean_of_median / len(meds)
            for m in meds:
                variance_of_median = variance_of_median + math.pow((m - mean_of_median),2)
            variance_of_median = variance_of_median / len(meds)
            deviation_of_median = math.sqrt(variance_of_median)
            zscore_of_median = (curr_median - mean_of_median) / deviation_of_median #number of std dev's away
            print(str(curr) + ": MOst recent median: " + str(curr_median) + "  mean of median: " + str(mean_of_median) + "  z-score: " + str(zscore_of_median))

            MAX_PERCENT_ALLOWANCE = .10
            if(zscore_of_median < -0.75): #Buying when price is in 0-22nd percentile
                purchase_amt = MAX_PERCENT_ALLOWANCE * p.getCashpool()
                purchase_price = curr_median
                shares = purchase_amt / purchase_price
                p.purchase(curr, shares)
                print("Buying " + str(shares) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(shares * purchase_price) + ").")
            elif(zscore_of_median > 0.3):
                share_ct = p.amount(curr) #Selling when price is in 62-100th percentile
                if not(share_ct == -1 or share_ct <= 0.0):
                    sell_ct = MAX_PERCENT_ALLOWANCE * share_ct
                    purchase_price = curr_median
                    p.sell(curr, sell_ct)
                    print("Selling " + str(sell_ct) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(sell_ct * purchase_price) + ").")
            else: #if price isnt significant, do nothing
                pass

        print(p)
        print("Total worth: " + str(p.getWorth()) + ".\n")
        time.sleep(TIME_BETWEEN_ITERATIONS) #sec

#using the portfolio trade history to influence trades
def strategy4():
    lookback = 75
    print("Running Strategy 4.")
    scpr = JScraper(browser_type="chrome",browser_driverpath="./browserdrivers/chromedriver")
    p = Portfolio("portfolio_strat4.pf")
    myportfolio = p.getPortfolio()
    while True:
        history = p.getTradeHistory()
        for curr in myportfolio: #do it this way because user has control over portfolio contents, not history
            if curr in history:
                curr_history = history[curr]
                curr_medians = scpr.retrieveMedians(curr=curr, max=lookback)

                #TODO: implement some trading method using the history and medians here

                print(curr_history)
                print(curr_medians)
                print("\n\n")
            

        print(p)
        print("Total worth: " + str(p.getWorth()) + ".\n")
        time.sleep(TIME_BETWEEN_ITERATIONS) #sec

# trying to use the vectorspace things to guide what i choose
def strategy5():
    API_ENDPOINT = "https://vectorspace.ai/recommend/app/correlated_cryptos"
    data = {"query" : "machine+learning&vxv_token_addr=0xC2A568489BF6AAC5907fa69f8FD4A9c04323081D"}
    r = requests.post(url = API_ENDPOINT, data = data)
    rec = json.loads(r.text)
    for cc in rec:
        print("Vectorspace recommended " + str(cc['sym']))
        



#### MAIN METHOD ####
#since a lot of these methods will be created dont
#use multithreading just run the program a bunch of times
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "scrape":
            dataScavenger()
        elif sys.argv[1] == "graphs":
            dataScavenger(rendergraphs=True)
        elif sys.argv[1] == "constscrape":
            dataScavenger(delay=1)
        elif sys.argv[1] == "one":
            strategy1()
        elif sys.argv[1] == "two":
            strategy2()
        elif sys.argv[1] == "three":
            strategy3()
        elif sys.argv[1] == "four":
            strategy4()
        elif sys.argv[1] == "five":
            strategy4()
        else: 
            dataScavenger()
    else: 
        dataScavenger()