#!/usr/bin/python

import ipaddress
import os


#ip address string must be in unicode to use ipaddress module
network = ipaddress.ip_network(unicode("10.11.1.0/24"))
#network = ipaddress.ip_network(unicode(input("What's your Network > ")))
print("Python Host Discovery on 10.11.1.0/24")

for i in network.hosts():
    #str(i)

    response = os.system("ping %s -c 1 > /dev/null" %i)

    if response == 0:
                print("%s is UP" %i)
    else:
                pass

print("Host Discovery completed")
