
sphostd:     file format elf64-x86-64


Disassembly of section .init:

0000000000002000 <.init>:
    2000:	f3 0f 1e fa          	endbr64
    2004:	48 83 ec 08          	sub    rsp,0x8
    2008:	48 8b 05 d9 9f 00 00 	mov    rax,QWORD PTR [rip+0x9fd9]        # bfe8 <socket@plt+0x9a18>
    200f:	48 85 c0             	test   rax,rax
    2012:	74 02                	je     2016 <__cxa_finalize@plt-0x2ea>
    2014:	ff d0                	call   rax
    2016:	48 83 c4 08          	add    rsp,0x8
    201a:	c3                   	ret

Disassembly of section .plt:

0000000000002020 <.plt>:
    2020:	ff 35 3a 9e 00 00    	push   QWORD PTR [rip+0x9e3a]        # be60 <socket@plt+0x9890>
    2026:	ff 25 3c 9e 00 00    	jmp    QWORD PTR [rip+0x9e3c]        # be68 <socket@plt+0x9898>
    202c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    2030:	f3 0f 1e fa          	endbr64
    2034:	68 00 00 00 00       	push   0x0
    2039:	e9 e2 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    203e:	66 90                	xchg   ax,ax
    2040:	f3 0f 1e fa          	endbr64
    2044:	68 01 00 00 00       	push   0x1
    2049:	e9 d2 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    204e:	66 90                	xchg   ax,ax
    2050:	f3 0f 1e fa          	endbr64
    2054:	68 02 00 00 00       	push   0x2
    2059:	e9 c2 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    205e:	66 90                	xchg   ax,ax
    2060:	f3 0f 1e fa          	endbr64
    2064:	68 03 00 00 00       	push   0x3
    2069:	e9 b2 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    206e:	66 90                	xchg   ax,ax
    2070:	f3 0f 1e fa          	endbr64
    2074:	68 04 00 00 00       	push   0x4
    2079:	e9 a2 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    207e:	66 90                	xchg   ax,ax
    2080:	f3 0f 1e fa          	endbr64
    2084:	68 05 00 00 00       	push   0x5
    2089:	e9 92 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    208e:	66 90                	xchg   ax,ax
    2090:	f3 0f 1e fa          	endbr64
    2094:	68 06 00 00 00       	push   0x6
    2099:	e9 82 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    209e:	66 90                	xchg   ax,ax
    20a0:	f3 0f 1e fa          	endbr64
    20a4:	68 07 00 00 00       	push   0x7
    20a9:	e9 72 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    20ae:	66 90                	xchg   ax,ax
    20b0:	f3 0f 1e fa          	endbr64
    20b4:	68 08 00 00 00       	push   0x8
    20b9:	e9 62 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    20be:	66 90                	xchg   ax,ax
    20c0:	f3 0f 1e fa          	endbr64
    20c4:	68 09 00 00 00       	push   0x9
    20c9:	e9 52 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    20ce:	66 90                	xchg   ax,ax
    20d0:	f3 0f 1e fa          	endbr64
    20d4:	68 0a 00 00 00       	push   0xa
    20d9:	e9 42 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    20de:	66 90                	xchg   ax,ax
    20e0:	f3 0f 1e fa          	endbr64
    20e4:	68 0b 00 00 00       	push   0xb
    20e9:	e9 32 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    20ee:	66 90                	xchg   ax,ax
    20f0:	f3 0f 1e fa          	endbr64
    20f4:	68 0c 00 00 00       	push   0xc
    20f9:	e9 22 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    20fe:	66 90                	xchg   ax,ax
    2100:	f3 0f 1e fa          	endbr64
    2104:	68 0d 00 00 00       	push   0xd
    2109:	e9 12 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    210e:	66 90                	xchg   ax,ax
    2110:	f3 0f 1e fa          	endbr64
    2114:	68 0e 00 00 00       	push   0xe
    2119:	e9 02 ff ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    211e:	66 90                	xchg   ax,ax
    2120:	f3 0f 1e fa          	endbr64
    2124:	68 0f 00 00 00       	push   0xf
    2129:	e9 f2 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    212e:	66 90                	xchg   ax,ax
    2130:	f3 0f 1e fa          	endbr64
    2134:	68 10 00 00 00       	push   0x10
    2139:	e9 e2 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    213e:	66 90                	xchg   ax,ax
    2140:	f3 0f 1e fa          	endbr64
    2144:	68 11 00 00 00       	push   0x11
    2149:	e9 d2 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    214e:	66 90                	xchg   ax,ax
    2150:	f3 0f 1e fa          	endbr64
    2154:	68 12 00 00 00       	push   0x12
    2159:	e9 c2 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    215e:	66 90                	xchg   ax,ax
    2160:	f3 0f 1e fa          	endbr64
    2164:	68 13 00 00 00       	push   0x13
    2169:	e9 b2 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    216e:	66 90                	xchg   ax,ax
    2170:	f3 0f 1e fa          	endbr64
    2174:	68 14 00 00 00       	push   0x14
    2179:	e9 a2 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    217e:	66 90                	xchg   ax,ax
    2180:	f3 0f 1e fa          	endbr64
    2184:	68 15 00 00 00       	push   0x15
    2189:	e9 92 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    218e:	66 90                	xchg   ax,ax
    2190:	f3 0f 1e fa          	endbr64
    2194:	68 16 00 00 00       	push   0x16
    2199:	e9 82 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    219e:	66 90                	xchg   ax,ax
    21a0:	f3 0f 1e fa          	endbr64
    21a4:	68 17 00 00 00       	push   0x17
    21a9:	e9 72 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    21ae:	66 90                	xchg   ax,ax
    21b0:	f3 0f 1e fa          	endbr64
    21b4:	68 18 00 00 00       	push   0x18
    21b9:	e9 62 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    21be:	66 90                	xchg   ax,ax
    21c0:	f3 0f 1e fa          	endbr64
    21c4:	68 19 00 00 00       	push   0x19
    21c9:	e9 52 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    21ce:	66 90                	xchg   ax,ax
    21d0:	f3 0f 1e fa          	endbr64
    21d4:	68 1a 00 00 00       	push   0x1a
    21d9:	e9 42 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    21de:	66 90                	xchg   ax,ax
    21e0:	f3 0f 1e fa          	endbr64
    21e4:	68 1b 00 00 00       	push   0x1b
    21e9:	e9 32 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    21ee:	66 90                	xchg   ax,ax
    21f0:	f3 0f 1e fa          	endbr64
    21f4:	68 1c 00 00 00       	push   0x1c
    21f9:	e9 22 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    21fe:	66 90                	xchg   ax,ax
    2200:	f3 0f 1e fa          	endbr64
    2204:	68 1d 00 00 00       	push   0x1d
    2209:	e9 12 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    220e:	66 90                	xchg   ax,ax
    2210:	f3 0f 1e fa          	endbr64
    2214:	68 1e 00 00 00       	push   0x1e
    2219:	e9 02 fe ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    221e:	66 90                	xchg   ax,ax
    2220:	f3 0f 1e fa          	endbr64
    2224:	68 1f 00 00 00       	push   0x1f
    2229:	e9 f2 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    222e:	66 90                	xchg   ax,ax
    2230:	f3 0f 1e fa          	endbr64
    2234:	68 20 00 00 00       	push   0x20
    2239:	e9 e2 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    223e:	66 90                	xchg   ax,ax
    2240:	f3 0f 1e fa          	endbr64
    2244:	68 21 00 00 00       	push   0x21
    2249:	e9 d2 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    224e:	66 90                	xchg   ax,ax
    2250:	f3 0f 1e fa          	endbr64
    2254:	68 22 00 00 00       	push   0x22
    2259:	e9 c2 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    225e:	66 90                	xchg   ax,ax
    2260:	f3 0f 1e fa          	endbr64
    2264:	68 23 00 00 00       	push   0x23
    2269:	e9 b2 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    226e:	66 90                	xchg   ax,ax
    2270:	f3 0f 1e fa          	endbr64
    2274:	68 24 00 00 00       	push   0x24
    2279:	e9 a2 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    227e:	66 90                	xchg   ax,ax
    2280:	f3 0f 1e fa          	endbr64
    2284:	68 25 00 00 00       	push   0x25
    2289:	e9 92 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    228e:	66 90                	xchg   ax,ax
    2290:	f3 0f 1e fa          	endbr64
    2294:	68 26 00 00 00       	push   0x26
    2299:	e9 82 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    229e:	66 90                	xchg   ax,ax
    22a0:	f3 0f 1e fa          	endbr64
    22a4:	68 27 00 00 00       	push   0x27
    22a9:	e9 72 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    22ae:	66 90                	xchg   ax,ax
    22b0:	f3 0f 1e fa          	endbr64
    22b4:	68 28 00 00 00       	push   0x28
    22b9:	e9 62 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    22be:	66 90                	xchg   ax,ax
    22c0:	f3 0f 1e fa          	endbr64
    22c4:	68 29 00 00 00       	push   0x29
    22c9:	e9 52 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    22ce:	66 90                	xchg   ax,ax
    22d0:	f3 0f 1e fa          	endbr64
    22d4:	68 2a 00 00 00       	push   0x2a
    22d9:	e9 42 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    22de:	66 90                	xchg   ax,ax
    22e0:	f3 0f 1e fa          	endbr64
    22e4:	68 2b 00 00 00       	push   0x2b
    22e9:	e9 32 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    22ee:	66 90                	xchg   ax,ax
    22f0:	f3 0f 1e fa          	endbr64
    22f4:	68 2c 00 00 00       	push   0x2c
    22f9:	e9 22 fd ff ff       	jmp    2020 <__cxa_finalize@plt-0x2e0>
    22fe:	66 90                	xchg   ax,ax

Disassembly of section .plt.got:

0000000000002300 <__cxa_finalize@plt>:
    2300:	f3 0f 1e fa          	endbr64
    2304:	ff 25 ee 9c 00 00    	jmp    QWORD PTR [rip+0x9cee]        # bff8 <socket@plt+0x9a28>
    230a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .plt.sec:

0000000000002310 <getenv@plt>:
    2310:	f3 0f 1e fa          	endbr64
    2314:	ff 25 56 9b 00 00    	jmp    QWORD PTR [rip+0x9b56]        # be70 <socket@plt+0x98a0>
    231a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002320 <__snprintf_chk@plt>:
    2320:	f3 0f 1e fa          	endbr64
    2324:	ff 25 4e 9b 00 00    	jmp    QWORD PTR [rip+0x9b4e]        # be78 <socket@plt+0x98a8>
    232a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002330 <free@plt>:
    2330:	f3 0f 1e fa          	endbr64
    2334:	ff 25 46 9b 00 00    	jmp    QWORD PTR [rip+0x9b46]        # be80 <socket@plt+0x98b0>
    233a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002340 <unlink@plt>:
    2340:	f3 0f 1e fa          	endbr64
    2344:	ff 25 3e 9b 00 00    	jmp    QWORD PTR [rip+0x9b3e]        # be88 <socket@plt+0x98b8>
    234a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002350 <strncpy@plt>:
    2350:	f3 0f 1e fa          	endbr64
    2354:	ff 25 36 9b 00 00    	jmp    QWORD PTR [rip+0x9b36]        # be90 <socket@plt+0x98c0>
    235a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002360 <_exit@plt>:
    2360:	f3 0f 1e fa          	endbr64
    2364:	ff 25 2e 9b 00 00    	jmp    QWORD PTR [rip+0x9b2e]        # be98 <socket@plt+0x98c8>
    236a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002370 <__isoc23_sscanf@plt>:
    2370:	f3 0f 1e fa          	endbr64
    2374:	ff 25 26 9b 00 00    	jmp    QWORD PTR [rip+0x9b26]        # bea0 <socket@plt+0x98d0>
    237a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002380 <mkdir@plt>:
    2380:	f3 0f 1e fa          	endbr64
    2384:	ff 25 1e 9b 00 00    	jmp    QWORD PTR [rip+0x9b1e]        # bea8 <socket@plt+0x98d8>
    238a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002390 <sigaction@plt>:
    2390:	f3 0f 1e fa          	endbr64
    2394:	ff 25 16 9b 00 00    	jmp    QWORD PTR [rip+0x9b16]        # beb0 <socket@plt+0x98e0>
    239a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000023a0 <fread@plt>:
    23a0:	f3 0f 1e fa          	endbr64
    23a4:	ff 25 0e 9b 00 00    	jmp    QWORD PTR [rip+0x9b0e]        # beb8 <socket@plt+0x98e8>
    23aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000023b0 <setsockopt@plt>:
    23b0:	f3 0f 1e fa          	endbr64
    23b4:	ff 25 06 9b 00 00    	jmp    QWORD PTR [rip+0x9b06]        # bec0 <socket@plt+0x98f0>
    23ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000023c0 <clock_gettime@plt>:
    23c0:	f3 0f 1e fa          	endbr64
    23c4:	ff 25 fe 9a 00 00    	jmp    QWORD PTR [rip+0x9afe]        # bec8 <socket@plt+0x98f8>
    23ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000023d0 <write@plt>:
    23d0:	f3 0f 1e fa          	endbr64
    23d4:	ff 25 f6 9a 00 00    	jmp    QWORD PTR [rip+0x9af6]        # bed0 <socket@plt+0x9900>
    23da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000023e0 <fclose@plt>:
    23e0:	f3 0f 1e fa          	endbr64
    23e4:	ff 25 ee 9a 00 00    	jmp    QWORD PTR [rip+0x9aee]        # bed8 <socket@plt+0x9908>
    23ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000023f0 <strlen@plt>:
    23f0:	f3 0f 1e fa          	endbr64
    23f4:	ff 25 e6 9a 00 00    	jmp    QWORD PTR [rip+0x9ae6]        # bee0 <socket@plt+0x9910>
    23fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002400 <__stack_chk_fail@plt>:
    2400:	f3 0f 1e fa          	endbr64
    2404:	ff 25 de 9a 00 00    	jmp    QWORD PTR [rip+0x9ade]        # bee8 <socket@plt+0x9918>
    240a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002410 <system@plt>:
    2410:	f3 0f 1e fa          	endbr64
    2414:	ff 25 d6 9a 00 00    	jmp    QWORD PTR [rip+0x9ad6]        # bef0 <socket@plt+0x9920>
    241a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002420 <strrchr@plt>:
    2420:	f3 0f 1e fa          	endbr64
    2424:	ff 25 ce 9a 00 00    	jmp    QWORD PTR [rip+0x9ace]        # bef8 <socket@plt+0x9928>
    242a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002430 <close@plt>:
    2430:	f3 0f 1e fa          	endbr64
    2434:	ff 25 c6 9a 00 00    	jmp    QWORD PTR [rip+0x9ac6]        # bf00 <socket@plt+0x9930>
    243a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002440 <read@plt>:
    2440:	f3 0f 1e fa          	endbr64
    2444:	ff 25 be 9a 00 00    	jmp    QWORD PTR [rip+0x9abe]        # bf08 <socket@plt+0x9938>
    244a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002450 <fgets@plt>:
    2450:	f3 0f 1e fa          	endbr64
    2454:	ff 25 b6 9a 00 00    	jmp    QWORD PTR [rip+0x9ab6]        # bf10 <socket@plt+0x9940>
    245a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002460 <calloc@plt>:
    2460:	f3 0f 1e fa          	endbr64
    2464:	ff 25 ae 9a 00 00    	jmp    QWORD PTR [rip+0x9aae]        # bf18 <socket@plt+0x9948>
    246a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002470 <strcmp@plt>:
    2470:	f3 0f 1e fa          	endbr64
    2474:	ff 25 a6 9a 00 00    	jmp    QWORD PTR [rip+0x9aa6]        # bf20 <socket@plt+0x9950>
    247a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002480 <signal@plt>:
    2480:	f3 0f 1e fa          	endbr64
    2484:	ff 25 9e 9a 00 00    	jmp    QWORD PTR [rip+0x9a9e]        # bf28 <socket@plt+0x9958>
    248a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002490 <__memcpy_chk@plt>:
    2490:	f3 0f 1e fa          	endbr64
    2494:	ff 25 96 9a 00 00    	jmp    QWORD PTR [rip+0x9a96]        # bf30 <socket@plt+0x9960>
    249a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000024a0 <memcpy@plt>:
    24a0:	f3 0f 1e fa          	endbr64
    24a4:	ff 25 8e 9a 00 00    	jmp    QWORD PTR [rip+0x9a8e]        # bf38 <socket@plt+0x9968>
    24aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000024b0 <time@plt>:
    24b0:	f3 0f 1e fa          	endbr64
    24b4:	ff 25 86 9a 00 00    	jmp    QWORD PTR [rip+0x9a86]        # bf40 <socket@plt+0x9970>
    24ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000024c0 <__isoc23_strtol@plt>:
    24c0:	f3 0f 1e fa          	endbr64
    24c4:	ff 25 7e 9a 00 00    	jmp    QWORD PTR [rip+0x9a7e]        # bf48 <socket@plt+0x9978>
    24ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000024d0 <malloc@plt>:
    24d0:	f3 0f 1e fa          	endbr64
    24d4:	ff 25 76 9a 00 00    	jmp    QWORD PTR [rip+0x9a76]        # bf50 <socket@plt+0x9980>
    24da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000024e0 <listen@plt>:
    24e0:	f3 0f 1e fa          	endbr64
    24e4:	ff 25 6e 9a 00 00    	jmp    QWORD PTR [rip+0x9a6e]        # bf58 <socket@plt+0x9988>
    24ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000024f0 <chmod@plt>:
    24f0:	f3 0f 1e fa          	endbr64
    24f4:	ff 25 66 9a 00 00    	jmp    QWORD PTR [rip+0x9a66]        # bf60 <socket@plt+0x9990>
    24fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002500 <bind@plt>:
    2500:	f3 0f 1e fa          	endbr64
    2504:	ff 25 5e 9a 00 00    	jmp    QWORD PTR [rip+0x9a5e]        # bf68 <socket@plt+0x9998>
    250a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002510 <waitpid@plt>:
    2510:	f3 0f 1e fa          	endbr64
    2514:	ff 25 56 9a 00 00    	jmp    QWORD PTR [rip+0x9a56]        # bf70 <socket@plt+0x99a0>
    251a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002520 <open@plt>:
    2520:	f3 0f 1e fa          	endbr64
    2524:	ff 25 4e 9a 00 00    	jmp    QWORD PTR [rip+0x9a4e]        # bf78 <socket@plt+0x99a8>
    252a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002530 <fopen@plt>:
    2530:	f3 0f 1e fa          	endbr64
    2534:	ff 25 46 9a 00 00    	jmp    QWORD PTR [rip+0x9a46]        # bf80 <socket@plt+0x99b0>
    253a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002540 <perror@plt>:
    2540:	f3 0f 1e fa          	endbr64
    2544:	ff 25 3e 9a 00 00    	jmp    QWORD PTR [rip+0x9a3e]        # bf88 <socket@plt+0x99b8>
    254a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002550 <__dprintf_chk@plt>:
    2550:	f3 0f 1e fa          	endbr64
    2554:	ff 25 36 9a 00 00    	jmp    QWORD PTR [rip+0x9a36]        # bf90 <socket@plt+0x99c0>
    255a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002560 <accept@plt>:
    2560:	f3 0f 1e fa          	endbr64
    2564:	ff 25 2e 9a 00 00    	jmp    QWORD PTR [rip+0x9a2e]        # bf98 <socket@plt+0x99c8>
    256a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002570 <getppid@plt>:
    2570:	f3 0f 1e fa          	endbr64
    2574:	ff 25 26 9a 00 00    	jmp    QWORD PTR [rip+0x9a26]        # bfa0 <socket@plt+0x99d0>
    257a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002580 <fwrite@plt>:
    2580:	f3 0f 1e fa          	endbr64
    2584:	ff 25 1e 9a 00 00    	jmp    QWORD PTR [rip+0x9a1e]        # bfa8 <socket@plt+0x99d8>
    258a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000002590 <__fprintf_chk@plt>:
    2590:	f3 0f 1e fa          	endbr64
    2594:	ff 25 16 9a 00 00    	jmp    QWORD PTR [rip+0x9a16]        # bfb0 <socket@plt+0x99e0>
    259a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000025a0 <getrandom@plt>:
    25a0:	f3 0f 1e fa          	endbr64
    25a4:	ff 25 0e 9a 00 00    	jmp    QWORD PTR [rip+0x9a0e]        # bfb8 <socket@plt+0x99e8>
    25aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000025b0 <fork@plt>:
    25b0:	f3 0f 1e fa          	endbr64
    25b4:	ff 25 06 9a 00 00    	jmp    QWORD PTR [rip+0x9a06]        # bfc0 <socket@plt+0x99f0>
    25ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000025c0 <strstr@plt>:
    25c0:	f3 0f 1e fa          	endbr64
    25c4:	ff 25 fe 99 00 00    	jmp    QWORD PTR [rip+0x99fe]        # bfc8 <socket@plt+0x99f8>
    25ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000025d0 <socket@plt>:
    25d0:	f3 0f 1e fa          	endbr64
    25d4:	ff 25 f6 99 00 00    	jmp    QWORD PTR [rip+0x99f6]        # bfd0 <socket@plt+0x9a00>
    25da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

