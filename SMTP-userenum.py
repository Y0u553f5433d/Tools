#!/usr/bin/python
import socket
import sys

print ('')
if len(sys.argv) != 2:
    print( "Usage: vrfy.py <username.txt>")
    sys.exit(0)

users=open(sys.argv[1]).read().splitlines()
for user in users:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect(('10.11.1.217',25))
    banner = s.recv(1024)
    #print (banner)
    s.send('VRFY ' + user + '\r\n')
    print ('VRFY ' + user + '\n')
    result = s.recv(1024)
    print (result)
    s.close()
