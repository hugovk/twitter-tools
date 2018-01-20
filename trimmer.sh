#!/bin/bash
#
# Replace lines over 280 chars with 279 chars and an ellipsis
#
# Usage: trimmer.sh short_and_long_lines.txt > trimmed.txt
#
# http://askubuntu.com/a/523865/41229

max=280

awk "{if (length(\$0) > $max) {print substr(\$0, 1, $max-1)\"…\"} else print}" $1
