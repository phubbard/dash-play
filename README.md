## What is this?

These scripts let me use the cheap Dash buttons to trigger music and podcasts. It Feels Like The Future (tm)!

## How It's Made
Python and more Python. 

## Root and Other Bad Things
The packet sniffing code requires root in order to listen for ARP packets, so to reduce the risks I broke the code into
two pieces:

 1. run.py must be run as root, and just re-sends any button (or other ARP packet) out via HTTP. Ignores any TCP or HTTP errors.
 2. itunes.py Uses Flask to listen to http://localhost:4321 and has all of the itunes control and button logic.

I like this much better. You can run the ./run.py script using forever or nohup and it shouldn't require any changes. 

The itunes.py script looks into config.ini for

 1. URL of the [iTunes API](https://github.com/maddox/itunes-api) host
 2. Button names and MAC addresses

The logic in itunes.py should, I hope, be clear and simple.

## How to Run It

1. sudo nohup ./run.py &
2. ./itunes.py (or nohup)

## What It Does

Changes speakers and starts playlists, some according to the hour of the day.

On all buttons, if playing they stop playback. Wife request that feature.

# Requirements

1. iTunes API running on network-accesible machine. I'm running it on my el-cheapo Mini.
2. These scripts, probably on Linux. The scapy library seems to hate OSX, so I'm using a Raspberry Pi 2 to run these. Works great.

# Setup and installation

0. Setup Dash buttons as per [this link](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8)
1. brew install libdnet2. pip install -r requirements.txt
3. sudo python ./arp.py
4. Press Dash button
5. Note MAC address(es)
6. Edit config.ini file with MACs from 5

# Bugs and notes


