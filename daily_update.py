# Authors: Mariusz Wisniewski, Kinga Marek
import sys, getopt, datetime, codecs, pyquery
import GetOldTweets3 as got
from datetime import datetime, timedelta
import argparse
# to execute try: python daily_update.py --querysearch '#Intel' --output 'today.csv' 
def main(argv):
	if len(argv) == 0:
		print('You must pass some parameters. Use "-h" to help.')
		return

	if len(argv) == 1 and argv[0] == "-h":
		f = open("exporter_help_text.txt", "r")
		print(f.read())
		f.close()

		return


	tweetCriteria = got.manager.TweetCriteria()
	outputFileName = "output_got.csv"
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--querysearch",
		dest="querysearch",
		help="Type in your query key",
	)
	parser.add_argument(
		"--output",
		dest="output",
		help="Output data to the specified csv file",
	)
	args = parser.parse_args()

	if args.querysearch != None:
		tweetCriteria.querySearch = args.querysearch

	if args.output != None:
		outputFileName = args.output

	outputFile = codecs.open(outputFileName, "w+", "utf-8")

	outputFile.write(
		"username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink"
	)

	def receiveBuffer(tweets):
		for t in tweets:
			outputFile.write(
				(
					'\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s'
					% (
						t.username,
						t.date.strftime("%Y-%m-%d %H:%M"),
						t.retweets,
						t.favorites,
						t.text,
						t.geo,
						t.mentions,
						t.hashtags,
						t.id,
						t.permalink,
					)
				)
			)
		outputFile.flush()
		print("Next %d tweets saved in the file...\n" % len(tweets))

	yesterday = str((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"))
	tweetCriteria.since = yesterday
	tweetCriteria.until = str(datetime.today().strftime("%Y-%m-%d"))
	got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	outputFile.close()
	print('Done. Output file generated "%s".' % outputFileName)


if __name__ == "__main__":
	main(sys.argv[1:])
