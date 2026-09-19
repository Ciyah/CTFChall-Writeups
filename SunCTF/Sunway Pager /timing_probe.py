import socket, time

def recv_prompt(s):
    d = b""
    while not d.endswith(b"command> "):
        x = s.recv(4096)
        if not x: raise EOFError
        d += x
    return d

s = socket.create_connection(("pager.chal.sunwaycybersecurityclub.org", 3838), timeout=15)
s.settimeout(30)
start = time.monotonic()
recv_prompt(s)
for i in range(20):
    s.sendall(b"ENC hex:00\n")
    try:
        reply = recv_prompt(s)
    except Exception as e:
        print(i + 1, round(time.monotonic()-start, 3), type(e).__name__)
        break
    print(i + 1, round(time.monotonic()-start, 3), repr(reply))
