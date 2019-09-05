import json
import csv


def merge_data_files(twitter_file, stock_file, output_file):
    all_data = []

    # Load twitter trainig dataset
    with open(twitter_file, "r") as json_file:
        twitter_dict = json.load(json_file)

    max_tweets = max([tweet[0] for tweet in twitter_dict.values()])  # Adam don't want
    max_dict = {"max_tweets": max_tweets}
    # max_tweets = 225  # Magic number special for Adam <3

    # Load stock trainig dataset
    with open(stock_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        # next(reader)  # Skip row with headers
        for stock_row in reader:
            date = stock_row[0]
            twitter_row = twitter_dict.get(date, [0 for x in range(4)])
            # Append only if twitter_row for this date is not empty
            if twitter_row:
                twitter_row[0] /= max_tweets  # Also special for Adam
                all_data_row = [date] + twitter_row + stock_row[1:]
                all_data.append(all_data_row)

    # Save merged dataset to the file
    with open(output_file, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(all_data)

    with open("datasets/training/support/max_tweet.json", 'w') as json_file:
        json.dump(max_dict, json_file, indent=4)


if __name__ == "__main__":
    merge_data_files(
        twitter_file="datasets/inference/support/tweets_to_merge.json",
        stock_file="datasets/inference/support/stock.csv",
        output_file="datasets/inference/prepared/training_data.csv",
    )
