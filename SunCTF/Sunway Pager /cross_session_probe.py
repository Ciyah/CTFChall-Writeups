import re, socket, time

def recv_prompt(s):
    d=b""
    while not d.endswith(b"command> "):
        d += s.recv(4096)
    return d

for i in range(12):
    before=time.time_ns()
    s=socket.create_connection(("pager.chal.sunwaycybersecurityclub.org",3838),timeout=5)
    after=time.time_ns()
    s.settimeout(5); recv_prompt(s)
    s.sendall(b"GETFLAG\n"); f=recv_prompt(s)
    s.sendall(b"ENC hex:0000000000000000\n"); e=recv_prompt(s)
    fh=re.search(rb"([0-9a-f]{76})",f).group(1).decode()
    eh=re.search(rb"(?m)^([0-9a-f]{16})\r?$",e).group(1).decode()
    print(before,after,fh,eh)
    s.close()
