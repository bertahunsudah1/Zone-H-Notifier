#!/usr/bin/env python3
"""
${REPO_NAME} - realistic utility example
Non-destructive demo program with sub-commands, logging & tests compatibility.
"""
import argparse, base64, hashlib, json, logging, random, string, sys, time

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def b64encode(s):
    return base64.b64encode(s.encode()).decode()

def b64decode(s):
    try:
        return base64.b64decode(s.encode()).decode()
    except Exception:
        return "<invalid>"

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def gen_random_token(length=32):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def analyze_payload(payload: str):
    # simplistic heuristic checks for "shell" signatures (non-destructive)
    sigs = ["eval(", "base64_decode(", "system(", "passthru(", "preg_replace(", "exec("]
    findings = []
    for s in sigs:
        if s in payload:
            findings.append(s)
    return findings

def main():
    p = argparse.ArgumentParser(prog="${REPO_NAME}")
    p.add_argument("action", choices=["demo", "encode", "decode", "hash", "check"], help="action")
    p.add_argument("value", nargs="?", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    out = {}
    if args.action == "demo":
        out = {"timestamp": int(time.time()), "sample": gen_random_token(8)}
    elif args.action == "encode":
        out = {"input": args.value, "b64": b64encode(args.value)}
    elif args.action == "decode":
        out = {"input": args.value, "decoded": b64decode(args.value)}
    elif args.action == "hash":
        out = {"input": args.value, "md5": md5(args.value)}
    elif args.action == "check":
        out = {"input": args.value, "findings": analyze_payload(args.value)}

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(out)

if __name__ == "__main__":
    main()
