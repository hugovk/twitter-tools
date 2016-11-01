#!/usr/bin/env python
# encoding: utf-8
"""
Find the best tweets from last month, by faves and RTs
"""
from __future__ import print_function, unicode_literals
from dateutil.relativedelta import relativedelta

import argparse
import datetime
import time
import twitter
import yaml

# from pprint import pprint

TWITTER = None


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    AND (
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
        OR
    oauth_token: TODO_ENTER_YOURS
    oauth_token_secret: TODO_ENTER_YOURS
    )
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()

    return data


def get_user_timeline(username, max_id=None):
    got_them = False
    while not got_them:
        # Get another batch
        try:
            if max_id:
                user_timeline = TWITTER.statuses.user_timeline(
                    screen_name=username, count=200, trim_user=True,
                    max_id=max_id)
            else:
                user_timeline = TWITTER.statuses.user_timeline(
                    screen_name=username, count=200, trim_user=True)
            got_them = True
        except twitter.api.TwitterHTTPError as e:
            # Rate limit? Try again soon.
            print("*"*80)
            print(e)
            print("*"*80)
            print("Sleep for just over a minute")
            time.sleep(61)
    print(len(user_timeline))
    return user_timeline


def best_tweets(username):
    global TWITTER
    if TWITTER is None:
        try:
            access_token = data['access_token']
            access_token_secret = data['access_token_secret']
        except KeyError:  # Older YAMLs
            access_token = data['oauth_token']
            access_token_secret = data['oauth_token_secret']
        TWITTER = twitter.Twitter(auth=twitter.OAuth(
            access_token,
            access_token_secret,
            data['consumer_key'],
            data['consumer_secret']))

    today = datetime.date.today()
    first_of_this_month = today.replace(day=1)
    print(first_of_this_month)
    last_of_last_month = first_of_this_month - datetime.timedelta(days=1)
    print(last_of_last_month)

    first_of_last_month = first_of_this_month - relativedelta(months=1)
    print(first_of_last_month)

    # Get the first batch
    max_id = None
    user_timeline = get_user_timeline(username)

    max_id = None
    get_more = True
    tweets = []

    # Find the tweets from last month
    while get_more:

        # Go through each batch
        for tweet in user_timeline:
            created_at = tweet['created_at']

            # Convert Twitter timestamp to Python datetime
            created_at = datetime.datetime.strptime(
                created_at, '%a %b %d %H:%M:%S +0000 %Y')

            # Convert to datetime
            created_at = created_at.date()

            # Keep track of last tweet
            max_id = tweet['id']

            if first_of_last_month <= created_at <= last_of_last_month:
                # print(str(created_at) + "*")
                tweet['fav_rt_count'] = (tweet['favorite_count'] +
                                         tweet['retweet_count'])

                tweets.append(tweet)

            elif created_at < first_of_last_month:
                # print(str(created_at) + "x")
                # Don't need any more batches
                get_more = False

            # else:
                # print(created_at)

        print("Kept", len(tweets), "tweets")

        if get_more:
            user_timeline = get_user_timeline(username, max_id)

    # Sort the found tweets by fav_rt_count
    best_tweet_list = sorted(tweets, key=lambda k: k['fav_rt_count'],
                             reverse=True)

    # # Only list enough that'll fit in a single tweet
    # count = 0

    # Print with details
    for tweet in best_tweet_list[:25]:

        # count += len(tweet['text']) + 1
        # if count > 140:
            # break

        print_it(str(tweet['fav_rt_count']) + " " +
                 str(tweet['favorite_count']) + " " +
                 str(tweet['retweet_count']) + "\t" +
                 "https://twitter.com/" + username + "/status/" +
                 tweet['id_str'] + "\t" + tweet['text'])

    # # Reset
    # count = 0

    # Print just statuses
    print("Popular tweets by @kaikkisanat in " +
          first_of_last_month.strftime("%B") + ":")
    for tweet in best_tweet_list[:25]:

        # count += len(tweet['text'])
        # if count > 140:
            # break

        print_it(tweet['text'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the best tweets from last month, by faves and RTs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-u', '--user',
        default='kaikkisanat',
        help="The Twitter account to check")
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/cookerybot.yaml',
        help="YAML file location containing Twitter keys and secrets. "
              "Just for read-only access, doesn't post to Twitter.")
    args = parser.parse_args()

    data = load_yaml(args.yaml)

    best_tweets(args.user)

# End of file
