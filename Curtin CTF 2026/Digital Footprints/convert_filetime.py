"""
Evidence script: convert the raw Windows FILETIME from SOMETHING.EXE-0A0B02BB.pf
to IST to reproduce the flag independently.

FILETIME at offset 0x80 in decompressed Prefetch data: 0x01DD65708F80E872
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ticks = 0x01DD65708F80E872
epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
utc = epoch + timedelta(microseconds=ticks // 10)
ist = utc.astimezone(ZoneInfo("Asia/Kolkata"))

print(f"UTC : {utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"IST : {ist.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Flag: {ist.strftime('CURTIN_CTF{%d_%m_%Y_%H:%M:%S}')}")
