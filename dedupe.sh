#!/bin/bash

# Deduplicate lines without sorting

# (`sort -u $1` dedupes and sorts and is slower than awk)

# Usage: dedupe.sh has_dupe_lines.txt > no_duplicate_lines.txt

awk '!a[$0]++' $1
