#!/usr/bin/env python
# encoding: utf-8
"""
Like these tweets
Usage: python like_tweets.py tweet1 [tweet2 [tweet3]]
"""
from __future__ import print_function, unicode_literals
from sys import platform as _platform

import argparse
import doctest
import os
import twitter
import yaml

# from pprint import pprint

TWITTER = None


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode("utf-8"))


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
    with open(filename) as f:
        data = yaml.safe_load(f)

    return data


def id_from_tweet_url(url):
    """
    >>> url = "https://twitter.com/hugovk/status/771714518724579328"
    >>> id_from_tweet_url(url)
    771714518724579328L
    """
    return int(url[url.rfind("/") + 1 :])


def like_tweets(tweets):
    global TWITTER
    if TWITTER is None:
        try:
            access_token = data["access_token"]
            access_token_secret = data["access_token_secret"]
        except KeyError:  # Older YAMLs
            access_token = data["oauth_token"]
            access_token_secret = data["oauth_token_secret"]
        TWITTER = twitter.Twitter(
            auth=twitter.OAuth(
                access_token,
                access_token_secret,
                data["consumer_key"],
                data["consumer_secret"],
            )
        )

    for tweet in tweets:
        print(tweet)
        TWITTER.favorites.create(_id=id_from_tweet_url(tweet))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Like these tweets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("tweets", nargs="+", help="The tweets to like")
    parser.add_argument(
        "-u",
        "--unixpath",
        default="/Users/hugo/Dropbox/bin/data/",
        help="Unixy (Linux/Mac) root path to YAML file.",
    )
    parser.add_argument(
        "-w",
        "--winpath",
        default="M:/bin/data/",
        help="Windows root path to YAML file.",
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="kaikkisanat.yaml",
        help="YAML file location containing Twitter keys and secrets "
        "for the account to do the liking. Needs write permission.",
    )
    parser.add_argument("--html", action="store_true", help="HTML tags for formatting")
    args = parser.parse_args()
    doctest.testmod()

    path = yaml_path(args.unixpath, args.winpath, args.yaml)
    data = load_yaml(path)

    like_tweets(args.tweets)

# End of file
