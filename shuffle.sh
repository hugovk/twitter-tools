#!/bin/bash

# Shuffle lines in a file

# OS X: `brew install coreutils` for `gshuf`
# Linux: try `shuf`

# Usage: shuffle.sh unshuffled.sh > shuffled.sh

gshuf $1
