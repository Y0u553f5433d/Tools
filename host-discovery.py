#!/usr/bin/python

import ipaddress
import os


network = ipaddress.ip_network(unicode("*Network-ID*/*mask*"))
print("Python Host Discovery on *Network-ID*/*mask*")

for i in network.hosts():
    
    response = os.system("ping %s -c 1 > /dev/null" %i)

    if response == 0:
                print("Host %s is UP" %i)
    else:
                pass

print("Host Discovery completed")
