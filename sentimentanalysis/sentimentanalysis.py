# @author Jake Runyan
# sentimentanalysis.py
# Following along with sentdex's twitter sentiment analysis tutorial on youtube.

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s

#consumer key, consumer secret, access token, access secret.
ckey="WsN6anOVvQaaUOSVQ0aDMimUj"
csecret="5Wx6R4OZRQh1rNzyq8FePXiO0Uo9yuz0fggGJqMnqxK4ibI0Ip"
atoken="1025266565619445760-IA52p8ZOqx2DHxydyXCYMkL4gmtEsn"
asecret="TPNzK9xgUjUQkpUWk9aFRJ3xx8z8XyXenUxLJJfWI7K2L"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]

        sentiment_value, confidence = s.sentiment(tweet)

        print(tweet, sentiment_value, confidence)

        if confidence*100 >= 80:
            output = open("twitterout.txt", "a")
            output.write(sentiment_value + tweet)
            output.write("\n")
            output.close()
        
        return True

    def on_error(self, status):
        print (status)

#Main execution

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["google"])