from __future__ import annotations

import argparse
import csv
import json
import platform
import subprocess
import sys
from pathlib import Path


def _read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def _first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def _pip_freeze() -> str:
    try:
        proc = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, timeout=60, check=False)
        return proc.stdout
    except subprocess.TimeoutExpired:
        return "pip freeze timed out"


def write_reports(run: Path | str) -> list[Path]:
    """Write compact Markdown reports for the minimal output tree.

    Generates only:
    - plan.md
    - RUN_SUMMARY.md
    - tuning/TUNING_SUMMARY.md (if tuning was run)
    """
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    tuning_dir = run / "tuning"
    best_path = _first_existing(tuning_dir / "best_parameters.json", run / "best_parameters.json")
    best = _read_json(best_path) if best_path else {}
    tuning_rows = []
    tuning_csv = _first_existing(tuning_dir / "tuning_results.csv", run / "tuning_results.csv")
    if tuning_csv:
        tuning_rows = list(csv.DictReader(tuning_csv.open()))
    figures = sorted((run / "figures").glob("*.svg")) if (run / "figures").exists() else []
    figure_links = "\n".join(f"![{path.stem}](figures/{path.name})" for path in figures)

    reports = {
        "RUN_SUMMARY.md": f"""# Run Summary

## Status
{{status}}

## Source
{{source}}

## Commands Run
{{commands}}

## Evidence
{{evidence}}

## Results
{{results}}

## Figures
{figure_links or 'No figures generated.'}

## Patches
{{patches}}

## Limitations
{{limitations}}

## Optional Tuning Recommendation
{{tuning_recommendation}}
""",
    }

    if tuning_rows:
        reports["tuning/TUNING_SUMMARY.md"] = f"""# Tuning Summary

## Status
{{status}}

## Budget
{{budget}}

## Search Method
{{method}}

## Best Parameters
```
{json.dumps(best, indent=2)}
```

## Baseline vs Best
{{baseline_vs_best}}

## Evidence
{{evidence}}

## Limitations
{{limitations}}
"""

    written = []
    for name, body in reports.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    print(json.dumps([str(path) for path in write_reports(args.run)], indent=2))


if __name__ == "__main__":
    main()
