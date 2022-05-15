#!/usr/bin/python

import ipaddress
import os


network = ipaddress.ip_network(unicode("10.11.1.0/24"))
print("Python Host Discovery on 10.11.1.0/24")

for i in network.hosts():
    
    response = os.system("ping %s -c 1 > /dev/null" %i)

    if response == 0:
                print("Host %s is UP" %i)
    else:
                pass

print("Host Discovery completed")
