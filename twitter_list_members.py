#!/usr/bin/env python
# encoding: utf-8
"""
Print out the members of a Twitter list.

Usage examples:
python twitter_list_members.py hugovk my-twitterbot-army
python twitter_list_members.py botally omnibots
"""
from __future__ import print_function, unicode_literals

import argparse
from twitter import Twitter, OAuth
import yaml

# from pprint import pprint

TWITTER = None


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def load_yaml(filename):
    """
    TODO
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
    # https://dev.twitter.com/rest/reference/get/lists/members

    # Page 1
    cursor = -1

    all_users = []

    while cursor != 0:
        # print("Cursor:", cursor)
        users = TWITTER.lists.members(owner_screen_name=list_owner,
                                      slug=list_name,
                                      cursor=cursor,
                                      include_user_entities=False,
                                      skip_status=True,
                                      count=5000)
        cursor = users['next_cursor']
        all_users.extend(users['users'])

    return all_users


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print out the members of a Twitter list.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='data/cookerybot.yaml',
        help="YAML file location containing Twitter keys and secrets. "
              "Just for read-only access, doesn't post to Twitter.")
    parser.add_argument('user', help="The list owner")
    parser.add_argument('list', help="The list slug")
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)

    if TWITTER is None:
        TWITTER = Twitter(auth=OAuth(
            credentials['access_token'],
            credentials['access_token_secret'],
            credentials['consumer_key'],
            credentials['consumer_secret']))

    members = get_list_members(args.user, args.list)

#     pprint(members)
    for member in members:
        print(member["screen_name"], "\t", member["created_at"])

# End of file
