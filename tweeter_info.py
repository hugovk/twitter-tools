#!/usr/bin/env python3
# encoding: utf-8
"""
Get some info about a Twitter user, like clients used.
Usage for CLI: python tweeter_info.py
Usage for web: python tweeter_info.py --html > tweeter_info.html
"""
from sys import platform as _platform

import argparse
import calendar
import os
import re
import time
import twitter
import yaml

# from pprint import pprint

TWITTER = None


def username_from_url(url):
    """ Given https://twitter.com/gutendelight, return gutendelight """
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


def commafy(number):
    """ Given an int, return a string with thousands separators """
    return f"{number:,}"


def summarise_tweet_clients(tweets):
    sources = {}
    for tweet in tweets:
        try:
            sources[tweet["source"]] += 1
        except KeyError:
            sources[tweet["source"]] = 1
    return sources


def get_tweets(username):
    global TWITTER
    tweets = TWITTER.statuses.user_timeline(screen_name=username, count=100)
    return tweets


def taggy(text, class_name):
    """Wrap in HTML tags"""
    if args.html:
        return f'<span class="{class_name}">{text}</span>'
    else:
        return text


def strip_tags(text):
    """Strip HTML tags"""
    return re.sub("<[^<]+?>", "", text)


def tweeter_info(username):

    # Assumes a single username, not a list
    username = username_from_url(username)

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

    users = [TWITTER.users.show(screen_name=",".join([username]))]  # TODO fix

    if args.html:
        print(
            """
<html>
  <head>
  <title>Tweeter info</title>
  <style type="text/css">
  body {
    background-color: lightsteelblue;
    font-family: sans-serif;
  }
  .danger,
  .danger a:link,
  .danger a:visited {
    color: red;
    font-weight: bold;
  }
  .warning,
  .warning a:link,
  .warning a:visited {
    color: orange;
    font-weight: bold;
  }
  li.user {
    background-color: white;
    border: 1px solid #000;
    display: inline-block;
    margin: 5px;
    min-height: 250px;
    padding: 5px;
    vertical-align: top;
    width: 240px;
  }
  .tweet div {
    padding-bottom: 10px;
  }
  .screen_name {
    text-align: center;
  }
  .status {
    word-break: break-word;
  }
  .stats {
    font-size: smaller;
  }
  .stats span {
    display: block;
  }
  </style>
</head>
<body>
  <ol>
"""
        )

    now = time.time()

    for user in users:

        # pprint(user)
        if "status" not in user:
            continue
        status = user["status"]
        # pprint(status)
        created_at = status["created_at"]
        timestamp = calendar.timegm(
            time.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
        )
        seconds = now - timestamp
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        ago = "%dh %02dm ago" % (h, m)
        extra_classes = ""
        if h > 24:
            extra_classes = "danger"
        elif h > 12:
            extra_classes = "warning"

        text = status["text"].replace("\n", "<br>")

        # "Mon Jun 08 11:23:45 +0000 2015"
        created = user["created_at"]
        # "08 Jun 2015"
        created = created[8:11] + created[4:7] + created[-5:]

        tweets = commafy(user["statuses_count"])
        following = commafy(user["friends_count"])
        followers = commafy(user["followers_count"])

        user_link = "https://twitter.com/" + user["screen_name"]
        status_link = user_link + "/status/" + status["id_str"]
        status_a_href = '<a href="' + status_link + '" target="twitter">'

        statuses = get_tweets(username)
        clients = summarise_tweet_clients(statuses)

        if args.html:
            print('    <li class="user"><div class="tweet ' + extra_classes + '">')
            print(
                '      <div class="screen_name"><a href="'
                + user_link
                + '" target="twitter">@'
                + user["screen_name"]
                + "</a></div>"
            )
            print('      <div class="status">' + text + "</div>")
            print(
                '      <div class="created_at">'
                + status_a_href
                + status["created_at"]
                + "</a></div>"
            )
            print('      <div class="ago">' + status_a_href + ago + "</a></div>")
            print('      <div class="stats">')
        else:
            print("@" + user["screen_name"])
            print(status["text"])
            print(status["created_at"])

        print(taggy("Created: " + created, "created"))
        print(taggy("Tweets: " + tweets, "tweets"))
        print(taggy("Following: " + following, "following"))
        print(taggy("Followers: " + followers, "followers"))

        if args.html:
            print('        <span class="clients">' "Clients for last 100 tweets: ")
            print("          <ul>")
        else:
            print("Clients for last 100 tweets: ")
        for client in clients:
            if args.html:
                print("            <li>" + client + ": " + str(clients[client]))
            else:
                print("   * " + strip_tags(client) + ": " + str(clients[client]))
        if args.html:
            print(
                """
          </ul>
        </span>
      </div>
    </li>
"""
            )

    if args.html:
        print(
            """
  </ol>
</body>
</html>
"""
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get some info about a Twitter user, like clients used.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("user", help="The Twitter account to check")
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
        default="bin/data/cookerybot.yaml",
        help="YAML file location containing Twitter keys and secrets. "
        "Just for read-only access, doesn't post to Twitter.",
    )
    parser.add_argument("--html", action="store_true", help="HTML tags for formatting")
    args = parser.parse_args()

    path = yaml_path(args.unixpath, args.winpath, args.yaml)
    data = load_yaml(path)

    tweeter_info(args.user)

# End of file
