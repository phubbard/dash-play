## What is this?

These scripts let me use the cheap Dash buttons to trigger music and podcasts. It Feels Like The Future (tm)!

## How It's Made
Python + AppleScript.

## What It Does

Currently, my 'Glad' button script

1. Switches to the kids' (AirPlay) speakers
2. Turns on shuffle, by song
3. Plays playlist 'Bed'

The 'Bounty' button script

1. Updates all podcasts
2. Selects two AirPlay speakers
3. Turns on shuffle, by song
4. Plays playlist 'dishes'

Next I plan to use another button to play my Marketplace podcasts, but that's why step 1 is there. Soon.

# Requirements

My setup is OSX, minor edits will be needed for Linux/*BSD.

# Setup and installation

0. Setup Dash buttons as per [this link](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8)
1. brew install libdnet
2. pip install -r requirements.txt
3. sudo python ./arp.py
4. Press Dash button
5. Note MAC address(es)
6. Edit run.py script with MACs from 5

# Running it

1. Start iTunes
2. From a terminal, run
   sudo ./run.py
3. Press a button!

# Bugs and notes

1. Seems to not always select the Airplay. Don't understand this yet.

# Read the applescript

The .scpt files are binary, so I've also included the text in applescript.txt
