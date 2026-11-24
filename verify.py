"""Replay the bundled operations against one candidate and print a JSON report."""
import argparse
import csv
import hashlib
import importlib
import json
from pathlib import Path

LOCAL = Path(__file__).resolve().parent


def perform(cart, row):
    action = row["action"]
    if action == "put":
        cart.put(row["item"], int(row["quantity"]))
    elif action == "begin":
        cart.begin()
    elif action == "finish":
        save = {"true": True, "false": False}.get(row["save"], row["save"])
        cart.finish(save)
    elif action == "read":
        return {"value": cart.read(row["item"])}
    elif action == "probe_export":
        cart.export()["q"] = 9
    else:
        raise ValueError(f"Unknown fixture action {action!r}")
    return {}


def check(cart_factory, rows, expected):
    ids = [row["case_id"] for row in rows]
    if not ids or len(ids) != len(set(ids)) or set(ids) != set(expected):
        raise ValueError("Operation and expectation IDs must match exactly and be unique")
    carts = {}
    findings = []
    for row in rows:
        if row["cart"] not in carts:
            carts[row["cart"]] = cart_factory()
        cart = carts[row["cart"]]
        case = row["case_id"]
        try:
            actual = perform(cart, row)
        except (ValueError, TypeError, RuntimeError) as error:
            actual = {"error": type(error).__name__}
        actual["items"] = cart.export()
        passed = actual == expected[case]
        findings.append({"case": case, "passed": passed, "actual": actual, "expected": expected[case]})
    return findings


def report(version):
    names = {"v1": "candidate_v1", "v2": "candidate_v2"}
    name = names[version]
    with (LOCAL / "orders.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = json.loads((LOCAL / "expected.json").read_text(encoding="utf-8"))
    findings = check(importlib.import_module(name).Cart, rows, expected)
    files = ["orders.csv", "expected.json", "requirements.md", "verify.py", f"{name}.py"]
    digests = {file: hashlib.sha256((LOCAL / file).read_bytes()).hexdigest() for file in files}
    failures = sum(not row["passed"] for row in findings)
    return {"candidate": version, "status": "FAIL" if failures else "PASS", "failures": failures,
            "cases": len(findings), "sha256": digests, "findings": findings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", choices=["v1", "v2"])
    arguments = parser.parse_args()
    result = report(arguments.candidate)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["failures"] > 0)