00000000000025e0 <.text>:
    25e0:	48 8d 3d 4c 3a 00 00 	lea    rdi,[rip+0x3a4c]        # 6033 <socket@plt+0x3a63>
    25e7:	e8 54 ff ff ff       	call   2540 <perror@plt>
    25ec:	48 8b 84 24 18 01 00 	mov    rax,QWORD PTR [rsp+0x118]
    25f3:	00 
    25f4:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    25fb:	00 00 
    25fd:	75 2f                	jne    262e <socket@plt+0x5e>
    25ff:	48 81 c4 28 01 00 00 	add    rsp,0x128
    2606:	b8 01 00 00 00       	mov    eax,0x1
    260b:	5b                   	pop    rbx
    260c:	5d                   	pop    rbp
    260d:	41 5c                	pop    r12
    260f:	41 5d                	pop    r13
    2611:	c3                   	ret
    2612:	48 8d 3d 26 3a 00 00 	lea    rdi,[rip+0x3a26]        # 603f <socket@plt+0x3a6f>
    2619:	e8 22 ff ff ff       	call   2540 <perror@plt>
    261e:	eb cc                	jmp    25ec <socket@plt+0x1c>
    2620:	48 8d 3d 13 3a 00 00 	lea    rdi,[rip+0x3a13]        # 603a <socket@plt+0x3a6a>
    2627:	e8 14 ff ff ff       	call   2540 <perror@plt>
    262c:	eb be                	jmp    25ec <socket@plt+0x1c>
    262e:	e8 cd fd ff ff       	call   2400 <__stack_chk_fail@plt>
    2633:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    263a:	00 00 00 
    263d:	0f 1f 00             	nop    DWORD PTR [rax]
    2640:	f3 0f 1e fa          	endbr64
    2644:	41 55                	push   r13
    2646:	45 31 ed             	xor    r13d,r13d
    2649:	41 54                	push   r12
    264b:	55                   	push   rbp
    264c:	53                   	push   rbx
    264d:	48 81 ec 28 01 00 00 	sub    rsp,0x128
    2654:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    265b:	00 00 
    265d:	48 89 84 24 18 01 00 	mov    QWORD PTR [rsp+0x118],rax
    2664:	00 
    2665:	31 c0                	xor    eax,eax
    2667:	e8 c4 35 00 00       	call   5c30 <socket@plt+0x3660>
    266c:	be 01 00 00 00       	mov    esi,0x1
    2671:	bf 0d 00 00 00       	mov    edi,0xd
    2676:	e8 05 fe ff ff       	call   2480 <signal@plt>
    267b:	48 8d 94 24 88 00 00 	lea    rdx,[rsp+0x88]
    2682:	00 
    2683:	4c 89 e8             	mov    rax,r13
    2686:	b9 12 00 00 00       	mov    ecx,0x12
    268b:	48 89 d7             	mov    rdi,rdx
    268e:	48 8d b4 24 80 00 00 	lea    rsi,[rsp+0x80]
    2695:	00 
    2696:	31 d2                	xor    edx,edx
    2698:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    269b:	48 8d 05 7e 02 00 00 	lea    rax,[rip+0x27e]        # 2920 <socket@plt+0x350>
    26a2:	bf 11 00 00 00       	mov    edi,0x11
    26a7:	c7 84 24 08 01 00 00 	mov    DWORD PTR [rsp+0x108],0x10000001
    26ae:	01 00 00 10 
    26b2:	48 89 84 24 80 00 00 	mov    QWORD PTR [rsp+0x80],rax
    26b9:	00 
    26ba:	e8 d1 fc ff ff       	call   2390 <sigaction@plt>
    26bf:	48 8d 3d 58 39 00 00 	lea    rdi,[rip+0x3958]        # 601e <socket@plt+0x3a4e>
    26c6:	e8 45 fc ff ff       	call   2310 <getenv@plt>
    26cb:	be ed 01 00 00       	mov    esi,0x1ed
    26d0:	48 8d 3d 4f 39 00 00 	lea    rdi,[rip+0x394f]        # 6026 <socket@plt+0x3a56>
    26d7:	48 85 c0             	test   rax,rax
    26da:	48 89 c3             	mov    rbx,rax
    26dd:	48 8d 05 20 39 00 00 	lea    rax,[rip+0x3920]        # 6004 <socket@plt+0x3a34>
    26e4:	48 0f 44 d8          	cmove  rbx,rax
    26e8:	e8 93 fc ff ff       	call   2380 <mkdir@plt>
    26ed:	48 89 df             	mov    rdi,rbx
    26f0:	e8 4b fc ff ff       	call   2340 <unlink@plt>
    26f5:	e8 16 14 00 00       	call   3b10 <socket@plt+0x1540>
    26fa:	e8 d1 14 00 00       	call   3bd0 <socket@plt+0x1600>
    26ff:	e8 ec 16 00 00       	call   3df0 <socket@plt+0x1820>
    2704:	e8 b7 1c 00 00       	call   43c0 <socket@plt+0x1df0>
    2709:	e8 f2 1a 00 00       	call   4200 <socket@plt+0x1c30>
    270e:	31 d2                	xor    edx,edx
    2710:	be 01 00 00 00       	mov    esi,0x1
    2715:	bf 01 00 00 00       	mov    edi,0x1
    271a:	e8 b1 fe ff ff       	call   25d0 <socket@plt>
    271f:	85 c0                	test   eax,eax
    2721:	0f 88 b9 fe ff ff    	js     25e0 <socket@plt+0x10>
    2727:	4c 8d 44 24 12       	lea    r8,[rsp+0x12]
    272c:	48 8d 7c 24 18       	lea    rdi,[rsp+0x18]
    2731:	89 c5                	mov    ebp,eax
    2733:	4c 89 e8             	mov    rax,r13
    2736:	4c 89 c1             	mov    rcx,r8
    2739:	ba 6b 00 00 00       	mov    edx,0x6b
    273e:	4c 8d 64 24 10       	lea    r12,[rsp+0x10]
    2743:	48 89 de             	mov    rsi,rbx
    2746:	48 c7 44 24 12 00 00 	mov    QWORD PTR [rsp+0x12],0x0
    274d:	00 00 
    274f:	48 29 f9             	sub    rcx,rdi
    2752:	48 c7 44 24 76 00 00 	mov    QWORD PTR [rsp+0x76],0x0
    2759:	00 00 
    275b:	83 c1 6c             	add    ecx,0x6c
    275e:	c1 e9 03             	shr    ecx,0x3
    2761:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    2764:	b8 01 00 00 00       	mov    eax,0x1
    2769:	4c 89 c7             	mov    rdi,r8
    276c:	66 89 44 24 10       	mov    WORD PTR [rsp+0x10],ax
    2771:	e8 da fb ff ff       	call   2350 <strncpy@plt>
    2776:	ba 6e 00 00 00       	mov    edx,0x6e
    277b:	4c 89 e6             	mov    rsi,r12
    277e:	89 ef                	mov    edi,ebp
    2780:	e8 7b fd ff ff       	call   2500 <bind@plt>
    2785:	85 c0                	test   eax,eax
    2787:	0f 88 93 fe ff ff    	js     2620 <socket@plt+0x50>
    278d:	be b6 01 00 00       	mov    esi,0x1b6
    2792:	48 89 df             	mov    rdi,rbx
    2795:	e8 56 fd ff ff       	call   24f0 <chmod@plt>
    279a:	be 08 00 00 00       	mov    esi,0x8
    279f:	89 ef                	mov    edi,ebp
    27a1:	e8 3a fd ff ff       	call   24e0 <listen@plt>
    27a6:	85 c0                	test   eax,eax
    27a8:	0f 88 64 fe ff ff    	js     2612 <socket@plt+0x42>
    27ae:	66 90                	xchg   ax,ax
    27b0:	31 d2                	xor    edx,edx
    27b2:	31 f6                	xor    esi,esi
    27b4:	89 ef                	mov    edi,ebp
    27b6:	e8 a5 fd ff ff       	call   2560 <accept@plt>
    27bb:	89 c3                	mov    ebx,eax
    27bd:	85 c0                	test   eax,eax
    27bf:	78 ef                	js     27b0 <socket@plt+0x1e0>
    27c1:	e8 ea fd ff ff       	call   25b0 <fork@plt>
    27c6:	85 c0                	test   eax,eax
    27c8:	74 0e                	je     27d8 <socket@plt+0x208>
    27ca:	89 df                	mov    edi,ebx
    27cc:	e8 5f fc ff ff       	call   2430 <close@plt>
    27d1:	eb dd                	jmp    27b0 <socket@plt+0x1e0>
    27d3:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    27d8:	31 f6                	xor    esi,esi
    27da:	bf 11 00 00 00       	mov    edi,0x11
    27df:	e8 9c fc ff ff       	call   2480 <signal@plt>
    27e4:	89 ef                	mov    edi,ebp
    27e6:	e8 45 fc ff ff       	call   2430 <close@plt>
    27eb:	48 89 e1             	mov    rcx,rsp
    27ee:	41 b8 10 00 00 00    	mov    r8d,0x10
    27f4:	89 df                	mov    edi,ebx
    27f6:	66 0f 6f 05 32 3e 00 	movdqa xmm0,XMMWORD PTR [rip+0x3e32]        # 6630 <socket@plt+0x4060>
    27fd:	00 
    27fe:	ba 14 00 00 00       	mov    edx,0x14
    2803:	be 01 00 00 00       	mov    esi,0x1
    2808:	0f 29 04 24          	movaps XMMWORD PTR [rsp],xmm0
    280c:	e8 9f fb ff ff       	call   23b0 <setsockopt@plt>
    2811:	89 df                	mov    edi,ebx
    2813:	e8 08 0e 00 00       	call   3620 <socket@plt+0x1050>
    2818:	89 df                	mov    edi,ebx
    281a:	e8 11 fc ff ff       	call   2430 <close@plt>
    281f:	31 ff                	xor    edi,edi
    2821:	e8 3a fb ff ff       	call   2360 <_exit@plt>
    2826:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    282d:	00 00 00 
    2830:	f3 0f 1e fa          	endbr64
    2834:	31 ed                	xor    ebp,ebp
    2836:	49 89 d1             	mov    r9,rdx
    2839:	5e                   	pop    rsi
    283a:	48 89 e2             	mov    rdx,rsp
    283d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    2841:	50                   	push   rax
    2842:	54                   	push   rsp
    2843:	45 31 c0             	xor    r8d,r8d
    2846:	31 c9                	xor    ecx,ecx
    2848:	48 8d 3d f1 fd ff ff 	lea    rdi,[rip+0xfffffffffffffdf1]        # 2640 <socket@plt+0x70>
    284f:	ff 15 83 97 00 00    	call   QWORD PTR [rip+0x9783]        # bfd8 <socket@plt+0x9a08>
    2855:	f4                   	hlt
    2856:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    285d:	00 00 00 
    2860:	48 8d 3d b1 97 00 00 	lea    rdi,[rip+0x97b1]        # c018 <socket@plt+0x9a48>
    2867:	48 8d 05 aa 97 00 00 	lea    rax,[rip+0x97aa]        # c018 <socket@plt+0x9a48>
    286e:	48 39 f8             	cmp    rax,rdi
    2871:	74 15                	je     2888 <socket@plt+0x2b8>
    2873:	48 8b 05 66 97 00 00 	mov    rax,QWORD PTR [rip+0x9766]        # bfe0 <socket@plt+0x9a10>
    287a:	48 85 c0             	test   rax,rax
    287d:	74 09                	je     2888 <socket@plt+0x2b8>
    287f:	ff e0                	jmp    rax
    2881:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    2888:	c3                   	ret
    2889:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    2890:	48 8d 3d 81 97 00 00 	lea    rdi,[rip+0x9781]        # c018 <socket@plt+0x9a48>
    2897:	48 8d 35 7a 97 00 00 	lea    rsi,[rip+0x977a]        # c018 <socket@plt+0x9a48>
    289e:	48 29 fe             	sub    rsi,rdi
    28a1:	48 89 f0             	mov    rax,rsi
    28a4:	48 c1 ee 3f          	shr    rsi,0x3f
    28a8:	48 c1 f8 03          	sar    rax,0x3
    28ac:	48 01 c6             	add    rsi,rax
    28af:	48 d1 fe             	sar    rsi,1
    28b2:	74 14                	je     28c8 <socket@plt+0x2f8>
    28b4:	48 8b 05 35 97 00 00 	mov    rax,QWORD PTR [rip+0x9735]        # bff0 <socket@plt+0x9a20>
    28bb:	48 85 c0             	test   rax,rax
    28be:	74 08                	je     28c8 <socket@plt+0x2f8>
    28c0:	ff e0                	jmp    rax
    28c2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    28c8:	c3                   	ret
    28c9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    28d0:	f3 0f 1e fa          	endbr64
    28d4:	80 3d 45 97 00 00 00 	cmp    BYTE PTR [rip+0x9745],0x0        # c020 <socket@plt+0x9a50>
    28db:	75 2b                	jne    2908 <socket@plt+0x338>
    28dd:	55                   	push   rbp
    28de:	48 83 3d 12 97 00 00 	cmp    QWORD PTR [rip+0x9712],0x0        # bff8 <socket@plt+0x9a28>
    28e5:	00 
    28e6:	48 89 e5             	mov    rbp,rsp
    28e9:	74 0c                	je     28f7 <socket@plt+0x327>
    28eb:	48 8b 3d 16 97 00 00 	mov    rdi,QWORD PTR [rip+0x9716]        # c008 <socket@plt+0x9a38>
    28f2:	e8 09 fa ff ff       	call   2300 <__cxa_finalize@plt>
    28f7:	e8 64 ff ff ff       	call   2860 <socket@plt+0x290>
    28fc:	c6 05 1d 97 00 00 01 	mov    BYTE PTR [rip+0x971d],0x1        # c020 <socket@plt+0x9a50>
    2903:	5d                   	pop    rbp
    2904:	c3                   	ret
    2905:	0f 1f 00             	nop    DWORD PTR [rax]
    2908:	c3                   	ret
    2909:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    2910:	f3 0f 1e fa          	endbr64
    2914:	e9 77 ff ff ff       	jmp    2890 <socket@plt+0x2c0>
    2919:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    2920:	f3 0f 1e fa          	endbr64
    2924:	48 83 ec 08          	sub    rsp,0x8
    2928:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
    292f:	00 
    2930:	31 f6                	xor    esi,esi
    2932:	ba 01 00 00 00       	mov    edx,0x1
    2937:	bf ff ff ff ff       	mov    edi,0xffffffff
    293c:	e8 cf fb ff ff       	call   2510 <waitpid@plt>
    2941:	85 c0                	test   eax,eax
    2943:	7f eb                	jg     2930 <socket@plt+0x360>
    2945:	48 83 c4 08          	add    rsp,0x8
    2949:	c3                   	ret
    294a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    2950:	f3 0f 1e fa          	endbr64
    2954:	48 85 d2             	test   rdx,rdx
    2957:	74 54                	je     29ad <socket@plt+0x3dd>
    2959:	41 55                	push   r13
    295b:	49 89 f5             	mov    r13,rsi
    295e:	41 54                	push   r12
    2960:	41 89 fc             	mov    r12d,edi
    2963:	55                   	push   rbp
    2964:	48 89 d5             	mov    rbp,rdx
    2967:	53                   	push   rbx
    2968:	31 db                	xor    ebx,ebx
    296a:	48 83 ec 08          	sub    rsp,0x8
    296e:	eb 08                	jmp    2978 <socket@plt+0x3a8>
    2970:	48 01 c3             	add    rbx,rax
    2973:	48 39 eb             	cmp    rbx,rbp
    2976:	73 28                	jae    29a0 <socket@plt+0x3d0>
    2978:	48 89 ea             	mov    rdx,rbp
    297b:	49 8d 74 1d 00       	lea    rsi,[r13+rbx*1+0x0]
    2980:	44 89 e7             	mov    edi,r12d
    2983:	48 29 da             	sub    rdx,rbx
    2986:	e8 b5 fa ff ff       	call   2440 <read@plt>
    298b:	48 85 c0             	test   rax,rax
    298e:	7f e0                	jg     2970 <socket@plt+0x3a0>
    2990:	48 83 c4 08          	add    rsp,0x8
    2994:	b8 ff ff ff ff       	mov    eax,0xffffffff
    2999:	5b                   	pop    rbx
    299a:	5d                   	pop    rbp
    299b:	41 5c                	pop    r12
    299d:	41 5d                	pop    r13
    299f:	c3                   	ret
    29a0:	48 83 c4 08          	add    rsp,0x8
    29a4:	31 c0                	xor    eax,eax
    29a6:	5b                   	pop    rbx
    29a7:	5d                   	pop    rbp
    29a8:	41 5c                	pop    r12
    29aa:	41 5d                	pop    r13
    29ac:	c3                   	ret
    29ad:	31 c0                	xor    eax,eax
    29af:	c3                   	ret
    29b0:	f3 0f 1e fa          	endbr64
    29b4:	53                   	push   rbx
    29b5:	48 89 d3             	mov    rbx,rdx
    29b8:	e8 13 fa ff ff       	call   23d0 <write@plt>
    29bd:	48 39 c3             	cmp    rbx,rax
    29c0:	5b                   	pop    rbx
    29c1:	0f 95 c0             	setne  al
    29c4:	0f b6 c0             	movzx  eax,al
    29c7:	f7 d8                	neg    eax
    29c9:	c3                   	ret
    29ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    29d0:	f3 0f 1e fa          	endbr64
    29d4:	48 85 d2             	test   rdx,rdx
    29d7:	74 27                	je     2a00 <socket@plt+0x430>
    29d9:	31 c9                	xor    ecx,ecx
    29db:	31 c0                	xor    eax,eax
    29dd:	0f 1f 00             	nop    DWORD PTR [rax]
    29e0:	44 0f b6 04 0f       	movzx  r8d,BYTE PTR [rdi+rcx*1]
    29e5:	44 32 04 0e          	xor    r8b,BYTE PTR [rsi+rcx*1]
    29e9:	48 83 c1 01          	add    rcx,0x1
    29ed:	44 09 c0             	or     eax,r8d
    29f0:	48 39 ca             	cmp    rdx,rcx
    29f3:	75 eb                	jne    29e0 <socket@plt+0x410>
    29f5:	0f b6 c0             	movzx  eax,al
    29f8:	c3                   	ret
    29f9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    2a00:	31 c0                	xor    eax,eax
    2a02:	c3                   	ret
    2a03:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    2a0a:	00 00 00 00 
    2a0e:	66 90                	xchg   ax,ax
    2a10:	f3 0f 1e fa          	endbr64
    2a14:	41 55                	push   r13
    2a16:	49 89 f5             	mov    r13,rsi
    2a19:	41 54                	push   r12
    2a1b:	49 89 cc             	mov    r12,rcx
    2a1e:	55                   	push   rbp
    2a1f:	48 89 d5             	mov    rbp,rdx
    2a22:	ba 03 00 00 00       	mov    edx,0x3
    2a27:	53                   	push   rbx
    2a28:	89 fb                	mov    ebx,edi
    2a2a:	48 83 ec 18          	sub    rsp,0x18
    2a2e:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    2a35:	00 00 
    2a37:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
    2a3c:	31 c0                	xor    eax,eax
    2a3e:	48 8d 74 24 05       	lea    rsi,[rsp+0x5]
    2a43:	e8 08 ff ff ff       	call   2950 <socket@plt+0x380>
    2a48:	85 c0                	test   eax,eax
    2a4a:	75 54                	jne    2aa0 <socket@plt+0x4d0>
    2a4c:	0f b6 54 24 05       	movzx  edx,BYTE PTR [rsp+0x5]
    2a51:	41 88 55 00          	mov    BYTE PTR [r13+0x0],dl
    2a55:	0f b7 54 24 06       	movzx  edx,WORD PTR [rsp+0x6]
    2a5a:	66 41 89 14 24       	mov    WORD PTR [r12],dx
    2a5f:	66 81 fa 40 01       	cmp    dx,0x140
    2a64:	77 3a                	ja     2aa0 <socket@plt+0x4d0>
    2a66:	66 85 d2             	test   dx,dx
    2a69:	75 25                	jne    2a90 <socket@plt+0x4c0>
    2a6b:	48 8b 54 24 08       	mov    rdx,QWORD PTR [rsp+0x8]
    2a70:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    2a77:	00 00 
    2a79:	75 2c                	jne    2aa7 <socket@plt+0x4d7>
    2a7b:	48 83 c4 18          	add    rsp,0x18
    2a7f:	5b                   	pop    rbx
    2a80:	5d                   	pop    rbp
    2a81:	41 5c                	pop    r12
    2a83:	41 5d                	pop    r13
    2a85:	c3                   	ret
    2a86:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    2a8d:	00 00 00 
    2a90:	48 89 ee             	mov    rsi,rbp
    2a93:	89 df                	mov    edi,ebx
    2a95:	e8 b6 fe ff ff       	call   2950 <socket@plt+0x380>
    2a9a:	f7 d8                	neg    eax
    2a9c:	19 c0                	sbb    eax,eax
    2a9e:	eb cb                	jmp    2a6b <socket@plt+0x49b>
    2aa0:	b8 ff ff ff ff       	mov    eax,0xffffffff
    2aa5:	eb c4                	jmp    2a6b <socket@plt+0x49b>
    2aa7:	e8 54 f9 ff ff       	call   2400 <__stack_chk_fail@plt>
    2aac:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    2ab0:	f3 0f 1e fa          	endbr64
    2ab4:	41 54                	push   r12
    2ab6:	49 89 d4             	mov    r12,rdx
    2ab9:	ba 03 00 00 00       	mov    edx,0x3
    2abe:	55                   	push   rbp
    2abf:	89 fd                	mov    ebp,edi
    2ac1:	53                   	push   rbx
    2ac2:	89 cb                	mov    ebx,ecx
    2ac4:	48 83 ec 10          	sub    rsp,0x10
    2ac8:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    2acf:	00 00 
    2ad1:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
    2ad6:	31 c0                	xor    eax,eax
    2ad8:	40 88 74 24 05       	mov    BYTE PTR [rsp+0x5],sil
    2add:	48 8d 74 24 05       	lea    rsi,[rsp+0x5]
    2ae2:	66 89 4c 24 06       	mov    WORD PTR [rsp+0x6],cx
    2ae7:	e8 e4 f8 ff ff       	call   23d0 <write@plt>
    2aec:	48 83 f8 03          	cmp    rax,0x3
    2af0:	75 46                	jne    2b38 <socket@plt+0x568>
    2af2:	31 c0                	xor    eax,eax
    2af4:	66 85 db             	test   bx,bx
    2af7:	75 1f                	jne    2b18 <socket@plt+0x548>
    2af9:	48 8b 54 24 08       	mov    rdx,QWORD PTR [rsp+0x8]
    2afe:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    2b05:	00 00 
    2b07:	75 36                	jne    2b3f <socket@plt+0x56f>
    2b09:	48 83 c4 10          	add    rsp,0x10
    2b0d:	5b                   	pop    rbx
    2b0e:	5d                   	pop    rbp
    2b0f:	41 5c                	pop    r12
    2b11:	c3                   	ret
    2b12:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    2b18:	0f b7 db             	movzx  ebx,bx
    2b1b:	4c 89 e6             	mov    rsi,r12
    2b1e:	89 ef                	mov    edi,ebp
    2b20:	48 89 da             	mov    rdx,rbx
    2b23:	e8 a8 f8 ff ff       	call   23d0 <write@plt>
    2b28:	48 39 c3             	cmp    rbx,rax
    2b2b:	0f 95 c0             	setne  al
    2b2e:	0f b6 c0             	movzx  eax,al
    2b31:	f7 d8                	neg    eax
    2b33:	eb c4                	jmp    2af9 <socket@plt+0x529>
    2b35:	0f 1f 00             	nop    DWORD PTR [rax]
    2b38:	b8 ff ff ff ff       	mov    eax,0xffffffff
    2b3d:	eb ba                	jmp    2af9 <socket@plt+0x529>
    2b3f:	e8 bc f8 ff ff       	call   2400 <__stack_chk_fail@plt>
    2b44:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    2b4b:	00 00 00 00 
    2b4f:	90                   	nop
    2b50:	f3 0f 1e fa          	endbr64
    2b54:	40 80 ff 10          	cmp    dil,0x10
    2b58:	77 16                	ja     2b70 <socket@plt+0x5a0>
    2b5a:	40 0f b6 ff          	movzx  edi,dil
    2b5e:	48 8d 05 7b 90 00 00 	lea    rax,[rip+0x907b]        # bbe0 <socket@plt+0x9610>
    2b65:	48 8b 04 f8          	mov    rax,QWORD PTR [rax+rdi*8]
    2b69:	c3                   	ret
    2b6a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    2b70:	31 c0                	xor    eax,eax
    2b72:	c3                   	ret
    2b73:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    2b7a:	00 00 00 
    2b7d:	0f 1f 00             	nop    DWORD PTR [rax]
    2b80:	41 54                	push   r12
    2b82:	41 89 f9             	mov    r9d,edi
    2b85:	be 40 00 00 00       	mov    esi,0x40
    2b8a:	b9 40 00 00 00       	mov    ecx,0x40
    2b8f:	55                   	push   rbp
    2b90:	4c 8d 05 af 34 00 00 	lea    r8,[rip+0x34af]        # 6046 <socket@plt+0x3a76>
    2b97:	ba 02 00 00 00       	mov    edx,0x2
    2b9c:	53                   	push   rbx
    2b9d:	48 81 ec 50 04 00 00 	sub    rsp,0x450
    2ba4:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    2bab:	00 00 
    2bad:	48 89 84 24 48 04 00 	mov    QWORD PTR [rsp+0x448],rax
    2bb4:	00 
    2bb5:	31 c0                	xor    eax,eax
    2bb7:	48 89 e3             	mov    rbx,rsp
    2bba:	48 89 df             	mov    rdi,rbx
    2bbd:	e8 5e f7 ff ff       	call   2320 <__snprintf_chk@plt>
    2bc2:	31 f6                	xor    esi,esi
    2bc4:	31 c0                	xor    eax,eax
    2bc6:	48 89 df             	mov    rdi,rbx
    2bc9:	e8 52 f9 ff ff       	call   2520 <open@plt>
    2bce:	85 c0                	test   eax,eax
    2bd0:	78 5e                	js     2c30 <socket@plt+0x660>
    2bd2:	4c 8d 64 24 40       	lea    r12,[rsp+0x40]
    2bd7:	89 c7                	mov    edi,eax
    2bd9:	ba ff 03 00 00       	mov    edx,0x3ff
    2bde:	89 c3                	mov    ebx,eax
    2be0:	4c 89 e6             	mov    rsi,r12
    2be3:	e8 58 f8 ff ff       	call   2440 <read@plt>
    2be8:	89 df                	mov    edi,ebx
    2bea:	48 89 c5             	mov    rbp,rax
    2bed:	e8 3e f8 ff ff       	call   2430 <close@plt>
    2bf2:	48 85 ed             	test   rbp,rbp
    2bf5:	7e 39                	jle    2c30 <socket@plt+0x660>
    2bf7:	be 2f 00 00 00       	mov    esi,0x2f
    2bfc:	4c 89 e7             	mov    rdi,r12
    2bff:	c6 44 2c 40 00       	mov    BYTE PTR [rsp+rbp*1+0x40],0x0
    2c04:	e8 17 f8 ff ff       	call   2420 <strrchr@plt>
    2c09:	48 8d 35 47 34 00 00 	lea    rsi,[rip+0x3447]        # 6057 <socket@plt+0x3a87>
    2c10:	48 85 c0             	test   rax,rax
    2c13:	48 8d 78 01          	lea    rdi,[rax+0x1]
    2c17:	49 0f 44 fc          	cmove  rdi,r12
    2c1b:	e8 50 f8 ff ff       	call   2470 <strcmp@plt>
    2c20:	85 c0                	test   eax,eax
    2c22:	0f 94 c0             	sete   al
    2c25:	0f b6 c0             	movzx  eax,al
    2c28:	eb 08                	jmp    2c32 <socket@plt+0x662>
    2c2a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    2c30:	31 c0                	xor    eax,eax
    2c32:	48 8b 94 24 48 04 00 	mov    rdx,QWORD PTR [rsp+0x448]
    2c39:	00 
    2c3a:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    2c41:	00 00 
    2c43:	75 0c                	jne    2c51 <socket@plt+0x681>
    2c45:	48 81 c4 50 04 00 00 	add    rsp,0x450
    2c4c:	5b                   	pop    rbx
    2c4d:	5d                   	pop    rbp
    2c4e:	41 5c                	pop    r12
    2c50:	c3                   	ret
    2c51:	e8 aa f7 ff ff       	call   2400 <__stack_chk_fail@plt>
    2c56:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    2c5d:	00 00 00 
    2c60:	f3 0f 1e fa          	endbr64
    2c64:	31 c0                	xor    eax,eax
    2c66:	66 0f ef c0          	pxor   xmm0,xmm0
    2c6a:	c7 07 00 00 00 00    	mov    DWORD PTR [rdi],0x0
    2c70:	66 89 47 14          	mov    WORD PTR [rdi+0x14],ax
    2c74:	0f 11 47 04          	movups XMMWORD PTR [rdi+0x4],xmm0
    2c78:	c3                   	ret
    2c79:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    2c80:	f3 0f 1e fa          	endbr64
    2c84:	48 83 ec 18          	sub    rsp,0x18
    2c88:	48 89 f8             	mov    rax,rdi
    2c8b:	89 f7                	mov    edi,esi
    2c8d:	64 48 8b 34 25 28 00 	mov    rsi,QWORD PTR fs:0x28
    2c94:	00 00 
    2c96:	48 89 74 24 08       	mov    QWORD PTR [rsp+0x8],rsi
    2c9b:	31 f6                	xor    esi,esi
    2c9d:	66 83 f9 03          	cmp    cx,0x3
    2ca1:	76 4d                	jbe    2cf0 <socket@plt+0x720>
    2ca3:	0f b7 52 02          	movzx  edx,WORD PTR [rdx+0x2]
    2ca7:	83 e2 06             	and    edx,0x6
    2caa:	89 d1                	mov    ecx,edx
    2cac:	66 89 50 14          	mov    WORD PTR [rax+0x14],dx
    2cb0:	be 02 00 00 00       	mov    esi,0x2
    2cb5:	b8 03 01 00 00       	mov    eax,0x103
    2cba:	48 8d 54 24 04       	lea    rdx,[rsp+0x4]
    2cbf:	88 4c 24 06          	mov    BYTE PTR [rsp+0x6],cl
    2cc3:	b9 04 00 00 00       	mov    ecx,0x4
    2cc8:	66 89 44 24 04       	mov    WORD PTR [rsp+0x4],ax
    2ccd:	c6 44 24 07 00       	mov    BYTE PTR [rsp+0x7],0x0
    2cd2:	e8 d9 fd ff ff       	call   2ab0 <socket@plt+0x4e0>
    2cd7:	f7 d8                	neg    eax
    2cd9:	19 c0                	sbb    eax,eax
    2cdb:	48 8b 54 24 08       	mov    rdx,QWORD PTR [rsp+0x8]
    2ce0:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    2ce7:	00 00 
    2ce9:	75 0b                	jne    2cf6 <socket@plt+0x726>
    2ceb:	48 83 c4 18          	add    rsp,0x18
    2cef:	c3                   	ret
    2cf0:	31 c9                	xor    ecx,ecx
    2cf2:	31 d2                	xor    edx,edx
    2cf4:	eb b6                	jmp    2cac <socket@plt+0x6dc>
    2cf6:	e8 05 f7 ff ff       	call   2400 <__stack_chk_fail@plt>
    2cfb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    2d00:	f3 0f 1e fa          	endbr64
    2d04:	55                   	push   rbp
    2d05:	89 f5                	mov    ebp,esi
    2d07:	53                   	push   rbx
    2d08:	48 83 ec 08          	sub    rsp,0x8
    2d0c:	66 83 f9 10          	cmp    cx,0x10
    2d10:	74 1e                	je     2d30 <socket@plt+0x760>
    2d12:	48 8d 15 4e 33 00 00 	lea    rdx,[rip+0x334e]        # 6067 <socket@plt+0x3a97>
    2d19:	be 02 00 00 00       	mov    esi,0x2
    2d1e:	89 ef                	mov    edi,ebp
    2d20:	31 c0                	xor    eax,eax
    2d22:	e8 29 f8 ff ff       	call   2550 <__dprintf_chk@plt>
    2d27:	31 c0                	xor    eax,eax
    2d29:	48 83 c4 08          	add    rsp,0x8
    2d2d:	5b                   	pop    rbx
    2d2e:	5d                   	pop    rbp
    2d2f:	c3                   	ret
    2d30:	48 8d 5f 04          	lea    rbx,[rdi+0x4]
    2d34:	31 d2                	xor    edx,edx
    2d36:	be 10 00 00 00       	mov    esi,0x10
    2d3b:	48 89 df             	mov    rdi,rbx
    2d3e:	e8 5d f8 ff ff       	call   25a0 <getrandom@plt>
    2d43:	48 83 f8 10          	cmp    rax,0x10
    2d47:	75 27                	jne    2d70 <socket@plt+0x7a0>
    2d49:	48 89 da             	mov    rdx,rbx
    2d4c:	89 ef                	mov    edi,ebp
    2d4e:	b9 10 00 00 00       	mov    ecx,0x10
    2d53:	be 04 00 00 00       	mov    esi,0x4
    2d58:	e8 53 fd ff ff       	call   2ab0 <socket@plt+0x4e0>
    2d5d:	f7 d8                	neg    eax
    2d5f:	19 c0                	sbb    eax,eax
    2d61:	48 83 c4 08          	add    rsp,0x8
    2d65:	5b                   	pop    rbx
    2d66:	5d                   	pop    rbp
    2d67:	c3                   	ret
    2d68:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
    2d6f:	00 
    2d70:	b8 ff ff ff ff       	mov    eax,0xffffffff
    2d75:	eb b2                	jmp    2d29 <socket@plt+0x759>
    2d77:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    2d7e:	00 00 
    2d80:	f3 0f 1e fa          	endbr64
    2d84:	41 55                	push   r13
    2d86:	41 54                	push   r12
    2d88:	55                   	push   rbp
    2d89:	53                   	push   rbx
    2d8a:	89 f3                	mov    ebx,esi
    2d8c:	48 83 ec 28          	sub    rsp,0x28
    2d90:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    2d97:	00 00 
    2d99:	48 89 44 24 18       	mov    QWORD PTR [rsp+0x18],rax
    2d9e:	31 c0                	xor    eax,eax
    2da0:	66 83 f9 10          	cmp    cx,0x10
    2da4:	75 4a                	jne    2df0 <socket@plt+0x820>
    2da6:	49 89 e5             	mov    r13,rsp
    2da9:	49 89 d4             	mov    r12,rdx
    2dac:	be 10 00 00 00       	mov    esi,0x10
    2db1:	48 89 fd             	mov    rbp,rdi
    2db4:	4c 89 ea             	mov    rdx,r13
    2db7:	48 8d 7f 04          	lea    rdi,[rdi+0x4]
    2dbb:	e8 20 2a 00 00       	call   57e0 <socket@plt+0x3210>
    2dc0:	ba 10 00 00 00       	mov    edx,0x10
    2dc5:	4c 89 e6             	mov    rsi,r12
    2dc8:	4c 89 ef             	mov    rdi,r13
    2dcb:	e8 00 fc ff ff       	call   29d0 <socket@plt+0x400>
    2dd0:	85 c0                	test   eax,eax
    2dd2:	75 1c                	jne    2df0 <socket@plt+0x820>
    2dd4:	c7 45 00 01 00 00 00 	mov    DWORD PTR [rbp+0x0],0x1
    2ddb:	48 8d 15 a6 32 00 00 	lea    rdx,[rip+0x32a6]        # 6088 <socket@plt+0x3ab8>
    2de2:	be 02 00 00 00       	mov    esi,0x2
    2de7:	89 df                	mov    edi,ebx
    2de9:	e8 62 f7 ff ff       	call   2550 <__dprintf_chk@plt>
    2dee:	eb 15                	jmp    2e05 <socket@plt+0x835>
    2df0:	48 8d 15 7f 32 00 00 	lea    rdx,[rip+0x327f]        # 6076 <socket@plt+0x3aa6>
    2df7:	be 02 00 00 00       	mov    esi,0x2
    2dfc:	89 df                	mov    edi,ebx
    2dfe:	31 c0                	xor    eax,eax
    2e00:	e8 4b f7 ff ff       	call   2550 <__dprintf_chk@plt>
    2e05:	48 8b 44 24 18       	mov    rax,QWORD PTR [rsp+0x18]
    2e0a:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    2e11:	00 00 
    2e13:	75 0d                	jne    2e22 <socket@plt+0x852>
    2e15:	48 83 c4 28          	add    rsp,0x28
    2e19:	31 c0                	xor    eax,eax
    2e1b:	5b                   	pop    rbx
    2e1c:	5d                   	pop    rbp
    2e1d:	41 5c                	pop    r12
    2e1f:	41 5d                	pop    r13
    2e21:	c3                   	ret
    2e22:	e8 d9 f5 ff ff       	call   2400 <__stack_chk_fail@plt>
    2e27:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    2e2e:	00 00 
    2e30:	f3 0f 1e fa          	endbr64
    2e34:	55                   	push   rbp
    2e35:	89 f5                	mov    ebp,esi
    2e37:	53                   	push   rbx
    2e38:	48 83 ec 08          	sub    rsp,0x8
    2e3c:	8b 07                	mov    eax,DWORD PTR [rdi]
    2e3e:	85 c0                	test   eax,eax
    2e40:	7e 6e                	jle    2eb0 <socket@plt+0x8e0>
    2e42:	66 83 f9 10          	cmp    cx,0x10
    2e46:	75 48                	jne    2e90 <socket@plt+0x8c0>
    2e48:	48 89 fb             	mov    rbx,rdi
    2e4b:	8b 3a                	mov    edi,DWORD PTR [rdx]
    2e4d:	e8 2e fd ff ff       	call   2b80 <socket@plt+0x5b0>
    2e52:	85 c0                	test   eax,eax
    2e54:	74 7a                	je     2ed0 <socket@plt+0x900>
    2e56:	c7 03 02 00 00 00    	mov    DWORD PTR [rbx],0x2
    2e5c:	be 02 00 00 00       	mov    esi,0x2
    2e61:	89 ef                	mov    edi,ebp
    2e63:	31 c0                	xor    eax,eax
    2e65:	48 8d 15 6b 32 00 00 	lea    rdx,[rip+0x326b]        # 60d7 <socket@plt+0x3b07>
    2e6c:	e8 df f6 ff ff       	call   2550 <__dprintf_chk@plt>
    2e71:	89 ef                	mov    edi,ebp
    2e73:	e8 98 11 00 00       	call   4010 <socket@plt+0x1a40>
    2e78:	bf 06 00 00 00       	mov    edi,0x6
    2e7d:	e8 5e 17 00 00       	call   45e0 <socket@plt+0x2010>
    2e82:	e8 b9 18 00 00       	call   4740 <socket@plt+0x2170>
    2e87:	48 83 c4 08          	add    rsp,0x8
    2e8b:	31 c0                	xor    eax,eax
    2e8d:	5b                   	pop    rbx
    2e8e:	5d                   	pop    rbp
    2e8f:	c3                   	ret
    2e90:	89 ef                	mov    edi,ebp
    2e92:	48 8d 15 18 32 00 00 	lea    rdx,[rip+0x3218]        # 60b1 <socket@plt+0x3ae1>
    2e99:	be 02 00 00 00       	mov    esi,0x2
    2e9e:	31 c0                	xor    eax,eax
    2ea0:	e8 ab f6 ff ff       	call   2550 <__dprintf_chk@plt>
    2ea5:	48 83 c4 08          	add    rsp,0x8
    2ea9:	31 c0                	xor    eax,eax
    2eab:	5b                   	pop    rbx
    2eac:	5d                   	pop    rbp
    2ead:	c3                   	ret
    2eae:	66 90                	xchg   ax,ax
    2eb0:	89 ef                	mov    edi,ebp
    2eb2:	48 8d 15 e1 31 00 00 	lea    rdx,[rip+0x31e1]        # 609a <socket@plt+0x3aca>
    2eb9:	be 02 00 00 00       	mov    esi,0x2
    2ebe:	31 c0                	xor    eax,eax
    2ec0:	e8 8b f6 ff ff       	call   2550 <__dprintf_chk@plt>
    2ec5:	48 83 c4 08          	add    rsp,0x8
    2ec9:	31 c0                	xor    eax,eax
    2ecb:	5b                   	pop    rbx
    2ecc:	5d                   	pop    rbp
    2ecd:	c3                   	ret
    2ece:	66 90                	xchg   ax,ax
    2ed0:	89 ef                	mov    edi,ebp
    2ed2:	48 8d 15 ea 31 00 00 	lea    rdx,[rip+0x31ea]        # 60c3 <socket@plt+0x3af3>
    2ed9:	be 02 00 00 00       	mov    esi,0x2
    2ede:	e8 6d f6 ff ff       	call   2550 <__dprintf_chk@plt>
    2ee3:	48 83 c4 08          	add    rsp,0x8
    2ee7:	31 c0                	xor    eax,eax
    2ee9:	5b                   	pop    rbx
    2eea:	5d                   	pop    rbp
    2eeb:	c3                   	ret
    2eec:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    2ef0:	f3 0f 1e fa          	endbr64
    2ef4:	41 57                	push   r15
    2ef6:	41 56                	push   r14
    2ef8:	41 55                	push   r13
    2efa:	41 54                	push   r12
    2efc:	55                   	push   rbp
    2efd:	53                   	push   rbx
    2efe:	4c 8d 9c 24 00 c0 ff 	lea    r11,[rsp-0x4000]
    2f05:	ff 
    2f06:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    2f0d:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    2f12:	4c 39 dc             	cmp    rsp,r11
    2f15:	75 ef                	jne    2f06 <socket@plt+0x936>
    2f17:	48 81 ec e8 0d 00 00 	sub    rsp,0xde8
    2f1e:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    2f25:	00 00 
    2f27:	48 89 84 24 d8 4d 00 	mov    QWORD PTR [rsp+0x4dd8],rax
    2f2e:	00 
    2f2f:	31 c0                	xor    eax,eax
    2f31:	83 3f 01             	cmp    DWORD PTR [rdi],0x1
    2f34:	89 f5                	mov    ebp,esi
    2f36:	0f 8e 94 02 00 00    	jle    31d0 <socket@plt+0xc00>
    2f3c:	66 83 f9 02          	cmp    cx,0x2
    2f40:	76 1e                	jbe    2f60 <socket@plt+0x990>
    2f42:	48 89 d3             	mov    rbx,rdx
    2f45:	0f b6 12             	movzx  edx,BYTE PTR [rdx]
    2f48:	8d 42 ff             	lea    eax,[rdx-0x1]
    2f4b:	3c 2e                	cmp    al,0x2e
    2f4d:	77 11                	ja     2f60 <socket@plt+0x990>
    2f4f:	0f b6 c2             	movzx  eax,dl
    2f52:	0f b7 c9             	movzx  ecx,cx
    2f55:	8d 70 03             	lea    esi,[rax+0x3]
    2f58:	48 63 fe             	movsxd rdi,esi
    2f5b:	48 39 f9             	cmp    rcx,rdi
    2f5e:	73 40                	jae    2fa0 <socket@plt+0x9d0>
    2f60:	48 8d 15 7f 31 00 00 	lea    rdx,[rip+0x317f]        # 60e6 <socket@plt+0x3b16>
    2f67:	be 02 00 00 00       	mov    esi,0x2
    2f6c:	89 ef                	mov    edi,ebp
    2f6e:	31 c0                	xor    eax,eax
    2f70:	e8 db f5 ff ff       	call   2550 <__dprintf_chk@plt>
    2f75:	48 8b 84 24 d8 4d 00 	mov    rax,QWORD PTR [rsp+0x4dd8]
    2f7c:	00 
    2f7d:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    2f84:	00 00 
    2f86:	0f 85 b3 02 00 00    	jne    323f <socket@plt+0xc6f>
    2f8c:	48 81 c4 e8 4d 00 00 	add    rsp,0x4de8
    2f93:	31 c0                	xor    eax,eax
    2f95:	5b                   	pop    rbx
    2f96:	5d                   	pop    rbp
    2f97:	41 5c                	pop    r12
    2f99:	41 5d                	pop    r13
    2f9b:	41 5e                	pop    r14
    2f9d:	41 5f                	pop    r15
    2f9f:	c3                   	ret
    2fa0:	44 0f b6 ea          	movzx  r13d,dl
    2fa4:	4c 8d a4 24 a0 4c 00 	lea    r12,[rsp+0x4ca0]
    2fab:	00 
    2fac:	4c 8d 43 01          	lea    r8,[rbx+0x1]
    2fb0:	4d 89 e1             	mov    r9,r12
    2fb3:	4c 89 c2             	mov    rdx,r8
    2fb6:	41 83 fd 08          	cmp    r13d,0x8
    2fba:	0f 83 e0 01 00 00    	jae    31a0 <socket@plt+0xbd0>
    2fc0:	31 ff                	xor    edi,edi
    2fc2:	41 f6 c5 04          	test   r13b,0x4
    2fc6:	0f 85 b4 01 00 00    	jne    3180 <socket@plt+0xbb0>
    2fcc:	41 f6 c5 02          	test   r13b,0x2
    2fd0:	0f 85 8a 01 00 00    	jne    3160 <socket@plt+0xb90>
    2fd6:	41 f6 c5 01          	test   r13b,0x1
    2fda:	0f 85 70 01 00 00    	jne    3150 <socket@plt+0xb80>
    2fe0:	48 63 d0             	movsxd rdx,eax
    2fe3:	83 c0 01             	add    eax,0x1
    2fe6:	46 0f b6 74 2b 02    	movzx  r14d,BYTE PTR [rbx+r13*1+0x2]
    2fec:	48 98                	cdqe
    2fee:	c6 84 14 a0 4c 00 00 	mov    BYTE PTR [rsp+rdx*1+0x4ca0],0x0
    2ff5:	00 
    2ff6:	0f b6 04 03          	movzx  eax,BYTE PTR [rbx+rax*1]
    2ffa:	41 c1 e6 08          	shl    r14d,0x8
    2ffe:	41 09 c6             	or     r14d,eax
    3001:	41 0f b7 c6          	movzx  eax,r14w
    3005:	01 f0                	add    eax,esi
    3007:	48 98                	cdqe
    3009:	48 39 c8             	cmp    rax,rcx
    300c:	0f 85 4e ff ff ff    	jne    2f60 <socket@plt+0x990>
    3012:	66 41 81 fe ff 00    	cmp    r14w,0xff
    3018:	0f 87 42 ff ff ff    	ja     2f60 <socket@plt+0x990>
    301e:	48 b8 70 65 72 6d 61 	movabs rax,0x6e656e616d726570
    3025:	6e 65 6e 
    3028:	48 ba 74 5f 70 61 73 	movabs rdx,0x6f77737361705f74
    302f:	73 77 6f 
    3032:	48 33 84 24 a0 4c 00 	xor    rax,QWORD PTR [rsp+0x4ca0]
    3039:	00 
    303a:	48 33 94 24 a8 4c 00 	xor    rdx,QWORD PTR [rsp+0x4ca8]
    3041:	00 
    3042:	48 09 d0             	or     rax,rdx
    3045:	0f 84 a5 01 00 00    	je     31f0 <socket@plt+0xc20>
    304b:	4c 89 e7             	mov    rdi,r12
    304e:	e8 cd 07 00 00       	call   3820 <socket@plt+0x1250>
    3053:	41 89 c7             	mov    r15d,eax
    3056:	85 c0                	test   eax,eax
    3058:	0f 88 17 ff ff ff    	js     2f75 <socket@plt+0x9a5>
    305e:	89 c7                	mov    edi,eax
    3060:	e8 9b 07 00 00       	call   3800 <socket@plt+0x1230>
    3065:	f6 40 10 02          	test   BYTE PTR [rax+0x10],0x2
    3069:	0f 85 bb 00 00 00    	jne    312a <socket@plt+0xb5a>
    306f:	48 8d 7c 24 20       	lea    rdi,[rsp+0x20]
    3074:	48 89 44 24 10       	mov    QWORD PTR [rsp+0x10],rax
    3079:	48 89 7c 24 08       	mov    QWORD PTR [rsp+0x8],rdi
    307e:	e8 0d 0a 00 00       	call   3a90 <socket@plt+0x14c0>
    3083:	4d 0f bf ce          	movsx  r9,r14w
    3087:	48 8b 44 24 10       	mov    rax,QWORD PTR [rsp+0x10]
    308c:	4c 8d 84 24 d0 4c 00 	lea    r8,[rsp+0x4cd0]
    3093:	00 
    3094:	41 83 f9 08          	cmp    r9d,0x8
    3098:	4c 89 c7             	mov    rdi,r8
    309b:	4a 8d 74 2b 03       	lea    rsi,[rbx+r13*1+0x3]
    30a0:	72 09                	jb     30ab <socket@plt+0xadb>
    30a2:	44 89 c9             	mov    ecx,r9d
    30a5:	c1 e9 03             	shr    ecx,0x3
    30a8:	f3 48 a5             	rep movs QWORD PTR [rdi],QWORD PTR [rsi]
    30ab:	31 c9                	xor    ecx,ecx
    30ad:	41 f6 c1 04          	test   r9b,0x4
    30b1:	74 09                	je     30bc <socket@plt+0xaec>
    30b3:	8b 0e                	mov    ecx,DWORD PTR [rsi]
    30b5:	89 0f                	mov    DWORD PTR [rdi],ecx
    30b7:	b9 04 00 00 00       	mov    ecx,0x4
    30bc:	41 f6 c1 02          	test   r9b,0x2
    30c0:	74 0e                	je     30d0 <socket@plt+0xb00>
    30c2:	44 0f b7 14 0e       	movzx  r10d,WORD PTR [rsi+rcx*1]
    30c7:	66 44 89 14 0f       	mov    WORD PTR [rdi+rcx*1],r10w
    30cc:	48 83 c1 02          	add    rcx,0x2
    30d0:	41 f6 c1 01          	test   r9b,0x1
    30d4:	74 08                	je     30de <socket@plt+0xb0e>
    30d6:	0f b6 34 0e          	movzx  esi,BYTE PTR [rsi+rcx*1]
    30da:	40 88 34 0f          	mov    BYTE PTR [rdi+rcx*1],sil
    30de:	f6 40 10 04          	test   BYTE PTR [rax+0x10],0x4
    30e2:	0f 85 33 01 00 00    	jne    321b <socket@plt+0xc4b>
    30e8:	49 63 d7             	movsxd rdx,r15d
    30eb:	b8 80 4c 00 00       	mov    eax,0x4c80
    30f0:	4c 8b 7c 24 08       	mov    r15,QWORD PTR [rsp+0x8]
    30f5:	4c 89 c6             	mov    rsi,r8
    30f8:	48 69 da 32 01 00 00 	imul   rbx,rdx,0x132
    30ff:	4c 89 ca             	mov    rdx,r9
    3102:	48 8d 7b 32          	lea    rdi,[rbx+0x32]
    3106:	48 39 c7             	cmp    rdi,rax
    3109:	48 0f 43 c7          	cmovae rax,rdi
    310d:	4c 01 ff             	add    rdi,r15
    3110:	48 29 d8             	sub    rax,rbx
    3113:	48 8d 48 ce          	lea    rcx,[rax-0x32]
    3117:	e8 74 f3 ff ff       	call   2490 <__memcpy_chk@plt>
    311c:	4c 89 ff             	mov    rdi,r15
    311f:	66 44 89 74 1c 50    	mov    WORD PTR [rsp+rbx*1+0x50],r14w
    3125:	e8 f6 08 00 00       	call   3a20 <socket@plt+0x1450>
    312a:	4c 89 e1             	mov    rcx,r12
    312d:	48 8d 15 ed 2f 00 00 	lea    rdx,[rip+0x2fed]        # 6121 <socket@plt+0x3b51>
    3134:	89 ef                	mov    edi,ebp
    3136:	31 c0                	xor    eax,eax
    3138:	be 02 00 00 00       	mov    esi,0x2
    313d:	e8 0e f4 ff ff       	call   2550 <__dprintf_chk@plt>
    3142:	e9 2e fe ff ff       	jmp    2f75 <socket@plt+0x9a5>
    3147:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    314e:	00 00 
    3150:	0f b6 14 3a          	movzx  edx,BYTE PTR [rdx+rdi*1]
    3154:	41 88 14 39          	mov    BYTE PTR [r9+rdi*1],dl
    3158:	e9 83 fe ff ff       	jmp    2fe0 <socket@plt+0xa10>
    315d:	0f 1f 00             	nop    DWORD PTR [rax]
    3160:	44 0f b7 04 3a       	movzx  r8d,WORD PTR [rdx+rdi*1]
    3165:	66 45 89 04 39       	mov    WORD PTR [r9+rdi*1],r8w
    316a:	48 83 c7 02          	add    rdi,0x2
    316e:	41 f6 c5 01          	test   r13b,0x1
    3172:	0f 84 68 fe ff ff    	je     2fe0 <socket@plt+0xa10>
    3178:	eb d6                	jmp    3150 <socket@plt+0xb80>
    317a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    3180:	8b 3a                	mov    edi,DWORD PTR [rdx]
    3182:	41 89 39             	mov    DWORD PTR [r9],edi
    3185:	bf 04 00 00 00       	mov    edi,0x4
    318a:	41 f6 c5 02          	test   r13b,0x2
    318e:	0f 84 42 fe ff ff    	je     2fd6 <socket@plt+0xa06>
    3194:	eb ca                	jmp    3160 <socket@plt+0xb90>
    3196:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    319d:	00 00 00 
    31a0:	45 89 ea             	mov    r10d,r13d
    31a3:	31 d2                	xor    edx,edx
    31a5:	41 83 e2 f8          	and    r10d,0xfffffff8
    31a9:	89 d7                	mov    edi,edx
    31ab:	83 c2 08             	add    edx,0x8
    31ae:	4d 8b 0c 38          	mov    r9,QWORD PTR [r8+rdi*1]
    31b2:	4d 89 0c 3c          	mov    QWORD PTR [r12+rdi*1],r9
    31b6:	44 39 d2             	cmp    edx,r10d
    31b9:	72 ee                	jb     31a9 <socket@plt+0xbd9>
    31bb:	4d 8d 0c 14          	lea    r9,[r12+rdx*1]
    31bf:	4c 01 c2             	add    rdx,r8
    31c2:	e9 f9 fd ff ff       	jmp    2fc0 <socket@plt+0x9f0>
    31c7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    31ce:	00 00 
    31d0:	48 8d 15 ec 2e 00 00 	lea    rdx,[rip+0x2eec]        # 60c3 <socket@plt+0x3af3>
    31d7:	be 02 00 00 00       	mov    esi,0x2
    31dc:	89 ef                	mov    edi,ebp
    31de:	e8 6d f3 ff ff       	call   2550 <__dprintf_chk@plt>
    31e3:	e9 8d fd ff ff       	jmp    2f75 <socket@plt+0x9a5>
    31e8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
    31ef:	00 
    31f0:	81 bc 24 af 4c 00 00 	cmp    DWORD PTR [rsp+0x4caf],0x64726f
    31f7:	6f 72 64 00 
    31fb:	0f 85 4a fe ff ff    	jne    304b <socket@plt+0xa7b>
    3201:	48 8d 15 02 2f 00 00 	lea    rdx,[rip+0x2f02]        # 610a <socket@plt+0x3b3a>
    3208:	be 02 00 00 00       	mov    esi,0x2
    320d:	89 ef                	mov    edi,ebp
    320f:	31 c0                	xor    eax,eax
    3211:	e8 3a f3 ff ff       	call   2550 <__dprintf_chk@plt>
    3216:	e9 5a fd ff ff       	jmp    2f75 <socket@plt+0x9a5>
    321b:	4c 89 ce             	mov    rsi,r9
    321e:	4c 89 c7             	mov    rdi,r8
    3221:	4c 89 4c 24 18       	mov    QWORD PTR [rsp+0x18],r9
    3226:	4c 89 44 24 10       	mov    QWORD PTR [rsp+0x10],r8
    322b:	e8 50 06 00 00       	call   3880 <socket@plt+0x12b0>
    3230:	4c 8b 4c 24 18       	mov    r9,QWORD PTR [rsp+0x18]
    3235:	4c 8b 44 24 10       	mov    r8,QWORD PTR [rsp+0x10]
    323a:	e9 a9 fe ff ff       	jmp    30e8 <socket@plt+0xb18>
    323f:	e8 bc f1 ff ff       	call   2400 <__stack_chk_fail@plt>
    3244:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    324b:	00 00 00 00 
    324f:	90                   	nop
    3250:	f3 0f 1e fa          	endbr64
    3254:	41 54                	push   r12
    3256:	55                   	push   rbp
    3257:	53                   	push   rbx
    3258:	4c 8d 9c 24 00 c0 ff 	lea    r11,[rsp-0x4000]
    325f:	ff 
    3260:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    3267:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    326c:	4c 39 dc             	cmp    rsp,r11
    326f:	75 ef                	jne    3260 <socket@plt+0xc90>
    3271:	48 81 ec 90 0d 00 00 	sub    rsp,0xd90
    3278:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    327f:	00 00 
    3281:	48 89 84 24 88 4d 00 	mov    QWORD PTR [rsp+0x4d88],rax
    3288:	00 
    3289:	31 c0                	xor    eax,eax
    328b:	83 3f 01             	cmp    DWORD PTR [rdi],0x1
    328e:	89 f3                	mov    ebx,esi
    3290:	0f 8e ba 00 00 00    	jle    3350 <socket@plt+0xd80>
    3296:	49 89 e4             	mov    r12,rsp
    3299:	4c 89 e7             	mov    rdi,r12
    329c:	e8 ef 07 00 00       	call   3a90 <socket@plt+0x14c0>
    32a1:	48 8d 3d 84 2e 00 00 	lea    rdi,[rip+0x2e84]        # 612c <socket@plt+0x3b5c>
    32a8:	e8 73 05 00 00       	call   3820 <socket@plt+0x1250>
    32ad:	48 98                	cdqe
    32af:	48 69 c0 32 01 00 00 	imul   rax,rax,0x132
    32b6:	0f b7 6c 04 30       	movzx  ebp,WORD PTR [rsp+rax*1+0x30]
    32bb:	66 85 ed             	test   bp,bp
    32be:	74 70                	je     3330 <socket@plt+0xd60>
    32c0:	0f b7 d5             	movzx  edx,bp
    32c3:	49 8d 74 04 32       	lea    rsi,[r12+rax*1+0x32]
    32c8:	b9 00 01 00 00       	mov    ecx,0x100
    32cd:	48 8d bc 24 80 4c 00 	lea    rdi,[rsp+0x4c80]
    32d4:	00 
    32d5:	e8 b6 f1 ff ff       	call   2490 <__memcpy_chk@plt>
    32da:	c6 84 2c 80 4c 00 00 	mov    BYTE PTR [rsp+rbp*1+0x4c80],0x0
    32e1:	00 
    32e2:	48 89 c7             	mov    rdi,rax
    32e5:	e8 26 f1 ff ff       	call   2410 <system@plt>
    32ea:	bf 0a 00 00 00       	mov    edi,0xa
    32ef:	e8 ec 12 00 00       	call   45e0 <socket@plt+0x2010>
    32f4:	48 8d 15 5b 2e 00 00 	lea    rdx,[rip+0x2e5b]        # 6156 <socket@plt+0x3b86>
    32fb:	89 df                	mov    edi,ebx
    32fd:	31 c0                	xor    eax,eax
    32ff:	be 02 00 00 00       	mov    esi,0x2
    3304:	e8 47 f2 ff ff       	call   2550 <__dprintf_chk@plt>
    3309:	48 8b 84 24 88 4d 00 	mov    rax,QWORD PTR [rsp+0x4d88]
    3310:	00 
    3311:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3318:	00 00 
    331a:	75 49                	jne    3365 <socket@plt+0xd95>
    331c:	48 81 c4 90 4d 00 00 	add    rsp,0x4d90
    3323:	31 c0                	xor    eax,eax
    3325:	5b                   	pop    rbx
    3326:	5d                   	pop    rbp
    3327:	41 5c                	pop    r12
    3329:	c3                   	ret
    332a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    3330:	48 8d 15 07 2e 00 00 	lea    rdx,[rip+0x2e07]        # 613e <socket@plt+0x3b6e>
    3337:	be 02 00 00 00       	mov    esi,0x2
    333c:	89 df                	mov    edi,ebx
    333e:	31 c0                	xor    eax,eax
    3340:	e8 0b f2 ff ff       	call   2550 <__dprintf_chk@plt>
    3345:	eb c2                	jmp    3309 <socket@plt+0xd39>
    3347:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    334e:	00 00 
    3350:	48 8d 15 6c 2d 00 00 	lea    rdx,[rip+0x2d6c]        # 60c3 <socket@plt+0x3af3>
    3357:	be 02 00 00 00       	mov    esi,0x2
    335c:	89 df                	mov    edi,ebx
    335e:	e8 ed f1 ff ff       	call   2550 <__dprintf_chk@plt>
    3363:	eb a4                	jmp    3309 <socket@plt+0xd39>
    3365:	e8 96 f0 ff ff       	call   2400 <__stack_chk_fail@plt>
    336a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    3370:	f3 0f 1e fa          	endbr64
    3374:	41 57                	push   r15
    3376:	41 56                	push   r14
    3378:	41 55                	push   r13
    337a:	41 54                	push   r12
    337c:	55                   	push   rbp
    337d:	53                   	push   rbx
    337e:	4c 8d 9c 24 00 c0 ff 	lea    r11,[rsp-0x4000]
    3385:	ff 
    3386:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    338d:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    3392:	4c 39 dc             	cmp    rsp,r11
    3395:	75 ef                	jne    3386 <socket@plt+0xdb6>
    3397:	48 81 ec a8 0d 00 00 	sub    rsp,0xda8
    339e:	48 89 7c 24 08       	mov    QWORD PTR [rsp+0x8],rdi
    33a3:	41 89 f7             	mov    r15d,esi
    33a6:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    33ad:	00 00 
    33af:	48 89 84 24 98 4d 00 	mov    QWORD PTR [rsp+0x4d98],rax
    33b6:	00 
    33b7:	31 c0                	xor    eax,eax
    33b9:	8d 41 ff             	lea    eax,[rcx-0x1]
    33bc:	66 3d fe 00          	cmp    ax,0xfe
    33c0:	77 65                	ja     3427 <socket@plt+0xe57>
    33c2:	4c 8d 74 24 10       	lea    r14,[rsp+0x10]
    33c7:	49 89 d4             	mov    r12,rdx
    33ca:	89 cd                	mov    ebp,ecx
    33cc:	4c 89 f7             	mov    rdi,r14
    33cf:	e8 bc 06 00 00       	call   3a90 <socket@plt+0x14c0>
    33d4:	48 8d 3d a7 2d 00 00 	lea    rdi,[rip+0x2da7]        # 6182 <socket@plt+0x3bb2>
    33db:	e8 40 04 00 00       	call   3820 <socket@plt+0x1250>
    33e0:	b9 00 01 00 00       	mov    ecx,0x100
    33e5:	48 63 d8             	movsxd rbx,eax
    33e8:	48 69 db 32 01 00 00 	imul   rbx,rbx,0x132
    33ef:	44 0f b7 6c 1c 40    	movzx  r13d,WORD PTR [rsp+rbx*1+0x40]
    33f5:	49 8d 74 1e 32       	lea    rsi,[r14+rbx*1+0x32]
    33fa:	4c 8d b4 24 90 4c 00 	lea    r14,[rsp+0x4c90]
    3401:	00 
    3402:	4c 89 f7             	mov    rdi,r14
    3405:	4c 89 ea             	mov    rdx,r13
    3408:	e8 83 f0 ff ff       	call   2490 <__memcpy_chk@plt>
    340d:	4c 89 ee             	mov    rsi,r13
    3410:	4c 89 f7             	mov    rdi,r14
    3413:	e8 68 04 00 00       	call   3880 <socket@plt+0x12b0>
    3418:	0f b7 44 1c 40       	movzx  eax,WORD PTR [rsp+rbx*1+0x40]
    341d:	66 39 e8             	cmp    ax,bp
    3420:	75 05                	jne    3427 <socket@plt+0xe57>
    3422:	66 85 c0             	test   ax,ax
    3425:	75 41                	jne    3468 <socket@plt+0xe98>
    3427:	48 8d 15 3c 2d 00 00 	lea    rdx,[rip+0x2d3c]        # 616a <socket@plt+0x3b9a>
    342e:	be 02 00 00 00       	mov    esi,0x2
    3433:	44 89 ff             	mov    edi,r15d
    3436:	31 c0                	xor    eax,eax
    3438:	e8 13 f1 ff ff       	call   2550 <__dprintf_chk@plt>
    343d:	48 8b 84 24 98 4d 00 	mov    rax,QWORD PTR [rsp+0x4d98]
    3444:	00 
    3445:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    344c:	00 00 
    344e:	75 4d                	jne    349d <socket@plt+0xecd>
    3450:	48 81 c4 a8 4d 00 00 	add    rsp,0x4da8
    3457:	31 c0                	xor    eax,eax
    3459:	5b                   	pop    rbx
    345a:	5d                   	pop    rbp
    345b:	41 5c                	pop    r12
    345d:	41 5d                	pop    r13
    345f:	41 5e                	pop    r14
    3461:	41 5f                	pop    r15
    3463:	c3                   	ret
    3464:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    3468:	0f b7 d5             	movzx  edx,bp
    346b:	4c 89 e6             	mov    rsi,r12
    346e:	4c 89 f7             	mov    rdi,r14
    3471:	e8 5a f5 ff ff       	call   29d0 <socket@plt+0x400>
    3476:	85 c0                	test   eax,eax
    3478:	75 ad                	jne    3427 <socket@plt+0xe57>
    347a:	48 8b 44 24 08       	mov    rax,QWORD PTR [rsp+0x8]
    347f:	48 8d 15 ea 31 00 00 	lea    rdx,[rip+0x31ea]        # 6670 <socket@plt+0x40a0>
    3486:	be 02 00 00 00       	mov    esi,0x2
    348b:	44 89 ff             	mov    edi,r15d
    348e:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
    3494:	31 c0                	xor    eax,eax
    3496:	e8 b5 f0 ff ff       	call   2550 <__dprintf_chk@plt>
    349b:	eb a0                	jmp    343d <socket@plt+0xe6d>
    349d:	e8 5e ef ff ff       	call   2400 <__stack_chk_fail@plt>
    34a2:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    34a9:	00 00 00 00 
    34ad:	0f 1f 00             	nop    DWORD PTR [rax]
    34b0:	f3 0f 1e fa          	endbr64
    34b4:	41 57                	push   r15
    34b6:	41 56                	push   r14
    34b8:	41 55                	push   r13
    34ba:	41 54                	push   r12
    34bc:	55                   	push   rbp
    34bd:	53                   	push   rbx
    34be:	4c 8d 9c 24 00 c0 ff 	lea    r11,[rsp-0x4000]
    34c5:	ff 
    34c6:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    34cd:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    34d2:	4c 39 dc             	cmp    rsp,r11
    34d5:	75 ef                	jne    34c6 <socket@plt+0xef6>
    34d7:	48 81 ec 08 0e 00 00 	sub    rsp,0xe08
    34de:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    34e5:	00 00 
    34e7:	48 89 84 24 f8 4d 00 	mov    QWORD PTR [rsp+0x4df8],rax
    34ee:	00 
    34ef:	31 c0                	xor    eax,eax
    34f1:	8d 41 ff             	lea    eax,[rcx-0x1]
    34f4:	89 f5                	mov    ebp,esi
    34f6:	66 3d fe 00          	cmp    ax,0xfe
    34fa:	0f 87 d0 00 00 00    	ja     35d0 <socket@plt+0x1000>
    3500:	49 89 e4             	mov    r12,rsp
    3503:	49 89 d5             	mov    r13,rdx
    3506:	89 cb                	mov    ebx,ecx
    3508:	4c 89 e7             	mov    rdi,r12
    350b:	0f b7 db             	movzx  ebx,bx
    350e:	e8 7d 05 00 00       	call   3a90 <socket@plt+0x14c0>
    3513:	48 8d 3d 83 2c 00 00 	lea    rdi,[rip+0x2c83]        # 619d <socket@plt+0x3bcd>
    351a:	e8 01 03 00 00       	call   3820 <socket@plt+0x1250>
    351f:	b9 31 01 00 00       	mov    ecx,0x131
    3524:	48 98                	cdqe
    3526:	48 69 c0 32 01 00 00 	imul   rax,rax,0x132
    352d:	44 0f b7 7c 04 30    	movzx  r15d,WORD PTR [rsp+rax*1+0x30]
    3533:	49 8d 74 04 32       	lea    rsi,[r12+rax*1+0x32]
    3538:	4c 8d a4 24 c0 4c 00 	lea    r12,[rsp+0x4cc0]
    353f:	00 
    3540:	4c 89 e7             	mov    rdi,r12
    3543:	4c 89 fa             	mov    rdx,r15
    3546:	4d 8d 77 01          	lea    r14,[r15+0x1]
    354a:	e8 41 ef ff ff       	call   2490 <__memcpy_chk@plt>
    354f:	b9 31 01 00 00       	mov    ecx,0x131
    3554:	48 89 da             	mov    rdx,rbx
    3557:	4c 89 ee             	mov    rsi,r13
    355a:	49 39 ce             	cmp    r14,rcx
    355d:	4b 8d 3c 34          	lea    rdi,[r12+r14*1]
    3561:	4c 8d ac 24 80 4c 00 	lea    r13,[rsp+0x4c80]
    3568:	00 
    3569:	42 c6 84 3c c0 4c 00 	mov    BYTE PTR [rsp+r15*1+0x4cc0],0x3a
    3570:	00 3a 
    3572:	49 0f 43 ce          	cmovae rcx,r14
    3576:	4c 29 f1             	sub    rcx,r14
    3579:	e8 12 ef ff ff       	call   2490 <__memcpy_chk@plt>
    357e:	4a 8d 34 33          	lea    rsi,[rbx+r14*1]
    3582:	4c 89 e7             	mov    rdi,r12
    3585:	4c 89 ea             	mov    rdx,r13
    3588:	e8 c3 25 00 00       	call   5b50 <socket@plt+0x3580>
    358d:	48 8d 9c 24 a0 4c 00 	lea    rbx,[rsp+0x4ca0]
    3594:	00 
    3595:	48 89 df             	mov    rdi,rbx
    3598:	e8 f3 09 00 00       	call   3f90 <socket@plt+0x19c0>
    359d:	85 c0                	test   eax,eax
    359f:	75 2f                	jne    35d0 <socket@plt+0x1000>
    35a1:	ba 20 00 00 00       	mov    edx,0x20
    35a6:	48 89 de             	mov    rsi,rbx
    35a9:	4c 89 ef             	mov    rdi,r13
    35ac:	e8 1f f4 ff ff       	call   29d0 <socket@plt+0x400>
    35b1:	85 c0                	test   eax,eax
    35b3:	75 1b                	jne    35d0 <socket@plt+0x1000>
    35b5:	48 8d 15 b4 30 00 00 	lea    rdx,[rip+0x30b4]        # 6670 <socket@plt+0x40a0>
    35bc:	be 02 00 00 00       	mov    esi,0x2
    35c1:	89 ef                	mov    edi,ebp
    35c3:	e8 88 ef ff ff       	call   2550 <__dprintf_chk@plt>
    35c8:	eb 1b                	jmp    35e5 <socket@plt+0x1015>
    35ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    35d0:	48 8d 15 93 2b 00 00 	lea    rdx,[rip+0x2b93]        # 616a <socket@plt+0x3b9a>
    35d7:	be 02 00 00 00       	mov    esi,0x2
    35dc:	89 ef                	mov    edi,ebp
    35de:	31 c0                	xor    eax,eax
    35e0:	e8 6b ef ff ff       	call   2550 <__dprintf_chk@plt>
    35e5:	48 8b 84 24 f8 4d 00 	mov    rax,QWORD PTR [rsp+0x4df8]
    35ec:	00 
    35ed:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    35f4:	00 00 
    35f6:	75 14                	jne    360c <socket@plt+0x103c>
    35f8:	48 81 c4 08 4e 00 00 	add    rsp,0x4e08
    35ff:	31 c0                	xor    eax,eax
    3601:	5b                   	pop    rbx
    3602:	5d                   	pop    rbp
    3603:	41 5c                	pop    r12
    3605:	41 5d                	pop    r13
    3607:	41 5e                	pop    r14
    3609:	41 5f                	pop    r15
    360b:	c3                   	ret
    360c:	e8 ef ed ff ff       	call   2400 <__stack_chk_fail@plt>
    3611:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    3618:	00 00 00 00 
    361c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    3620:	f3 0f 1e fa          	endbr64
    3624:	41 56                	push   r14
    3626:	66 0f ef c0          	pxor   xmm0,xmm0
    362a:	41 55                	push   r13
    362c:	41 54                	push   r12
    362e:	55                   	push   rbp
    362f:	53                   	push   rbx
    3630:	89 fb                	mov    ebx,edi
    3632:	48 81 ec 80 01 00 00 	sub    rsp,0x180
    3639:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    3640:	00 00 
    3642:	48 89 84 24 78 01 00 	mov    QWORD PTR [rsp+0x178],rax
    3649:	00 
    364a:	31 c0                	xor    eax,eax
    364c:	31 c0                	xor    eax,eax
    364e:	0f 11 44 24 14       	movups XMMWORD PTR [rsp+0x14],xmm0
    3653:	4c 8d 6c 24 0e       	lea    r13,[rsp+0xe]
    3658:	66 89 44 24 24       	mov    WORD PTR [rsp+0x24],ax
    365d:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
    3662:	4c 8d 64 24 0d       	lea    r12,[rsp+0xd]
    3667:	c7 44 24 10 00 00 00 	mov    DWORD PTR [rsp+0x10],0x0
    366e:	00 
    366f:	4c 8d 74 24 10       	lea    r14,[rsp+0x10]
    3674:	eb 1d                	jmp    3693 <socket@plt+0x10c3>
    3676:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    367d:	00 00 00 
    3680:	0f b7 4c 24 0e       	movzx  ecx,WORD PTR [rsp+0xe]
    3685:	48 89 ea             	mov    rdx,rbp
    3688:	89 de                	mov    esi,ebx
    368a:	4c 89 f7             	mov    rdi,r14
    368d:	ff d0                	call   rax
    368f:	85 c0                	test   eax,eax
    3691:	78 3d                	js     36d0 <socket@plt+0x1100>
    3693:	4c 89 e9             	mov    rcx,r13
    3696:	48 89 ea             	mov    rdx,rbp
    3699:	4c 89 e6             	mov    rsi,r12
    369c:	89 df                	mov    edi,ebx
    369e:	e8 6d f3 ff ff       	call   2a10 <socket@plt+0x440>
    36a3:	85 c0                	test   eax,eax
    36a5:	75 29                	jne    36d0 <socket@plt+0x1100>
    36a7:	0f b6 7c 24 0d       	movzx  edi,BYTE PTR [rsp+0xd]
    36ac:	e8 9f f4 ff ff       	call   2b50 <socket@plt+0x580>
    36b1:	48 85 c0             	test   rax,rax
    36b4:	75 ca                	jne    3680 <socket@plt+0x10b0>
    36b6:	48 8d 15 fd 2a 00 00 	lea    rdx,[rip+0x2afd]        # 61ba <socket@plt+0x3bea>
    36bd:	be 02 00 00 00       	mov    esi,0x2
    36c2:	89 df                	mov    edi,ebx
    36c4:	e8 87 ee ff ff       	call   2550 <__dprintf_chk@plt>
    36c9:	eb c8                	jmp    3693 <socket@plt+0x10c3>
    36cb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    36d0:	48 8b 84 24 78 01 00 	mov    rax,QWORD PTR [rsp+0x178]
    36d7:	00 
    36d8:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    36df:	00 00 
    36e1:	75 10                	jne    36f3 <socket@plt+0x1123>
    36e3:	48 81 c4 80 01 00 00 	add    rsp,0x180
    36ea:	5b                   	pop    rbx
    36eb:	5d                   	pop    rbp
    36ec:	41 5c                	pop    r12
    36ee:	41 5d                	pop    r13
    36f0:	41 5e                	pop    r14
    36f2:	c3                   	ret
    36f3:	e8 08 ed ff ff       	call   2400 <__stack_chk_fail@plt>
    36f8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
    36ff:	00 
    3700:	41 57                	push   r15
    3702:	49 89 f7             	mov    r15,rsi
    3705:	41 56                	push   r14
    3707:	49 89 d6             	mov    r14,rdx
    370a:	41 55                	push   r13
    370c:	41 54                	push   r12
    370e:	41 89 fc             	mov    r12d,edi
    3711:	48 89 f7             	mov    rdi,rsi
    3714:	55                   	push   rbp
    3715:	89 cd                	mov    ebp,ecx
    3717:	53                   	push   rbx
    3718:	48 81 ec 68 01 00 00 	sub    rsp,0x168
    371f:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    3726:	00 00 
    3728:	48 89 84 24 58 01 00 	mov    QWORD PTR [rsp+0x158],rax
    372f:	00 
    3730:	31 c0                	xor    eax,eax
    3732:	e8 b9 ec ff ff       	call   23f0 <strlen@plt>
    3737:	48 83 f8 2f          	cmp    rax,0x2f
    373b:	77 19                	ja     3756 <socket@plt+0x1186>
    373d:	44 0f b7 c5          	movzx  r8d,bp
    3741:	48 89 c3             	mov    rbx,rax
    3744:	49 8d 44 00 03       	lea    rax,[r8+rax*1+0x3]
    3749:	4c 89 44 24 08       	mov    QWORD PTR [rsp+0x8],r8
    374e:	48 3d 40 01 00 00    	cmp    rax,0x140
    3754:	76 2a                	jbe    3780 <socket@plt+0x11b0>
    3756:	48 8b 84 24 58 01 00 	mov    rax,QWORD PTR [rsp+0x158]
    375d:	00 
    375e:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3765:	00 00 
    3767:	75 73                	jne    37dc <socket@plt+0x120c>
    3769:	48 81 c4 68 01 00 00 	add    rsp,0x168
    3770:	5b                   	pop    rbx
    3771:	5d                   	pop    rbp
    3772:	41 5c                	pop    r12
    3774:	41 5d                	pop    r13
    3776:	41 5e                	pop    r14
    3778:	41 5f                	pop    r15
    377a:	c3                   	ret
    377b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    3780:	48 8d 7c 24 11       	lea    rdi,[rsp+0x11]
    3785:	48 89 da             	mov    rdx,rbx
    3788:	4c 89 fe             	mov    rsi,r15
    378b:	88 5c 24 10          	mov    BYTE PTR [rsp+0x10],bl
    378f:	e8 0c ed ff ff       	call   24a0 <memcpy@plt>
    3794:	4c 8d 6c 24 10       	lea    r13,[rsp+0x10]
    3799:	48 8d 7b 03          	lea    rdi,[rbx+0x3]
    379d:	89 e8                	mov    eax,ebp
    379f:	48 8b 54 24 08       	mov    rdx,QWORD PTR [rsp+0x8]
    37a4:	b9 40 01 00 00       	mov    ecx,0x140
    37a9:	4c 89 f6             	mov    rsi,r14
    37ac:	88 64 1c 12          	mov    BYTE PTR [rsp+rbx*1+0x12],ah
    37b0:	48 29 f9             	sub    rcx,rdi
    37b3:	4c 01 ef             	add    rdi,r13
    37b6:	40 88 6c 1c 11       	mov    BYTE PTR [rsp+rbx*1+0x11],bpl
    37bb:	e8 d0 ec ff ff       	call   2490 <__memcpy_chk@plt>
    37c0:	8d 4c 1d 03          	lea    ecx,[rbp+rbx*1+0x3]
    37c4:	4c 89 ea             	mov    rdx,r13
    37c7:	44 89 e7             	mov    edi,r12d
    37ca:	0f b7 c9             	movzx  ecx,cx
    37cd:	be 07 00 00 00       	mov    esi,0x7
    37d2:	e8 d9 f2 ff ff       	call   2ab0 <socket@plt+0x4e0>
    37d7:	e9 7a ff ff ff       	jmp    3756 <socket@plt+0x1186>
    37dc:	e8 1f ec ff ff       	call   2400 <__stack_chk_fail@plt>
    37e1:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    37e8:	00 00 00 00 
    37ec:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    37f0:	f3 0f 1e fa          	endbr64
    37f4:	b8 21 00 00 00       	mov    eax,0x21
    37f9:	c3                   	ret
    37fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    3800:	f3 0f 1e fa          	endbr64
    3804:	31 c0                	xor    eax,eax
    3806:	83 ff 20             	cmp    edi,0x20
    3809:	77 12                	ja     381d <socket@plt+0x124d>
    380b:	48 63 ff             	movsxd rdi,edi
    380e:	48 8d 05 2b 80 00 00 	lea    rax,[rip+0x802b]        # b840 <socket@plt+0x9270>
    3815:	48 8d 14 7f          	lea    rdx,[rdi+rdi*2]
    3819:	48 8d 04 d0          	lea    rax,[rax+rdx*8]
    381d:	c3                   	ret
    381e:	66 90                	xchg   ax,ax
    3820:	f3 0f 1e fa          	endbr64
    3824:	41 54                	push   r12
    3826:	49 89 fc             	mov    r12,rdi
    3829:	55                   	push   rbp
    382a:	48 8d 2d 0f 80 00 00 	lea    rbp,[rip+0x800f]        # b840 <socket@plt+0x9270>
    3831:	53                   	push   rbx
    3832:	31 db                	xor    ebx,ebx
    3834:	eb 16                	jmp    384c <socket@plt+0x127c>
    3836:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    383d:	00 00 00 
    3840:	83 c3 01             	add    ebx,0x1
    3843:	48 83 c5 18          	add    rbp,0x18
    3847:	83 fb 21             	cmp    ebx,0x21
    384a:	74 1c                	je     3868 <socket@plt+0x1298>
    384c:	48 8b 75 00          	mov    rsi,QWORD PTR [rbp+0x0]
    3850:	4c 89 e7             	mov    rdi,r12
    3853:	e8 18 ec ff ff       	call   2470 <strcmp@plt>
    3858:	85 c0                	test   eax,eax
    385a:	75 e4                	jne    3840 <socket@plt+0x1270>
    385c:	89 d8                	mov    eax,ebx
    385e:	5b                   	pop    rbx
    385f:	5d                   	pop    rbp
    3860:	41 5c                	pop    r12
    3862:	c3                   	ret
    3863:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    3868:	bb ff ff ff ff       	mov    ebx,0xffffffff
    386d:	89 d8                	mov    eax,ebx
    386f:	5b                   	pop    rbx
    3870:	5d                   	pop    rbp
    3871:	41 5c                	pop    r12
    3873:	c3                   	ret
    3874:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    387b:	00 00 00 00 
    387f:	90                   	nop
    3880:	f3 0f 1e fa          	endbr64
    3884:	48 85 f6             	test   rsi,rsi
    3887:	74 2d                	je     38b6 <socket@plt+0x12e6>
    3889:	80 37 0d             	xor    BYTE PTR [rdi],0xd
    388c:	b8 01 00 00 00       	mov    eax,0x1
    3891:	48 8d 0d 38 2e 00 00 	lea    rcx,[rip+0x2e38]        # 66d0 <socket@plt+0x4100>
    3898:	48 83 fe 01          	cmp    rsi,0x1
    389c:	74 18                	je     38b6 <socket@plt+0x12e6>
    389e:	66 90                	xchg   ax,ax
    38a0:	48 89 c2             	mov    rdx,rax
    38a3:	83 e2 0f             	and    edx,0xf
    38a6:	0f b6 14 11          	movzx  edx,BYTE PTR [rcx+rdx*1]
    38aa:	30 14 07             	xor    BYTE PTR [rdi+rax*1],dl
    38ad:	48 83 c0 01          	add    rax,0x1
    38b1:	48 39 c6             	cmp    rsi,rax
    38b4:	75 ea                	jne    38a0 <socket@plt+0x12d0>
    38b6:	c3                   	ret
    38b7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    38be:	00 00 
    38c0:	f3 0f 1e fa          	endbr64
    38c4:	48 83 ec 08          	sub    rsp,0x8
    38c8:	48 8d 3d 1a 29 00 00 	lea    rdi,[rip+0x291a]        # 61e9 <socket@plt+0x3c19>
    38cf:	e8 3c ea ff ff       	call   2310 <getenv@plt>
    38d4:	48 8d 15 f4 28 00 00 	lea    rdx,[rip+0x28f4]        # 61cf <socket@plt+0x3bff>
    38db:	48 85 c0             	test   rax,rax
    38de:	48 0f 44 c2          	cmove  rax,rdx
    38e2:	48 83 c4 08          	add    rsp,0x8
    38e6:	c3                   	ret
    38e7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    38ee:	00 00 
    38f0:	f3 0f 1e fa          	endbr64
    38f4:	41 56                	push   r14
    38f6:	41 55                	push   r13
    38f8:	4c 8d 2d 49 7f 00 00 	lea    r13,[rip+0x7f49]        # b848 <socket@plt+0x9278>
    38ff:	41 54                	push   r12
    3901:	4d 8d a5 18 03 00 00 	lea    r12,[r13+0x318]
    3908:	55                   	push   rbp
    3909:	31 ed                	xor    ebp,ebp
    390b:	53                   	push   rbx
    390c:	48 89 fb             	mov    rbx,rdi
    390f:	eb 39                	jmp    394a <socket@plt+0x137a>
    3911:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    3918:	a8 04                	test   al,0x4
    391a:	0f 85 c0 00 00 00    	jne    39e0 <socket@plt+0x1410>
    3920:	85 c0                	test   eax,eax
    3922:	74 0e                	je     3932 <socket@plt+0x1362>
    3924:	41 0f b6 16          	movzx  edx,BYTE PTR [r14]
    3928:	88 11                	mov    BYTE PTR [rcx],dl
    392a:	a8 02                	test   al,0x2
    392c:	0f 85 d6 00 00 00    	jne    3a08 <socket@plt+0x1438>
    3932:	49 83 c5 18          	add    r13,0x18
    3936:	66 89 43 30          	mov    WORD PTR [rbx+0x30],ax
    393a:	48 81 c3 32 01 00 00 	add    rbx,0x132
    3941:	4d 39 e5             	cmp    r13,r12
    3944:	0f 84 ae 00 00 00    	je     39f8 <socket@plt+0x1428>
    394a:	48 8d 7b 08          	lea    rdi,[rbx+0x8]
    394e:	48 89 d9             	mov    rcx,rbx
    3951:	48 89 e8             	mov    rax,rbp
    3954:	ba 2f 00 00 00       	mov    edx,0x2f
    3959:	48 83 e7 f8          	and    rdi,0xfffffffffffffff8
    395d:	48 c7 03 00 00 00 00 	mov    QWORD PTR [rbx],0x0
    3964:	48 c7 83 2a 01 00 00 	mov    QWORD PTR [rbx+0x12a],0x0
    396b:	00 00 00 00 
    396f:	48 29 f9             	sub    rcx,rdi
    3972:	81 c1 32 01 00 00    	add    ecx,0x132
    3978:	c1 e9 03             	shr    ecx,0x3
    397b:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    397e:	48 89 df             	mov    rdi,rbx
    3981:	49 8b 75 f8          	mov    rsi,QWORD PTR [r13-0x8]
    3985:	e8 c6 e9 ff ff       	call   2350 <strncpy@plt>
    398a:	4d 8b 75 00          	mov    r14,QWORD PTR [r13+0x0]
    398e:	4c 89 f7             	mov    rdi,r14
    3991:	e8 5a ea ff ff       	call   23f0 <strlen@plt>
    3996:	ba 00 01 00 00       	mov    edx,0x100
    399b:	48 8d 4b 32          	lea    rcx,[rbx+0x32]
    399f:	48 39 d0             	cmp    rax,rdx
    39a2:	48 0f 47 c2          	cmova  rax,rdx
    39a6:	83 f8 08             	cmp    eax,0x8
    39a9:	0f 82 69 ff ff ff    	jb     3918 <socket@plt+0x1348>
    39af:	49 8b 16             	mov    rdx,QWORD PTR [r14]
    39b2:	48 8d 7b 3a          	lea    rdi,[rbx+0x3a]
    39b6:	48 83 e7 f8          	and    rdi,0xfffffffffffffff8
    39ba:	48 89 53 32          	mov    QWORD PTR [rbx+0x32],rdx
    39be:	89 c2                	mov    edx,eax
    39c0:	49 8b 74 16 f8       	mov    rsi,QWORD PTR [r14+rdx*1-0x8]
    39c5:	48 89 74 11 f8       	mov    QWORD PTR [rcx+rdx*1-0x8],rsi
    39ca:	48 29 f9             	sub    rcx,rdi
    39cd:	4c 89 f6             	mov    rsi,r14
    39d0:	48 29 ce             	sub    rsi,rcx
    39d3:	01 c1                	add    ecx,eax
    39d5:	c1 e9 03             	shr    ecx,0x3
    39d8:	f3 48 a5             	rep movs QWORD PTR [rdi],QWORD PTR [rsi]
    39db:	e9 52 ff ff ff       	jmp    3932 <socket@plt+0x1362>
    39e0:	41 8b 16             	mov    edx,DWORD PTR [r14]
    39e3:	89 11                	mov    DWORD PTR [rcx],edx
    39e5:	89 c2                	mov    edx,eax
    39e7:	41 8b 74 16 fc       	mov    esi,DWORD PTR [r14+rdx*1-0x4]
    39ec:	89 74 11 fc          	mov    DWORD PTR [rcx+rdx*1-0x4],esi
    39f0:	e9 3d ff ff ff       	jmp    3932 <socket@plt+0x1362>
    39f5:	0f 1f 00             	nop    DWORD PTR [rax]
    39f8:	5b                   	pop    rbx
    39f9:	5d                   	pop    rbp
    39fa:	41 5c                	pop    r12
    39fc:	41 5d                	pop    r13
    39fe:	41 5e                	pop    r14
    3a00:	c3                   	ret
    3a01:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    3a08:	89 c2                	mov    edx,eax
    3a0a:	41 0f b7 74 16 fe    	movzx  esi,WORD PTR [r14+rdx*1-0x2]
    3a10:	66 89 74 11 fe       	mov    WORD PTR [rcx+rdx*1-0x2],si
    3a15:	e9 18 ff ff ff       	jmp    3932 <socket@plt+0x1362>
    3a1a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    3a20:	f3 0f 1e fa          	endbr64
    3a24:	55                   	push   rbp
    3a25:	48 89 fd             	mov    rbp,rdi
    3a28:	48 8d 3d ba 27 00 00 	lea    rdi,[rip+0x27ba]        # 61e9 <socket@plt+0x3c19>
    3a2f:	53                   	push   rbx
    3a30:	48 83 ec 08          	sub    rsp,0x8
    3a34:	e8 d7 e8 ff ff       	call   2310 <getenv@plt>
    3a39:	48 8d 35 b5 27 00 00 	lea    rsi,[rip+0x27b5]        # 61f5 <socket@plt+0x3c25>
    3a40:	48 85 c0             	test   rax,rax
    3a43:	48 89 c7             	mov    rdi,rax
    3a46:	48 8d 05 82 27 00 00 	lea    rax,[rip+0x2782]        # 61cf <socket@plt+0x3bff>
    3a4d:	48 0f 44 f8          	cmove  rdi,rax
    3a51:	e8 da ea ff ff       	call   2530 <fopen@plt>
    3a56:	48 85 c0             	test   rax,rax
    3a59:	74 26                	je     3a81 <socket@plt+0x14b1>
    3a5b:	48 89 ef             	mov    rdi,rbp
    3a5e:	48 89 c1             	mov    rcx,rax
    3a61:	ba 21 00 00 00       	mov    edx,0x21
    3a66:	be 32 01 00 00       	mov    esi,0x132
    3a6b:	48 89 c3             	mov    rbx,rax
    3a6e:	e8 0d eb ff ff       	call   2580 <fwrite@plt>
    3a73:	48 83 c4 08          	add    rsp,0x8
    3a77:	48 89 df             	mov    rdi,rbx
    3a7a:	5b                   	pop    rbx
    3a7b:	5d                   	pop    rbp
    3a7c:	e9 5f e9 ff ff       	jmp    23e0 <fclose@plt>
    3a81:	58                   	pop    rax
    3a82:	5b                   	pop    rbx
    3a83:	5d                   	pop    rbp
    3a84:	c3                   	ret
    3a85:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    3a8c:	00 00 00 00 
    3a90:	f3 0f 1e fa          	endbr64
    3a94:	41 54                	push   r12
    3a96:	55                   	push   rbp
    3a97:	48 89 fd             	mov    rbp,rdi
    3a9a:	48 8d 3d 48 27 00 00 	lea    rdi,[rip+0x2748]        # 61e9 <socket@plt+0x3c19>
    3aa1:	53                   	push   rbx
    3aa2:	e8 69 e8 ff ff       	call   2310 <getenv@plt>
    3aa7:	48 8d 35 4a 27 00 00 	lea    rsi,[rip+0x274a]        # 61f8 <socket@plt+0x3c28>
    3aae:	48 85 c0             	test   rax,rax
    3ab1:	48 89 c7             	mov    rdi,rax
    3ab4:	48 8d 05 14 27 00 00 	lea    rax,[rip+0x2714]        # 61cf <socket@plt+0x3bff>
    3abb:	48 0f 44 f8          	cmove  rdi,rax
    3abf:	e8 6c ea ff ff       	call   2530 <fopen@plt>
    3ac4:	48 85 c0             	test   rax,rax
    3ac7:	74 37                	je     3b00 <socket@plt+0x1530>
    3ac9:	48 89 ef             	mov    rdi,rbp
    3acc:	48 89 c1             	mov    rcx,rax
    3acf:	ba 21 00 00 00       	mov    edx,0x21
    3ad4:	be 32 01 00 00       	mov    esi,0x132
    3ad9:	48 89 c3             	mov    rbx,rax
    3adc:	e8 bf e8 ff ff       	call   23a0 <fread@plt>
    3ae1:	48 89 df             	mov    rdi,rbx
    3ae4:	49 89 c4             	mov    r12,rax
    3ae7:	e8 f4 e8 ff ff       	call   23e0 <fclose@plt>
    3aec:	49 83 fc 21          	cmp    r12,0x21
    3af0:	75 0e                	jne    3b00 <socket@plt+0x1530>
    3af2:	5b                   	pop    rbx
    3af3:	5d                   	pop    rbp
    3af4:	41 5c                	pop    r12
    3af6:	c3                   	ret
    3af7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    3afe:	00 00 
    3b00:	5b                   	pop    rbx
    3b01:	48 89 ef             	mov    rdi,rbp
    3b04:	5d                   	pop    rbp
    3b05:	41 5c                	pop    r12
    3b07:	e9 e4 fd ff ff       	jmp    38f0 <socket@plt+0x1320>
    3b0c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    3b10:	f3 0f 1e fa          	endbr64
    3b14:	53                   	push   rbx
    3b15:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    3b1c:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    3b21:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    3b28:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    3b2d:	48 81 ec 80 07 00 00 	sub    rsp,0x780
    3b34:	48 8d 3d ae 26 00 00 	lea    rdi,[rip+0x26ae]        # 61e9 <socket@plt+0x3c19>
    3b3b:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    3b42:	00 00 
    3b44:	48 89 84 24 78 27 00 	mov    QWORD PTR [rsp+0x2778],rax
    3b4b:	00 
    3b4c:	31 c0                	xor    eax,eax
    3b4e:	e8 bd e7 ff ff       	call   2310 <getenv@plt>
    3b53:	48 8d 35 9e 26 00 00 	lea    rsi,[rip+0x269e]        # 61f8 <socket@plt+0x3c28>
    3b5a:	48 85 c0             	test   rax,rax
    3b5d:	48 89 c7             	mov    rdi,rax
    3b60:	48 8d 05 68 26 00 00 	lea    rax,[rip+0x2668]        # 61cf <socket@plt+0x3bff>
    3b67:	48 0f 44 f8          	cmove  rdi,rax
    3b6b:	e8 c0 e9 ff ff       	call   2530 <fopen@plt>
    3b70:	48 85 c0             	test   rax,rax
    3b73:	74 23                	je     3b98 <socket@plt+0x15c8>
    3b75:	48 89 c7             	mov    rdi,rax
    3b78:	48 8b 84 24 78 27 00 	mov    rax,QWORD PTR [rsp+0x2778]
    3b7f:	00 
    3b80:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3b87:	00 00 
    3b89:	75 3c                	jne    3bc7 <socket@plt+0x15f7>
    3b8b:	48 81 c4 80 27 00 00 	add    rsp,0x2780
    3b92:	5b                   	pop    rbx
    3b93:	e9 48 e8 ff ff       	jmp    23e0 <fclose@plt>
    3b98:	48 89 e3             	mov    rbx,rsp
    3b9b:	48 89 df             	mov    rdi,rbx
    3b9e:	e8 4d fd ff ff       	call   38f0 <socket@plt+0x1320>
    3ba3:	48 89 df             	mov    rdi,rbx
    3ba6:	e8 75 fe ff ff       	call   3a20 <socket@plt+0x1450>
    3bab:	48 8b 84 24 78 27 00 	mov    rax,QWORD PTR [rsp+0x2778]
    3bb2:	00 
    3bb3:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3bba:	00 00 
    3bbc:	75 09                	jne    3bc7 <socket@plt+0x15f7>
    3bbe:	48 81 c4 80 27 00 00 	add    rsp,0x2780
    3bc5:	5b                   	pop    rbx
    3bc6:	c3                   	ret
    3bc7:	e8 34 e8 ff ff       	call   2400 <__stack_chk_fail@plt>
    3bcc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    3bd0:	f3 0f 1e fa          	endbr64
    3bd4:	41 55                	push   r13
    3bd6:	41 54                	push   r12
    3bd8:	55                   	push   rbp
    3bd9:	53                   	push   rbx
    3bda:	48 8d 1d 34 26 00 00 	lea    rbx,[rip+0x2634]        # 6215 <socket@plt+0x3c45>
    3be1:	48 89 df             	mov    rdi,rbx
    3be4:	48 81 ec c8 03 00 00 	sub    rsp,0x3c8
    3beb:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    3bf2:	00 00 
    3bf4:	48 89 84 24 b8 03 00 	mov    QWORD PTR [rsp+0x3b8],rax
    3bfb:	00 
    3bfc:	31 c0                	xor    eax,eax
    3bfe:	e8 0d e7 ff ff       	call   2310 <getenv@plt>
    3c03:	48 8d 35 ee 25 00 00 	lea    rsi,[rip+0x25ee]        # 61f8 <socket@plt+0x3c28>
    3c0a:	48 85 c0             	test   rax,rax
    3c0d:	48 89 c7             	mov    rdi,rax
    3c10:	48 8d 05 e4 25 00 00 	lea    rax,[rip+0x25e4]        # 61fb <socket@plt+0x3c2b>
    3c17:	48 0f 44 f8          	cmove  rdi,rax
    3c1b:	e8 10 e9 ff ff       	call   2530 <fopen@plt>
    3c20:	48 85 c0             	test   rax,rax
    3c23:	74 2c                	je     3c51 <socket@plt+0x1681>
    3c25:	48 8b 94 24 b8 03 00 	mov    rdx,QWORD PTR [rsp+0x3b8]
    3c2c:	00 
    3c2d:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    3c34:	00 00 
    3c36:	0f 85 e2 00 00 00    	jne    3d1e <socket@plt+0x174e>
    3c3c:	48 81 c4 c8 03 00 00 	add    rsp,0x3c8
    3c43:	48 89 c7             	mov    rdi,rax
    3c46:	5b                   	pop    rbx
    3c47:	5d                   	pop    rbp
    3c48:	41 5c                	pop    r12
    3c4a:	41 5d                	pop    r13
    3c4c:	e9 8f e7 ff ff       	jmp    23e0 <fclose@plt>
    3c51:	48 89 e5             	mov    rbp,rsp
    3c54:	b9 72 00 00 00       	mov    ecx,0x72
    3c59:	ba 2f 00 00 00       	mov    edx,0x2f
    3c5e:	45 31 e4             	xor    r12d,r12d
    3c61:	48 89 ef             	mov    rdi,rbp
    3c64:	48 8d 35 b6 25 00 00 	lea    rsi,[rip+0x25b6]        # 6221 <socket@plt+0x3c51>
    3c6b:	4c 8d ac 24 a3 03 00 	lea    r13,[rsp+0x3a3]
    3c72:	00 
    3c73:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    3c76:	ab                   	stos   DWORD PTR [rdi],eax
    3c77:	66 ab                	stos   WORD PTR [rdi],ax
    3c79:	48 89 ef             	mov    rdi,rbp
    3c7c:	e8 cf e6 ff ff       	call   2350 <strncpy@plt>
    3c81:	48 8d bc 24 32 01 00 	lea    rdi,[rsp+0x132]
    3c88:	00 
    3c89:	ba 2f 00 00 00       	mov    edx,0x2f
    3c8e:	48 8d 35 96 25 00 00 	lea    rsi,[rip+0x2596]        # 622b <socket@plt+0x3c5b>
    3c95:	e8 b6 e6 ff ff       	call   2350 <strncpy@plt>
    3c9a:	48 8d bc 24 64 02 00 	lea    rdi,[rsp+0x264]
    3ca1:	00 
    3ca2:	ba 2f 00 00 00       	mov    edx,0x2f
    3ca7:	48 8d 35 8d 25 00 00 	lea    rsi,[rip+0x258d]        # 623b <socket@plt+0x3c6b>
    3cae:	e8 9d e6 ff ff       	call   2350 <strncpy@plt>
    3cb3:	31 d2                	xor    edx,edx
    3cb5:	be 09 00 00 00       	mov    esi,0x9
    3cba:	4c 89 ef             	mov    rdi,r13
    3cbd:	e8 de e8 ff ff       	call   25a0 <getrandom@plt>
    3cc2:	31 c9                	xor    ecx,ecx
    3cc4:	41 b9 cd ff ff ff    	mov    r9d,0xffffffcd
    3cca:	41 b8 24 00 00 00    	mov    r8d,0x24
    3cd0:	eb 19                	jmp    3ceb <socket@plt+0x171b>
    3cd2:	48 63 f6             	movsxd rsi,esi
    3cd5:	41 83 c4 02          	add    r12d,0x2
    3cd9:	c6 84 34 ac 03 00 00 	mov    BYTE PTR [rsp+rsi*1+0x3ac],0x20
    3ce0:	20 
    3ce1:	48 83 c1 01          	add    rcx,0x1
    3ce5:	48 83 f9 09          	cmp    rcx,0x9
    3ce9:	74 38                	je     3d23 <socket@plt+0x1753>
    3ceb:	41 0f b6 54 0d 00    	movzx  edx,BYTE PTR [r13+rcx*1+0x0]
    3cf1:	49 63 fc             	movsxd rdi,r12d
    3cf4:	41 8d 74 24 01       	lea    esi,[r12+0x1]
    3cf9:	89 d0                	mov    eax,edx
    3cfb:	41 f6 e1             	mul    r9b
    3cfe:	66 c1 e8 0b          	shr    ax,0xb
    3d02:	8d 04 80             	lea    eax,[rax+rax*4]
    3d05:	01 c0                	add    eax,eax
    3d07:	29 c2                	sub    edx,eax
    3d09:	49 0f a3 c8          	bt     r8,rcx
    3d0d:	8d 42 30             	lea    eax,[rdx+0x30]
    3d10:	88 84 3c ac 03 00 00 	mov    BYTE PTR [rsp+rdi*1+0x3ac],al
    3d17:	72 b9                	jb     3cd2 <socket@plt+0x1702>
    3d19:	41 89 f4             	mov    r12d,esi
    3d1c:	eb c3                	jmp    3ce1 <socket@plt+0x1711>
    3d1e:	e8 dd e6 ff ff       	call   2400 <__stack_chk_fail@plt>
    3d23:	49 63 d4             	movsxd rdx,r12d
    3d26:	48 8d 7c 24 32       	lea    rdi,[rsp+0x32]
    3d2b:	b9 64 03 00 00       	mov    ecx,0x364
    3d30:	48 8d b4 24 ac 03 00 	lea    rsi,[rsp+0x3ac]
    3d37:	00 
    3d38:	e8 53 e7 ff ff       	call   2490 <__memcpy_chk@plt>
    3d3d:	66 0f 6f 05 fb 28 00 	movdqa xmm0,XMMWORD PTR [rip+0x28fb]        # 6640 <socket@plt+0x4070>
    3d44:	00 
    3d45:	48 89 df             	mov    rdi,rbx
    3d48:	66 44 89 64 24 30    	mov    WORD PTR [rsp+0x30],r12w
    3d4e:	c6 84 24 74 01 00 00 	mov    BYTE PTR [rsp+0x174],0x38
    3d55:	38 
    3d56:	66 c7 84 24 62 01 00 	mov    WORD PTR [rsp+0x162],0x11
    3d5d:	00 11 00 
    3d60:	c7 84 24 96 02 00 00 	mov    DWORD PTR [rsp+0x296],0x65657246
    3d67:	46 72 65 65 
    3d6b:	66 c7 84 24 94 02 00 	mov    WORD PTR [rsp+0x294],0x4
    3d72:	00 04 00 
    3d75:	0f 11 84 24 64 01 00 	movups XMMWORD PTR [rsp+0x164],xmm0
    3d7c:	00 
    3d7d:	e8 8e e5 ff ff       	call   2310 <getenv@plt>
    3d82:	48 89 c7             	mov    rdi,rax
    3d85:	48 85 c0             	test   rax,rax
    3d88:	74 56                	je     3de0 <socket@plt+0x1810>
    3d8a:	48 8d 35 64 24 00 00 	lea    rsi,[rip+0x2464]        # 61f5 <socket@plt+0x3c25>
    3d91:	e8 9a e7 ff ff       	call   2530 <fopen@plt>
    3d96:	48 89 c3             	mov    rbx,rax
    3d99:	48 85 c0             	test   rax,rax
    3d9c:	74 1d                	je     3dbb <socket@plt+0x17eb>
    3d9e:	48 89 ef             	mov    rdi,rbp
    3da1:	48 89 c1             	mov    rcx,rax
    3da4:	ba 03 00 00 00       	mov    edx,0x3
    3da9:	be 32 01 00 00       	mov    esi,0x132
    3dae:	e8 cd e7 ff ff       	call   2580 <fwrite@plt>
    3db3:	48 89 df             	mov    rdi,rbx
    3db6:	e8 25 e6 ff ff       	call   23e0 <fclose@plt>
    3dbb:	48 8b 84 24 b8 03 00 	mov    rax,QWORD PTR [rsp+0x3b8]
    3dc2:	00 
    3dc3:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3dca:	00 00 
    3dcc:	0f 85 4c ff ff ff    	jne    3d1e <socket@plt+0x174e>
    3dd2:	48 81 c4 c8 03 00 00 	add    rsp,0x3c8
    3dd9:	5b                   	pop    rbx
    3dda:	5d                   	pop    rbp
    3ddb:	41 5c                	pop    r12
    3ddd:	41 5d                	pop    r13
    3ddf:	c3                   	ret
    3de0:	48 8d 3d 14 24 00 00 	lea    rdi,[rip+0x2414]        # 61fb <socket@plt+0x3c2b>
    3de7:	eb a1                	jmp    3d8a <socket@plt+0x17ba>
    3de9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    3df0:	f3 0f 1e fa          	endbr64
    3df4:	41 56                	push   r14
    3df6:	41 55                	push   r13
    3df8:	41 54                	push   r12
    3dfa:	55                   	push   rbp
    3dfb:	53                   	push   rbx
    3dfc:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    3e03:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    3e08:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    3e0f:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    3e14:	48 81 ec e0 08 00 00 	sub    rsp,0x8e0
    3e1b:	48 8d 2d 40 24 00 00 	lea    rbp,[rip+0x2440]        # 6262 <socket@plt+0x3c92>
    3e22:	48 8d 1d 1f 24 00 00 	lea    rbx,[rip+0x241f]        # 6248 <socket@plt+0x3c78>
    3e29:	48 89 ef             	mov    rdi,rbp
    3e2c:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    3e33:	00 00 
    3e35:	48 89 84 24 d8 28 00 	mov    QWORD PTR [rsp+0x28d8],rax
    3e3c:	00 
    3e3d:	31 c0                	xor    eax,eax
    3e3f:	e8 cc e4 ff ff       	call   2310 <getenv@plt>
    3e44:	48 8d 35 ad 23 00 00 	lea    rsi,[rip+0x23ad]        # 61f8 <socket@plt+0x3c28>
    3e4b:	48 85 c0             	test   rax,rax
    3e4e:	48 89 c7             	mov    rdi,rax
    3e51:	48 0f 44 fb          	cmove  rdi,rbx
    3e55:	e8 d6 e6 ff ff       	call   2530 <fopen@plt>
    3e5a:	48 85 c0             	test   rax,rax
    3e5d:	74 2e                	je     3e8d <socket@plt+0x18bd>
    3e5f:	48 89 c7             	mov    rdi,rax
    3e62:	48 8b 84 24 d8 28 00 	mov    rax,QWORD PTR [rsp+0x28d8]
    3e69:	00 
    3e6a:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3e71:	00 00 
    3e73:	0f 85 0b 01 00 00    	jne    3f84 <socket@plt+0x19b4>
    3e79:	48 81 c4 e0 28 00 00 	add    rsp,0x28e0
    3e80:	5b                   	pop    rbx
    3e81:	5d                   	pop    rbp
    3e82:	41 5c                	pop    r12
    3e84:	41 5d                	pop    r13
    3e86:	41 5e                	pop    r14
    3e88:	e9 53 e5 ff ff       	jmp    23e0 <fclose@plt>
    3e8d:	49 89 e5             	mov    r13,rsp
    3e90:	4c 8d b4 24 80 27 00 	lea    r14,[rsp+0x2780]
    3e97:	00 
    3e98:	4c 89 ef             	mov    rdi,r13
    3e9b:	e8 f0 fb ff ff       	call   3a90 <socket@plt+0x14c0>
    3ea0:	48 8d 3d f6 22 00 00 	lea    rdi,[rip+0x22f6]        # 619d <socket@plt+0x3bcd>
    3ea7:	e8 74 f9 ff ff       	call   3820 <socket@plt+0x1250>
    3eac:	b9 31 01 00 00       	mov    ecx,0x131
    3eb1:	48 98                	cdqe
    3eb3:	48 69 c0 32 01 00 00 	imul   rax,rax,0x132
    3eba:	44 0f b7 64 04 30    	movzx  r12d,WORD PTR [rsp+rax*1+0x30]
    3ec0:	49 8d 74 05 32       	lea    rsi,[r13+rax*1+0x32]
    3ec5:	4c 8d ac 24 a0 27 00 	lea    r13,[rsp+0x27a0]
    3ecc:	00 
    3ecd:	4c 89 ef             	mov    rdi,r13
    3ed0:	4c 89 e2             	mov    rdx,r12
    3ed3:	e8 b8 e5 ff ff       	call   2490 <__memcpy_chk@plt>
    3ed8:	49 8d 44 24 01       	lea    rax,[r12+0x1]
    3edd:	ba 31 01 00 00       	mov    edx,0x131
    3ee2:	48 8d 35 d7 27 00 00 	lea    rsi,[rip+0x27d7]        # 66c0 <socket@plt+0x40f0>
    3ee9:	48 39 d0             	cmp    rax,rdx
    3eec:	49 8d 7c 05 00       	lea    rdi,[r13+rax*1+0x0]
    3ef1:	42 c6 84 24 a0 27 00 	mov    BYTE PTR [rsp+r12*1+0x27a0],0x3a
    3ef8:	00 3a 
    3efa:	48 0f 43 d0          	cmovae rdx,rax
    3efe:	48 89 d1             	mov    rcx,rdx
    3f01:	ba 0e 00 00 00       	mov    edx,0xe
    3f06:	48 29 c1             	sub    rcx,rax
    3f09:	e8 82 e5 ff ff       	call   2490 <__memcpy_chk@plt>
    3f0e:	49 8d 74 24 0f       	lea    rsi,[r12+0xf]
    3f13:	4c 89 f2             	mov    rdx,r14
    3f16:	4c 89 ef             	mov    rdi,r13
    3f19:	e8 32 1c 00 00       	call   5b50 <socket@plt+0x3580>
    3f1e:	48 89 ef             	mov    rdi,rbp
    3f21:	e8 ea e3 ff ff       	call   2310 <getenv@plt>
    3f26:	48 8d 35 c8 22 00 00 	lea    rsi,[rip+0x22c8]        # 61f5 <socket@plt+0x3c25>
    3f2d:	48 89 c7             	mov    rdi,rax
    3f30:	48 85 c0             	test   rax,rax
    3f33:	48 0f 44 fb          	cmove  rdi,rbx
    3f37:	e8 f4 e5 ff ff       	call   2530 <fopen@plt>
    3f3c:	48 89 c3             	mov    rbx,rax
    3f3f:	48 85 c0             	test   rax,rax
    3f42:	74 1d                	je     3f61 <socket@plt+0x1991>
    3f44:	4c 89 f7             	mov    rdi,r14
    3f47:	48 89 c1             	mov    rcx,rax
    3f4a:	ba 20 00 00 00       	mov    edx,0x20
    3f4f:	be 01 00 00 00       	mov    esi,0x1
    3f54:	e8 27 e6 ff ff       	call   2580 <fwrite@plt>
    3f59:	48 89 df             	mov    rdi,rbx
    3f5c:	e8 7f e4 ff ff       	call   23e0 <fclose@plt>
    3f61:	48 8b 84 24 d8 28 00 	mov    rax,QWORD PTR [rsp+0x28d8]
    3f68:	00 
    3f69:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    3f70:	00 00 
    3f72:	75 10                	jne    3f84 <socket@plt+0x19b4>
    3f74:	48 81 c4 e0 28 00 00 	add    rsp,0x28e0
    3f7b:	5b                   	pop    rbx
    3f7c:	5d                   	pop    rbp
    3f7d:	41 5c                	pop    r12
    3f7f:	41 5d                	pop    r13
    3f81:	41 5e                	pop    r14
    3f83:	c3                   	ret
    3f84:	e8 77 e4 ff ff       	call   2400 <__stack_chk_fail@plt>
    3f89:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    3f90:	f3 0f 1e fa          	endbr64
    3f94:	55                   	push   rbp
    3f95:	48 89 fd             	mov    rbp,rdi
    3f98:	48 8d 3d c3 22 00 00 	lea    rdi,[rip+0x22c3]        # 6262 <socket@plt+0x3c92>
    3f9f:	53                   	push   rbx
    3fa0:	48 83 ec 08          	sub    rsp,0x8
    3fa4:	e8 67 e3 ff ff       	call   2310 <getenv@plt>
    3fa9:	48 8d 35 48 22 00 00 	lea    rsi,[rip+0x2248]        # 61f8 <socket@plt+0x3c28>
    3fb0:	48 85 c0             	test   rax,rax
    3fb3:	48 89 c7             	mov    rdi,rax
    3fb6:	48 8d 05 8b 22 00 00 	lea    rax,[rip+0x228b]        # 6248 <socket@plt+0x3c78>
    3fbd:	48 0f 44 f8          	cmove  rdi,rax
    3fc1:	e8 6a e5 ff ff       	call   2530 <fopen@plt>
    3fc6:	48 85 c0             	test   rax,rax
    3fc9:	74 35                	je     4000 <socket@plt+0x1a30>
    3fcb:	48 89 ef             	mov    rdi,rbp
    3fce:	48 89 c1             	mov    rcx,rax
    3fd1:	ba 20 00 00 00       	mov    edx,0x20
    3fd6:	be 01 00 00 00       	mov    esi,0x1
    3fdb:	48 89 c3             	mov    rbx,rax
    3fde:	e8 bd e3 ff ff       	call   23a0 <fread@plt>
    3fe3:	48 89 df             	mov    rdi,rbx
    3fe6:	48 89 c5             	mov    rbp,rax
    3fe9:	e8 f2 e3 ff ff       	call   23e0 <fclose@plt>
    3fee:	31 c0                	xor    eax,eax
    3ff0:	48 83 fd 20          	cmp    rbp,0x20
    3ff4:	0f 95 c0             	setne  al
    3ff7:	f7 d8                	neg    eax
    3ff9:	48 83 c4 08          	add    rsp,0x8
    3ffd:	5b                   	pop    rbx
    3ffe:	5d                   	pop    rbp
    3fff:	c3                   	ret
    4000:	83 c8 ff             	or     eax,0xffffffff
    4003:	eb f4                	jmp    3ff9 <socket@plt+0x1a29>
    4005:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    400c:	00 00 00 00 
    4010:	f3 0f 1e fa          	endbr64
    4014:	41 57                	push   r15
    4016:	41 56                	push   r14
    4018:	41 55                	push   r13
    401a:	41 54                	push   r12
    401c:	55                   	push   rbp
    401d:	53                   	push   rbx
    401e:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    4025:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    402a:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    4031:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    4036:	48 81 ec 48 0c 00 00 	sub    rsp,0xc48
    403d:	4c 8d 3d 0c 78 00 00 	lea    r15,[rip+0x780c]        # b850 <socket@plt+0x9280>
    4044:	4c 8d 25 85 26 00 00 	lea    r12,[rip+0x2685]        # 66d0 <socket@plt+0x4100>
    404b:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    4052:	00 00 
    4054:	48 89 84 24 38 2c 00 	mov    QWORD PTR [rsp+0x2c38],rax
    405b:	00 
    405c:	31 c0                	xor    eax,eax
    405e:	48 8d 9c 24 b0 03 00 	lea    rbx,[rsp+0x3b0]
    4065:	00 
    4066:	41 89 fd             	mov    r13d,edi
    4069:	4c 8d b4 24 22 2b 00 	lea    r14,[rsp+0x2b22]
    4070:	00 
    4071:	48 89 df             	mov    rdi,rbx
    4074:	e8 17 fa ff ff       	call   3a90 <socket@plt+0x14c0>
    4079:	eb 26                	jmp    40a1 <socket@plt+0x1ad1>
    407b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    4080:	48 89 f2             	mov    rdx,rsi
    4083:	0f b7 cd             	movzx  ecx,bp
    4086:	48 89 de             	mov    rsi,rbx
    4089:	44 89 ef             	mov    edi,r13d
    408c:	e8 6f f6 ff ff       	call   3700 <socket@plt+0x1130>
    4091:	48 81 c3 32 01 00 00 	add    rbx,0x132
    4098:	49 83 c7 18          	add    r15,0x18
    409c:	49 39 de             	cmp    r14,rbx
    409f:	74 6f                	je     4110 <socket@plt+0x1b40>
    40a1:	0f b7 6b 30          	movzx  ebp,WORD PTR [rbx+0x30]
    40a5:	48 8d 73 32          	lea    rsi,[rbx+0x32]
    40a9:	41 f6 07 04          	test   BYTE PTR [r15],0x4
    40ad:	74 d1                	je     4080 <socket@plt+0x1ab0>
    40af:	66 85 ed             	test   bp,bp
    40b2:	74 cc                	je     4080 <socket@plt+0x1ab0>
    40b4:	44 0f b7 c5          	movzx  r8d,bp
    40b8:	48 8d bc 24 30 2b 00 	lea    rdi,[rsp+0x2b30]
    40bf:	00 
    40c0:	b9 00 01 00 00       	mov    ecx,0x100
    40c5:	4c 89 c2             	mov    rdx,r8
    40c8:	4c 89 44 24 08       	mov    QWORD PTR [rsp+0x8],r8
    40cd:	e8 be e3 ff ff       	call   2490 <__memcpy_chk@plt>
    40d2:	4c 8b 44 24 08       	mov    r8,QWORD PTR [rsp+0x8]
    40d7:	80 b4 24 30 2b 00 00 	xor    BYTE PTR [rsp+0x2b30],0xd
    40de:	0d 
    40df:	48 89 c7             	mov    rdi,rax
    40e2:	b8 01 00 00 00       	mov    eax,0x1
    40e7:	49 83 f8 01          	cmp    r8,0x1
    40eb:	74 1a                	je     4107 <socket@plt+0x1b37>
    40ed:	0f 1f 00             	nop    DWORD PTR [rax]
    40f0:	48 89 c2             	mov    rdx,rax
    40f3:	83 e2 0f             	and    edx,0xf
    40f6:	41 0f b6 14 14       	movzx  edx,BYTE PTR [r12+rdx*1]
    40fb:	30 14 07             	xor    BYTE PTR [rdi+rax*1],dl
    40fe:	48 83 c0 01          	add    rax,0x1
    4102:	4c 39 c0             	cmp    rax,r8
    4105:	75 e9                	jne    40f0 <socket@plt+0x1b20>
    4107:	48 89 fe             	mov    rsi,rdi
    410a:	e9 71 ff ff ff       	jmp    4080 <socket@plt+0x1ab0>
    410f:	90                   	nop
    4110:	48 8d 3d fe 20 00 00 	lea    rdi,[rip+0x20fe]        # 6215 <socket@plt+0x3c45>
    4117:	48 8d 5c 24 10       	lea    rbx,[rsp+0x10]
    411c:	e8 ef e1 ff ff       	call   2310 <getenv@plt>
    4121:	48 8d 35 d0 20 00 00 	lea    rsi,[rip+0x20d0]        # 61f8 <socket@plt+0x3c28>
    4128:	48 85 c0             	test   rax,rax
    412b:	48 89 c7             	mov    rdi,rax
    412e:	48 8d 05 c6 20 00 00 	lea    rax,[rip+0x20c6]        # 61fb <socket@plt+0x3c2b>
    4135:	48 0f 44 f8          	cmove  rdi,rax
    4139:	e8 f2 e3 ff ff       	call   2530 <fopen@plt>
    413e:	48 89 c5             	mov    rbp,rax
    4141:	48 85 c0             	test   rax,rax
    4144:	74 7a                	je     41c0 <socket@plt+0x1bf0>
    4146:	48 89 df             	mov    rdi,rbx
    4149:	48 89 c1             	mov    rcx,rax
    414c:	ba 03 00 00 00       	mov    edx,0x3
    4151:	be 32 01 00 00       	mov    esi,0x132
    4156:	e8 45 e2 ff ff       	call   23a0 <fread@plt>
    415b:	48 89 ef             	mov    rdi,rbp
    415e:	e8 7d e2 ff ff       	call   23e0 <fclose@plt>
    4163:	48 8d ac 24 a6 03 00 	lea    rbp,[rsp+0x3a6]
    416a:	00 
    416b:	0f b7 4b 30          	movzx  ecx,WORD PTR [rbx+0x30]
    416f:	48 8d 53 32          	lea    rdx,[rbx+0x32]
    4173:	48 89 de             	mov    rsi,rbx
    4176:	44 89 ef             	mov    edi,r13d
    4179:	48 81 c3 32 01 00 00 	add    rbx,0x132
    4180:	e8 7b f5 ff ff       	call   3700 <socket@plt+0x1130>
    4185:	48 39 eb             	cmp    rbx,rbp
    4188:	75 e1                	jne    416b <socket@plt+0x1b9b>
    418a:	31 c9                	xor    ecx,ecx
    418c:	31 d2                	xor    edx,edx
    418e:	be 08 00 00 00       	mov    esi,0x8
    4193:	44 89 ef             	mov    edi,r13d
    4196:	e8 15 e9 ff ff       	call   2ab0 <socket@plt+0x4e0>
    419b:	48 8b 84 24 38 2c 00 	mov    rax,QWORD PTR [rsp+0x2c38]
    41a2:	00 
    41a3:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    41aa:	00 00 
    41ac:	75 22                	jne    41d0 <socket@plt+0x1c00>
    41ae:	48 81 c4 48 2c 00 00 	add    rsp,0x2c48
    41b5:	5b                   	pop    rbx
    41b6:	5d                   	pop    rbp
    41b7:	41 5c                	pop    r12
    41b9:	41 5d                	pop    r13
    41bb:	41 5e                	pop    r14
    41bd:	41 5f                	pop    r15
    41bf:	c3                   	ret
    41c0:	b9 72 00 00 00       	mov    ecx,0x72
    41c5:	48 89 df             	mov    rdi,rbx
    41c8:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    41cb:	ab                   	stos   DWORD PTR [rdi],eax
    41cc:	66 ab                	stos   WORD PTR [rdi],ax
    41ce:	eb 93                	jmp    4163 <socket@plt+0x1b93>
    41d0:	e8 2b e2 ff ff       	call   2400 <__stack_chk_fail@plt>
    41d5:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    41dc:	00 00 00 
    41df:	90                   	nop
    41e0:	49 89 c8             	mov    r8,rcx
    41e3:	31 c0                	xor    eax,eax
    41e5:	48 89 d1             	mov    rcx,rdx
    41e8:	48 89 f2             	mov    rdx,rsi
    41eb:	48 8d 35 da 22 00 00 	lea    rsi,[rip+0x22da]        # 64cc <socket@plt+0x3efc>
    41f2:	e9 79 e1 ff ff       	jmp    2370 <__isoc23_sscanf@plt>
    41f7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    41fe:	00 00 
    4200:	f3 0f 1e fa          	endbr64
    4204:	48 83 ec 28          	sub    rsp,0x28
    4208:	48 8d 3d c6 22 00 00 	lea    rdi,[rip+0x22c6]        # 64d5 <socket@plt+0x3f05>
    420f:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    4216:	00 00 
    4218:	48 89 44 24 18       	mov    QWORD PTR [rsp+0x18],rax
    421d:	31 c0                	xor    eax,eax
    421f:	48 8d 4c 24 14       	lea    rcx,[rsp+0x14]
    4224:	48 8d 54 24 10       	lea    rdx,[rsp+0x10]
    4229:	48 8d 74 24 0c       	lea    rsi,[rsp+0xc]
    422e:	e8 ad ff ff ff       	call   41e0 <socket@plt+0x1c10>
    4233:	48 8b 44 24 18       	mov    rax,QWORD PTR [rsp+0x18]
    4238:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    423f:	00 00 
    4241:	75 05                	jne    4248 <socket@plt+0x1c78>
    4243:	48 83 c4 28          	add    rsp,0x28
    4247:	c3                   	ret
    4248:	e8 b3 e1 ff ff       	call   2400 <__stack_chk_fail@plt>
    424d:	0f 1f 00             	nop    DWORD PTR [rax]
    4250:	f3 0f 1e fa          	endbr64
    4254:	53                   	push   rbx
    4255:	89 f3                	mov    ebx,esi
    4257:	48 89 d6             	mov    rsi,rdx
    425a:	48 83 ec 40          	sub    rsp,0x40
    425e:	64 48 8b 14 25 28 00 	mov    rdx,QWORD PTR fs:0x28
    4265:	00 00 
    4267:	48 89 54 24 38       	mov    QWORD PTR [rsp+0x38],rdx
    426c:	31 d2                	xor    edx,edx
    426e:	8d 51 ff             	lea    edx,[rcx-0x1]
    4271:	66 83 fa 1e          	cmp    dx,0x1e
    4275:	76 49                	jbe    42c0 <socket@plt+0x1cf0>
    4277:	45 31 c0             	xor    r8d,r8d
    427a:	31 c0                	xor    eax,eax
    427c:	41 b9 03 00 00 00    	mov    r9d,0x3
    4282:	b9 01 00 00 00       	mov    ecx,0x1
    4287:	48 8d 15 4d 22 00 00 	lea    rdx,[rip+0x224d]        # 64db <socket@plt+0x3f0b>
    428e:	be 02 00 00 00       	mov    esi,0x2
    4293:	89 df                	mov    edi,ebx
    4295:	e8 b6 e2 ff ff       	call   2550 <__dprintf_chk@plt>
    429a:	48 8b 44 24 38       	mov    rax,QWORD PTR [rsp+0x38]
    429f:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    42a6:	00 00 
    42a8:	0f 85 ca 00 00 00    	jne    4378 <socket@plt+0x1da8>
    42ae:	48 83 c4 40          	add    rsp,0x40
    42b2:	31 c0                	xor    eax,eax
    42b4:	5b                   	pop    rbx
    42b5:	c3                   	ret
    42b6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    42bd:	00 00 00 
    42c0:	89 c8                	mov    eax,ecx
    42c2:	48 8d 7c 24 10       	lea    rdi,[rsp+0x10]
    42c7:	0f b7 c9             	movzx  ecx,cx
    42ca:	48 89 f2             	mov    rdx,rsi
    42cd:	49 89 f8             	mov    r8,rdi
    42d0:	83 f9 08             	cmp    ecx,0x8
    42d3:	73 7b                	jae    4350 <socket@plt+0x1d80>
    42d5:	31 f6                	xor    esi,esi
    42d7:	f6 c1 04             	test   cl,0x4
    42da:	75 5c                	jne    4338 <socket@plt+0x1d68>
    42dc:	f6 c1 02             	test   cl,0x2
    42df:	75 3f                	jne    4320 <socket@plt+0x1d50>
    42e1:	83 e1 01             	and    ecx,0x1
    42e4:	75 2a                	jne    4310 <socket@plt+0x1d40>
    42e6:	0f b7 c0             	movzx  eax,ax
    42e9:	48 8d 4c 24 0c       	lea    rcx,[rsp+0xc]
    42ee:	48 8d 54 24 08       	lea    rdx,[rsp+0x8]
    42f3:	48 8d 74 24 04       	lea    rsi,[rsp+0x4]
    42f8:	c6 44 04 10 00       	mov    BYTE PTR [rsp+rax*1+0x10],0x0
    42fd:	e8 de fe ff ff       	call   41e0 <socket@plt+0x1c10>
    4302:	e9 70 ff ff ff       	jmp    4277 <socket@plt+0x1ca7>
    4307:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    430e:	00 00 
    4310:	0f b6 14 32          	movzx  edx,BYTE PTR [rdx+rsi*1]
    4314:	41 88 14 30          	mov    BYTE PTR [r8+rsi*1],dl
    4318:	eb cc                	jmp    42e6 <socket@plt+0x1d16>
    431a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    4320:	44 0f b7 0c 32       	movzx  r9d,WORD PTR [rdx+rsi*1]
    4325:	66 45 89 0c 30       	mov    WORD PTR [r8+rsi*1],r9w
    432a:	48 83 c6 02          	add    rsi,0x2
    432e:	83 e1 01             	and    ecx,0x1
    4331:	74 b3                	je     42e6 <socket@plt+0x1d16>
    4333:	eb db                	jmp    4310 <socket@plt+0x1d40>
    4335:	0f 1f 00             	nop    DWORD PTR [rax]
    4338:	8b 32                	mov    esi,DWORD PTR [rdx]
    433a:	41 89 30             	mov    DWORD PTR [r8],esi
    433d:	be 04 00 00 00       	mov    esi,0x4
    4342:	f6 c1 02             	test   cl,0x2
    4345:	74 9a                	je     42e1 <socket@plt+0x1d11>
    4347:	eb d7                	jmp    4320 <socket@plt+0x1d50>
    4349:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    4350:	41 89 ca             	mov    r10d,ecx
    4353:	31 d2                	xor    edx,edx
    4355:	41 83 e2 f8          	and    r10d,0xfffffff8
    4359:	41 89 d0             	mov    r8d,edx
    435c:	83 c2 08             	add    edx,0x8
    435f:	4e 8b 0c 06          	mov    r9,QWORD PTR [rsi+r8*1]
    4363:	4e 89 0c 07          	mov    QWORD PTR [rdi+r8*1],r9
    4367:	44 39 d2             	cmp    edx,r10d
    436a:	72 ed                	jb     4359 <socket@plt+0x1d89>
    436c:	4c 8d 04 17          	lea    r8,[rdi+rdx*1]
    4370:	48 01 f2             	add    rdx,rsi
    4373:	e9 5d ff ff ff       	jmp    42d5 <socket@plt+0x1d05>
    4378:	e8 83 e0 ff ff       	call   2400 <__stack_chk_fail@plt>
    437d:	0f 1f 00             	nop    DWORD PTR [rax]
    4380:	80 3f 53             	cmp    BYTE PTR [rdi],0x53
    4383:	75 34                	jne    43b9 <socket@plt+0x1de9>
    4385:	80 7f 01 50          	cmp    BYTE PTR [rdi+0x1],0x50
    4389:	75 2e                	jne    43b9 <socket@plt+0x1de9>
    438b:	80 7f 02 31          	cmp    BYTE PTR [rdi+0x2],0x31
    438f:	75 28                	jne    43b9 <socket@plt+0x1de9>
    4391:	f3 0f 7e 07          	movq   xmm0,QWORD PTR [rdi]
    4395:	66 0f ef c9          	pxor   xmm1,xmm1
    4399:	66 0f 6f d0          	movdqa xmm2,xmm0
    439d:	66 0f f6 d1          	psadbw xmm2,xmm1
    43a1:	66 48 0f 7e d0       	movq   rax,xmm2
    43a6:	38 47 08             	cmp    BYTE PTR [rdi+0x8],al
    43a9:	75 0e                	jne    43b9 <socket@plt+0x1de9>
    43ab:	8b 47 03             	mov    eax,DWORD PTR [rdi+0x3]
    43ae:	89 06                	mov    DWORD PTR [rsi],eax
    43b0:	0f b6 47 07          	movzx  eax,BYTE PTR [rdi+0x7]
    43b4:	88 02                	mov    BYTE PTR [rdx],al
    43b6:	31 c0                	xor    eax,eax
    43b8:	c3                   	ret
    43b9:	b8 ff ff ff ff       	mov    eax,0xffffffff
    43be:	c3                   	ret
    43bf:	90                   	nop
    43c0:	f3 0f 1e fa          	endbr64
    43c4:	48 83 ec 28          	sub    rsp,0x28
    43c8:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    43cf:	00 00 
    43d1:	48 89 44 24 18       	mov    QWORD PTR [rsp+0x18],rax
    43d6:	31 c0                	xor    eax,eax
    43d8:	48 8d 54 24 03       	lea    rdx,[rsp+0x3]
    43dd:	b8 57 86 ff ff       	mov    eax,0xffff8657
    43e2:	48 8d 74 24 04       	lea    rsi,[rsp+0x4]
    43e7:	48 8d 7c 24 08       	lea    rdi,[rsp+0x8]
    43ec:	c6 44 24 10 a5       	mov    BYTE PTR [rsp+0x10],0xa5
    43f1:	48 c7 44 24 08 53 50 	mov    QWORD PTR [rsp+0x8],0x315053
    43f8:	31 00 
    43fa:	66 89 44 24 0c       	mov    WORD PTR [rsp+0xc],ax
    43ff:	c6 44 24 0e f4       	mov    BYTE PTR [rsp+0xe],0xf4
    4404:	e8 77 ff ff ff       	call   4380 <socket@plt+0x1db0>
    4409:	85 c0                	test   eax,eax
    440b:	74 1b                	je     4428 <socket@plt+0x1e58>
    440d:	48 8b 44 24 18       	mov    rax,QWORD PTR [rsp+0x18]
    4412:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    4419:	00 00 
    441b:	75 2a                	jne    4447 <socket@plt+0x1e77>
    441d:	48 83 c4 28          	add    rsp,0x28
    4421:	c3                   	ret
    4422:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    4428:	31 ff                	xor    edi,edi
    442a:	e8 81 e0 ff ff       	call   24b0 <time@plt>
    442f:	39 44 24 04          	cmp    DWORD PTR [rsp+0x4],eax
    4433:	76 d8                	jbe    440d <socket@plt+0x1e3d>
    4435:	31 c0                	xor    eax,eax
    4437:	80 7c 24 03 00       	cmp    BYTE PTR [rsp+0x3],0x0
    443c:	0f 95 c0             	setne  al
    443f:	89 05 df 7b 00 00    	mov    DWORD PTR [rip+0x7bdf],eax        # c024 <socket@plt+0x9a54>
    4445:	eb c6                	jmp    440d <socket@plt+0x1e3d>
    4447:	e8 b4 df ff ff       	call   2400 <__stack_chk_fail@plt>
    444c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    4450:	f3 0f 1e fa          	endbr64
    4454:	48 83 ec 08          	sub    rsp,0x8
    4458:	8b 05 c6 7b 00 00    	mov    eax,DWORD PTR [rip+0x7bc6]        # c024 <socket@plt+0x9a54>
    445e:	89 f7                	mov    edi,esi
    4460:	48 8d 0d 94 20 00 00 	lea    rcx,[rip+0x2094]        # 64fb <socket@plt+0x3f2b>
    4467:	48 8d 15 93 20 00 00 	lea    rdx,[rip+0x2093]        # 6501 <socket@plt+0x3f31>
    446e:	be 02 00 00 00       	mov    esi,0x2
    4473:	85 c0                	test   eax,eax
    4475:	48 8d 05 77 20 00 00 	lea    rax,[rip+0x2077]        # 64f3 <socket@plt+0x3f23>
    447c:	48 0f 45 c8          	cmovne rcx,rax
    4480:	31 c0                	xor    eax,eax
    4482:	e8 c9 e0 ff ff       	call   2550 <__dprintf_chk@plt>
    4487:	31 c0                	xor    eax,eax
    4489:	48 83 c4 08          	add    rsp,0x8
    448d:	c3                   	ret
    448e:	66 90                	xchg   ax,ax
    4490:	55                   	push   rbp
    4491:	89 fd                	mov    ebp,edi
    4493:	31 ff                	xor    edi,edi
    4495:	53                   	push   rbx
    4496:	89 f3                	mov    ebx,esi
    4498:	48 83 ec 08          	sub    rsp,0x8
    449c:	e8 0f e0 ff ff       	call   24b0 <time@plt>
    44a1:	48 63 0d 9c 7b 00 00 	movsxd rcx,DWORD PTR [rip+0x7b9c]        # c044 <socket@plt+0x9a74>
    44a8:	48 8d 15 b1 7b 00 00 	lea    rdx,[rip+0x7bb1]        # c060 <socket@plt+0x9a90>
    44af:	48 89 c6             	mov    rsi,rax
    44b2:	48 89 c8             	mov    rax,rcx
    44b5:	89 34 ca             	mov    DWORD PTR [rdx+rcx*8],esi
    44b8:	83 c0 01             	add    eax,0x1
    44bb:	66 89 6c ca 04       	mov    WORD PTR [rdx+rcx*8+0x4],bp
    44c0:	66 89 5c ca 06       	mov    WORD PTR [rdx+rcx*8+0x6],bx
    44c5:	99                   	cdq
    44c6:	c1 ea 1a             	shr    edx,0x1a
    44c9:	01 d0                	add    eax,edx
    44cb:	83 e0 3f             	and    eax,0x3f
    44ce:	29 d0                	sub    eax,edx
    44d0:	89 05 6e 7b 00 00    	mov    DWORD PTR [rip+0x7b6e],eax        # c044 <socket@plt+0x9a74>
    44d6:	8b 05 64 7b 00 00    	mov    eax,DWORD PTR [rip+0x7b64]        # c040 <socket@plt+0x9a70>
    44dc:	83 f8 3f             	cmp    eax,0x3f
    44df:	7f 09                	jg     44ea <socket@plt+0x1f1a>
    44e1:	83 c0 01             	add    eax,0x1
    44e4:	89 05 56 7b 00 00    	mov    DWORD PTR [rip+0x7b56],eax        # c040 <socket@plt+0x9a70>
    44ea:	48 83 c4 08          	add    rsp,0x8
    44ee:	5b                   	pop    rbx
    44ef:	5d                   	pop    rbp
    44f0:	c3                   	ret
    44f1:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
    44f8:	00 00 00 00 
    44fc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    4500:	41 56                	push   r14
    4502:	48 8d 3d 22 20 00 00 	lea    rdi,[rip+0x2022]        # 652b <socket@plt+0x3f5b>
    4509:	41 55                	push   r13
    450b:	41 54                	push   r12
    450d:	55                   	push   rbp
    450e:	53                   	push   rbx
    450f:	e8 fc dd ff ff       	call   2310 <getenv@plt>
    4514:	48 8d 35 1d 20 00 00 	lea    rsi,[rip+0x201d]        # 6538 <socket@plt+0x3f68>
    451b:	48 85 c0             	test   rax,rax
    451e:	48 89 c7             	mov    rdi,rax
    4521:	48 8d 05 e8 1f 00 00 	lea    rax,[rip+0x1fe8]        # 6510 <socket@plt+0x3f40>
    4528:	48 0f 44 f8          	cmove  rdi,rax
    452c:	e8 ff df ff ff       	call   2530 <fopen@plt>
    4531:	48 85 c0             	test   rax,rax
    4534:	0f 84 9a 00 00 00    	je     45d4 <socket@plt+0x2004>
    453a:	8b 15 00 7b 00 00    	mov    edx,DWORD PTR [rip+0x7b00]        # c040 <socket@plt+0x9a70>
    4540:	8b 1d fe 7a 00 00    	mov    ebx,DWORD PTR [rip+0x7afe]        # c044 <socket@plt+0x9a74>
    4546:	48 89 c5             	mov    rbp,rax
    4549:	29 d3                	sub    ebx,edx
    454b:	83 c3 40             	add    ebx,0x40
    454e:	89 d8                	mov    eax,ebx
    4550:	c1 f8 1f             	sar    eax,0x1f
    4553:	c1 e8 1a             	shr    eax,0x1a
    4556:	01 c3                	add    ebx,eax
    4558:	83 e3 3f             	and    ebx,0x3f
    455b:	29 c3                	sub    ebx,eax
    455d:	85 d2                	test   edx,edx
    455f:	7e 57                	jle    45b8 <socket@plt+0x1fe8>
    4561:	45 31 ed             	xor    r13d,r13d
    4564:	4c 8d 35 f5 7a 00 00 	lea    r14,[rip+0x7af5]        # c060 <socket@plt+0x9a90>
    456b:	4c 8d 25 c9 1f 00 00 	lea    r12,[rip+0x1fc9]        # 653b <socket@plt+0x3f6b>
    4572:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    4578:	42 8d 04 2b          	lea    eax,[rbx+r13*1]
    457c:	be 02 00 00 00       	mov    esi,0x2
    4581:	48 89 ef             	mov    rdi,rbp
    4584:	41 83 c5 01          	add    r13d,0x1
    4588:	99                   	cdq
    4589:	c1 ea 1a             	shr    edx,0x1a
    458c:	01 d0                	add    eax,edx
    458e:	83 e0 3f             	and    eax,0x3f
    4591:	29 d0                	sub    eax,edx
    4593:	4c 89 e2             	mov    rdx,r12
    4596:	48 98                	cdqe
    4598:	41 8b 0c c6          	mov    ecx,DWORD PTR [r14+rax*8]
    459c:	45 0f b7 4c c6 06    	movzx  r9d,WORD PTR [r14+rax*8+0x6]
    45a2:	45 0f b7 44 c6 04    	movzx  r8d,WORD PTR [r14+rax*8+0x4]
    45a8:	31 c0                	xor    eax,eax
    45aa:	e8 e1 df ff ff       	call   2590 <__fprintf_chk@plt>
    45af:	44 39 2d 8a 7a 00 00 	cmp    DWORD PTR [rip+0x7a8a],r13d        # c040 <socket@plt+0x9a70>
    45b6:	7f c0                	jg     4578 <socket@plt+0x1fa8>
    45b8:	48 89 ef             	mov    rdi,rbp
    45bb:	e8 20 de ff ff       	call   23e0 <fclose@plt>
    45c0:	c7 05 76 7a 00 00 00 	mov    DWORD PTR [rip+0x7a76],0x0        # c040 <socket@plt+0x9a70>
    45c7:	00 00 00 
    45ca:	c7 05 70 7a 00 00 00 	mov    DWORD PTR [rip+0x7a70],0x0        # c044 <socket@plt+0x9a74>
    45d1:	00 00 00 
    45d4:	5b                   	pop    rbx
    45d5:	5d                   	pop    rbp
    45d6:	41 5c                	pop    r12
    45d8:	41 5d                	pop    r13
    45da:	41 5e                	pop    r14
    45dc:	c3                   	ret
    45dd:	0f 1f 00             	nop    DWORD PTR [rax]
    45e0:	f3 0f 1e fa          	endbr64
    45e4:	48 83 ec 08          	sub    rsp,0x8
    45e8:	31 f6                	xor    esi,esi
    45ea:	0f b7 ff             	movzx  edi,di
    45ed:	e8 9e fe ff ff       	call   4490 <socket@plt+0x1ec0>
    45f2:	83 3d 47 7a 00 00 3f 	cmp    DWORD PTR [rip+0x7a47],0x3f        # c040 <socket@plt+0x9a70>
    45f9:	7f 05                	jg     4600 <socket@plt+0x2030>
    45fb:	48 83 c4 08          	add    rsp,0x8
    45ff:	c3                   	ret
    4600:	48 83 c4 08          	add    rsp,0x8
    4604:	e9 f7 fe ff ff       	jmp    4500 <socket@plt+0x1f30>
    4609:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    4610:	f3 0f 1e fa          	endbr64
    4614:	53                   	push   rbx
    4615:	89 f3                	mov    ebx,esi
    4617:	66 83 f9 01          	cmp    cx,0x1
    461b:	76 53                	jbe    4670 <socket@plt+0x20a0>
    461d:	0f b7 3a             	movzx  edi,WORD PTR [rdx]
    4620:	31 f6                	xor    esi,esi
    4622:	66 83 f9 03          	cmp    cx,0x3
    4626:	77 28                	ja     4650 <socket@plt+0x2080>
    4628:	e8 63 fe ff ff       	call   4490 <socket@plt+0x1ec0>
    462d:	83 3d 0c 7a 00 00 1f 	cmp    DWORD PTR [rip+0x7a0c],0x1f        # c040 <socket@plt+0x9a70>
    4634:	7f 2c                	jg     4662 <socket@plt+0x2092>
    4636:	89 df                	mov    edi,ebx
    4638:	48 8d 15 06 1f 00 00 	lea    rdx,[rip+0x1f06]        # 6545 <socket@plt+0x3f75>
    463f:	be 02 00 00 00       	mov    esi,0x2
    4644:	31 c0                	xor    eax,eax
    4646:	e8 05 df ff ff       	call   2550 <__dprintf_chk@plt>
    464b:	31 c0                	xor    eax,eax
    464d:	5b                   	pop    rbx
    464e:	c3                   	ret
    464f:	90                   	nop
    4650:	0f b7 72 02          	movzx  esi,WORD PTR [rdx+0x2]
    4654:	e8 37 fe ff ff       	call   4490 <socket@plt+0x1ec0>
    4659:	83 3d e0 79 00 00 1f 	cmp    DWORD PTR [rip+0x79e0],0x1f        # c040 <socket@plt+0x9a70>
    4660:	7e d4                	jle    4636 <socket@plt+0x2066>
    4662:	e8 99 fe ff ff       	call   4500 <socket@plt+0x1f30>
    4667:	eb cd                	jmp    4636 <socket@plt+0x2066>
    4669:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    4670:	31 ff                	xor    edi,edi
    4672:	31 f6                	xor    esi,esi
    4674:	eb b2                	jmp    4628 <socket@plt+0x2058>
    4676:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    467d:	00 00 00 
    4680:	f3 0f 1e fa          	endbr64
    4684:	55                   	push   rbp
    4685:	53                   	push   rbx
    4686:	89 f3                	mov    ebx,esi
    4688:	48 83 ec 08          	sub    rsp,0x8
    468c:	66 83 f9 05          	cmp    cx,0x5
    4690:	76 23                	jbe    46b5 <socket@plt+0x20e5>
    4692:	0f b7 42 04          	movzx  eax,WORD PTR [rdx+0x4]
    4696:	8b 32                	mov    esi,DWORD PTR [rdx]
    4698:	8d 50 ff             	lea    edx,[rax-0x1]
    469b:	66 83 fa 7e          	cmp    dx,0x7e
    469f:	77 14                	ja     46b5 <socket@plt+0x20e5>
    46a1:	48 83 c0 06          	add    rax,0x6
    46a5:	0f b7 c9             	movzx  ecx,cx
    46a8:	48 39 c8             	cmp    rax,rcx
    46ab:	75 08                	jne    46b5 <socket@plt+0x20e5>
    46ad:	81 fe 00 00 00 04    	cmp    esi,0x4000000
    46b3:	76 23                	jbe    46d8 <socket@plt+0x2108>
    46b5:	48 8d 15 2a 1a 00 00 	lea    rdx,[rip+0x1a2a]        # 60e6 <socket@plt+0x3b16>
    46bc:	be 02 00 00 00       	mov    esi,0x2
    46c1:	89 df                	mov    edi,ebx
    46c3:	31 c0                	xor    eax,eax
    46c5:	e8 86 de ff ff       	call   2550 <__dprintf_chk@plt>
    46ca:	48 83 c4 08          	add    rsp,0x8
    46ce:	31 c0                	xor    eax,eax
    46d0:	5b                   	pop    rbx
    46d1:	5d                   	pop    rbp
    46d2:	c3                   	ret
    46d3:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    46d8:	48 89 fd             	mov    rbp,rdi
    46db:	be 84 00 00 00       	mov    esi,0x84
    46e0:	bf 01 00 00 00       	mov    edi,0x1
    46e5:	e8 76 dd ff ff       	call   2460 <calloc@plt>
    46ea:	48 89 c7             	mov    rdi,rax
    46ed:	48 85 c0             	test   rax,rax
    46f0:	74 c3                	je     46b5 <socket@plt+0x20e5>
    46f2:	0f b7 6d 14          	movzx  ebp,WORD PTR [rbp+0x14]
    46f6:	83 e5 01             	and    ebp,0x1
    46f9:	e8 32 dc ff ff       	call   2330 <free@plt>
    46fe:	66 85 ed             	test   bp,bp
    4701:	74 25                	je     4728 <socket@plt+0x2158>
    4703:	89 df                	mov    edi,ebx
    4705:	48 8d 15 50 1e 00 00 	lea    rdx,[rip+0x1e50]        # 655c <socket@plt+0x3f8c>
    470c:	be 02 00 00 00       	mov    esi,0x2
    4711:	31 c0                	xor    eax,eax
    4713:	e8 38 de ff ff       	call   2550 <__dprintf_chk@plt>
    4718:	48 83 c4 08          	add    rsp,0x8
    471c:	31 c0                	xor    eax,eax
    471e:	5b                   	pop    rbx
    471f:	5d                   	pop    rbp
    4720:	c3                   	ret
    4721:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    4728:	48 8d 15 61 1f 00 00 	lea    rdx,[rip+0x1f61]        # 6690 <socket@plt+0x40c0>
    472f:	be 02 00 00 00       	mov    esi,0x2
    4734:	89 df                	mov    edi,ebx
    4736:	31 c0                	xor    eax,eax
    4738:	e8 13 de ff ff       	call   2550 <__dprintf_chk@plt>
    473d:	eb 8b                	jmp    46ca <socket@plt+0x20fa>
    473f:	90                   	nop
    4740:	f3 0f 1e fa          	endbr64
    4744:	53                   	push   rbx
    4745:	4c 8d 9c 24 00 c0 ff 	lea    r11,[rsp-0x4000]
    474c:	ff 
    474d:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
    4754:	48 83 0c 24 00       	or     QWORD PTR [rsp],0x0
    4759:	4c 39 dc             	cmp    rsp,r11
    475c:	75 ef                	jne    474d <socket@plt+0x217d>
    475e:	48 81 ec 90 0c 00 00 	sub    rsp,0xc90
    4765:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    476c:	00 00 
    476e:	48 89 84 24 88 4c 00 	mov    QWORD PTR [rsp+0x4c88],rax
    4775:	00 
    4776:	31 c0                	xor    eax,eax
    4778:	48 89 e7             	mov    rdi,rsp
    477b:	e8 10 f3 ff ff       	call   3a90 <socket@plt+0x14c0>
    4780:	48 8d 3d c6 1c 00 00 	lea    rdi,[rip+0x1cc6]        # 644d <socket@plt+0x3e7d>
    4787:	e8 94 f0 ff ff       	call   3820 <socket@plt+0x1250>
    478c:	85 c0                	test   eax,eax
    478e:	78 11                	js     47a1 <socket@plt+0x21d1>
    4790:	48 98                	cdqe
    4792:	48 69 c0 32 01 00 00 	imul   rax,rax,0x132
    4799:	66 83 7c 04 30 01    	cmp    WORD PTR [rsp+rax*1+0x30],0x1
    479f:	74 1f                	je     47c0 <socket@plt+0x21f0>
    47a1:	48 8b 84 24 88 4c 00 	mov    rax,QWORD PTR [rsp+0x4c88]
    47a8:	00 
    47a9:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    47b0:	00 00 
    47b2:	75 67                	jne    481b <socket@plt+0x224b>
    47b4:	48 81 c4 90 4c 00 00 	add    rsp,0x4c90
    47bb:	5b                   	pop    rbx
    47bc:	c3                   	ret
    47bd:	0f 1f 00             	nop    DWORD PTR [rax]
    47c0:	80 7c 04 32 31       	cmp    BYTE PTR [rsp+rax*1+0x32],0x31
    47c5:	75 da                	jne    47a1 <socket@plt+0x21d1>
    47c7:	48 8d 3d ba 1d 00 00 	lea    rdi,[rip+0x1dba]        # 6588 <socket@plt+0x3fb8>
    47ce:	e8 3d db ff ff       	call   2310 <getenv@plt>
    47d3:	48 8d 35 5e 1d 00 00 	lea    rsi,[rip+0x1d5e]        # 6538 <socket@plt+0x3f68>
    47da:	48 85 c0             	test   rax,rax
    47dd:	48 89 c7             	mov    rdi,rax
    47e0:	48 8d 05 88 1d 00 00 	lea    rax,[rip+0x1d88]        # 656f <socket@plt+0x3f9f>
    47e7:	48 0f 44 f8          	cmove  rdi,rax
    47eb:	e8 40 dd ff ff       	call   2530 <fopen@plt>
    47f0:	48 89 c3             	mov    rbx,rax
    47f3:	48 85 c0             	test   rax,rax
    47f6:	74 a9                	je     47a1 <socket@plt+0x21d1>
    47f8:	48 89 c1             	mov    rcx,rax
    47fb:	ba 08 00 00 00       	mov    edx,0x8
    4800:	be 01 00 00 00       	mov    esi,0x1
    4805:	48 8d 3d d4 1e 00 00 	lea    rdi,[rip+0x1ed4]        # 66e0 <socket@plt+0x4110>
    480c:	e8 6f dd ff ff       	call   2580 <fwrite@plt>
    4811:	48 89 df             	mov    rdi,rbx
    4814:	e8 c7 db ff ff       	call   23e0 <fclose@plt>
    4819:	eb 86                	jmp    47a1 <socket@plt+0x21d1>
    481b:	e8 e0 db ff ff       	call   2400 <__stack_chk_fail@plt>
    4820:	f3 0f 1e fa          	endbr64
    4824:	48 81 ec 58 08 00 00 	sub    rsp,0x858
    482b:	66 0f ef c0          	pxor   xmm0,xmm0
    482f:	49 89 d0             	mov    r8,rdx
    4832:	49 89 c9             	mov    r9,rcx
    4835:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    483c:	00 00 
    483e:	48 89 84 24 48 08 00 	mov    QWORD PTR [rsp+0x848],rax
    4845:	00 
    4846:	31 c0                	xor    eax,eax
    4848:	48 8d 05 63 01 00 00 	lea    rax,[rip+0x163]        # 49b2 <socket@plt+0x23e2>
    484f:	0f 29 04 24          	movaps XMMWORD PTR [rsp],xmm0
    4853:	48 8d 94 24 40 08 00 	lea    rdx,[rsp+0x840]
    485a:	00 
    485b:	0f 29 44 24 10       	movaps XMMWORD PTR [rsp+0x10],xmm0
    4860:	0f 29 44 24 20       	movaps XMMWORD PTR [rsp+0x20],xmm0
    4865:	0f 29 44 24 30       	movaps XMMWORD PTR [rsp+0x30],xmm0
    486a:	66 48 0f 6e c0       	movq   xmm0,rax
    486f:	48 8d 44 24 40       	lea    rax,[rsp+0x40]
    4874:	66 0f 6c c0          	punpcklqdq xmm0,xmm0
    4878:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
    487f:	00 
    4880:	0f 29 00             	movaps XMMWORD PTR [rax],xmm0
    4883:	48 83 c0 20          	add    rax,0x20
    4887:	0f 29 40 f0          	movaps XMMWORD PTR [rax-0x10],xmm0
    488b:	48 39 c2             	cmp    rdx,rax
    488e:	75 f0                	jne    4880 <socket@plt+0x22b0>
    4890:	48 8d 05 23 04 00 00 	lea    rax,[rip+0x423]        # 4cba <socket@plt+0x26ea>
    4897:	48 8d 0d 6a 04 00 00 	lea    rcx,[rip+0x46a]        # 4d08 <socket@plt+0x2738>
    489e:	66 48 0f 6e c1       	movq   xmm0,rcx
    48a3:	66 48 0f 6e c8       	movq   xmm1,rax
    48a8:	48 8d 0d bf 03 00 00 	lea    rcx,[rip+0x3bf]        # 4c6e <socket@plt+0x269e>
    48af:	66 0f 6c c1          	punpcklqdq xmm0,xmm1
    48b3:	48 8d 05 e7 02 00 00 	lea    rax,[rip+0x2e7]        # 4ba1 <socket@plt+0x25d1>
    48ba:	66 48 0f 6e d0       	movq   xmm2,rax
    48bf:	0f 11 44 24 48       	movups XMMWORD PTR [rsp+0x48],xmm0
    48c4:	66 48 0f 6e c1       	movq   xmm0,rcx
    48c9:	48 8d 05 53 02 00 00 	lea    rax,[rip+0x253]        # 4b23 <socket@plt+0x2553>
    48d0:	66 0f 6c c2          	punpcklqdq xmm0,xmm2
    48d4:	48 8d 0d 87 02 00 00 	lea    rcx,[rip+0x287]        # 4b62 <socket@plt+0x2592>
    48db:	66 48 0f 6e d8       	movq   xmm3,rax
    48e0:	0f 11 44 24 58       	movups XMMWORD PTR [rsp+0x58],xmm0
    48e5:	66 48 0f 6e c1       	movq   xmm0,rcx
    48ea:	48 8d 05 86 01 00 00 	lea    rax,[rip+0x186]        # 4a77 <socket@plt+0x24a7>
    48f1:	48 8d 0d ec 01 00 00 	lea    rcx,[rip+0x1ec]        # 4ae4 <socket@plt+0x2514>
    48f8:	66 0f 6c c3          	punpcklqdq xmm0,xmm3
    48fc:	66 48 0f 6e e0       	movq   xmm4,rax
    4901:	48 8d 05 08 01 00 00 	lea    rax,[rip+0x108]        # 4a10 <socket@plt+0x2440>
    4908:	0f 11 44 24 68       	movups XMMWORD PTR [rsp+0x68],xmm0
    490d:	66 48 0f 6e c1       	movq   xmm0,rcx
    4912:	66 48 0f 6e e8       	movq   xmm5,rax
    4917:	48 8d 0d 20 01 00 00 	lea    rcx,[rip+0x120]        # 4a3e <socket@plt+0x246e>
    491e:	66 0f 6c c4          	punpcklqdq xmm0,xmm4
    4922:	48 8d 05 15 04 00 00 	lea    rax,[rip+0x415]        # 4d3e <socket@plt+0x276e>
    4929:	0f 11 44 24 78       	movups XMMWORD PTR [rsp+0x78],xmm0
    492e:	66 48 0f 6e c1       	movq   xmm0,rcx
    4933:	66 48 0f 6e f0       	movq   xmm6,rax
    4938:	48 8d 0d a3 00 00 00 	lea    rcx,[rip+0xa3]        # 49e2 <socket@plt+0x2412>
    493f:	66 0f 6c c5          	punpcklqdq xmm0,xmm5
    4943:	48 8d 05 dc 02 00 00 	lea    rax,[rip+0x2dc]        # 4c26 <socket@plt+0x2656>
    494a:	0f 11 84 24 88 00 00 	movups XMMWORD PTR [rsp+0x88],xmm0
    4951:	00 
    4952:	66 48 0f 6e c1       	movq   xmm0,rcx
    4957:	48 8d 0d 49 01 00 00 	lea    rcx,[rip+0x149]        # 4aa7 <socket@plt+0x24d7>
    495e:	66 48 0f 6e f8       	movq   xmm7,rax
    4963:	66 0f 6c c6          	punpcklqdq xmm0,xmm6
    4967:	48 8d 05 72 02 00 00 	lea    rax,[rip+0x272]        # 4be0 <socket@plt+0x2610>
    496e:	0f 11 84 24 98 00 00 	movups XMMWORD PTR [rsp+0x98],xmm0
    4975:	00 
    4976:	66 48 0f 6e c1       	movq   xmm0,rcx
    497b:	48 89 84 24 b8 00 00 	mov    QWORD PTR [rsp+0xb8],rax
    4982:	00 
    4983:	66 0f 6c c7          	punpcklqdq xmm0,xmm7
    4987:	48 8d 05 4c 00 00 00 	lea    rax,[rip+0x4c]        # 49da <socket@plt+0x240a>
    498e:	48 89 84 24 38 08 00 	mov    QWORD PTR [rsp+0x838],rax
    4995:	00 
    4996:	0f 11 84 24 a8 00 00 	movups XMMWORD PTR [rsp+0xa8],xmm0
    499d:	00 
    499e:	48 85 f6             	test   rsi,rsi
    49a1:	74 3b                	je     49de <socket@plt+0x240e>
    49a3:	0f b6 07             	movzx  eax,BYTE PTR [rdi]
    49a6:	48 8b 54 c4 40       	mov    rdx,QWORD PTR [rsp+rax*8+0x40]
    49ab:	b8 01 00 00 00       	mov    eax,0x1
    49b0:	ff e2                	jmp    rdx
    49b2:	f3 0f 1e fa          	endbr64
    49b6:	b8 01 00 00 00       	mov    eax,0x1
    49bb:	48 8b 94 24 48 08 00 	mov    rdx,QWORD PTR [rsp+0x848]
    49c2:	00 
    49c3:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    49ca:	00 00 
    49cc:	0f 85 af 03 00 00    	jne    4d81 <socket@plt+0x27b1>
    49d2:	48 81 c4 58 08 00 00 	add    rsp,0x858
    49d9:	c3                   	ret
    49da:	f3 0f 1e fa          	endbr64
    49de:	31 c0                	xor    eax,eax
    49e0:	eb d9                	jmp    49bb <socket@plt+0x23eb>
    49e2:	f3 0f 1e fa          	endbr64
    49e6:	4c 8d 50 02          	lea    r10,[rax+0x2]
    49ea:	4c 39 d6             	cmp    rsi,r10
    49ed:	72 c3                	jb     49b2 <socket@plt+0x23e2>
    49ef:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    49f3:	0f b6 4c 07 01       	movzx  ecx,BYTE PTR [rdi+rax*1+0x1]
    49f8:	83 e2 0f             	and    edx,0xf
    49fb:	d3 24 94             	shl    DWORD PTR [rsp+rdx*4],cl
    49fe:	49 39 f2             	cmp    r10,rsi
    4a01:	74 db                	je     49de <socket@plt+0x240e>
    4a03:	42 0f b6 14 17       	movzx  edx,BYTE PTR [rdi+r10*1]
    4a08:	48 83 c0 03          	add    rax,0x3
    4a0c:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4a10:	f3 0f 1e fa          	endbr64
    4a14:	4c 8d 50 02          	lea    r10,[rax+0x2]
    4a18:	4c 39 d6             	cmp    rsi,r10
    4a1b:	72 95                	jb     49b2 <socket@plt+0x23e2>
    4a1d:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4a21:	0f b6 4c 07 01       	movzx  ecx,BYTE PTR [rdi+rax*1+0x1]
    4a26:	83 e2 0f             	and    edx,0xf
    4a29:	d3 2c 94             	shr    DWORD PTR [rsp+rdx*4],cl
    4a2c:	49 39 f2             	cmp    r10,rsi
    4a2f:	74 ad                	je     49de <socket@plt+0x240e>
    4a31:	42 0f b6 14 17       	movzx  edx,BYTE PTR [rdi+r10*1]
    4a36:	48 83 c0 03          	add    rax,0x3
    4a3a:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4a3e:	f3 0f 1e fa          	endbr64
    4a42:	48 8d 50 02          	lea    rdx,[rax+0x2]
    4a46:	48 39 d6             	cmp    rsi,rdx
    4a49:	0f 82 63 ff ff ff    	jb     49b2 <socket@plt+0x23e2>
    4a4f:	0f b6 4c 07 01       	movzx  ecx,BYTE PTR [rdi+rax*1+0x1]
    4a54:	44 0f b6 14 07       	movzx  r10d,BYTE PTR [rdi+rax*1]
    4a59:	83 e1 1f             	and    ecx,0x1f
    4a5c:	0f 85 12 03 00 00    	jne    4d74 <socket@plt+0x27a4>
    4a62:	48 39 f2             	cmp    rdx,rsi
    4a65:	0f 84 73 ff ff ff    	je     49de <socket@plt+0x240e>
    4a6b:	0f b6 14 17          	movzx  edx,BYTE PTR [rdi+rdx*1]
    4a6f:	48 83 c0 03          	add    rax,0x3
    4a73:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4a77:	f3 0f 1e fa          	endbr64
    4a7b:	48 8d 48 01          	lea    rcx,[rax+0x1]
    4a7f:	48 39 ce             	cmp    rsi,rcx
    4a82:	0f 82 2a ff ff ff    	jb     49b2 <socket@plt+0x23e2>
    4a88:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4a8c:	83 e2 0f             	and    edx,0xf
    4a8f:	f7 14 94             	not    DWORD PTR [rsp+rdx*4]
    4a92:	48 39 f1             	cmp    rcx,rsi
    4a95:	0f 84 43 ff ff ff    	je     49de <socket@plt+0x240e>
    4a9b:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4a9f:	48 83 c0 02          	add    rax,0x2
    4aa3:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4aa7:	f3 0f 1e fa          	endbr64
    4aab:	48 8d 50 02          	lea    rdx,[rax+0x2]
    4aaf:	48 39 d6             	cmp    rsi,rdx
    4ab2:	0f 82 fa fe ff ff    	jb     49b2 <socket@plt+0x23e2>
    4ab8:	0f b6 4c 07 01       	movzx  ecx,BYTE PTR [rdi+rax*1+0x1]
    4abd:	83 e1 0f             	and    ecx,0xf
    4ac0:	44 8b 14 8c          	mov    r10d,DWORD PTR [rsp+rcx*4]
    4ac4:	0f b6 0c 07          	movzx  ecx,BYTE PTR [rdi+rax*1]
    4ac8:	83 e1 0f             	and    ecx,0xf
    4acb:	44 89 14 8c          	mov    DWORD PTR [rsp+rcx*4],r10d
    4acf:	48 39 f2             	cmp    rdx,rsi
    4ad2:	0f 84 06 ff ff ff    	je     49de <socket@plt+0x240e>
    4ad8:	0f b6 14 17          	movzx  edx,BYTE PTR [rdi+rdx*1]
    4adc:	48 83 c0 03          	add    rax,0x3
    4ae0:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4ae4:	f3 0f 1e fa          	endbr64
    4ae8:	48 8d 48 02          	lea    rcx,[rax+0x2]
    4aec:	48 39 ce             	cmp    rsi,rcx
    4aef:	0f 82 bd fe ff ff    	jb     49b2 <socket@plt+0x23e2>
    4af5:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4af9:	44 0f b6 54 07 01    	movzx  r10d,BYTE PTR [rdi+rax*1+0x1]
    4aff:	83 e2 0f             	and    edx,0xf
    4b02:	41 83 e2 0f          	and    r10d,0xf
    4b06:	46 8b 14 94          	mov    r10d,DWORD PTR [rsp+r10*4]
    4b0a:	44 09 14 94          	or     DWORD PTR [rsp+rdx*4],r10d
    4b0e:	48 39 f1             	cmp    rcx,rsi
    4b11:	0f 84 c7 fe ff ff    	je     49de <socket@plt+0x240e>
    4b17:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4b1b:	48 83 c0 03          	add    rax,0x3
    4b1f:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4b23:	f3 0f 1e fa          	endbr64
    4b27:	48 8d 48 02          	lea    rcx,[rax+0x2]
    4b2b:	48 39 ce             	cmp    rsi,rcx
    4b2e:	0f 82 7e fe ff ff    	jb     49b2 <socket@plt+0x23e2>
    4b34:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4b38:	44 0f b6 54 07 01    	movzx  r10d,BYTE PTR [rdi+rax*1+0x1]
    4b3e:	83 e2 0f             	and    edx,0xf
    4b41:	41 83 e2 0f          	and    r10d,0xf
    4b45:	46 8b 14 94          	mov    r10d,DWORD PTR [rsp+r10*4]
    4b49:	44 21 14 94          	and    DWORD PTR [rsp+rdx*4],r10d
    4b4d:	48 39 f1             	cmp    rcx,rsi
    4b50:	0f 84 88 fe ff ff    	je     49de <socket@plt+0x240e>
    4b56:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4b5a:	48 83 c0 03          	add    rax,0x3
    4b5e:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4b62:	f3 0f 1e fa          	endbr64
    4b66:	48 8d 48 02          	lea    rcx,[rax+0x2]
    4b6a:	48 39 ce             	cmp    rsi,rcx
    4b6d:	0f 82 3f fe ff ff    	jb     49b2 <socket@plt+0x23e2>
    4b73:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4b77:	44 0f b6 54 07 01    	movzx  r10d,BYTE PTR [rdi+rax*1+0x1]
    4b7d:	83 e2 0f             	and    edx,0xf
    4b80:	41 83 e2 0f          	and    r10d,0xf
    4b84:	46 8b 14 94          	mov    r10d,DWORD PTR [rsp+r10*4]
    4b88:	44 31 14 94          	xor    DWORD PTR [rsp+rdx*4],r10d
    4b8c:	48 39 f1             	cmp    rcx,rsi
    4b8f:	0f 84 49 fe ff ff    	je     49de <socket@plt+0x240e>
    4b95:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4b99:	48 83 c0 03          	add    rax,0x3
    4b9d:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4ba1:	f3 0f 1e fa          	endbr64
    4ba5:	48 8d 48 02          	lea    rcx,[rax+0x2]
    4ba9:	48 39 ce             	cmp    rsi,rcx
    4bac:	0f 82 00 fe ff ff    	jb     49b2 <socket@plt+0x23e2>
    4bb2:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4bb6:	44 0f b6 54 07 01    	movzx  r10d,BYTE PTR [rdi+rax*1+0x1]
    4bbc:	83 e2 0f             	and    edx,0xf
    4bbf:	41 83 e2 0f          	and    r10d,0xf
    4bc3:	46 8b 14 94          	mov    r10d,DWORD PTR [rsp+r10*4]
    4bc7:	44 01 14 94          	add    DWORD PTR [rsp+rdx*4],r10d
    4bcb:	48 39 f1             	cmp    rcx,rsi
    4bce:	0f 84 0a fe ff ff    	je     49de <socket@plt+0x240e>
    4bd4:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4bd8:	48 83 c0 03          	add    rax,0x3
    4bdc:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4be0:	f3 0f 1e fa          	endbr64
    4be4:	48 8d 48 03          	lea    rcx,[rax+0x3]
    4be8:	48 39 ce             	cmp    rsi,rcx
    4beb:	0f 82 c1 fd ff ff    	jb     49b2 <socket@plt+0x23e2>
    4bf1:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4bf5:	44 0f b7 54 07 01    	movzx  r10d,WORD PTR [rdi+rax*1+0x1]
    4bfb:	83 e2 0f             	and    edx,0xf
    4bfe:	4d 39 ca             	cmp    r10,r9
    4c01:	0f 83 ab fd ff ff    	jae    49b2 <socket@plt+0x23e2>
    4c07:	83 e2 0f             	and    edx,0xf
    4c0a:	8b 14 94             	mov    edx,DWORD PTR [rsp+rdx*4]
    4c0d:	43 88 14 10          	mov    BYTE PTR [r8+r10*1],dl
    4c11:	48 39 f1             	cmp    rcx,rsi
    4c14:	0f 84 c4 fd ff ff    	je     49de <socket@plt+0x240e>
    4c1a:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4c1e:	48 83 c0 04          	add    rax,0x4
    4c22:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4c26:	f3 0f 1e fa          	endbr64
    4c2a:	48 8d 48 03          	lea    rcx,[rax+0x3]
    4c2e:	48 39 ce             	cmp    rsi,rcx
    4c31:	0f 82 7b fd ff ff    	jb     49b2 <socket@plt+0x23e2>
    4c37:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4c3b:	44 0f b7 54 07 01    	movzx  r10d,WORD PTR [rdi+rax*1+0x1]
    4c41:	83 e2 0f             	and    edx,0xf
    4c44:	4d 39 ca             	cmp    r10,r9
    4c47:	0f 83 65 fd ff ff    	jae    49b2 <socket@plt+0x23e2>
    4c4d:	47 0f b6 14 10       	movzx  r10d,BYTE PTR [r8+r10*1]
    4c52:	83 e2 0f             	and    edx,0xf
    4c55:	44 89 14 94          	mov    DWORD PTR [rsp+rdx*4],r10d
    4c59:	48 39 f1             	cmp    rcx,rsi
    4c5c:	0f 84 7c fd ff ff    	je     49de <socket@plt+0x240e>
    4c62:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4c66:	48 83 c0 04          	add    rax,0x4
    4c6a:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4c6e:	f3 0f 1e fa          	endbr64
    4c72:	48 8d 48 03          	lea    rcx,[rax+0x3]
    4c76:	48 39 ce             	cmp    rsi,rcx
    4c79:	0f 82 33 fd ff ff    	jb     49b2 <socket@plt+0x23e2>
    4c7f:	44 0f b7 54 07 01    	movzx  r10d,WORD PTR [rdi+rax*1+0x1]
    4c85:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4c89:	4d 8d 5a 04          	lea    r11,[r10+0x4]
    4c8d:	83 e2 0f             	and    edx,0xf
    4c90:	4d 39 d9             	cmp    r9,r11
    4c93:	0f 82 19 fd ff ff    	jb     49b2 <socket@plt+0x23e2>
    4c99:	83 e2 0f             	and    edx,0xf
    4c9c:	8b 14 94             	mov    edx,DWORD PTR [rsp+rdx*4]
    4c9f:	0f ca                	bswap  edx
    4ca1:	43 89 14 10          	mov    DWORD PTR [r8+r10*1],edx
    4ca5:	48 39 f1             	cmp    rcx,rsi
    4ca8:	0f 84 30 fd ff ff    	je     49de <socket@plt+0x240e>
    4cae:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4cb2:	48 83 c0 04          	add    rax,0x4
    4cb6:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4cba:	f3 0f 1e fa          	endbr64
    4cbe:	48 8d 48 03          	lea    rcx,[rax+0x3]
    4cc2:	48 39 ce             	cmp    rsi,rcx
    4cc5:	0f 82 e7 fc ff ff    	jb     49b2 <socket@plt+0x23e2>
    4ccb:	44 0f b7 54 07 01    	movzx  r10d,WORD PTR [rdi+rax*1+0x1]
    4cd1:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4cd5:	4d 8d 5a 04          	lea    r11,[r10+0x4]
    4cd9:	83 e2 0f             	and    edx,0xf
    4cdc:	4d 39 d9             	cmp    r9,r11
    4cdf:	0f 82 cd fc ff ff    	jb     49b2 <socket@plt+0x23e2>
    4ce5:	47 8b 14 10          	mov    r10d,DWORD PTR [r8+r10*1]
    4ce9:	83 e2 0f             	and    edx,0xf
    4cec:	41 0f ca             	bswap  r10d
    4cef:	44 89 14 94          	mov    DWORD PTR [rsp+rdx*4],r10d
    4cf3:	48 39 f1             	cmp    rcx,rsi
    4cf6:	0f 84 e2 fc ff ff    	je     49de <socket@plt+0x240e>
    4cfc:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4d00:	48 83 c0 04          	add    rax,0x4
    4d04:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4d08:	f3 0f 1e fa          	endbr64
    4d0c:	48 8d 50 05          	lea    rdx,[rax+0x5]
    4d10:	48 39 d6             	cmp    rsi,rdx
    4d13:	0f 82 99 fc ff ff    	jb     49b2 <socket@plt+0x23e2>
    4d19:	0f b6 0c 07          	movzx  ecx,BYTE PTR [rdi+rax*1]
    4d1d:	44 8b 54 07 01       	mov    r10d,DWORD PTR [rdi+rax*1+0x1]
    4d22:	83 e1 0f             	and    ecx,0xf
    4d25:	44 89 14 8c          	mov    DWORD PTR [rsp+rcx*4],r10d
    4d29:	48 39 f2             	cmp    rdx,rsi
    4d2c:	0f 84 ac fc ff ff    	je     49de <socket@plt+0x240e>
    4d32:	0f b6 14 17          	movzx  edx,BYTE PTR [rdi+rdx*1]
    4d36:	48 83 c0 06          	add    rax,0x6
    4d3a:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4d3e:	f3 0f 1e fa          	endbr64
    4d42:	48 8d 48 05          	lea    rcx,[rax+0x5]
    4d46:	48 39 ce             	cmp    rsi,rcx
    4d49:	0f 82 63 fc ff ff    	jb     49b2 <socket@plt+0x23e2>
    4d4f:	0f b6 14 07          	movzx  edx,BYTE PTR [rdi+rax*1]
    4d53:	44 8b 54 07 01       	mov    r10d,DWORD PTR [rdi+rax*1+0x1]
    4d58:	83 e2 0f             	and    edx,0xf
    4d5b:	44 01 14 94          	add    DWORD PTR [rsp+rdx*4],r10d
    4d5f:	48 39 f1             	cmp    rcx,rsi
    4d62:	0f 84 76 fc ff ff    	je     49de <socket@plt+0x240e>
    4d68:	0f b6 14 0f          	movzx  edx,BYTE PTR [rdi+rcx*1]
    4d6c:	48 83 c0 06          	add    rax,0x6
    4d70:	ff 64 d4 40          	jmp    QWORD PTR [rsp+rdx*8+0x40]
    4d74:	41 83 e2 0f          	and    r10d,0xf
    4d78:	42 d3 0c 94          	ror    DWORD PTR [rsp+r10*4],cl
    4d7c:	e9 e1 fc ff ff       	jmp    4a62 <socket@plt+0x2492>
    4d81:	e8 7a d6 ff ff       	call   2400 <__stack_chk_fail@plt>
    4d86:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    4d8d:	00 00 00 
    4d90:	41 57                	push   r15
    4d92:	b9 40 00 00 00       	mov    ecx,0x40
    4d97:	49 89 f0             	mov    r8,rsi
    4d9a:	41 56                	push   r14
    4d9c:	41 55                	push   r13
    4d9e:	41 54                	push   r12
    4da0:	55                   	push   rbp
    4da1:	48 89 fd             	mov    rbp,rdi
    4da4:	53                   	push   rbx
    4da5:	48 81 ec 58 02 00 00 	sub    rsp,0x258
    4dac:	f3 0f 7e 45 00       	movq   xmm0,QWORD PTR [rbp+0x0]
    4db1:	f3 0f 7e 75 08       	movq   xmm6,QWORD PTR [rbp+0x8]
    4db6:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    4dbd:	00 00 
    4dbf:	48 89 84 24 48 02 00 	mov    QWORD PTR [rsp+0x248],rax
    4dc6:	00 
    4dc7:	31 c0                	xor    eax,eax
    4dc9:	f3 0f 7e 55 10       	movq   xmm2,QWORD PTR [rbp+0x10]
    4dce:	f3 0f 7e 6d 18       	movq   xmm5,QWORD PTR [rbp+0x18]
    4dd3:	4c 8d 64 24 40       	lea    r12,[rsp+0x40]
    4dd8:	66 0f 6f e0          	movdqa xmm4,xmm0
    4ddc:	66 0f 6f ce          	movdqa xmm1,xmm6
    4de0:	4c 89 e7             	mov    rdi,r12
    4de3:	66 0f 72 d4 18       	psrld  xmm4,0x18
    4de8:	66 0f 72 d1 18       	psrld  xmm1,0x18
    4ded:	66 0f 6f dc          	movdqa xmm3,xmm4
    4df1:	66 0f 61 e1          	punpcklwd xmm4,xmm1
    4df5:	66 0f 61 d9          	punpcklwd xmm3,xmm1
    4df9:	66 0f 6f cd          	movdqa xmm1,xmm5
    4dfd:	66 0f 70 db 4e       	pshufd xmm3,xmm3,0x4e
    4e02:	66 0f 72 d1 18       	psrld  xmm1,0x18
    4e07:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    4e0a:	66 0f 61 e3          	punpcklwd xmm4,xmm3
    4e0e:	66 0f 6f da          	movdqa xmm3,xmm2
    4e12:	66 0f 72 d3 18       	psrld  xmm3,0x18
    4e17:	66 0f 6f fb          	movdqa xmm7,xmm3
    4e1b:	66 0f 61 d9          	punpcklwd xmm3,xmm1
    4e1f:	66 0f 61 f9          	punpcklwd xmm7,xmm1
    4e23:	f3 0f 7e 0d 15 54 00 	movq   xmm1,QWORD PTR [rip+0x5415]        # a240 <socket@plt+0x7c70>
    4e2a:	00 
    4e2b:	66 0f 70 ff 4e       	pshufd xmm7,xmm7,0x4e
    4e30:	66 0f db e1          	pand   xmm4,xmm1
    4e34:	66 0f 61 df          	punpcklwd xmm3,xmm7
    4e38:	66 0f db d9          	pand   xmm3,xmm1
    4e3c:	66 0f 6f fc          	movdqa xmm7,xmm4
    4e40:	66 0f 6f e0          	movdqa xmm4,xmm0
    4e44:	66 0f 67 fb          	packuswb xmm7,xmm3
    4e48:	66 0f 72 d4 10       	psrld  xmm4,0x10
    4e4d:	66 0f 6f de          	movdqa xmm3,xmm6
    4e51:	66 0f 70 ff 08       	pshufd xmm7,xmm7,0x8
    4e56:	66 0f 72 d3 10       	psrld  xmm3,0x10
    4e5b:	66 48 0f 7e f9       	movq   rcx,xmm7
    4e60:	66 0f 6f fc          	movdqa xmm7,xmm4
    4e64:	66 0f 61 e3          	punpcklwd xmm4,xmm3
    4e68:	66 0f 61 fb          	punpcklwd xmm7,xmm3
    4e6c:	66 0f 6f da          	movdqa xmm3,xmm2
    4e70:	48 89 cf             	mov    rdi,rcx
    4e73:	49 89 c9             	mov    r9,rcx
    4e76:	66 0f 70 ff 4e       	pshufd xmm7,xmm7,0x4e
    4e7b:	66 0f 72 d3 10       	psrld  xmm3,0x10
    4e80:	48 c1 ef 10          	shr    rdi,0x10
    4e84:	48 89 0c 24          	mov    QWORD PTR [rsp],rcx
    4e88:	66 0f 61 e7          	punpcklwd xmm4,xmm7
    4e8c:	66 0f 6f fd          	movdqa xmm7,xmm5
    4e90:	66 44 0f 6f c3       	movdqa xmm8,xmm3
    4e95:	49 c1 e9 18          	shr    r9,0x18
    4e99:	66 0f 72 d7 10       	psrld  xmm7,0x10
    4e9e:	66 0f db e1          	pand   xmm4,xmm1
    4ea2:	48 89 7c 24 18       	mov    QWORD PTR [rsp+0x18],rdi
    4ea7:	66 44 0f 61 c7       	punpcklwd xmm8,xmm7
    4eac:	66 0f 61 df          	punpcklwd xmm3,xmm7
    4eb0:	66 0f 6f fc          	movdqa xmm7,xmm4
    4eb4:	4c 89 4c 24 38       	mov    QWORD PTR [rsp+0x38],r9
    4eb9:	66 45 0f 70 c0 4e    	pshufd xmm8,xmm8,0x4e
    4ebf:	66 41 0f 61 d8       	punpcklwd xmm3,xmm8
    4ec4:	66 0f db d9          	pand   xmm3,xmm1
    4ec8:	66 0f 67 fb          	packuswb xmm7,xmm3
    4ecc:	66 0f 6f d8          	movdqa xmm3,xmm0
    4ed0:	66 0f 61 c6          	punpcklwd xmm0,xmm6
    4ed4:	66 0f 61 de          	punpcklwd xmm3,xmm6
    4ed8:	66 0f 70 ff 08       	pshufd xmm7,xmm7,0x8
    4edd:	66 0f 70 db 4e       	pshufd xmm3,xmm3,0x4e
    4ee2:	66 48 0f 7e fb       	movq   rbx,xmm7
    4ee7:	66 0f 61 c3          	punpcklwd xmm0,xmm3
    4eeb:	66 0f 6f da          	movdqa xmm3,xmm2
    4eef:	66 0f 61 d5          	punpcklwd xmm2,xmm5
    4ef3:	48 89 da             	mov    rdx,rbx
    4ef6:	66 0f 61 dd          	punpcklwd xmm3,xmm5
    4efa:	66 0f 6f e0          	movdqa xmm4,xmm0
    4efe:	66 0f db c1          	pand   xmm0,xmm1
    4f02:	48 c1 ea 10          	shr    rdx,0x10
    4f06:	66 0f 70 db 4e       	pshufd xmm3,xmm3,0x4e
    4f0b:	66 0f 71 d4 08       	psrlw  xmm4,0x8
    4f10:	0f b6 ff             	movzx  edi,bh
    4f13:	49 89 d9             	mov    r9,rbx
    4f16:	66 0f 61 d3          	punpcklwd xmm2,xmm3
    4f1a:	66 0f db e1          	pand   xmm4,xmm1
    4f1e:	66 0f 6f f0          	movdqa xmm6,xmm0
    4f22:	44 0f b6 db          	movzx  r11d,bl
    4f26:	66 0f 6f da          	movdqa xmm3,xmm2
    4f2a:	66 0f 6f ec          	movdqa xmm5,xmm4
    4f2e:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
    4f33:	49 c1 e9 18          	shr    r9,0x18
    4f37:	66 0f 71 d3 08       	psrlw  xmm3,0x8
    4f3c:	45 0f b6 c9          	movzx  r9d,r9b
    4f40:	66 0f db d9          	pand   xmm3,xmm1
    4f44:	66 0f db ca          	pand   xmm1,xmm2
    4f48:	66 0f 67 eb          	packuswb xmm5,xmm3
    4f4c:	66 0f 67 f1          	packuswb xmm6,xmm1
    4f50:	66 0f 70 ed 08       	pshufd xmm5,xmm5,0x8
    4f55:	66 0f 70 f6 08       	pshufd xmm6,xmm6,0x8
    4f5a:	66 48 0f 7e ee       	movq   rsi,xmm5
    4f5f:	66 48 0f 7e f0       	movq   rax,xmm6
    4f64:	49 89 f7             	mov    r15,rsi
    4f67:	48 89 f2             	mov    rdx,rsi
    4f6a:	44 0f b6 f0          	movzx  r14d,al
    4f6e:	44 0f b6 ee          	movzx  r13d,sil
    4f72:	49 c1 ef 10          	shr    r15,0x10
    4f76:	0f b6 d6             	movzx  edx,dh
    4f79:	49 89 c2             	mov    r10,rax
    4f7c:	4c 89 7c 24 28       	mov    QWORD PTR [rsp+0x28],r15
    4f81:	49 89 c7             	mov    r15,rax
    4f84:	49 c1 ea 10          	shr    r10,0x10
    4f88:	41 81 e7 00 ff 00 00 	and    r15d,0xff00
    4f8f:	4c 89 54 24 30       	mov    QWORD PTR [rsp+0x30],r10
    4f94:	49 89 f2             	mov    r10,rsi
    4f97:	4c 09 fa             	or     rdx,r15
    4f9a:	49 c1 ea 18          	shr    r10,0x18
    4f9e:	49 89 f7             	mov    r15,rsi
    4fa1:	48 c1 e2 08          	shl    rdx,0x8
    4fa5:	45 0f b6 d2          	movzx  r10d,r10b
    4fa9:	48 09 fa             	or     rdx,rdi
    4fac:	0f b6 fd             	movzx  edi,ch
    4faf:	48 c1 e2 08          	shl    rdx,0x8
    4fb3:	48 09 fa             	or     rdx,rdi
    4fb6:	0f b6 3c 24          	movzx  edi,BYTE PTR [rsp]
    4fba:	48 c1 e2 08          	shl    rdx,0x8
    4fbe:	4c 09 f2             	or     rdx,r14
    4fc1:	49 89 de             	mov    r14,rbx
    4fc4:	48 c1 e2 08          	shl    rdx,0x8
    4fc8:	4c 09 ea             	or     rdx,r13
    4fcb:	49 89 cd             	mov    r13,rcx
    4fce:	48 c1 e2 08          	shl    rdx,0x8
    4fd2:	4c 09 da             	or     rdx,r11
    4fd5:	49 89 c3             	mov    r11,rax
    4fd8:	49 c1 eb 10          	shr    r11,0x10
    4fdc:	48 c1 e2 08          	shl    rdx,0x8
    4fe0:	41 81 e3 00 ff 00 00 	and    r11d,0xff00
    4fe7:	4d 09 d3             	or     r11,r10
    4fea:	44 0f b6 54 24 38    	movzx  r10d,BYTE PTR [rsp+0x38]
    4ff0:	49 c1 e3 08          	shl    r11,0x8
    4ff4:	4d 09 cb             	or     r11,r9
    4ff7:	49 c1 e3 08          	shl    r11,0x8
    4ffb:	4d 89 d9             	mov    r9,r11
    4ffe:	49 89 c3             	mov    r11,rax
    5001:	4d 09 d1             	or     r9,r10
    5004:	44 0f b6 54 24 30    	movzx  r10d,BYTE PTR [rsp+0x30]
    500a:	49 c1 e1 08          	shl    r9,0x8
    500e:	4d 09 d1             	or     r9,r10
    5011:	44 0f b6 54 24 28    	movzx  r10d,BYTE PTR [rsp+0x28]
    5017:	49 c1 e1 08          	shl    r9,0x8
    501b:	4d 09 d1             	or     r9,r10
    501e:	48 09 fa             	or     rdx,rdi
    5021:	44 0f b6 54 24 20    	movzx  r10d,BYTE PTR [rsp+0x20]
    5027:	49 c1 eb 20          	shr    r11,0x20
    502b:	48 89 14 24          	mov    QWORD PTR [rsp],rdx
    502f:	48 89 da             	mov    rdx,rbx
    5032:	49 c1 e1 08          	shl    r9,0x8
    5036:	48 89 cf             	mov    rdi,rcx
    5039:	48 c1 ea 20          	shr    rdx,0x20
    503d:	4d 09 d1             	or     r9,r10
    5040:	49 c1 ef 28          	shr    r15,0x28
    5044:	f3 41 0f 6f 30       	movdqu xmm6,XMMWORD PTR [r8]
    5049:	44 0f b6 54 24 18    	movzx  r10d,BYTE PTR [rsp+0x18]
    504f:	49 c1 ee 28          	shr    r14,0x28
    5053:	45 0f b6 ff          	movzx  r15d,r15b
    5057:	49 c1 ed 28          	shr    r13,0x28
    505b:	49 c1 e1 08          	shl    r9,0x8
    505f:	45 0f b6 f6          	movzx  r14d,r14b
    5063:	45 0f b6 ed          	movzx  r13d,r13b
    5067:	48 c1 ef 20          	shr    rdi,0x20
    506b:	48 89 54 24 18       	mov    QWORD PTR [rsp+0x18],rdx
    5070:	4c 89 da             	mov    rdx,r11
    5073:	4d 09 d1             	or     r9,r10
    5076:	45 0f b6 db          	movzx  r11d,r11b
    507a:	81 e2 00 ff 00 00    	and    edx,0xff00
    5080:	49 89 f2             	mov    r10,rsi
    5083:	4c 89 4c 24 08       	mov    QWORD PTR [rsp+0x8],r9
    5088:	49 89 c9             	mov    r9,rcx
    508b:	49 c1 ea 20          	shr    r10,0x20
    508f:	4c 09 fa             	or     rdx,r15
    5092:	66 0f 6f 14 24       	movdqa xmm2,XMMWORD PTR [rsp]
    5097:	49 c1 e9 30          	shr    r9,0x30
    509b:	48 c1 e2 08          	shl    rdx,0x8
    509f:	45 0f b6 d2          	movzx  r10d,r10b
    50a3:	48 89 3c 24          	mov    QWORD PTR [rsp],rdi
    50a7:	48 89 df             	mov    rdi,rbx
    50aa:	4c 09 f2             	or     rdx,r14
    50ad:	48 c1 ef 30          	shr    rdi,0x30
    50b1:	4c 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],r9
    50b6:	49 89 c1             	mov    r9,rax
    50b9:	48 c1 e2 08          	shl    rdx,0x8
    50bd:	48 c1 e8 38          	shr    rax,0x38
    50c1:	48 89 7c 24 28       	mov    QWORD PTR [rsp+0x28],rdi
    50c6:	48 89 f7             	mov    rdi,rsi
    50c9:	48 c1 ef 30          	shr    rdi,0x30
    50cd:	4c 09 ea             	or     rdx,r13
    50d0:	49 c1 e9 30          	shr    r9,0x30
    50d4:	0f 29 54 24 40       	movaps XMMWORD PTR [rsp+0x40],xmm2
    50d9:	48 c1 e2 08          	shl    rdx,0x8
    50dd:	48 0f a4 f0 08       	shld   rax,rsi,0x8
    50e2:	45 0f b6 c9          	movzx  r9d,r9b
    50e6:	40 0f b6 ff          	movzx  edi,dil
    50ea:	4c 09 da             	or     rdx,r11
    50ed:	f3 41 0f 6f 40 10    	movdqu xmm0,XMMWORD PTR [r8+0x10]
    50f3:	f3 41 0f 6f 50 20    	movdqu xmm2,XMMWORD PTR [r8+0x20]
    50f9:	0f 29 74 24 60       	movaps XMMWORD PTR [rsp+0x60],xmm6
    50fe:	48 c1 e2 08          	shl    rdx,0x8
    5102:	4c 09 d2             	or     rdx,r10
    5105:	44 0f b6 54 24 18    	movzx  r10d,BYTE PTR [rsp+0x18]
    510b:	0f 29 44 24 70       	movaps XMMWORD PTR [rsp+0x70],xmm0
    5110:	48 c1 e2 08          	shl    rdx,0x8
    5114:	0f 29 94 24 80 00 00 	movaps XMMWORD PTR [rsp+0x80],xmm2
    511b:	00 
    511c:	4c 09 d2             	or     rdx,r10
    511f:	44 0f b6 14 24       	movzx  r10d,BYTE PTR [rsp]
    5124:	48 c1 e2 08          	shl    rdx,0x8
    5128:	48 0f a4 d8 08       	shld   rax,rbx,0x8
    512d:	48 0f a4 c8 08       	shld   rax,rcx,0x8
    5132:	0f b6 4c 24 28       	movzx  ecx,BYTE PTR [rsp+0x28]
    5137:	4c 09 d2             	or     rdx,r10
    513a:	48 c1 e0 08          	shl    rax,0x8
    513e:	48 89 14 24          	mov    QWORD PTR [rsp],rdx
    5142:	4c 09 c8             	or     rax,r9
    5145:	48 c1 e0 08          	shl    rax,0x8
    5149:	48 09 f8             	or     rax,rdi
    514c:	48 8b 3d 25 71 00 00 	mov    rdi,QWORD PTR [rip+0x7125]        # c278 <socket@plt+0x9ca8>
    5153:	48 c1 e0 08          	shl    rax,0x8
    5157:	48 09 c8             	or     rax,rcx
    515a:	0f b6 4c 24 20       	movzx  ecx,BYTE PTR [rsp+0x20]
    515f:	48 c1 e0 08          	shl    rax,0x8
    5163:	48 09 c8             	or     rax,rcx
    5166:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
    516b:	66 0f 6f 2c 24       	movdqa xmm5,XMMWORD PTR [rsp]
    5170:	0f 29 6c 24 50       	movaps XMMWORD PTR [rsp+0x50],xmm5
    5175:	f3 41 0f 6f 68 30    	movdqu xmm5,XMMWORD PTR [r8+0x30]
    517b:	0f 29 ac 24 90 00 00 	movaps XMMWORD PTR [rsp+0x90],xmm5
    5182:	00 
    5183:	48 85 ff             	test   rdi,rdi
    5186:	74 51                	je     51d9 <socket@plt+0x2c09>
    5188:	b9 00 02 00 00       	mov    ecx,0x200
    518d:	4c 89 e2             	mov    rdx,r12
    5190:	be 29 34 00 00       	mov    esi,0x3429
    5195:	e8 86 f6 ff ff       	call   4820 <socket@plt+0x2250>
    519a:	31 c0                	xor    eax,eax
    519c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    51a0:	41 8b 14 04          	mov    edx,DWORD PTR [r12+rax*1]
    51a4:	0f ca                	bswap  edx
    51a6:	89 54 05 00          	mov    DWORD PTR [rbp+rax*1+0x0],edx
    51aa:	48 83 c0 04          	add    rax,0x4
    51ae:	48 83 f8 20          	cmp    rax,0x20
    51b2:	75 ec                	jne    51a0 <socket@plt+0x2bd0>
    51b4:	48 8b 84 24 48 02 00 	mov    rax,QWORD PTR [rsp+0x248]
    51bb:	00 
    51bc:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    51c3:	00 00 
    51c5:	75 62                	jne    5229 <socket@plt+0x2c59>
    51c7:	48 81 c4 58 02 00 00 	add    rsp,0x258
    51ce:	5b                   	pop    rbx
    51cf:	5d                   	pop    rbp
    51d0:	41 5c                	pop    r12
    51d2:	41 5d                	pop    r13
    51d4:	41 5e                	pop    r14
    51d6:	41 5f                	pop    r15
    51d8:	c3                   	ret
    51d9:	bf 29 34 00 00       	mov    edi,0x3429
    51de:	e8 ed d2 ff ff       	call   24d0 <malloc@plt>
    51e3:	ba 01 00 00 00       	mov    edx,0x1
    51e8:	48 8d 35 41 50 00 00 	lea    rsi,[rip+0x5041]        # a230 <socket@plt+0x7c60>
    51ef:	c6 00 02             	mov    BYTE PTR [rax],0x2
    51f2:	48 89 c7             	mov    rdi,rax
    51f5:	48 8d 05 04 1c 00 00 	lea    rax,[rip+0x1c04]        # 6e00 <socket@plt+0x4830>
    51fc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    5200:	48 89 d1             	mov    rcx,rdx
    5203:	83 e1 0f             	and    ecx,0xf
    5206:	0f b6 0c 0e          	movzx  ecx,BYTE PTR [rsi+rcx*1]
    520a:	32 0c 10             	xor    cl,BYTE PTR [rax+rdx*1]
    520d:	88 0c 17             	mov    BYTE PTR [rdi+rdx*1],cl
    5210:	48 83 c2 01          	add    rdx,0x1
    5214:	48 81 fa 29 34 00 00 	cmp    rdx,0x3429
    521b:	75 e3                	jne    5200 <socket@plt+0x2c30>
    521d:	48 89 3d 54 70 00 00 	mov    QWORD PTR [rip+0x7054],rdi        # c278 <socket@plt+0x9ca8>
    5224:	e9 5f ff ff ff       	jmp    5188 <socket@plt+0x2bb8>
    5229:	e8 d2 d1 ff ff       	call   2400 <__stack_chk_fail@plt>
    522e:	66 90                	xchg   ax,ax
    5230:	41 57                	push   r15
    5232:	41 56                	push   r14
    5234:	41 55                	push   r13
    5236:	49 89 fd             	mov    r13,rdi
    5239:	41 54                	push   r12
    523b:	49 89 f4             	mov    r12,rsi
    523e:	55                   	push   rbp
    523f:	53                   	push   rbx
    5240:	48 81 ec a8 00 00 00 	sub    rsp,0xa8
    5247:	48 89 54 24 18       	mov    QWORD PTR [rsp+0x18],rdx
    524c:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    5253:	00 00 
    5255:	48 89 84 24 98 00 00 	mov    QWORD PTR [rsp+0x98],rax
    525c:	00 
    525d:	48 8b 05 fc 6f 00 00 	mov    rax,QWORD PTR [rip+0x6ffc]        # c260 <socket@plt+0x9c90>
    5264:	48 85 c0             	test   rax,rax
    5267:	0f 84 13 05 00 00    	je     5780 <socket@plt+0x31b0>
    526d:	f3 0f 6f 10          	movdqu xmm2,XMMWORD PTR [rax]
    5271:	f3 0f 6f 68 10       	movdqu xmm5,XMMWORD PTR [rax+0x10]
    5276:	4d 89 e6             	mov    r14,r12
    5279:	49 c1 ee 06          	shr    r14,0x6
    527d:	0f 29 54 24 30       	movaps XMMWORD PTR [rsp+0x30],xmm2
    5282:	0f 29 6c 24 40       	movaps XMMWORD PTR [rsp+0x40],xmm5
    5287:	0f 84 43 05 00 00    	je     57d0 <socket@plt+0x3200>
    528d:	49 c1 e6 06          	shl    r14,0x6
    5291:	4c 89 eb             	mov    rbx,r13
    5294:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
    5299:	4d 01 ee             	add    r14,r13
    529c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    52a0:	48 89 de             	mov    rsi,rbx
    52a3:	48 89 ef             	mov    rdi,rbp
    52a6:	48 83 c3 40          	add    rbx,0x40
    52aa:	e8 e1 fa ff ff       	call   4d90 <socket@plt+0x27c0>
    52af:	49 39 de             	cmp    r14,rbx
    52b2:	75 ec                	jne    52a0 <socket@plt+0x2cd0>
    52b4:	4c 89 e1             	mov    rcx,r12
    52b7:	66 0f ef c0          	pxor   xmm0,xmm0
    52bb:	48 8d 5c 24 50       	lea    rbx,[rsp+0x50]
    52c0:	4c 89 e2             	mov    rdx,r12
    52c3:	48 83 e1 c0          	and    rcx,0xffffffffffffffc0
    52c7:	83 e2 3f             	and    edx,0x3f
    52ca:	0f 29 44 24 50       	movaps XMMWORD PTR [rsp+0x50],xmm0
    52cf:	48 89 de             	mov    rsi,rbx
    52d2:	4c 01 e9             	add    rcx,r13
    52d5:	0f 29 44 24 60       	movaps XMMWORD PTR [rsp+0x60],xmm0
    52da:	0f 29 44 24 70       	movaps XMMWORD PTR [rsp+0x70],xmm0
    52df:	48 89 c8             	mov    rax,rcx
    52e2:	0f 29 84 24 80 00 00 	movaps XMMWORD PTR [rsp+0x80],xmm0
    52e9:	00 
    52ea:	83 fa 08             	cmp    edx,0x8
    52ed:	0f 83 65 04 00 00    	jae    5758 <socket@plt+0x3188>
    52f3:	31 c9                	xor    ecx,ecx
    52f5:	f6 c2 04             	test   dl,0x4
    52f8:	0f 85 42 04 00 00    	jne    5740 <socket@plt+0x3170>
    52fe:	f6 c2 02             	test   dl,0x2
    5301:	0f 85 19 04 00 00    	jne    5720 <socket@plt+0x3150>
    5307:	f6 c2 01             	test   dl,0x1
    530a:	0f 85 00 04 00 00    	jne    5710 <socket@plt+0x3140>
    5310:	c6 44 14 50 80       	mov    BYTE PTR [rsp+rdx*1+0x50],0x80
    5315:	48 83 fa 37          	cmp    rdx,0x37
    5319:	76 26                	jbe    5341 <socket@plt+0x2d71>
    531b:	48 89 de             	mov    rsi,rbx
    531e:	48 89 ef             	mov    rdi,rbp
    5321:	e8 6a fa ff ff       	call   4d90 <socket@plt+0x27c0>
    5326:	66 0f ef c0          	pxor   xmm0,xmm0
    532a:	0f 29 44 24 50       	movaps XMMWORD PTR [rsp+0x50],xmm0
    532f:	0f 29 44 24 60       	movaps XMMWORD PTR [rsp+0x60],xmm0
    5334:	0f 29 44 24 70       	movaps XMMWORD PTR [rsp+0x70],xmm0
    5339:	0f 29 84 24 80 00 00 	movaps XMMWORD PTR [rsp+0x80],xmm0
    5340:	00 
    5341:	49 c1 e4 03          	shl    r12,0x3
    5345:	48 8d 84 24 88 00 00 	lea    rax,[rsp+0x88]
    534c:	00 
    534d:	b9 38 00 00 00       	mov    ecx,0x38
    5352:	48 8d bc 24 90 00 00 	lea    rdi,[rsp+0x90]
    5359:	00 
    535a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    5360:	4c 89 e2             	mov    rdx,r12
    5363:	48 83 c0 01          	add    rax,0x1
    5367:	48 d3 ea             	shr    rdx,cl
    536a:	83 e9 08             	sub    ecx,0x8
    536d:	88 50 ff             	mov    BYTE PTR [rax-0x1],dl
    5370:	48 39 c7             	cmp    rdi,rax
    5373:	75 eb                	jne    5360 <socket@plt+0x2d90>
    5375:	48 89 de             	mov    rsi,rbx
    5378:	48 89 ef             	mov    rdi,rbp
    537b:	e8 10 fa ff ff       	call   4d90 <socket@plt+0x27c0>
    5380:	f3 0f 7e 44 24 30    	movq   xmm0,QWORD PTR [rsp+0x30]
    5386:	f3 0f 7e 74 24 38    	movq   xmm6,QWORD PTR [rsp+0x38]
    538c:	f3 0f 7e 54 24 40    	movq   xmm2,QWORD PTR [rsp+0x40]
    5392:	f3 0f 7e 6c 24 48    	movq   xmm5,QWORD PTR [rsp+0x48]
    5398:	66 0f 6f e0          	movdqa xmm4,xmm0
    539c:	66 0f 6f ce          	movdqa xmm1,xmm6
    53a0:	66 0f 72 d4 18       	psrld  xmm4,0x18
    53a5:	66 0f 72 d1 18       	psrld  xmm1,0x18
    53aa:	66 0f 6f dc          	movdqa xmm3,xmm4
    53ae:	66 0f 61 e1          	punpcklwd xmm4,xmm1
    53b2:	66 0f 61 d9          	punpcklwd xmm3,xmm1
    53b6:	66 0f 6f cd          	movdqa xmm1,xmm5
    53ba:	66 0f 70 db 4e       	pshufd xmm3,xmm3,0x4e
    53bf:	66 0f 72 d1 18       	psrld  xmm1,0x18
    53c4:	66 0f 61 e3          	punpcklwd xmm4,xmm3
    53c8:	66 0f 6f da          	movdqa xmm3,xmm2
    53cc:	66 0f 72 d3 18       	psrld  xmm3,0x18
    53d1:	66 0f 6f fb          	movdqa xmm7,xmm3
    53d5:	66 0f 61 d9          	punpcklwd xmm3,xmm1
    53d9:	66 0f 61 f9          	punpcklwd xmm7,xmm1
    53dd:	f3 0f 7e 0d 5b 4e 00 	movq   xmm1,QWORD PTR [rip+0x4e5b]        # a240 <socket@plt+0x7c70>
    53e4:	00 
    53e5:	66 0f 70 ff 4e       	pshufd xmm7,xmm7,0x4e
    53ea:	66 0f db e1          	pand   xmm4,xmm1
    53ee:	66 0f 61 df          	punpcklwd xmm3,xmm7
    53f2:	66 0f db d9          	pand   xmm3,xmm1
    53f6:	66 0f 6f fc          	movdqa xmm7,xmm4
    53fa:	66 0f 6f e0          	movdqa xmm4,xmm0
    53fe:	66 0f 67 fb          	packuswb xmm7,xmm3
    5402:	66 0f 72 d4 10       	psrld  xmm4,0x10
    5407:	66 0f 6f de          	movdqa xmm3,xmm6
    540b:	66 0f 70 ff 08       	pshufd xmm7,xmm7,0x8
    5410:	66 0f 72 d3 10       	psrld  xmm3,0x10
    5415:	66 48 0f 7e f9       	movq   rcx,xmm7
    541a:	66 0f 6f fc          	movdqa xmm7,xmm4
    541e:	66 0f 61 e3          	punpcklwd xmm4,xmm3
    5422:	66 0f 61 fb          	punpcklwd xmm7,xmm3
    5426:	66 0f 6f da          	movdqa xmm3,xmm2
    542a:	48 89 cf             	mov    rdi,rcx
    542d:	49 89 c9             	mov    r9,rcx
    5430:	66 0f 70 ff 4e       	pshufd xmm7,xmm7,0x4e
    5435:	66 0f 72 d3 10       	psrld  xmm3,0x10
    543a:	48 c1 ef 10          	shr    rdi,0x10
    543e:	48 89 0c 24          	mov    QWORD PTR [rsp],rcx
    5442:	66 0f 61 e7          	punpcklwd xmm4,xmm7
    5446:	66 0f 6f fd          	movdqa xmm7,xmm5
    544a:	66 44 0f 6f c3       	movdqa xmm8,xmm3
    544f:	49 c1 e9 18          	shr    r9,0x18
    5453:	66 0f 72 d7 10       	psrld  xmm7,0x10
    5458:	66 0f db e1          	pand   xmm4,xmm1
    545c:	48 89 7c 24 20       	mov    QWORD PTR [rsp+0x20],rdi
    5461:	66 44 0f 61 c7       	punpcklwd xmm8,xmm7
    5466:	66 0f 61 df          	punpcklwd xmm3,xmm7
    546a:	66 0f 6f fc          	movdqa xmm7,xmm4
    546e:	66 45 0f 70 c0 4e    	pshufd xmm8,xmm8,0x4e
    5474:	66 41 0f 61 d8       	punpcklwd xmm3,xmm8
    5479:	66 0f db d9          	pand   xmm3,xmm1
    547d:	66 0f 67 fb          	packuswb xmm7,xmm3
    5481:	66 0f 6f d8          	movdqa xmm3,xmm0
    5485:	66 0f 61 c6          	punpcklwd xmm0,xmm6
    5489:	66 0f 61 de          	punpcklwd xmm3,xmm6
    548d:	66 0f 70 ff 08       	pshufd xmm7,xmm7,0x8
    5492:	66 0f 70 db 4e       	pshufd xmm3,xmm3,0x4e
    5497:	66 48 0f 7e fb       	movq   rbx,xmm7
    549c:	66 0f 61 c3          	punpcklwd xmm0,xmm3
    54a0:	66 0f 6f da          	movdqa xmm3,xmm2
    54a4:	66 0f 61 d5          	punpcklwd xmm2,xmm5
    54a8:	48 89 da             	mov    rdx,rbx
    54ab:	66 0f 61 dd          	punpcklwd xmm3,xmm5
    54af:	66 0f 6f e0          	movdqa xmm4,xmm0
    54b3:	66 0f db c1          	pand   xmm0,xmm1
    54b7:	48 c1 ea 10          	shr    rdx,0x10
    54bb:	66 0f 70 db 4e       	pshufd xmm3,xmm3,0x4e
    54c0:	66 0f 71 d4 08       	psrlw  xmm4,0x8
    54c5:	0f b6 ff             	movzx  edi,bh
    54c8:	49 89 da             	mov    r10,rbx
    54cb:	66 0f 61 d3          	punpcklwd xmm2,xmm3
    54cf:	66 0f db e1          	pand   xmm4,xmm1
    54d3:	66 0f 6f f0          	movdqa xmm6,xmm0
    54d7:	49 c1 ea 18          	shr    r10,0x18
    54db:	66 0f 6f da          	movdqa xmm3,xmm2
    54df:	66 0f 6f ec          	movdqa xmm5,xmm4
    54e3:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
    54e8:	0f b6 eb             	movzx  ebp,bl
    54eb:	66 0f 71 d3 08       	psrlw  xmm3,0x8
    54f0:	66 0f db d9          	pand   xmm3,xmm1
    54f4:	66 0f db ca          	pand   xmm1,xmm2
    54f8:	66 0f 67 eb          	packuswb xmm5,xmm3
    54fc:	66 0f 67 f1          	packuswb xmm6,xmm1
    5500:	66 0f 70 f6 08       	pshufd xmm6,xmm6,0x8
    5505:	66 0f 70 ed 08       	pshufd xmm5,xmm5,0x8
    550a:	66 48 0f 7e ee       	movq   rsi,xmm5
    550f:	66 48 0f 7e f0       	movq   rax,xmm6
    5514:	49 89 c6             	mov    r14,rax
    5517:	48 89 f2             	mov    rdx,rsi
    551a:	44 0f b6 e8          	movzx  r13d,al
    551e:	49 89 c0             	mov    r8,rax
    5521:	41 81 e6 00 ff 00 00 	and    r14d,0xff00
    5528:	0f b6 d6             	movzx  edx,dh
    552b:	49 89 f3             	mov    r11,rsi
    552e:	49 89 f7             	mov    r15,rsi
    5531:	49 c1 e8 10          	shr    r8,0x10
    5535:	4c 09 f2             	or     rdx,r14
    5538:	49 c1 eb 18          	shr    r11,0x18
    553c:	44 0f b6 e6          	movzx  r12d,sil
    5540:	48 c1 e2 08          	shl    rdx,0x8
    5544:	49 c1 ef 10          	shr    r15,0x10
    5548:	49 89 de             	mov    r14,rbx
    554b:	48 09 fa             	or     rdx,rdi
    554e:	0f b6 fd             	movzx  edi,ch
    5551:	45 0f b6 ff          	movzx  r15d,r15b
    5555:	48 c1 e2 08          	shl    rdx,0x8
    5559:	48 09 fa             	or     rdx,rdi
    555c:	0f b6 3c 24          	movzx  edi,BYTE PTR [rsp]
    5560:	48 c1 e2 08          	shl    rdx,0x8
    5564:	4c 09 ea             	or     rdx,r13
    5567:	49 89 cd             	mov    r13,rcx
    556a:	48 c1 e2 08          	shl    rdx,0x8
    556e:	4c 09 e2             	or     rdx,r12
    5571:	45 0f b6 e3          	movzx  r12d,r11b
    5575:	4d 89 c3             	mov    r11,r8
    5578:	41 81 e3 00 ff 00 00 	and    r11d,0xff00
    557f:	48 c1 e2 08          	shl    rdx,0x8
    5583:	4d 09 e3             	or     r11,r12
    5586:	48 09 ea             	or     rdx,rbp
    5589:	41 0f b6 ea          	movzx  ebp,r10b
    558d:	49 89 c4             	mov    r12,rax
    5590:	4d 89 da             	mov    r10,r11
    5593:	45 0f b6 d9          	movzx  r11d,r9b
    5597:	48 c1 e2 08          	shl    rdx,0x8
    559b:	49 c1 e2 08          	shl    r10,0x8
    559f:	49 09 ea             	or     r10,rbp
    55a2:	48 89 f5             	mov    rbp,rsi
    55a5:	4d 89 d1             	mov    r9,r10
    55a8:	45 0f b6 d0          	movzx  r10d,r8b
    55ac:	49 c1 e1 08          	shl    r9,0x8
    55b0:	4d 09 d9             	or     r9,r11
    55b3:	49 89 db             	mov    r11,rbx
    55b6:	49 c1 e1 08          	shl    r9,0x8
    55ba:	4d 89 c8             	mov    r8,r9
    55bd:	44 0f b6 4c 24 28    	movzx  r9d,BYTE PTR [rsp+0x28]
    55c3:	4d 09 d0             	or     r8,r10
    55c6:	49 89 c2             	mov    r10,rax
    55c9:	49 c1 e0 08          	shl    r8,0x8
    55cd:	4d 09 f8             	or     r8,r15
    55d0:	49 89 f7             	mov    r15,rsi
    55d3:	49 c1 e0 08          	shl    r8,0x8
    55d7:	4d 09 c8             	or     r8,r9
    55da:	44 0f b6 4c 24 20    	movzx  r9d,BYTE PTR [rsp+0x20]
    55e0:	48 09 fa             	or     rdx,rdi
    55e3:	49 c1 ec 20          	shr    r12,0x20
    55e7:	49 c1 e0 08          	shl    r8,0x8
    55eb:	48 89 14 24          	mov    QWORD PTR [rsp],rdx
    55ef:	48 8b 7c 24 18       	mov    rdi,QWORD PTR [rsp+0x18]
    55f4:	48 89 ca             	mov    rdx,rcx
    55f7:	48 c1 ea 20          	shr    rdx,0x20
    55fb:	4d 09 c8             	or     r8,r9
    55fe:	49 c1 ef 28          	shr    r15,0x28
    5602:	49 89 f1             	mov    r9,rsi
    5605:	4c 89 44 24 08       	mov    QWORD PTR [rsp+0x8],r8
    560a:	66 0f 6f 34 24       	movdqa xmm6,XMMWORD PTR [rsp]
    560f:	45 0f b6 ff          	movzx  r15d,r15b
    5613:	49 89 d8             	mov    r8,rbx
    5616:	49 c1 ee 28          	shr    r14,0x28
    561a:	49 c1 ed 28          	shr    r13,0x28
    561e:	0f 11 37             	movups XMMWORD PTR [rdi],xmm6
    5621:	48 89 d7             	mov    rdi,rdx
    5624:	48 89 ca             	mov    rdx,rcx
    5627:	45 0f b6 f6          	movzx  r14d,r14b
    562b:	48 c1 ea 30          	shr    rdx,0x30
    562f:	45 0f b6 ed          	movzx  r13d,r13b
    5633:	48 c1 ed 20          	shr    rbp,0x20
    5637:	40 0f b6 ff          	movzx  edi,dil
    563b:	48 89 14 24          	mov    QWORD PTR [rsp],rdx
    563f:	4c 89 e2             	mov    rdx,r12
    5642:	45 0f b6 e4          	movzx  r12d,r12b
    5646:	48 c1 e8 38          	shr    rax,0x38
    564a:	81 e2 00 ff 00 00    	and    edx,0xff00
    5650:	40 0f b6 ed          	movzx  ebp,bpl
    5654:	49 c1 eb 20          	shr    r11,0x20
    5658:	48 0f a4 f0 08       	shld   rax,rsi,0x8
    565d:	4c 09 fa             	or     rdx,r15
    5660:	45 0f b6 db          	movzx  r11d,r11b
    5664:	49 c1 ea 30          	shr    r10,0x30
    5668:	48 c1 e2 08          	shl    rdx,0x8
    566c:	48 0f a4 d8 08       	shld   rax,rbx,0x8
    5671:	45 0f b6 d2          	movzx  r10d,r10b
    5675:	48 0f a4 c8 08       	shld   rax,rcx,0x8
    567a:	4c 09 f2             	or     rdx,r14
    567d:	49 c1 e8 30          	shr    r8,0x30
    5681:	0f b6 0c 24          	movzx  ecx,BYTE PTR [rsp]
    5685:	48 c1 e2 08          	shl    rdx,0x8
    5689:	49 c1 e9 30          	shr    r9,0x30
    568d:	45 0f b6 c0          	movzx  r8d,r8b
    5691:	4c 09 ea             	or     rdx,r13
    5694:	45 0f b6 c9          	movzx  r9d,r9b
    5698:	48 c1 e2 08          	shl    rdx,0x8
    569c:	4c 09 e2             	or     rdx,r12
    569f:	48 c1 e2 08          	shl    rdx,0x8
    56a3:	48 09 ea             	or     rdx,rbp
    56a6:	48 c1 e2 08          	shl    rdx,0x8
    56aa:	4c 09 da             	or     rdx,r11
    56ad:	48 c1 e2 08          	shl    rdx,0x8
    56b1:	48 c1 e0 08          	shl    rax,0x8
    56b5:	4c 09 d0             	or     rax,r10
    56b8:	48 09 fa             	or     rdx,rdi
    56bb:	48 8b 7c 24 18       	mov    rdi,QWORD PTR [rsp+0x18]
    56c0:	48 c1 e0 08          	shl    rax,0x8
    56c4:	48 89 14 24          	mov    QWORD PTR [rsp],rdx
    56c8:	4c 09 c8             	or     rax,r9
    56cb:	48 c1 e0 08          	shl    rax,0x8
    56cf:	4c 09 c0             	or     rax,r8
    56d2:	48 c1 e0 08          	shl    rax,0x8
    56d6:	48 09 c8             	or     rax,rcx
    56d9:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
    56de:	66 0f 6f 14 24       	movdqa xmm2,XMMWORD PTR [rsp]
    56e3:	0f 11 57 10          	movups XMMWORD PTR [rdi+0x10],xmm2
    56e7:	48 8b 84 24 98 00 00 	mov    rax,QWORD PTR [rsp+0x98]
    56ee:	00 
    56ef:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    56f6:	00 00 
    56f8:	0f 85 dc 00 00 00    	jne    57da <socket@plt+0x320a>
    56fe:	48 81 c4 a8 00 00 00 	add    rsp,0xa8
    5705:	5b                   	pop    rbx
    5706:	5d                   	pop    rbp
    5707:	41 5c                	pop    r12
    5709:	41 5d                	pop    r13
    570b:	41 5e                	pop    r14
    570d:	41 5f                	pop    r15
    570f:	c3                   	ret
    5710:	0f b6 04 08          	movzx  eax,BYTE PTR [rax+rcx*1]
    5714:	88 04 0e             	mov    BYTE PTR [rsi+rcx*1],al
    5717:	e9 f4 fb ff ff       	jmp    5310 <socket@plt+0x2d40>
    571c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    5720:	0f b7 3c 08          	movzx  edi,WORD PTR [rax+rcx*1]
    5724:	66 89 3c 0e          	mov    WORD PTR [rsi+rcx*1],di
    5728:	48 83 c1 02          	add    rcx,0x2
    572c:	f6 c2 01             	test   dl,0x1
    572f:	0f 84 db fb ff ff    	je     5310 <socket@plt+0x2d40>
    5735:	eb d9                	jmp    5710 <socket@plt+0x3140>
    5737:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    573e:	00 00 
    5740:	8b 08                	mov    ecx,DWORD PTR [rax]
    5742:	89 0e                	mov    DWORD PTR [rsi],ecx
    5744:	b9 04 00 00 00       	mov    ecx,0x4
    5749:	f6 c2 02             	test   dl,0x2
    574c:	0f 84 b5 fb ff ff    	je     5307 <socket@plt+0x2d37>
    5752:	eb cc                	jmp    5720 <socket@plt+0x3150>
    5754:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    5758:	41 89 d0             	mov    r8d,edx
    575b:	31 c0                	xor    eax,eax
    575d:	41 83 e0 f8          	and    r8d,0xfffffff8
    5761:	89 c6                	mov    esi,eax
    5763:	83 c0 08             	add    eax,0x8
    5766:	48 8b 3c 31          	mov    rdi,QWORD PTR [rcx+rsi*1]
    576a:	48 89 3c 33          	mov    QWORD PTR [rbx+rsi*1],rdi
    576e:	44 39 c0             	cmp    eax,r8d
    5771:	72 ee                	jb     5761 <socket@plt+0x3191>
    5773:	48 8d 34 03          	lea    rsi,[rbx+rax*1]
    5777:	48 01 c8             	add    rax,rcx
    577a:	e9 74 fb ff ff       	jmp    52f3 <socket@plt+0x2d23>
    577f:	90                   	nop
    5780:	bf 20 00 00 00       	mov    edi,0x20
    5785:	e8 46 cd ff ff       	call   24d0 <malloc@plt>
    578a:	ba 01 00 00 00       	mov    edx,0x1
    578f:	48 8d 3d 9a 4a 00 00 	lea    rdi,[rip+0x4a9a]        # a230 <socket@plt+0x7c60>
    5796:	48 8d 35 63 0f 00 00 	lea    rsi,[rip+0xf63]        # 6700 <socket@plt+0x4130>
    579d:	c6 00 67             	mov    BYTE PTR [rax],0x67
    57a0:	48 89 d1             	mov    rcx,rdx
    57a3:	83 e1 0f             	and    ecx,0xf
    57a6:	0f b6 0c 0f          	movzx  ecx,BYTE PTR [rdi+rcx*1]
    57aa:	32 0c 16             	xor    cl,BYTE PTR [rsi+rdx*1]
    57ad:	88 0c 10             	mov    BYTE PTR [rax+rdx*1],cl
    57b0:	48 83 c2 01          	add    rdx,0x1
    57b4:	48 83 fa 20          	cmp    rdx,0x20
    57b8:	75 e6                	jne    57a0 <socket@plt+0x31d0>
    57ba:	48 89 05 9f 6a 00 00 	mov    QWORD PTR [rip+0x6a9f],rax        # c260 <socket@plt+0x9c90>
    57c1:	e9 a7 fa ff ff       	jmp    526d <socket@plt+0x2c9d>
    57c6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    57cd:	00 00 00 
    57d0:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
    57d5:	e9 da fa ff ff       	jmp    52b4 <socket@plt+0x2ce4>
    57da:	e8 21 cc ff ff       	call   2400 <__stack_chk_fail@plt>
    57df:	90                   	nop
    57e0:	f3 0f 1e fa          	endbr64
    57e4:	41 57                	push   r15
    57e6:	41 56                	push   r14
    57e8:	41 55                	push   r13
    57ea:	41 54                	push   r12
    57ec:	55                   	push   rbp
    57ed:	48 89 d5             	mov    rbp,rdx
    57f0:	53                   	push   rbx
    57f1:	48 89 f3             	mov    rbx,rsi
    57f4:	48 81 ec 28 02 00 00 	sub    rsp,0x228
    57fb:	4c 8b 2d 6e 6a 00 00 	mov    r13,QWORD PTR [rip+0x6a6e]        # c270 <socket@plt+0x9ca0>
    5802:	48 89 7c 24 08       	mov    QWORD PTR [rsp+0x8],rdi
    5807:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    580e:	00 00 
    5810:	48 89 84 24 18 02 00 	mov    QWORD PTR [rsp+0x218],rax
    5817:	00 
    5818:	31 c0                	xor    eax,eax
    581a:	4d 85 ed             	test   r13,r13
    581d:	0f 84 8c 02 00 00    	je     5aaf <socket@plt+0x34df>
    5823:	48 8b 35 3e 6a 00 00 	mov    rsi,QWORD PTR [rip+0x6a3e]        # c268 <socket@plt+0x9c98>
    582a:	4c 8d b4 24 50 01 00 	lea    r14,[rsp+0x150]
    5831:	00 
    5832:	31 c0                	xor    eax,eax
    5834:	b9 18 00 00 00       	mov    ecx,0x18
    5839:	4c 89 f7             	mov    rdi,r14
    583c:	4c 89 f2             	mov    rdx,r14
    583f:	4c 8d a4 24 b0 00 00 	lea    r12,[rsp+0xb0]
    5846:	00 
    5847:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
    584a:	4c 89 ef             	mov    rdi,r13
    584d:	b9 c0 00 00 00       	mov    ecx,0xc0
    5852:	8b 05 b8 67 00 00    	mov    eax,DWORD PTR [rip+0x67b8]        # c010 <socket@plt+0x9a40>
    5858:	4c 8d ac 24 f0 00 00 	lea    r13,[rsp+0xf0]
    585f:	00 
    5860:	f3 0f 6f 1e          	movdqu xmm3,XMMWORD PTR [rsi]
    5864:	0f 29 9c 24 50 01 00 	movaps XMMWORD PTR [rsp+0x150],xmm3
    586b:	00 
    586c:	f3 0f 6f 66 10       	movdqu xmm4,XMMWORD PTR [rsi+0x10]
    5871:	0f 29 a4 24 60 01 00 	movaps XMMWORD PTR [rsp+0x160],xmm4
    5878:	00 
    5879:	f3 0f 6f 6e 20       	movdqu xmm5,XMMWORD PTR [rsi+0x20]
    587e:	0f 29 ac 24 70 01 00 	movaps XMMWORD PTR [rsp+0x170],xmm5
    5885:	00 
    5886:	f3 0f 6f 76 30       	movdqu xmm6,XMMWORD PTR [rsi+0x30]
    588b:	0f 29 b4 24 80 01 00 	movaps XMMWORD PTR [rsp+0x180],xmm6
    5892:	00 
    5893:	f3 0f 6f 7e 40       	movdqu xmm7,XMMWORD PTR [rsi+0x40]
    5898:	0f 29 bc 24 90 01 00 	movaps XMMWORD PTR [rsp+0x190],xmm7
    589f:	00 
    58a0:	f3 0f 6f 5e 50       	movdqu xmm3,XMMWORD PTR [rsi+0x50]
    58a5:	be 61 06 00 00       	mov    esi,0x661
    58aa:	30 84 24 50 01 00 00 	xor    BYTE PTR [rsp+0x150],al
    58b1:	0f 29 9c 24 a0 01 00 	movaps XMMWORD PTR [rsp+0x1a0],xmm3
    58b8:	00 
    58b9:	e8 62 ef ff ff       	call   4820 <socket@plt+0x2250>
    58be:	48 8d 54 24 10       	lea    rdx,[rsp+0x10]
    58c3:	be 60 00 00 00       	mov    esi,0x60
    58c8:	4c 89 ef             	mov    rdi,r13
    58cb:	66 0f 6f a4 24 b0 01 	movdqa xmm4,XMMWORD PTR [rsp+0x1b0]
    58d2:	00 00 
    58d4:	66 0f 6f ac 24 c0 01 	movdqa xmm5,XMMWORD PTR [rsp+0x1c0]
    58db:	00 00 
    58dd:	66 0f 6f b4 24 d0 01 	movdqa xmm6,XMMWORD PTR [rsp+0x1d0]
    58e4:	00 00 
    58e6:	66 0f 6f bc 24 e0 01 	movdqa xmm7,XMMWORD PTR [rsp+0x1e0]
    58ed:	00 00 
    58ef:	66 0f 6f 9c 24 f0 01 	movdqa xmm3,XMMWORD PTR [rsp+0x1f0]
    58f6:	00 00 
    58f8:	0f 29 a4 24 f0 00 00 	movaps XMMWORD PTR [rsp+0xf0],xmm4
    58ff:	00 
    5900:	66 0f 6f a4 24 00 02 	movdqa xmm4,XMMWORD PTR [rsp+0x200]
    5907:	00 00 
    5909:	0f 29 ac 24 00 01 00 	movaps XMMWORD PTR [rsp+0x100],xmm5
    5910:	00 
    5911:	0f 29 b4 24 10 01 00 	movaps XMMWORD PTR [rsp+0x110],xmm6
    5918:	00 
    5919:	0f 29 bc 24 20 01 00 	movaps XMMWORD PTR [rsp+0x120],xmm7
    5920:	00 
    5921:	0f 29 9c 24 30 01 00 	movaps XMMWORD PTR [rsp+0x130],xmm3
    5928:	00 
    5929:	0f 29 a4 24 40 01 00 	movaps XMMWORD PTR [rsp+0x140],xmm4
    5930:	00 
    5931:	e8 fa f8 ff ff       	call   5230 <socket@plt+0x2c60>
    5936:	66 0f ef c0          	pxor   xmm0,xmm0
    593a:	31 c0                	xor    eax,eax
    593c:	48 8d 54 24 70       	lea    rdx,[rsp+0x70]
    5941:	66 0f 6f 6c 24 10    	movdqa xmm5,XMMWORD PTR [rsp+0x10]
    5947:	66 0f 6f 74 24 20    	movdqa xmm6,XMMWORD PTR [rsp+0x20]
    594d:	0f 29 84 24 90 00 00 	movaps XMMWORD PTR [rsp+0x90],xmm0
    5954:	00 
    5955:	66 0f 6f 15 f3 0c 00 	movdqa xmm2,XMMWORD PTR [rip+0xcf3]        # 6650 <socket@plt+0x4080>
    595c:	00 
    595d:	66 0f 6f 0d fb 0c 00 	movdqa xmm1,XMMWORD PTR [rip+0xcfb]        # 6660 <socket@plt+0x4090>
    5964:	00 
    5965:	0f 29 84 24 a0 00 00 	movaps XMMWORD PTR [rsp+0xa0],xmm0
    596c:	00 
    596d:	0f 29 6c 24 70       	movaps XMMWORD PTR [rsp+0x70],xmm5
    5972:	0f 29 b4 24 80 00 00 	movaps XMMWORD PTR [rsp+0x80],xmm6
    5979:	00 
    597a:	66 0f 6f 04 02       	movdqa xmm0,XMMWORD PTR [rdx+rax*1]
    597f:	66 0f ef c2          	pxor   xmm0,xmm2
    5983:	41 0f 29 04 04       	movaps XMMWORD PTR [r12+rax*1],xmm0
    5988:	66 0f 6f 04 02       	movdqa xmm0,XMMWORD PTR [rdx+rax*1]
    598d:	66 0f ef c1          	pxor   xmm0,xmm1
    5991:	41 0f 29 44 05 00    	movaps XMMWORD PTR [r13+rax*1+0x0],xmm0
    5997:	48 83 c0 10          	add    rax,0x10
    599b:	48 83 f8 40          	cmp    rax,0x40
    599f:	75 d9                	jne    597a <socket@plt+0x33aa>
    59a1:	4c 8d 7b 40          	lea    r15,[rbx+0x40]
    59a5:	4c 89 ff             	mov    rdi,r15
    59a8:	e8 23 cb ff ff       	call   24d0 <malloc@plt>
    59ad:	4c 89 f9             	mov    rcx,r15
    59b0:	ba 40 00 00 00       	mov    edx,0x40
    59b5:	4c 89 e6             	mov    rsi,r12
    59b8:	48 89 c7             	mov    rdi,rax
    59bb:	49 89 c5             	mov    r13,rax
    59be:	e8 cd ca ff ff       	call   2490 <__memcpy_chk@plt>
    59c3:	48 85 db             	test   rbx,rbx
    59c6:	0f 85 bd 00 00 00    	jne    5a89 <socket@plt+0x34b9>
    59cc:	48 8d 54 24 50       	lea    rdx,[rsp+0x50]
    59d1:	4c 89 fe             	mov    rsi,r15
    59d4:	4c 89 ef             	mov    rdi,r13
    59d7:	e8 54 f8 ff ff       	call   5230 <socket@plt+0x2c60>
    59dc:	4c 89 ef             	mov    rdi,r13
    59df:	e8 4c c9 ff ff       	call   2330 <free@plt>
    59e4:	66 0f 6f 64 24 50    	movdqa xmm4,XMMWORD PTR [rsp+0x50]
    59ea:	66 0f 6f 6c 24 60    	movdqa xmm5,XMMWORD PTR [rsp+0x60]
    59f0:	4c 89 f7             	mov    rdi,r14
    59f3:	66 0f 6f bc 24 f0 00 	movdqa xmm7,XMMWORD PTR [rsp+0xf0]
    59fa:	00 00 
    59fc:	48 8d 54 24 30       	lea    rdx,[rsp+0x30]
    5a01:	66 0f 6f 8c 24 00 01 	movdqa xmm1,XMMWORD PTR [rsp+0x100]
    5a08:	00 00 
    5a0a:	be 60 00 00 00       	mov    esi,0x60
    5a0f:	66 0f 6f 94 24 10 01 	movdqa xmm2,XMMWORD PTR [rsp+0x110]
    5a16:	00 00 
    5a18:	0f 29 a4 24 90 01 00 	movaps XMMWORD PTR [rsp+0x190],xmm4
    5a1f:	00 
    5a20:	66 0f 6f 9c 24 20 01 	movdqa xmm3,XMMWORD PTR [rsp+0x120]
    5a27:	00 00 
    5a29:	0f 29 bc 24 50 01 00 	movaps XMMWORD PTR [rsp+0x150],xmm7
    5a30:	00 
    5a31:	0f 29 8c 24 60 01 00 	movaps XMMWORD PTR [rsp+0x160],xmm1
    5a38:	00 
    5a39:	0f 29 94 24 70 01 00 	movaps XMMWORD PTR [rsp+0x170],xmm2
    5a40:	00 
    5a41:	0f 29 9c 24 80 01 00 	movaps XMMWORD PTR [rsp+0x180],xmm3
    5a48:	00 
    5a49:	0f 29 ac 24 a0 01 00 	movaps XMMWORD PTR [rsp+0x1a0],xmm5
    5a50:	00 
    5a51:	e8 da f7 ff ff       	call   5230 <socket@plt+0x2c60>
    5a56:	66 0f 6f 74 24 30    	movdqa xmm6,XMMWORD PTR [rsp+0x30]
    5a5c:	0f 11 75 00          	movups XMMWORD PTR [rbp+0x0],xmm6
    5a60:	48 8b 84 24 18 02 00 	mov    rax,QWORD PTR [rsp+0x218]
    5a67:	00 
    5a68:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    5a6f:	00 00 
    5a71:	0f 85 cf 00 00 00    	jne    5b46 <socket@plt+0x3576>
    5a77:	48 81 c4 28 02 00 00 	add    rsp,0x228
    5a7e:	5b                   	pop    rbx
    5a7f:	5d                   	pop    rbp
    5a80:	41 5c                	pop    r12
    5a82:	41 5d                	pop    r13
    5a84:	41 5e                	pop    r14
    5a86:	41 5f                	pop    r15
    5a88:	c3                   	ret
    5a89:	b8 40 00 00 00       	mov    eax,0x40
    5a8e:	48 8b 74 24 08       	mov    rsi,QWORD PTR [rsp+0x8]
    5a93:	49 8d 7d 40          	lea    rdi,[r13+0x40]
    5a97:	48 89 da             	mov    rdx,rbx
    5a9a:	49 39 c7             	cmp    r15,rax
    5a9d:	49 0f 43 c7          	cmovae rax,r15
    5aa1:	48 8d 48 c0          	lea    rcx,[rax-0x40]
    5aa5:	e8 e6 c9 ff ff       	call   2490 <__memcpy_chk@plt>
    5aaa:	e9 1d ff ff ff       	jmp    59cc <socket@plt+0x33fc>
    5aaf:	bf 61 06 00 00       	mov    edi,0x661
    5ab4:	4c 8d 35 75 47 00 00 	lea    r14,[rip+0x4775]        # a230 <socket@plt+0x7c60>
    5abb:	e8 10 ca ff ff       	call   24d0 <malloc@plt>
    5ac0:	48 8d 0d b9 0c 00 00 	lea    rcx,[rip+0xcb9]        # 6780 <socket@plt+0x41b0>
    5ac7:	c6 00 0e             	mov    BYTE PTR [rax],0xe
    5aca:	49 89 c5             	mov    r13,rax
    5acd:	b8 01 00 00 00       	mov    eax,0x1
    5ad2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    5ad8:	48 89 c2             	mov    rdx,rax
    5adb:	83 e2 0f             	and    edx,0xf
    5ade:	41 0f b6 14 16       	movzx  edx,BYTE PTR [r14+rdx*1]
    5ae3:	32 14 01             	xor    dl,BYTE PTR [rcx+rax*1]
    5ae6:	41 88 54 05 00       	mov    BYTE PTR [r13+rax*1+0x0],dl
    5aeb:	48 83 c0 01          	add    rax,0x1
    5aef:	48 3d 61 06 00 00    	cmp    rax,0x661
    5af5:	75 e1                	jne    5ad8 <socket@plt+0x3508>
    5af7:	bf 60 00 00 00       	mov    edi,0x60
    5afc:	e8 cf c9 ff ff       	call   24d0 <malloc@plt>
    5b01:	48 8d 0d 18 0c 00 00 	lea    rcx,[rip+0xc18]        # 6720 <socket@plt+0x4150>
    5b08:	c6 00 aa             	mov    BYTE PTR [rax],0xaa
    5b0b:	48 89 c6             	mov    rsi,rax
    5b0e:	b8 01 00 00 00       	mov    eax,0x1
    5b13:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    5b18:	48 89 c2             	mov    rdx,rax
    5b1b:	83 e2 0f             	and    edx,0xf
    5b1e:	41 0f b6 14 16       	movzx  edx,BYTE PTR [r14+rdx*1]
    5b23:	32 14 01             	xor    dl,BYTE PTR [rcx+rax*1]
    5b26:	88 14 06             	mov    BYTE PTR [rsi+rax*1],dl
    5b29:	48 83 c0 01          	add    rax,0x1
    5b2d:	48 83 f8 60          	cmp    rax,0x60
    5b31:	75 e5                	jne    5b18 <socket@plt+0x3548>
    5b33:	4c 89 2d 36 67 00 00 	mov    QWORD PTR [rip+0x6736],r13        # c270 <socket@plt+0x9ca0>
    5b3a:	48 89 35 27 67 00 00 	mov    QWORD PTR [rip+0x6727],rsi        # c268 <socket@plt+0x9c98>
    5b41:	e9 e4 fc ff ff       	jmp    582a <socket@plt+0x325a>
    5b46:	e8 b5 c8 ff ff       	call   2400 <__stack_chk_fail@plt>
    5b4b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
    5b50:	f3 0f 1e fa          	endbr64
    5b54:	e9 d7 f6 ff ff       	jmp    5230 <socket@plt+0x2c60>
    5b59:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    5b60:	41 55                	push   r13
    5b62:	48 8d 35 2e 09 00 00 	lea    rsi,[rip+0x92e]        # 6497 <socket@plt+0x3ec7>
    5b69:	48 8d 3d 2b 0a 00 00 	lea    rdi,[rip+0xa2b]        # 659b <socket@plt+0x3fcb>
    5b70:	41 54                	push   r12
    5b72:	55                   	push   rbp
    5b73:	53                   	push   rbx
    5b74:	48 81 ec 18 02 00 00 	sub    rsp,0x218
    5b7b:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    5b82:	00 00 
    5b84:	48 89 84 24 08 02 00 	mov    QWORD PTR [rsp+0x208],rax
    5b8b:	00 
    5b8c:	31 c0                	xor    eax,eax
    5b8e:	e8 9d c9 ff ff       	call   2530 <fopen@plt>
    5b93:	48 85 c0             	test   rax,rax
    5b96:	0f 84 8a 00 00 00    	je     5c26 <socket@plt+0x3656>
    5b9c:	49 89 c4             	mov    r12,rax
    5b9f:	48 89 e5             	mov    rbp,rsp
    5ba2:	4c 8d 2d ec 09 00 00 	lea    r13,[rip+0x9ec]        # 6595 <socket@plt+0x3fc5>
    5ba9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    5bb0:	4c 89 e2             	mov    rdx,r12
    5bb3:	be 00 02 00 00       	mov    esi,0x200
    5bb8:	48 89 ef             	mov    rdi,rbp
    5bbb:	e8 90 c8 ff ff       	call   2450 <fgets@plt>
    5bc0:	48 85 c0             	test   rax,rax
    5bc3:	74 5d                	je     5c22 <socket@plt+0x3652>
    5bc5:	48 8d 1d 94 5f 00 00 	lea    rbx,[rip+0x5f94]        # bb60 <socket@plt+0x9590>
    5bcc:	4c 89 ee             	mov    rsi,r13
    5bcf:	eb 14                	jmp    5be5 <socket@plt+0x3615>
    5bd1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    5bd8:	48 8b 73 08          	mov    rsi,QWORD PTR [rbx+0x8]
    5bdc:	48 83 c3 08          	add    rbx,0x8
    5be0:	48 85 f6             	test   rsi,rsi
    5be3:	74 cb                	je     5bb0 <socket@plt+0x35e0>
    5be5:	48 89 ef             	mov    rdi,rbp
    5be8:	e8 d3 c9 ff ff       	call   25c0 <strstr@plt>
    5bed:	48 85 c0             	test   rax,rax
    5bf0:	74 e6                	je     5bd8 <socket@plt+0x3608>
    5bf2:	bb 01 00 00 00       	mov    ebx,0x1
    5bf7:	4c 89 e7             	mov    rdi,r12
    5bfa:	e8 e1 c7 ff ff       	call   23e0 <fclose@plt>
    5bff:	48 8b 84 24 08 02 00 	mov    rax,QWORD PTR [rsp+0x208]
    5c06:	00 
    5c07:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    5c0e:	00 00 
    5c10:	75 18                	jne    5c2a <socket@plt+0x365a>
    5c12:	48 81 c4 18 02 00 00 	add    rsp,0x218
    5c19:	89 d8                	mov    eax,ebx
    5c1b:	5b                   	pop    rbx
    5c1c:	5d                   	pop    rbp
    5c1d:	41 5c                	pop    r12
    5c1f:	41 5d                	pop    r13
    5c21:	c3                   	ret
    5c22:	31 db                	xor    ebx,ebx
    5c24:	eb d1                	jmp    5bf7 <socket@plt+0x3627>
    5c26:	31 db                	xor    ebx,ebx
    5c28:	eb d5                	jmp    5bff <socket@plt+0x362f>
    5c2a:	e8 d1 c7 ff ff       	call   2400 <__stack_chk_fail@plt>
    5c2f:	90                   	nop
    5c30:	f3 0f 1e fa          	endbr64
    5c34:	41 55                	push   r13
    5c36:	4c 8d 2d 5a 08 00 00 	lea    r13,[rip+0x85a]        # 6497 <socket@plt+0x3ec7>
    5c3d:	48 8d 3d 6b 09 00 00 	lea    rdi,[rip+0x96b]        # 65af <socket@plt+0x3fdf>
    5c44:	41 54                	push   r12
    5c46:	4c 89 ee             	mov    rsi,r13
    5c49:	55                   	push   rbp
    5c4a:	53                   	push   rbx
    5c4b:	48 81 ec 88 01 00 00 	sub    rsp,0x188
    5c52:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    5c59:	00 00 
    5c5b:	48 89 84 24 78 01 00 	mov    QWORD PTR [rsp+0x178],rax
    5c62:	00 
    5c63:	31 c0                	xor    eax,eax
    5c65:	e8 c6 c8 ff ff       	call   2530 <fopen@plt>
    5c6a:	48 85 c0             	test   rax,rax
    5c6d:	0f 84 2c 02 00 00    	je     5e9f <socket@plt+0x38cf>
    5c73:	49 89 c4             	mov    r12,rax
    5c76:	48 8d 5c 24 70       	lea    rbx,[rsp+0x70]
    5c7b:	48 bd 54 72 61 63 65 	movabs rbp,0x6950726563617254
    5c82:	72 50 69 
    5c85:	0f 1f 00             	nop    DWORD PTR [rax]
    5c88:	4c 89 e2             	mov    rdx,r12
    5c8b:	be 00 01 00 00       	mov    esi,0x100
    5c90:	48 89 df             	mov    rdi,rbx
    5c93:	e8 b8 c7 ff ff       	call   2450 <fgets@plt>
    5c98:	48 85 c0             	test   rax,rax
    5c9b:	0f 84 cf 01 00 00    	je     5e70 <socket@plt+0x38a0>
    5ca1:	48 39 2b             	cmp    QWORD PTR [rbx],rbp
    5ca4:	75 e2                	jne    5c88 <socket@plt+0x36b8>
    5ca6:	66 81 7b 08 64 3a    	cmp    WORD PTR [rbx+0x8],0x3a64
    5cac:	75 da                	jne    5c88 <socket@plt+0x36b8>
    5cae:	31 f6                	xor    esi,esi
    5cb0:	48 8d 7c 24 7a       	lea    rdi,[rsp+0x7a]
    5cb5:	ba 0a 00 00 00       	mov    edx,0xa
    5cba:	31 ed                	xor    ebp,ebp
    5cbc:	e8 ff c7 ff ff       	call   24c0 <__isoc23_strtol@plt>
    5cc1:	85 c0                	test   eax,eax
    5cc3:	40 0f 95 c5          	setne  bpl
    5cc7:	4c 89 e7             	mov    rdi,r12
    5cca:	e8 11 c7 ff ff       	call   23e0 <fclose@plt>
    5ccf:	e8 9c c8 ff ff       	call   2570 <getppid@plt>
    5cd4:	48 8d 5c 24 30       	lea    rbx,[rsp+0x30]
    5cd9:	b9 40 00 00 00       	mov    ecx,0x40
    5cde:	4c 8d 05 e7 08 00 00 	lea    r8,[rip+0x8e7]        # 65cc <socket@plt+0x3ffc>
    5ce5:	41 89 c1             	mov    r9d,eax
    5ce8:	ba 02 00 00 00       	mov    edx,0x2
    5ced:	be 40 00 00 00       	mov    esi,0x40
    5cf2:	48 89 df             	mov    rdi,rbx
    5cf5:	31 c0                	xor    eax,eax
    5cf7:	e8 24 c6 ff ff       	call   2320 <__snprintf_chk@plt>
    5cfc:	4c 89 ee             	mov    rsi,r13
    5cff:	48 89 df             	mov    rdi,rbx
    5d02:	e8 29 c8 ff ff       	call   2530 <fopen@plt>
    5d07:	49 89 c4             	mov    r12,rax
    5d0a:	48 85 c0             	test   rax,rax
    5d0d:	74 7f                	je     5d8e <socket@plt+0x37be>
    5d0f:	48 8d 5c 24 70       	lea    rbx,[rsp+0x70]
    5d14:	66 0f ef c0          	pxor   xmm0,xmm0
    5d18:	48 89 c1             	mov    rcx,rax
    5d1b:	ba 3f 00 00 00       	mov    edx,0x3f
    5d20:	48 89 df             	mov    rdi,rbx
    5d23:	be 01 00 00 00       	mov    esi,0x1
    5d28:	0f 29 44 24 70       	movaps XMMWORD PTR [rsp+0x70],xmm0
    5d2d:	0f 29 84 24 80 00 00 	movaps XMMWORD PTR [rsp+0x80],xmm0
    5d34:	00 
    5d35:	0f 29 84 24 90 00 00 	movaps XMMWORD PTR [rsp+0x90],xmm0
    5d3c:	00 
    5d3d:	0f 29 84 24 a0 00 00 	movaps XMMWORD PTR [rsp+0xa0],xmm0
    5d44:	00 
    5d45:	e8 56 c6 ff ff       	call   23a0 <fread@plt>
    5d4a:	4c 89 e7             	mov    rdi,r12
    5d4d:	49 89 c5             	mov    r13,rax
    5d50:	e8 8b c6 ff ff       	call   23e0 <fclose@plt>
    5d55:	4d 85 ed             	test   r13,r13
    5d58:	0f 85 19 01 00 00    	jne    5e77 <socket@plt+0x38a7>
    5d5e:	4c 8d 25 23 5e 00 00 	lea    r12,[rip+0x5e23]        # bb88 <socket@plt+0x95b8>
    5d65:	48 8d 35 3f 08 00 00 	lea    rsi,[rip+0x83f]        # 65ab <socket@plt+0x3fdb>
    5d6c:	eb 0f                	jmp    5d7d <socket@plt+0x37ad>
    5d6e:	66 90                	xchg   ax,ax
    5d70:	49 8b 34 24          	mov    rsi,QWORD PTR [r12]
    5d74:	49 83 c4 08          	add    r12,0x8
    5d78:	48 85 f6             	test   rsi,rsi
    5d7b:	74 11                	je     5d8e <socket@plt+0x37be>
    5d7d:	48 89 df             	mov    rdi,rbx
    5d80:	e8 eb c6 ff ff       	call   2470 <strcmp@plt>
    5d85:	85 c0                	test   eax,eax
    5d87:	75 e7                	jne    5d70 <socket@plt+0x37a0>
    5d89:	bd 01 00 00 00       	mov    ebp,0x1
    5d8e:	48 8d 3d 45 08 00 00 	lea    rdi,[rip+0x845]        # 65da <socket@plt+0x400a>
    5d95:	e8 76 c5 ff ff       	call   2310 <getenv@plt>
    5d9a:	48 85 c0             	test   rax,rax
    5d9d:	74 09                	je     5da8 <socket@plt+0x37d8>
    5d9f:	80 38 00             	cmp    BYTE PTR [rax],0x0
    5da2:	0f 85 e6 00 00 00    	jne    5e8e <socket@plt+0x38be>
    5da8:	48 8d 3d 36 08 00 00 	lea    rdi,[rip+0x836]        # 65e5 <socket@plt+0x4015>
    5daf:	e8 5c c5 ff ff       	call   2310 <getenv@plt>
    5db4:	48 85 c0             	test   rax,rax
    5db7:	74 0b                	je     5dc4 <socket@plt+0x37f4>
    5db9:	80 38 00             	cmp    BYTE PTR [rax],0x0
    5dbc:	0f 95 c0             	setne  al
    5dbf:	0f b6 c0             	movzx  eax,al
    5dc2:	09 c5                	or     ebp,eax
    5dc4:	e8 97 fd ff ff       	call   5b60 <socket@plt+0x3590>
    5dc9:	48 8d 74 24 10       	lea    rsi,[rsp+0x10]
    5dce:	bf 01 00 00 00       	mov    edi,0x1
    5dd3:	89 c3                	mov    ebx,eax
    5dd5:	e8 e6 c5 ff ff       	call   23c0 <clock_gettime@plt>
    5dda:	c7 44 24 0c 00 00 00 	mov    DWORD PTR [rsp+0xc],0x0
    5de1:	00 
    5de2:	31 c0                	xor    eax,eax
    5de4:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    5de8:	8b 54 24 0c          	mov    edx,DWORD PTR [rsp+0xc]
    5dec:	01 c2                	add    edx,eax
    5dee:	2d 4f 86 c8 61       	sub    eax,0x61c8864f
    5df3:	89 54 24 0c          	mov    DWORD PTR [rsp+0xc],edx
    5df7:	3d 40 69 1f cc       	cmp    eax,0xcc1f6940
    5dfc:	75 ea                	jne    5de8 <socket@plt+0x3818>
    5dfe:	48 8d 74 24 20       	lea    rsi,[rsp+0x20]
    5e03:	bf 01 00 00 00       	mov    edi,0x1
    5e08:	e8 b3 c5 ff ff       	call   23c0 <clock_gettime@plt>
    5e0d:	48 8b 44 24 20       	mov    rax,QWORD PTR [rsp+0x20]
    5e12:	48 2b 44 24 10       	sub    rax,QWORD PTR [rsp+0x10]
    5e17:	48 69 c0 00 ca 9a 3b 	imul   rax,rax,0x3b9aca00
    5e1e:	48 03 44 24 28       	add    rax,QWORD PTR [rsp+0x28]
    5e23:	48 2b 44 24 18       	sub    rax,QWORD PTR [rsp+0x18]
    5e28:	09 eb                	or     ebx,ebp
    5e2a:	74 11                	je     5e3d <socket@plt+0x386d>
    5e2c:	c7 05 da 61 00 00 ef 	mov    DWORD PTR [rip+0x61da],0xdeadbeef        # c010 <socket@plt+0x9a40>
    5e33:	be ad de 
    5e36:	31 ff                	xor    edi,edi
    5e38:	e8 23 c5 ff ff       	call   2360 <_exit@plt>
    5e3d:	c7 05 c9 61 00 00 00 	mov    DWORD PTR [rip+0x61c9],0x0        # c010 <socket@plt+0x9a40>
    5e44:	00 00 00 
    5e47:	48 3d 00 94 35 77    	cmp    rax,0x77359400
    5e4d:	7f 49                	jg     5e98 <socket@plt+0x38c8>
    5e4f:	48 8b 84 24 78 01 00 	mov    rax,QWORD PTR [rsp+0x178]
    5e56:	00 
    5e57:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
    5e5e:	00 00 
    5e60:	75 44                	jne    5ea6 <socket@plt+0x38d6>
    5e62:	48 81 c4 88 01 00 00 	add    rsp,0x188
    5e69:	5b                   	pop    rbx
    5e6a:	5d                   	pop    rbp
    5e6b:	41 5c                	pop    r12
    5e6d:	41 5d                	pop    r13
    5e6f:	c3                   	ret
    5e70:	31 ed                	xor    ebp,ebp
    5e72:	e9 50 fe ff ff       	jmp    5cc7 <socket@plt+0x36f7>
    5e77:	42 80 7c 2c 6f 0a    	cmp    BYTE PTR [rsp+r13*1+0x6f],0xa
    5e7d:	0f 85 db fe ff ff    	jne    5d5e <socket@plt+0x378e>
    5e83:	42 c6 44 2c 6f 00    	mov    BYTE PTR [rsp+r13*1+0x6f],0x0
    5e89:	e9 d0 fe ff ff       	jmp    5d5e <socket@plt+0x378e>
    5e8e:	bd 01 00 00 00       	mov    ebp,0x1
    5e93:	e9 2c ff ff ff       	jmp    5dc4 <socket@plt+0x37f4>
    5e98:	31 ff                	xor    edi,edi
    5e9a:	e8 c1 c4 ff ff       	call   2360 <_exit@plt>
    5e9f:	31 ed                	xor    ebp,ebp
    5ea1:	e9 29 fe ff ff       	jmp    5ccf <socket@plt+0x36ff>
    5ea6:	e8 55 c5 ff ff       	call   2400 <__stack_chk_fail@plt>

Disassembly of section .fini:

0000000000005eac <.fini>:
    5eac:	f3 0f 1e fa          	endbr64
    5eb0:	48 83 ec 08          	sub    rsp,0x8
    5eb4:	48 83 c4 08          	add    rsp,0x8
    5eb8:	c3                   	ret
