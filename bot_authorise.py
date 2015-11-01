#!/usr/bin/env python
"""
Authorise a Twitter bot account against a Twitter bot application.

It works by giving you a URL to authorise with, you paste that into a browser
that's logged in as the given (bot) user. You'll get a PIN back, which the app
is now waiting for -- from there you get your access key and secret.

Based on beaugunderson's:
https://gist.github.com/moonmilk/035917e668872013c1bd#gistcomment-1333900
"""
from __future__ import print_function, unicode_literals
import argparse
import tweepy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Authorise a Twitter account against an app.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'consumer_key',
        help="From your app settings page")
    parser.add_argument(
        'consumer_secret',
        help="From your app settings page")
    args = parser.parse_args()

    auth = tweepy.OAuthHandler(args.consumer_key, args.consumer_secret)
    auth.secure = True
    auth_url = auth.get_authorization_url()

    print()
    print("Please open this URL in a browser that's logged in as your bot,\n"
          "authorise the application, and then type in the PIN back here.")
    print()
    print(auth_url)

    verifier = raw_input('PIN: ').strip()

    auth.get_access_token(verifier)

    print()
    print("consumer_key: " + args.consumer_key)
    print("consumer_secret: " + args.consumer_secret)
    print("access_token: " + auth.access_token)
    print("access_token_secret: " + auth.access_token_secret)

# End of file
