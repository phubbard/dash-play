#!/usr/bin/env python
# pfh 9/6/15
# see http://stackoverflow.com/questions/17314510/how-to-fix-scapy-warning-pcapy-api-does-not-permit-to-get-capure-file-descripto
# 
# As of 9/26/15, updating to split into separate pieces - the itunes API to REST-ify iTunes, and this code to call it. Simpler
# and lets me run the packet capture on the raspberry Pi.
# See https://github.com/maddox/itunes-api

import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")
import os
import logging
from datetime import datetime

from scapy.all import *

from itunes import glad_button, bounty_button


def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      d = datetime.now()
      if pkt[ARP].hwsrc == '74:c2:46:a4:4c:e7': # Glad
        glad_button()
      elif pkt[ARP].hwsrc == '74:c2:46:3e:94:78': # Bounty
        bounty_button()
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0)
 
