#!/usr/bin/env python3
"""Replication script for the jevlint benchmark run.

Requirements:
    python3 -m pip install jevlint==1.2.0   (needs Python 3.10+)
    TYPESAFE_API_KEY in the environment (the checks that ask Jev, and the
    re-send runs, call the API)

Runs, in order:
    1. static pass   jevlint check <query> --static-only   (no API calls)
    2. model pass    jevlint check <query>                 (2n+2 to 4n+2 calls per query)
    3. re-sends      jevlint probe <query> --repeats=5     (only RESEND_QUERIES, ~6-7 calls each;
                    the command is the tool's own name for resending a query unchanged and
                    then in small rewrites, to see whether the answer moves)

Outputs:
    reports/static_reports.json
    reports/model_reports.json
    resend-tests/<query>.probe.txt   (transcripts; the .probe suffix is the tool's name)

Reference numbers from the original run (jevlint 1.2.0, catalogue v1 5231d67e7d46
for jev-1.13): static 40 findings (0 errors), model pass 143 calls with
16 error / 23 warning / 54 advice findings, all runs complete. Readings from
Jev move at the 0.01-0.03 level between runs, so per-finding probabilities
reproduce only to that tolerance; the recorded reports in this repository are
the exact outputs of the original run.
"""
import collections
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reports")
RESENDS = os.path.join(HERE, "resend-tests")
RESEND_QUERIES = [
    os.path.join(HERE, "queries", "q_origin_overlap_00.json"),
    os.path.join(HERE, "queries", "q_bayes_claims_00.json"),
    os.path.join(HERE, "queries", "q_bayes_claims_01.json"),
    os.path.join(HERE, "queries", "q_bayes_claims_02.json"),
    os.path.join(HERE, "queries", "q_bayes_claims_03.json"),
    os.path.join(HERE, "queries", "q_bayes_claims_04.json"),
]
RUN_RESENDS = os.environ.get("JEVLINT_BENCH_RESENDS", "1") != "0"


def run_jevlint(args):
    p = subprocess.run(["jevlint", *args], capture_output=True, text=True)
    if p.returncode == 2:
        sys.exit(f"jevlint could not run: {p.stdout}{p.stderr}")
    return p


def parse(p):
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"error": {"kind": "parse", "stdout": p.stdout[:400], "stderr": p.stderr[:400]}}


def summarize(findings):
    sev = collections.Counter(f["severity"] for f in findings)
    chk = collections.Counter(f["check"] for f in findings)
    return {"severity": dict(sev), "by_check": dict(chk)}


def main():
    queries = sorted(glob.glob(os.path.join(HERE, "queries", "*.json")))
    if not queries:
        sys.exit(f"no query files found under {os.path.join(HERE, 'queries')}")
    print(f"{len(queries)} queries")

    out = os.path.join(HERE, "reports")
    os.makedirs(out, exist_ok=True)
    os.makedirs(RESENDS, exist_ok=True)

    static = []
    for f in queries:
        p = run_jevlint(["check", f, "--static-only", "--format=json"])
        static.append(parse(p))
        print(f"  static {os.path.basename(f)}: exit={p.returncode}")
    with open(os.path.join(out, "static_reports.json"), "w") as fh:
        json.dump(static, fh, indent=1)
    print("static totals:", summarize([x for d in static for x in d.get("findings", [])]))

    model = {}
    for f in queries:
        p = run_jevlint(["check", f, "--format=json"])
        model[os.path.basename(f)] = parse(p)
        s = parse(p).get("summary") or {}
        print(f"  model  {os.path.basename(f)}: exit={p.returncode} calls={s.get('calls')} complete={s.get('complete')}")
    with open(os.path.join(out, "model_reports.json"), "w") as fh:
        json.dump(model, fh, indent=1)
    findings = [x for d in model.values() for x in d.get("findings", [])]
    calls = sum((d.get("summary") or {}).get("calls") or 0 for d in model.values())
    print("model totals:", summarize(findings), "| calls:", calls)

    if RUN_RESENDS:
        for f in RESEND_QUERIES:
            if not os.path.exists(f):
                print(f"  re-send {f}: not found, skipped")
                continue
            p = run_jevlint(["probe", f, "--repeats=5"])
            dst = os.path.join(RESENDS, os.path.basename(f)[:-5] + ".probe.txt")
            with open(dst, "w") as fh:
                fh.write(p.stdout)
                if p.stderr:
                    fh.write("\n[stderr]\n" + p.stderr)
            print(f"  re-send {os.path.basename(f)}: exit={p.returncode} -> {dst}")


if __name__ == "__main__":
    main()
