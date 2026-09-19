import socket
import time

t_before = time.time()
s = socket.create_connection(("pager.chal.sunwaycybersecurityclub.org", 3838), timeout=15)
t_after = time.time()

s.settimeout(2)
banner = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        banner += chunk
except socket.timeout:
    pass

payload = "GETFLAG\n" + "ENC hex:" + "00" * 256 + "\n"
s.sendall(payload.encode())

data = b""
s.settimeout(5)
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
except socket.timeout:
    pass

print("t_before:", t_before)
print("t_after:", t_after)
print("RAW:", repr(data.decode(errors="replace")))
s.close()
