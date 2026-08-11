#!/usr/bin/env python3
import base64
import re
import subprocess
import urllib.parse


PCAP = "sustraffic.pcapng"
TAG_HEX = dict(
    zip(
        [
            "cite", "h1", "p", "a", "img", "ul", "ol", "button",
            "div", "span", "label", "textarea", "nav", "b", "i",
            "blockquote",
        ],
        "0123456789abcdef",
    )
)


def packets():
    output = subprocess.check_output(
        [
            "tshark", "-r", PCAP, "-Y", "http", "-T", "fields",
            "-E", "separator=|", "-e", "frame.number",
            "-e", "http.request.method", "-e", "http.request.uri",
            "-e", "http.response.code", "-e", "http.file_data",
        ],
        text=True,
    )
    for line in output.splitlines():
        fields = line.split("|", 4)
        if len(fields) == 5 and fields[4]:
            yield fields[:4], bytes.fromhex(fields[4]).decode(errors="replace")


def decode_command(html):
    body = re.search(r"<body>(.*?)</body>", html, re.DOTALL).group(1)
    # The malware runs on Windows and splits on CRLF. The server uses LF, so all
    # of the generated tags remain in the first logical line seen by the client.
    body = body.split("\r\n", 1)[0]
    encoded = "".join(
        TAG_HEX[tag]
        for tag in re.findall(r"<(\w+)[\s>]", body)
        if tag != "li"
    )
    return bytes.fromhex(encoded).decode("ascii")


def decode_output(form):
    feedback = urllib.parse.parse_qs(form)["feedback"][0]
    encoded = "".join(token[0] for token in feedback.split())
    return base64.b64decode(encoded).decode(errors="replace")


commands = []
outputs = []
for (frame, method, uri, status), body in packets():
    if status == "200" and uri == "/" and "<body>" in body:
        value = decode_command(body)
        commands.append(value)
        print(f"frame {frame:>3} command: {value}")
    elif method == "POST":
        value = decode_output(body)
        outputs.append(value)
        print(f"frame {frame:>3} output:  {value!r}")

first = re.search(r"HTB\{[^\s']*", "\n".join(commands)).group(0)
second = re.search(r"[^\s']+\}", "\n".join(outputs)).group(0)
print(f"\nFLAG: {first}{second}")
