# API for twitter
# Authors: Maciej Szuilk, Mariusz Wisniewski

import tweepy

consumer_key = 'XWoLg0xPqVv89ngEBdCa7I6lj'
consumer_secret = '8bDefO95U1TzRc3i3kjLLeDQmr0SkJ4zDE0bAa4OsfzAkPNSIH'
access_token = '1056429787-Y0WK0EQwPpdwMKzACw2GVS7syOzto6z5S4BvSM2'
access_token_secret = 'Jiy5l7XUR8hFsz0z4NauggNuXUorLWYteezAGJYQP3g1D'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def grab_tweets(query, start_date="2019-09-03", end_date="2019-09-04", tweet_count=10):
    tweets = {'date': [], 'text': [], 'screen_name': [], 'followers_count': []}
    for index,tweet in enumerate(tweepy.Cursor(api.search,q=query,lang="en",since=start_date,until=end_date,tweet_mode='extended').items(tweet_count)):
        tweets['date'].append(tweet.created_at)
        tweets['text'].append(tweet.full_text)
        tweets['screen_name'].append(tweet.user.screen_name)
        tweets['followers_count'].append(count_followers(tweets, index))
    return tweets

def count_max_tweets(query, start_date="2019-09-03", end_date="2019-09-04"):
    num_of_tweets = 0
    for tweet in tweepy.Cursor(api.search,q=query,since=start_date,until=end_date).items():
        num_of_tweets += 1

    return num_of_tweets

def count_followers(tweets, idx):
    user = api.get_user(screen_name=tweets['screen_name'][idx])
    return user.followers_count

def main():
    tweets = grab_tweets('#Intel', "2019-09-01", "2019-09-04", 2)
    num_of_tweets = count_max_tweets('#Intel', "2019-09-01", "2019-09-04")
    print(tweets.items())
    print(num_of_tweets)

if __name__ == "__main__":
    main()
