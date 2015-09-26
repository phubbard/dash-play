#!/usr/bin/env python
# pfh 9/6/15
# see http://stackoverflow.com/questions/17314510/how-to-fix-scapy-warning-pcapy-api-does-not-permit-to-get-capure-file-descripto

import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")
import os
import logging

from datetime import datetime

from scapy.all import *


def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      d = datetime.now()
      if pkt[ARP].hwsrc == '74:c2:46:a4:4c:e7': # Glad
        print "Pushed Glad"
        if d.hour < 12:
          os.system('osascript play-glad-am.scpt')
        else:
          os.system('osascript play-glad-pm.scpt')
      elif pkt[ARP].hwsrc == '74:c2:46:3e:94:78':
        print "Pushed Bounty"
        if d.hour < 12:
          os.system('osascript play-bounty-am.scpt')
        else:
          os.system('osascript play-bounty-pm.scpt')
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0)
 
