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


def _pip_freeze() -> str:
    try:
        proc = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, timeout=60, check=False)
        return proc.stdout
    except subprocess.TimeoutExpired:
        return "pip freeze timed out"


def write_reports(run: Path | str) -> list[Path]:
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    analysis = _read_json(run / "repo_analysis.json") or {}
    executions = [json.loads(line) for line in (run / "execution_log.jsonl").read_text().splitlines()] if (run / "execution_log.jsonl").exists() else []
    best = _read_json(run / "best_parameters.json") or {}
    tuning_rows = []
    if (run / "tuning_results.csv").exists():
        tuning_rows = list(csv.DictReader((run / "tuning_results.csv").open()))
    figures = sorted((run / "figures").glob("*.svg")) if (run / "figures").exists() else []
    figure_links = "\n".join(f"![{path.stem}](figures/{path.name})" for path in figures)
    convergence_links = "\n".join(f"![{path.stem}](figures/{path.name})" for path in figures if path.name.startswith("convergence"))
    tuning_links = "\n".join(f"![{path.stem}](figures/{path.name})" for path in figures if path.name.startswith("tuning"))

    reports = {
        "environment_report.md": f"""# Environment Report

- OS: {platform.platform()}
- Python version: {sys.version.split()[0]}
- Detected dependency files: {analysis.get('dependency_files', [])}
- Installation status: not_run_or_external
- Installation warnings: {analysis.get('warnings', [])}

## pip freeze
```text
{_pip_freeze()}
```
""",
        "reproduce_report.md": f"""# Reproduce Report

- Repo path: {analysis.get('repo_path', 'unknown')}
- Source type: local_or_fetched
- Commit hash: unknown
- Detected language: {analysis.get('language', 'unknown')}
- Detected algorithm: {analysis.get('detected_algorithms', [])}
- Dependency files: {analysis.get('dependency_files', [])}
- Candidate entrypoints: {analysis.get('candidate_entrypoints', [])}
- Run status: {[item.get('status') for item in executions]}
- Runtime: {[item.get('runtime') for item in executions]}
- Reproduction status: {'success' if any(item.get('status') == 'success' for item in executions) else 'needs_human_review'}

See `run_log.txt` for stdout/stderr summaries and `collected_results.json` when available.

## Figures
{convergence_links or 'No convergence figures generated.'}
""",
        "tuning_report.md": f"""# Tuning Report

- Tuning objective: runtime
- Search method: random_search_or_grid_search
- Budget: {len(tuning_rows)}
- Best parameters: {best}
- Best metric value: {best.get('runtime', 'unknown')}
- tuning_results.csv: `{run / 'tuning_results.csv'}`
- Failed trials: {sum(1 for row in tuning_rows if str(row.get('success')).lower() in {'false', '0'})}
- Recommended configuration: {best}

## Figures
{tuning_links or 'No tuning figures generated.'}
""",
        "failure_analysis.md": (run / "failure_analysis.md").read_text() if (run / "failure_analysis.md").exists() else """# Failure Analysis

No failure evidence has been recorded.
""",
        "final_summary.md": f"""# Final Summary

- Final status: {'success_or_partial' if executions or tuning_rows else 'needs_human_review'}
- Main evidence: reports, logs, metrics, checkpoints, and tuning results under this run directory.
- Reproduction goal reached: {any(item.get('status') == 'success' for item in executions)}
- Tuning completed: {bool(tuning_rows)}
- Human follow-up needed: review `checkpoints/05_final_review.md`.
- Next suggestions: expand language backends, sandbox runners, Optuna/Bayesian tuning, solver routing, and PDE/FEM coverage.

## Figures
{figure_links or 'No figures generated.'}
""",
    }
    written = []
    for name, body in reports.items():
        path = run / name
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
