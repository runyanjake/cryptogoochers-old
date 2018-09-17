# @author Jake Runyan
# @desc A bot made from a JScraper and Portfolio

from JScraper import JScraper 
from Portfolio import Portfolio
import time

TIME_BETWEEN_ITERATIONS = 900 #15min

#buys cryptocurrencies whose last median was greater than the average of the last LOOKBACK_LENGTH medians
LOOKBACK_LENGTH = 10
def strategy1():
    print("Running Strategy 1.")
    scpr = JScraper()
    p = Portfolio("portfolio_strat1.pf")
    #scrapes up until a critical pt (num of entries in database >= 200)
    #trades away currency if it has appreciated in value relative to average of medians
    #buys currency that is lower than average of medians
    #issues is that money will get locked up in bad investments
    #   TODO: ^ fix that
    myportfolio = p.getPortfolio()
    while True:
        # do scraping
        data = scpr.scrape()
        scpr.recordData(data)
        # try to intelligently buy
        for curr in myportfolio:
            meds = scpr.retrieveMedians(curr=curr, max=LOOKBACK_LENGTH)
            if len(meds) < 10:
                continue #Do nothing until 
            curr_median = meds[0]
            mean_of_median = 0
            itor = 0
            for m in meds:
                if itor > LOOKBACK_LENGTH:
                    break
                else:
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
    scpr = JScraper()
    p = Portfolio("portfolio_strat2.pf")
    myportfolio = p.getPortfolio()
    while True:
        # do scraping
        data = scpr.scrape()
        scpr.recordData(data)
        # try to intelligently buy
        for curr in myportfolio:
            meds = scpr.retrieveMedians(curr=curr, max=LOOKBACK_LENGTH)
            if len(meds) < 10:
                continue #Do nothing until 
            curr_median = meds[0]
            mean_of_median = 0
            itor = 0
            for m in meds:
                if itor > LOOKBACK_LENGTH:
                    break
                else:
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
    #TODO

# trying to use the vectorspace things to guide what i choose
def strategy4():
    import requests
    import json
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
    strategy1()