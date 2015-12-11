#!/usr/bin/env python
# encoding: utf-8
"""
Print out a user's friends and followers.
"""
from __future__ import print_function, unicode_literals

import argparse
from twitter import Twitter, OAuth  # pip install twitter
import yaml

from pprint import pprint

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


def get_following(user):
    # print("GET friends/list")

    # Page 1
    cursor = -1

    all_users = []

    while cursor != 0:
        print("Cursor:", cursor)
        users = TWITTER.friends.list(screen_name=user,
                                       cursor=cursor,
                                       include_user_entities=False,
                                       skip_status=True,
                                       count=200)
        cursor = users['next_cursor']
        all_users.extend(users['users'])

    return all_users


def get_followers(user):
    # print("GET followers/list")

    # Page 1
    cursor = -1

    all_users = []

    while cursor != 0:
        # print("Cursor:", cursor)
        users = TWITTER.followers.list(screen_name=user,
                                       cursor=cursor,
                                       include_user_entities=False,
                                       skip_status=True,
                                       count=200)
        cursor = users['next_cursor']
        all_users.extend(users['users'])

    return all_users


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-u', '--user', default='kaikkisanat',
        help="User to check")
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)

    if TWITTER is None:
        TWITTER = Twitter(auth=OAuth(
       credentials['oauth_token'],
       credentials['oauth_token_secret'],
       credentials['consumer_key'],
       credentials['consumer_secret']))

    data = load_yaml(args.yaml)

    users = get_followers(args.user)

#     pprint(members)
    for user in users:
        print(user["screen_name"], "\t", user["created_at"])

# End of file
