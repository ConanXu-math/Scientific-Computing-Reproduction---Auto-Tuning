# Computational Math Reproduction & Tuning Skills

[中文 README](README.zh-CN.md)

This repository provides coding-agent-facing Skills for computational math research-code reproduction, environment deployment, parameter tuning, visualization, and report generation. Codex is the primary reference operator, but the workflow artifacts are designed for coding agents in general.

The MVP focuses on Python continuous optimization.

### What open-source users actually depend on

The **supported interface** is the **Skills** under `skills/` (start at `computational_math_reproduction_workflow_skill`). You describe the task in conversation; the agent follows the Skill routing, checkpoints, and optional scripts. **You** supply the code to reproduce (path, clone URL, archive, etc.) and approve risky steps.  
`tests/` and `tests/fixtures/` are **maintainer-only** harnesses for CI; they are **not** part of the end-user mental model and are not required to get work done.

## Usage

Tell your coding agent the goal in natural language. For end-to-end computational math research-code reproduction work, ask the agent to start with `computational_math_reproduction_workflow_skill`; it will inspect files, route to specialist Skills, summarize evidence, and pause for confirmation before consequential steps.

Example prompts:

```text
Inspect /path/to/my/repository (or the paper code I linked), identify the optimization problem,
and propose a run plan for review before executing anything.
```

```text
Search for external algorithm candidates relevant to this LASSO / ADMM task.
Prioritize papers, project pages, and GitHub implementations. Let me choose.
```

```text
The demo has reproduced. Propose a tuning plan with parameter space,
budget, objective metric, and constraints. Wait for approval.
```

## Full Workflow Test Prompt

To test the conversation-first workflow end to end, start a fresh agent session in this repository and send this prompt:

```text
Use computational_math_reproduction_workflow_skill as the entrypoint.
Treat this as a full workflow smoke test for the coding-agent Skill protocol.

Search topic: ADMM or closely related splitting methods for LASSO / sparse
linear regression in continuous optimization.
Run id: outputs/full_workflow_search_first_admm_lasso

Goal:
1. Understand the task as a search-first computational math reproduction
   workflow. Identify the problem type, algorithm family, expected metrics,
   and reproduction goal.
2. Write the task-understanding checkpoint and stop for my decision.
3. After I approve, search for external algorithm candidates from public
   sources such as papers, project pages, and GitHub repositories. Prefer
   candidates with runnable Python code, clear optimization metrics, and a
   close match to ADMM / LASSO.
4. Rank the candidates with source URLs, match evidence, code availability,
   likely entrypoints, and risks. Write the algorithm-match checkpoint and
   stop for my decision.
5. After I approve one candidate, fetch or inspect only the approved source.
   If no external candidate is safe enough, stop and ask me for a local path to use,
   or wait until I supply one; do not assume a demo directory in this repo.
6. Analyze the selected repository or fallback source and environment.
7. Propose a run plan with candidate commands, reasons, risk levels, timeouts,
   and expected outputs. Write the run-plan checkpoint and stop for my decision.
8. After I approve, execute only the approved low-risk run using the ai4math
   environment and save logs under the run directory.
9. If the run succeeds, propose a small tuning plan with a tiny budget suitable
   for a smoke test. Write the tuning-plan checkpoint and stop for my decision.
10. After I approve, run the approved tuning, generate any available figures or
    summaries, and draft the final review checkpoint.
11. Stop before accepting the final conclusion and ask me to approve, revise,
    reject, or skip.

Follow the agent-neutral workflow contract:
- maintain workflow_state.json;
- use pending_checkpoint and pending_user_decision;
- record approvals in approvals/approval_log.jsonl;
- keep durable evidence under outputs/full_workflow_search_first_admm_lasso/;
- do not execute high-risk commands;
- do not modify source code or dependencies.
```

Then reply at each checkpoint with one of:

```text
approve
```

or:

```text
revise: <what should change>
reject: <why>
skip: <why this optional stage should be skipped>
```

Expected evidence after the smoke test includes `workflow_state.json`, checkpoint Markdown files, `approvals/approval_log.jsonl`, search/discovery notes, execution logs, and final-review material under `outputs/full_workflow_search_first_admm_lasso/`.

## Skills

- `computational_math_reproduction_workflow_skill`: default entrypoint for open-source users of this computational math reproduction system; routes work across specialist Skills and maintains `workflow_state.json`.
- `repo_reproduction_skill`: repository analysis, run planning, execution, result collection.
- `environment_deployment_skill`: deployment plans, dependency detection, environment reports.
- `continuous_optimization_skill`: ADMM/PPA/proximal/primal-dual algorithm detection.
- `algorithm_discovery_skill`: external algorithm candidate search.
- `auto_tuning_skill`: tuning plans and grid/random search.
- `visualization_skill`: convergence and tuning figures.
- `failure_diagnosis_skill`: failure classification and repair proposals.
- `human_review_skill`: checkpoints and approval logs.
- `report_generation_skill`: environment, reproduction, tuning, failure, and final reports.

## Checkpoints

Review artifacts may be written under `outputs/{run_id}/checkpoints/`:

- `01_task_understanding.md`
- `02_run_plan_review.md`
- `03_failure_fix_review.md`
- `04_tuning_plan_review.md`
- `05_final_review.md`
- `06_algorithm_match_review.md`

Approvals are appended to `outputs/{run_id}/approvals/approval_log.jsonl`.

Cross-Skill workflow state is stored in `outputs/{run_id}/workflow_state.json`.

## Environment

Use the same Conda environment as `/Users/conanxu/paper-to-skill`: `ai4math`.

```bash
conda create -y -n ai4math python=3.13 pip
conda run -n ai4math python -m pip install -e ".[dev]"
```

See `docs/environment.md`.

## Optional Commands

Structured batch helpers (`computational_math_skills.cli`) are optional; Skills-first workflows often skip them.

Use **`--task` pointing at a YAML you own** (domain, metrics, tuning space). For a **YAML shape reference** maintained for CI only, see `tests/fixtures/tasks/admm_tuning_task.yaml` and copy or adapt—it is not required at runtime unless you invoke the CLI.

Prepare analysis and checkpoints:

```bash
conda run -n ai4math python -m computational_math_skills.cli run \
  --task path/to/my_task.yaml \
  --out outputs/run_001
```

Structured external discovery:

```bash
conda run -n ai4math python -m computational_math_skills.cli discover-algorithms \
  --task path/to/my_task.yaml \
  --out outputs/run_001 \
  --sources arxiv,github \
  --max-results 5
```

Demo auto-run (if your task file enables it):

```bash
conda run -n ai4math python -m computational_math_skills.cli run \
  --task path/to/my_task.yaml \
  --out outputs/run_demo \
  --demo-auto-run
```

## Test (maintainers)

```bash
conda run -n ai4math pytest
```

End users rely on **Skills**; running this suite is not part of the supported open-source workflow unless you contribute to the repo.
