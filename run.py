#!/usr/bin/env python
# pfh 9/6/15
# see http://stackoverflow.com/questions/17314510/how-to-fix-scapy-warning-pcapy-api-does-not-permit-to-get-capure-file-descripto

import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == '74:c2:46:a4:4c:e7': # Glad
        print "Pushed Glad"
        os.system('osascript play-glad.scpt')
      elif pkt[ARP].hwsrc == '74:c2:46:3e:94:78':
        print "Pushed Bounty"
        os.system('osascript play-bounty.scpt')
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0)
 
