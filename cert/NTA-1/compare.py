#!/usr/bin/env python3
"""Compare the JSON result lines of the primary (NTA-1.out) and cross-check (NTA-1_x.out).
Usage: python compare.py out/NTA-1.out out/NTA-1_x.out"""
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if l.startswith("JSON ")]
    assert len(lines) == 1, f"{path}: expected one JSON line, found {len(lines)}"
    return json.loads(lines[0][5:])


def passline(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.startswith("PASS ") or l.startswith("FAIL ")]


a, b = load(sys.argv[1]), load(sys.argv[2])
same = a == b
for pa, pb in zip(a["results"], b["results"]):
    for ra, rb in zip(pa["rows"], pb["rows"]):
        flag = "agree" if ra == rb else "DISAGREE"
        print(f"part ({pa['part']}) a={pa['a']} m={ra['m']}: {ra['value']} mod 121 = {ra['mod121']} | "
              f"{rb['value']} mod 121 = {rb['mod121']}  [{flag}]")
pl = passline(sys.argv[1]) + passline(sys.argv[2])
print("verdict lines:", pl)
ok = same and len(pl) == 2 and all(l.startswith("PASS ") for l in pl)
print("PASS NTA-1 compare (primary and cross-check identical)" if ok else "FAIL NTA-1 compare")
sys.exit(0 if ok else 1)
