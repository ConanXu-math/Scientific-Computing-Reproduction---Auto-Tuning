---
name: repo-reproduction-skill
description: This skill should be used when the user asks to analyze, reproduce, or run a computational math repository. Use when inspecting source code, detecting algorithms, planning runs, executing experiments, or collecting results from optimization code.
version: 0.1.0
---

# Repo Reproduction Skill

Analyzes a computational math repository, generates run plans, executes them, and collects results.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Scripts

### repo_analyzer
Analyzes source code directory. Input: `--source <path>`. Output: `repo_analysis.json` with language, dependencies, entrypoints, detected algorithms, confidence, warnings.

```bash
python -m skills.repo_reproduction_skill.scripts.repo_analyzer --source /path/to/repo --out /path/to/output
```

### run_planner
Generates candidate run plans from `repo_analysis.json`. Input: `--analysis <repo_analysis.json>`. Output: `run_plan.json` with commands, risk levels, timeouts.

```bash
python -m skills.repo_reproduction_skill.scripts.run_planner --analysis repo_analysis.json --out /path/to/output
```

### executor
Executes an approved run plan. Input: `--plan <run_plan.json>`. Use `--require-approval <checkpoint>` to block on human approval. Writes `execution_log.jsonl` and `run_log.txt`.

```bash
python -m skills.repo_reproduction_skill.scripts.executor --plan run_plan.json --out /path/to/output --require-approval run_plan
```

### result_collector
Scans executed output for result files and extracts metrics. Input: `--source`, `--out`. Output: `collected_results.json`.

```bash
python -m skills.repo_reproduction_skill.scripts.result_collector --source /path/to/repo --out /path/to/output
```

## Workflow

1. Run `repo_analyzer` to understand the repository
2. Review `repo_analysis.json` — ask user for confirmation or corrections
3. Run `run_planner` to generate candidate execution plans
4. Present plans to user for approval
5. Run `executor` with approved plan
6. Run `result_collector` to gather results
