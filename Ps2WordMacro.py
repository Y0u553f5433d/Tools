#!/usr/bin/python
str = "Powershell Command Here"
n = 50
for i in range(0, len(str), n):
 print " Str = Str + " + '"' + str[i:i+n] + '"'
