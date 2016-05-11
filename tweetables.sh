#!/bin/bash

# Output only lines 140 or shorter

# Usage: tweetables.sh short_and_long_lines.txt > only_short.txt

awk 'length($0)<=140' $1
