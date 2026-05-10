# Computational Math Reproduction & Tuning Skills

[中文 README](README.zh-CN.md)

This repository is a Skill-first, Codex-native workspace for computational math research-code reproduction. It gives a coding agent a set of readable Skills for understanding a user goal, inspecting a research repository, planning a minimal run, collecting evidence, proposing repairs, tuning parameters, making figures, and writing a concise summary.

The first focus area is Python continuous optimization, especially ADMM, proximal methods, primal-dual methods, PPA, and augmented Lagrangian workflows.

## How It Works

You talk to Codex in natural language. Codex reads the Skills under `skills/`, inspects the target source, writes a compact plan, asks for approval before consequential steps, then records evidence under `outputs/{run_id}/`.

Start end-to-end reproduction work with `skills/computational_math_reproduction_workflow_skill/SKILL.md`. The human remains the decision maker at approval points; scripts are small optional tools Codex can call when they make execution, logging, plotting, or approval records easier to verify.

## Codex-Native Usage

Tell your coding agent the goal in natural language. For end-to-end computational math research-code reproduction work, ask the agent to start with `computational_math_reproduction_workflow_skill`; it will inspect files, route to specialist Skills, summarize evidence, and pause for confirmation before consequential steps.

Example prompt:

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Search for an ADMM/LASSO Python implementation, reproduce the minimal serial demo,
and after it runs, optionally propose a small tuning plan.

Output policy:
- keep outputs compact;
- write plan.md before execution;
- write repair_plan.md only when source/dependency changes are needed;
- write RUN_SUMMARY.md at the end;
- put tuning artifacts under tuning/ only when tuning is approved;
- use scripts only as optional tools, not as the workflow driver.
```

Other useful prompts:

```text
Inspect /path/to/my/repository, identify the optimization problem,
and write plan.md for review before executing anything.
```

```text
Search for external algorithm candidates relevant to this LASSO / ADMM task.
Prioritize papers, project pages, and GitHub implementations. Let me choose.
```

```text
The demo has reproduced. Propose tuning/tuning_plan.md with parameter space,
budget, objective metric, and constraints. Wait for approval.
```

## Skills

- `computational_math_reproduction_workflow_skill`: default entrypoint for open-source users of this computational math reproduction system; routes work across specialist Skills and keeps Codex in the operator role.
- `repo_reproduction_skill`: repository analysis, run planning, execution, result collection.
- `environment_deployment_skill`: deployment plans, dependency detection, environment reports.
- `continuous_optimization_skill`: ADMM/PPA/proximal/primal-dual algorithm detection.
- `algorithm_discovery_skill`: external algorithm candidate search.
- `auto_tuning_skill`: tuning plans and grid/random search.
- `visualization_skill`: convergence and tuning figures.
- `failure_diagnosis_skill`: failure classification and repair proposals.
- `human_review_skill`: optional approval logs for high-risk operations.
- `report_generation_skill`: plan, run summary, and tuning summary reports.

## Default Artifacts

The compact default workflow writes artifacts under `outputs/{run_id}/`:

- `plan.md` before execution;
- `repair_plan.md` only when source or dependency changes are needed;
- `RUN_SUMMARY.md` at the end;
- `tuning/tuning_plan.md` only when tuning is proposed;
- `tuning/tuning_results.csv`, `tuning/best_parameters.json`, `tuning/tuning.log`, `tuning/tuning_figures/`, and `tuning/TUNING_SUMMARY.md` only after tuning is approved.

Checkpoint files under `outputs/{run_id}/checkpoints/` and approval logs under `outputs/{run_id}/approvals/` remain available as optional durable review mechanisms.

## Environment

Use the same Conda environment as `/Users/conanxu/paper-to-skill`: `ai4math`.

```bash
conda create -y -n ai4math python=3.13 pip
conda run -n ai4math python -m pip install -e ".[dev]"
```

See `docs/environment.md`.

## Maintainer Tests

```bash
conda run -n ai4math pytest
```

Pytest covers helper tools. End-to-end reproduction behavior is validated through Codex smoke runs.
