#!/usr/bin/env python
# encoding: utf-8
"""
Given a Twitter list (owner's screen_name + list slug),
follow the owner and each of the list members.
"""
from __future__ import print_function, unicode_literals

import argparse
import twitter
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
    with open(filename) as f:
        data = yaml.safe_load(f)

    return data


def get_list_members(user, list_name):
    print("GET lists/members")
    # Assumption: no more than 5000 in list.
    members = TWITTER.lists.members(owner_screen_name=user, slug=list_name,
                                    include_entities=False, skip_status=True,
                                    count=5000)
    # pprint(members)

    # Extract IDs
    ids = [member['id'] for member in members['users']]
    pprint(ids)
    return ids


def get_authenticated_user_id():
    print("GET account/verify_credentials")
    own_id = TWITTER.account.verify_credentials(include_entities=False,
                                                skip_status=True)
    # pprint(own_id)
    own_id = own_id['id']
    pprint(own_id)
    return own_id


def get_friends(user_id):
    print("GET friends/ids")
    # Assumption: no more than 5000 friends.
    friends = TWITTER.friends.ids(user_id=user_id, count=5000,
                                  include_entities=False, skip_status=True)
    # pprint(friends)

    # Extract IDs
    ids = friends['ids']
    pprint(ids)
    return ids


def get_user_id(screen_name):
    print("GET users/show")
    user = TWITTER.users.show(screen_name=screen_name,
                              include_entities=False)
    # pprint(user)

    # Extract ID
    id = user['id']
    pprint(id)
    return id


def follow_by_id(user_ids):
    for user_id in user_ids:
        print("POST friendships/create")
        ret = TWITTER.friendships.create(user_id=user_id)
        # pprint(ret)
        print(ret['id'], "@"+ret['screen_name'], ret['name'])


def follow_list_members(user, list_name):
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

    users_to_follow = get_list_members(user, list_name)

    # Get authenticated user's friends so as not to follow the already followed
    own_id = get_authenticated_user_id()
    friends = get_friends(own_id)

    # And the list owner's ID
    list_owner = get_user_id(user)
    users_to_follow.append(list_owner)

    # And @botally
    botally = get_user_id("botally")
    users_to_follow.append(botally)

    # Find who to follow
    users_to_follow = list(
        set(users_to_follow) - set(friends) - set([own_id]))
    pprint(users_to_follow)

    # Follow 'em!
    print("Following (before):", len(friends))
    if users_to_follow:
        follow_by_id(users_to_follow)
    friends = get_friends(own_id)
    print("Following (after):", len(friends))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Follow the owner and members of a Twitter list",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-u', '--user', default='hugovk',
        help="Owner of the list to follow")
    parser.add_argument(
        '-l', '--list', default='my-twitterbot-army',
        help="Name of the list to follow")
    args = parser.parse_args()

    data = load_yaml(args.yaml)

    follow_list_members(args.user, args.list)

# End of file
