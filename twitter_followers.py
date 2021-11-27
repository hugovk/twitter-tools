#!/usr/bin/env python
"""
Print out a user's followers (TODO and friends).
"""
import argparse
import time
from operator import itemgetter
from pprint import pprint  # noqa: F401

import yaml
from twitter import OAuth, Twitter, api  # pip install twitter

TWITTER = None


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode("utf-8"))


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


def get_following(user):
    # print("GET friends/list")

    # Page 1
    cursor = -1

    all_users = []

    while cursor != 0:
        print("Cursor:", cursor)
        users = TWITTER.friends.list(
            screen_name=user,
            cursor=cursor,
            include_user_entities=False,
            skip_status=True,
            count=200,
        )
        cursor = users["next_cursor"]
        all_users.extend(users["users"])

    return all_users


def get_followers(user):
    # print("GET followers/list")

    # Page 1
    cursor = -1

    all_users = []

    while cursor != 0:
        # print("Cursor:", cursor)
        try:
            users = TWITTER.followers.list(
                screen_name=user,
                cursor=cursor,
                include_user_entities=False,
                skip_status=True,
                count=200,
            )
            cursor = users["next_cursor"]
            all_users.extend(users["users"])
        except api.TwitterHTTPError as e:
            # Rate limit? Try again soon.
            print("*" * 80)
            print(e)
            print("*" * 80)
            print("Sleep for just over a minute")
            time.sleep(61)

    return all_users


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print out a user's followers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-y", "--yaml", help="YAML file location containing Twitter keys and secrets"
    )
    parser.add_argument("-u", "--user", default="kaikkisanat", help="User to check")
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)

    if TWITTER is None:
        try:
            access_token = credentials["access_token"]
            access_token_secret = credentials["access_token_secret"]
        except KeyError:  # Older YAMLs
            access_token = credentials["oauth_token"]
            access_token_secret = credentials["oauth_token_secret"]
        TWITTER = Twitter(
            auth=OAuth(
                access_token,
                access_token_secret,
                credentials["consumer_key"],
                credentials["consumer_secret"],
            )
        )

    data = load_yaml(args.yaml)

    users = get_followers(args.user)

    # Sort by most followed
    users = sorted(users, key=itemgetter("followers_count"), reverse=True)

    fields_to_show = ["followers_count", "created_at", "screen_name"]
    print("\t".join(fields_to_show))
    for user in users:
        data_to_show = [str(user[field]) for field in fields_to_show]
        print("\t".join(data_to_show))

# End of file
