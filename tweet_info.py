#!/usr/bin/env python3
"""
Get some info about a single tweet.
Usage for CLI: python tweet_info.py
"""
import argparse
import os

# from pprint import pprint
from sys import platform as _platform

import twitter
import yaml

TWITTER = None


def id_from_url(url):
    """Given https://twitter.com/WeirdSatellite/status/1464653049910153217
    return 1464653049910153217"""
    return url.rsplit("/", 1)[-1]


def yaml_path(unixpath, winpath, yaml):
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


def tweet_info(url):
    # Assumes a single URL or ID, not a list
    id = id_from_url(url)

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
    tweet = TWITTER.statuses.show(id=id)
    # pprint(tweet)
    print(tweet["user"]["screen_name"])
    print(tweet["id"])
    print(tweet["text"])
    print(tweet["created_at"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get some info about a single tweet.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("tweet", help="The tweet URL to check")
    parser.add_argument(
        "-u",
        "--unixpath",
        default="/Users/hugo/Dropbox/",
        help="Unixy (Linux/Mac) root path to YAML file.",
    )
    parser.add_argument(
        "-w", "--winpath", default="M:/", help="Windows root path to YAML file."
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="bin/data/bewithyoubot.yaml",
        help="YAML file location containing Twitter keys and secrets. "
        "Just for read-only access, doesn't post to Twitter.",
    )
    args = parser.parse_args()

    path = yaml_path(args.unixpath, args.winpath, args.yaml)
    data = load_yaml(path)

    tweet_info(args.tweet)

# End of file
