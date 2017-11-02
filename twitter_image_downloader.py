#!/usr/bin/env python3
# encoding: utf-8
"""
Download the images from these tweets
Usage: python twitter_image_downloader.py tweet1 [tweet2 [tweet3]]
"""
from __future__ import print_function, unicode_literals
from sys import platform as _platform

import argparse
import doctest
import os
import twitter  # pip install twitter
import yaml     # pip install pyyaml

# from pprint import pprint

TWITTER = None


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def yaml_path(unixpath, winpath, yaml):
    if not yaml.endswith(".yaml"):
        yaml += ".yaml"
    if _platform == "win32":
        return os.path.join(winpath, yaml)
    else:
        return os.path.join(unixpath, yaml)


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


def id_from_tweet_url(url):
    """
    >>> # macOS
    >>> url = "https://twitter.com/hugovk/status/771714518724579328"
    >>> id_from_tweet_url(url)
    771714518724579328
    """
    return int(url[url.rfind("/")+1:])


def download_tweets_images(tweets):
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

    usernames = set()
    urls = []
    for tweet in tweets:
        print(tweet)
        tweet_id = id_from_tweet_url(tweet)
        tweet = TWITTER.statuses.show(_id=tweet_id, include_entities=True)
        # pprint(tweet)
        username = tweet['user']['screen_name']
        print(username)
        try:
            media = tweet['extended_entities']['media']
            # pprint(media)
            for item in media:
                url = item['media_url_https'] + ":large"
                outfile = "{}-{}-{}.jpg".format(username, tweet_id, item['id'])
                print(url, outfile)
                urls.append(url)
                cmd = "wget --no-verbose -nc {} -O {}".format(url, outfile)
                print(cmd)
                os.system(cmd)
            usernames.add(username)
        except KeyError:
            continue

    credits = " ".join(["@{}".format(u) for u in usernames])
    print(credits)
    os.system('echo "{}" >> credits.txt'.format("\n".join(tweets)))
    os.system('echo "{}" >> credits.txt'.format(credits))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download the images from these tweets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'tweets',
        nargs='+',
        help="The tweets to like")
    parser.add_argument(
        '-u', '--unixpath',
        default='/Users/hugo/Dropbox/bin/data/',
        help="Unixy (Linux/Mac) root path to YAML file.")
    parser.add_argument(
        '-w', '--winpath',
        default='M:/bin/data/',
        help="Windows root path to YAML file.")
    parser.add_argument(
        '-y', '--yaml',
        default='kaikkisanat.yaml',
        help="YAML file location containing Twitter keys and secrets "
             "for the account to do the liking. Needs write permission.")
    parser.add_argument(
        '--html', action='store_true',
        help="HTML tags for formatting")
    args = parser.parse_args()
    doctest.testmod()

    path = yaml_path(args.unixpath, args.winpath, args.yaml)
    data = load_yaml(path)

    download_tweets_images(args.tweets)

# End of file
