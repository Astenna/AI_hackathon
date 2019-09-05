# API for twitter
# Authors: Kinga Marek, Mariusz Wisniewski

import json
import os
import sys
import datetime
from textblob import TextBlob
import numpy as np
import csv
import collections
import argparse

input_file_name = "./datasets/training/support/twitter_converted.json"
output_file_name = "./datasets/training/support/tweets_summary.json"

def count_valuable_data(tweets):

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
                output[tweet["date"]]["pos_retweets"] = int(tweet["retweets"]) + int(
                    output[tweet["date"]]["pos_retweets"]
                )
                output[tweet["date"]]["pos_favorites"] = int(tweet["favorites"]) + int(
                    output[tweet["date"]]["pos_favorites"]
                )
            elif tweet["sentiment"] < 0:
                output[tweet["date"]]["neg_sent"] += 1
                output[tweet["date"]]["neg_retweets"] = int(tweet["retweets"]) + int(
                    output[tweet["date"]]["neg_retweets"]
                )
                output[tweet["date"]]["neg_favorites"] = int(tweet["favorites"]) + int(
                    output[tweet["date"]]["neg_favorites"]
                )
        else:
            output[tweet["date"]] = dict()
            output[tweet["date"]]["pos_sent"] = 0
            output[tweet["date"]]["neg_sent"] = 0
            output[tweet["date"]]["neg_retweets"] = 0
            output[tweet["date"]]["neg_favorites"] = 0
            output[tweet["date"]]["pos_retweets"] = 0
            output[tweet["date"]]["pos_favorites"] = 0
            output[tweet["date"]]["daily_tweets"] = 1
            if tweet["sentiment"] > 0:
                output[tweet["date"]]["pos_sent"] += 1
                output[tweet["date"]]["pos_retweets"] = int(tweet["retweets"]) + int(
                    output[tweet["date"]]["pos_retweets"]
                )
                output[tweet["date"]]["pos_favorites"] = int(tweet["favorites"]) + int(
                    output[tweet["date"]]["pos_favorites"]
                )
            elif tweet["sentiment"] < 0:
                output[tweet["date"]]["neg_sent"] += 1
                output[tweet["date"]]["neg_retweets"] = int(tweet["retweets"]) + int(
                    output[tweet["date"]]["neg_retweets"]
                )
                output[tweet["date"]]["neg_favorites"] = int(tweet["favorites"]) + int(
                    output[tweet["date"]]["neg_favorites"]
                )

    print(output)
    daily_tweets_list = [day.get("daily_tweets") for day in output.values()]
    print(daily_tweets_list)
    max_daily = max(daily_tweets_list)
    print("MAX")
    print(max_daily)

    csv_list = []  # data, p1, p2, p3, p4 (data, daily_tweets, p2 ok,  )
    twitter_dict = dict()
    for key, value in output.items():
        data = []
        # data.append(key)
        data.append(value["daily_tweets"])
        total_sent = value["pos_sent"] + value["neg_sent"]
        data.append(np.round(value["pos_sent"] / total_sent, 5))
        data.append(np.round(value["neg_sent"] / total_sent, 5))
        # ((2*retweets+likes)pos - (2*retweets+likes)neg)/((2*retweets+likes)pos + (2*retweets+likes)neg)
        data.append(
            (
                2 * value["pos_retweets"]
                + value["pos_favorites"]
                - 2 * value["neg_retweets"]
                + value["neg_favorites"]
            )
            / (
                2 * value["pos_retweets"]
                + value["pos_favorites"]
                + 2 * value["neg_retweets"]
                + value["neg_favorites"]
            )
        )
        twitter_dict[key] = data
        csv_list.append(data)

    # with open("data.csv", "w", newline="") as myfile:
    #     wr = csv.writer(myfile)
    #     wr.writerow(["date", "p1", "p2", "p3", "p4"])
    #     wr.writerows(csv_list)

    with open(output_file_name, 'w') as json_file:
        json.dump(twitter_dict, json_file, indent=4)


def execute_sentimentation(tweets):
    for tweet in tweets:
        tweet["sentiment"] = TextBlob(tweet["text"]).polarity


def parse_timestamp(tweets):
    for tweet in tweets:
        tweet["date"] = tweet["date"].split(" ")[0]
        # tweet["date"] = str(datetime.datetime.strptime(tweet["date"], '%a %b %d %X +0000 %Y').date())

def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        dest="input",
        help="Input data from the specified json file",
    )
    parser.add_argument(
        "--output",
        dest="output",
        help="Ouput data to the specified json file",
    )
    args = parser.parse_args()
    
    if args.output != None:
        output_file_name = args.output

    if args.input != None:
        # if os.path.exists(os.path.joinargs.input):
        #     raise OSError("Input file not found!")
        input_file_name = args.input

def main():
    
    parse_command_line_args()   

    with open(input_file_name, "r") as tweets_file:
        tweets = json.load(tweets_file)

    parse_timestamp(tweets)
    execute_sentimentation(tweets)
    count_valuable_data(tweets)

if __name__ == "__main__": 

    main()
