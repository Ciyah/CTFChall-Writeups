#!/usr/bin/env python3
import re
import time

import requests

TARGET = "http://154.57.164.72:32179"
HOST = "edulearn.htb:32179"
ASSIGNMENT = "1786604528483"
COOKIE = "s%3Ayve069_dIxGm6AJw12-V_R9cK-0sXTQz.MG6aKxiBrhNQzdSB0RXEeALOSmUfr3rflQZx3vDqxcA"

session = requests.Session()
session.headers.update({"Host": HOST, "Cookie": f"connect.sid={COOKIE}"})

before = session.get(f"{TARGET}/assignment/{ASSIGNMENT}", timeout=10).text
old_ids = set(re.findall(r'href="/submission/(\d+)"', before))

for index in range(52):
    response = session.post(
        f"{TARGET}/submit",
        data={"assignmentId": ASSIGNMENT, "content": f"prng-{index:02d}"},
        allow_redirects=False,
        timeout=10,
    )
    response.raise_for_status()

time.sleep(13)
page = session.get(f"{TARGET}/assignment/{ASSIGNMENT}", timeout=10).text
pairs = re.findall(r"Score:\s*(\d+)\s*/100.*?href=\"/submission/(\d+)\"", page, re.S)
newest_first = [(submission_id, int(score)) for score, submission_id in pairs if submission_id not in old_ids]

for submission_id, score in reversed(newest_first):
    print(submission_id, score)
print(f"collected={len(newest_first)}")
