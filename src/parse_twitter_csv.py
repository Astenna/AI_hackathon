import csv
import json


def read_twitter_csv(csv_path="datasets/training/support/output_got_bigger.csv"):
    with open(csv_path) as csv_file:
        csvReader = csv.DictReader(
            csv_file,
            delimiter=";",
            fieldnames=(
                "username",
                "date",
                "retweets",
                "favorites",
                "text",
                "geo",
                "mentions",
                "hashtags",
                "id",
                "permalink",
            ),
        )
        next(csv_file)  # Skip headers
        out = [row for row in csvReader]

    # write the data to the json file
    with open("datasets/training/support/twitter_converted.json", "w") as jsonFile:
        json.dump(out, jsonFile, indent=4)


if __name__ == "__main__":
    read_twitter_csv()
