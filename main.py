import tweepy
import re
import pymongo
from pymongo import MongoClient

api_key = "6INs83tvX75u1CuRvNKqhmR3L"
api_secret_key = "TSOL5EyfFrUwFGHhrKos3IFyOLYspOfV8iNpnFKuzRkPzLuUyr"
access_token = "1226568217147002880-5z9utuAc0OyfmM3yFGaksZVQiPTF7X"
access_token_secret = "cnsPtRZjLhn54OmMsaZGSCY952qww835aQ4uQ2nf0Qeoq"

auth = tweepy.OAuthHandler(api_key,api_secret_key)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)
maxTweets = 200
tweetCount = 0
maxId = -1

while tweetCount < maxTweets:
    if (maxId <= 0):
        hasilSearch = api.search(q="omnibus law -filter:retweets",lang="en",count=100, tweet_mode="extended")
    else:
        hasilSearch = api.search(q="omnibus law -filter:retweets",lang="en", max_id=str(maxId - 1), count=100, tweet_mode="extended")

    if not hasilSearch:
        print("Tweet Habis")
        break

    count = 0
    for tweet in hasilSearch:
        count += 1
        tweet_properties = {}
        tweet_properties["id"] = tweet.id
        tweet_properties["tanggal_tweet"] = tweet.created_at
        tweet_properties["user"] = tweet.user.screen_name
        tweet_properties["tweet"] = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet.full_text).split())
        print(count,tweet_properties)

        client = MongoClient()
        db = client.tbd_tweet
        collection = db.tweet_collection
        collection.create_index([("id", pymongo.ASCENDING)], unique=True)
        collection.insert(tweet_properties)

    tweetCount += len(hasilSearch)
    maxId = hasilSearch[-1].id