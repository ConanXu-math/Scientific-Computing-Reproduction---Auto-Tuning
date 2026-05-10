from __future__ import annotations

import argparse
import json
from pathlib import Path


def classify_failure(stderr: str, stdout: str = "") -> dict:
    text = f"{stderr}\n{stdout}".lower()
    if "modulenotfounderror" in text or "no module named" in text:
        kind = "dependency_error"
    elif "version conflict" in text or "resolutionimpossible" in text:
        kind = "version_conflict"
    elif "no such file" in text or "file not found" in text:
        kind = "missing_data"
    elif "can't open file" in text or "missing_entrypoint" in text:
        kind = "missing_entrypoint"
    elif "timeout" in text or "timed out" in text:
        kind = "timeout"
    elif "nan" in text or "diverge" in text or "overflow" in text:
        kind = "numerical_failure"
    elif "permission denied" in text:
        kind = "permission_error"
    elif "high_risk_command" in text or "sudo" in text or "rm -rf" in text:
        kind = "high_risk_command"
    elif "readme" in text and "unclear" in text:
        kind = "readme_unclear"
    else:
        kind = "unknown_error"
    high = kind in {"high_risk_command", "version_conflict", "missing_data", "permission_error", "unknown_error"}
    return {
        "failure_type": kind,
        "summary": text[:500],
        "risk_level": "high" if high else "medium",
        "requires_human_confirmation": high,
    }


def write_failure_analysis(out: Path | str, stderr: str, stdout: str = "", command: str = "") -> Path:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    result = classify_failure(stderr, stdout)
    body = f"""# Failure Analysis

## Error Summary
{result['summary'] or 'No stderr/stdout evidence was captured.'}

## Failure Type
{result['failure_type']}

## Evidence
Command: `{command}`

## Suggested Fix
Review dependencies, entrypoints, data availability, and numerical settings. Do not apply high-risk fixes automatically.

## Risk Level
{result['risk_level']}

## Requires Human Confirmation
{result['requires_human_confirmation']}

## Next Step
Generate or review `03_failure_fix_review.md` before changing source code or dependencies.
"""
    path = out / "failure_analysis.md"
    path.write_text(body)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stderr", default="")
    parser.add_argument("--stdout", default="")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = classify_failure(args.stderr, args.stdout)
    if args.out:
        write_failure_analysis(args.out, args.stderr, args.stdout)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
