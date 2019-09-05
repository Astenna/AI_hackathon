import json
import csv


def merge_data_files(twitter_file, stock_file, output_file):
    all_data = []

    # Load twitter trainig dataset
    with open(twitter_file, "r") as json_file:
        twitter_dict = json.load(json_file)

    # max_tweets = max([tweet[0] for tweet in twitter_dict.values()])  # Adam don't want
    max_tweets = 225  # Magic number special for Adam <3

    # Load stock trainig dataset
    with open(stock_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip row with headers
        for stock_row in reader:
            date = stock_row[1]
            twitter_row = twitter_dict.get(date, [0 for x in range(4)])
            # Append only if twitter_row for this date is not empty
            if twitter_row:
                twitter_row[0] /= max_tweets  # Also special for Adam
                all_data_row = [date] + twitter_row + stock_row[2:]
                all_data.append(all_data_row)

    # Save merged dataset to the file
    with open(output_file, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(all_data)


if __name__ == "__main__":
    merge_data_files(
        twitter_file="datasets/training/support/training_twitter.json",
        stock_file="datasets/training/support/stock_data_04-09-2019.csv",
        output_file="datasets/training/prepared/training_data.csv",
    )
