# API for twitter
# Authors: Maciej Szuilk, Mariusz Wisniewski

import tweepy
import json
import os
import datetime
from textblob import TextBlob
import numpy as np
import csv
import collections


consumer_key = 'XWoLg0xPqVv89ngEBdCa7I6lj'
consumer_secret = '8bDefO95U1TzRc3i3kjLLeDQmr0SkJ4zDE0bAa4OsfzAkPNSIH'
access_token = '1056429787-Y0WK0EQwPpdwMKzACw2GVS7syOzto6z5S4BvSM2'
access_token_secret = 'Jiy5l7XUR8hFsz0z4NauggNuXUorLWYteezAGJYQP3g1D'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
file_name = "tweets.json"
results_dir = "./"

'''def download_tweets(query, start_date="2019-09-03", end_date="2019-09-04", tweet_count=5):
    # tweets = {'date': [], 'text': [], 'screen_name': [], 'followers_count': []}
    tweets = []
    for tweet in tweepy.Cursor(api.search,q=query,lang="en",since=start_date,until=end_date,tweet_mode='extended').items():
        tweets.append(tweet._json)
    with open(os.path.join(results_dir, file_name), "w") as tweets_file:
       json.dump(tweets, tweets_file, indent=4)'''

def count_valuable_data(tweets):
    valuable_data = []

    dates = [tweet.get("date") for tweet in tweets]
    from collections import Counter

    cnt = Counter()
    for date in dates:
        cnt[date] += 1

    output = collections.OrderedDict()
    for tweet in tweets:
        tweet.get("date")
        if tweet["date"] in output.keys():
            output[tweet["date"]]["daily_tweets"] += 1
            if tweet["sentiment"] > 0:
                output[tweet["date"]]["pos_sent"] += 1
                output[tweet["date"]]["pos_retweets"] += tweet["retweets"]
                output[tweet["date"]]["pos_favourites"] += tweet["favourites"]
            elif tweet["sentiment"] < 0:
                output[tweet["date"]]["neg_sent"] += 1
                output[tweet["date"]]["neg_retweets"] += tweet["retweets"]
                output[tweet["date"]]["neg_favourites"] += tweet["favourites"]
        else:
            output[tweet["date"]] = dict()
            output[tweet["date"]]["pos_sent"] = 0
            output[tweet["date"]]["neg_sent"] = 0
            output[tweet["date"]]["neg_retweets"] = 0
            output[tweet["date"]]["neg_favourites"] = 0
            output[tweet["date"]]["neg_retweets"] = 0
            output[tweet["date"]]["neg_favourites"] = 0
            output[tweet["date"]]["daily_tweets"] = 1
            if tweet["sentiment"] > 0:
                output[tweet["date"]]["pos_sent"] += 1
                output[tweet["date"]]["pos_retweets"] += tweet["retweets"]
                output[tweet["date"]]["pos_favourites"] += tweet["favourites"]
            elif tweet["sentiment"] < 0:
                output[tweet["date"]]["neg_sent"] += 1
                output[tweet["date"]]["neg_retweets"] += tweet["retweets"]
                output[tweet["date"]]["neg_favourites"] += tweet["favourites"]
                
    print(output)
    daily_tweets_list = [day.get("daily_tweets") for day in output.values()]
    print(daily_tweets_list)
    max_daily = max(daily_tweets_list)

    csv_list = [] # data, p1, p2, p3, p4 (data, daily_tweets, p2 ok,  )
    for key, value in output.items():
        data = []
        data.append(key)
        data.append(value['daily_tweets'])
        total_sent = value['pos_sent'] + value['neg_sent'] 
        data.append(np.round(value['pos_sent']/total_sent, 5))
        data.append(np.round(value['neg_sent']/total_sent, 5))
        # ((2*retweets+likes)pos - (2*retweets+likes)neg)/((2*retweets+likes)pos + (2*retweets+likes)neg)
        data.append((2*value["pos_retweets"]+value["pos_favourites"] - 2*value["neg_retweets"]+value["neg_favourites"])
            /(2*value["pos_retweets"]+value["pos_favourites"] + 2*value["neg_retweets"]+value["neg_favourites"]))
        csv_list.append(data)
        
    with open('data.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["date", "p1", "p2", "p3", "p4"])
        wr.writerows(csv_list)


def execute_sentimentation(tweets):
    for tweet in tweets:
        tweet["sentiment"] = TextBlob(tweet["full_text"]).polarity

'''def parse_timestamp(tweets):
    for tweet in tweets:
        tweet["date"] = str(datetime.datetime.strptime(tweet["date"], '%a %b %d %X +0000 %Y').date())'''

        
def main():
    with open("tweets_converted.json", "r") as tweets_file:
        tweets = json.load(tweets_file)
    
    execute_sentimentation(tweets)
    count_valuable_data(tweets)


if __name__ == "__main__":
    main()
