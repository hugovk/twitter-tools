#!/usr/bin/env python
# encoding: utf-8
"""
Given a Twitter list make a dashboard of their latest tweets.
Doesn't post anything to Twitter.

Usage: python tweetboard.py > tweetboard.html
"""
from __future__ import print_function, unicode_literals

import argparse
import calendar
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


def get_list_members(list_owner, list_name):
    # print("GET lists/members")
    # Assumption: no more than 5000 in list.
    members = TWITTER.lists.members(owner_screen_name=list_owner,
                                    slug=list_name,
                                    include_entities=False,
                                    # skip_status=True,
                                    count=5000)
    # pprint(members)

    # Extract IDs
    # ids = [member['id'] for member in members['users']]
    # pprint(ids)
    return members["users"]


def tweetboard(list_owner, list_name):
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

    users = get_list_members(list_owner, list_name)

    print('''
<html>
<head>
    <title>Tweetboard</title>
        <style type="text/css">
        body {
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
        .tweet div {
            padding-bottom: 10px;
        }
        .status {
            word-break: break-word;
        }
        li {
            border: 1px solid #000;
            display: inline-block;
            margin: 5px;
            min-height: 250px;
            padding: 5px;
            vertical-align: top;
            width: 240px;
        }
        </style>
        </head>
        <body>
            <ol>
          ''')

    now = time.time()

    for user in users:
        # pprint(user)
        if 'status' not in user:
            continue
        status = user['status']
        # pprint(status)
        created_at = status['created_at']
        timestamp = calendar.timegm(time.strptime(
            created_at, "%a %b %d %H:%M:%S +0000 %Y"))
        seconds = now-timestamp
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        ago = "%dh %02dm ago" % (h, m)
        extra_classes = ""
        if h > 24:
            extra_classes = "danger"
        elif h > 12:
            extra_classes = "warning"

        user_link = "https://twitter.com/" + user['screen_name']
        status_link = user_link + "/status/" + status['id_str']

        print('<li><div class="tweet ' + extra_classes + '">')
        print_it('<div class="screen_name"><a href="' + user_link +
                 '" target="twitter">@' + user['screen_name'] +
                 '</a>:</div> <div class="status">' + status['text'] +
                 '</div>')
        status_a_href = '<a href="' + status_link + '" target="twitter">'
        print('<div class="created_at">' + status_a_href +
              status['created_at'] + '</a></div>')
        print('<div class="ago">' + status_a_href + ago + '</a></div>')
        print("</div>")

    print("</ol></body></html>")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given a Twitter list make a "
                    "dashboard of their latest tweets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/cookerybot.yaml',
        help="YAML file location containing Twitter keys and secrets. "
              "Just for read-only access, doesn't post to Twitter.")
    parser.add_argument(
        '-u', '--user', default='hugovk',
        help="The list owner")
    parser.add_argument(
        '-l', '--list', default='my-twitterbot-army',
        help="The list slug")
    args = parser.parse_args()

    data = load_yaml(args.yaml)

    tweetboard(args.user, args.list)

# End of file
