# @author Jake Runyan
# @desc A bot made from a JScraper and Portfolio

from JScraper import JScraper 
from Portfolio import Portfolio

if __name__ == "__main__":
    scpr = JScraper()
    p = Portfolio("portfolio.pf")

    #scrapes up until a critical pt (num of entries in database >= 200)
    #trades away currency if it has appreciated in value relative to average of medians
    #buys currency that is lower than average of medians
    #issues is that money will get locked up in bad investments
    #   TODO: ^ fix that
    while True:
        scpr.scrape()
        for currency in p.
        lows = scpr.retrieveLows()