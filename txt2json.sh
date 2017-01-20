#!/bin/bash

# Convert a text file to JSON

# Usage: txt2json.sh textlines.txt > jsonlines.json

echo {
echo \"origin\":[

# Replace " with \"
# Prepend "
# Append ",
# Remove comma from last line (`$` matches the last line)

sed -e 's/"/\\"/g' $1 | sed -e 's/^/"/' | sed -e 's/$/",/' | sed '$s/,$//'

echo ]
echo }
