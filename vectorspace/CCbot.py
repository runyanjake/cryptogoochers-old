# @author Jake Runyan
# @desc A bot made from a JScraper and Portfolio

from JScraper import JScraper 
from Portfolio import Portfolio
import time

TIME_BETWEEN_ITERATIONS = 900 #15min

if __name__ == "__main__":
    scpr = JScraper()
    p = Portfolio("portfolio.pf")

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
            lows = scpr.retrieveLows(curr=curr, max=200)
            # if len(lows) < 200:
            #     continue #Do nothing until 
            curr_median = lows[0]
            mean_of_median = 0
            for l in lows:
                mean_of_median = mean_of_median + l
            mean_of_median = mean_of_median / len(lows)
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
                    sell_ct = MAX_PERCENT_ALLOWANCE * p.share_ct
                    purchase_price = curr_median
                    p.sell(curr, sell_ct)
                    print("Selling " + str(sell_ct) + " of " + str(curr) + " at " + str(curr_median) + "(Total price " + str(sell_ct * purchase_price) + ").")
            else: #if price constant, do nothing
                pass

        print(p)
        print("Total worth: " + str(p.getWorth()))
        time.sleep(TIME_BETWEEN_ITERATIONS) #sec