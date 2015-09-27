#!/usr/bin/env python
# pfh 9/6/15
# see http://stackoverflow.com/questions/17314510/how-to-fix-scapy-warning-pcapy-api-does-not-permit-to-get-capure-file-descripto
# 
# As of 9/26/15, updating to split into separate pieces - the itunes API to REST-ify iTunes, and this code to call it. Simpler
# and lets me run the packet capture on the raspberry Pi.
# See https://github.com/maddox/itunes-api

import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")

import requests
from scapy.all import *


def send_push(hw_addr):
  """
  Decouple root-required code from userland by using HTTP over TCP. Remote end runs as user.
  """
  # Basic sanity check - 6 octets plus 5 colons
  assert(len(hw_addr) <= 17)

  try:
    requests.put('http://localhost:4321/button/' + hw_addr)
  except:
    pass


def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      send_push(pkt[ARP].hwsrc)


print sniff(prn=arp_display, filter="arp", store=0)
 
