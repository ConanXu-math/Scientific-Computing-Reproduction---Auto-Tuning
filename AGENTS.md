# AGENTS.md

This repository develops a Skill-driven Computational Math Reproduction, Deployment, Auto-Tuning, Visualization, and Reporting System for coding agents.

A coding agent is the operator. Codex is the primary reference operator and implementation profile for this repository, but the workflow artifacts are intended to be usable by other coding agents. Skills are the workflow control layer. Scripts are optional tools that an agent can call during the conversation. The human is the decision maker at checkpoints.

The whole repository is agent-native first. Prefer the active coding agent's native abilities to read files, search, reason, edit, inspect outputs, and explain evidence in conversation. Use scripts or CLI only when reproducibility, structured artifacts, logs, tests, or batch execution make them useful.

For open-source end-to-end use, start with `skills/computational_math_reproduction_workflow_skill/SKILL.md`. It is the default entrypoint for computational math research-code reproduction workflows, routing the active coding agent to specialist Skills, maintaining `outputs/{run_id}/workflow_state.json`, and enforcing human checkpoints.

## Open-source product boundary

What you **ship to users** is the **Skill layer** under `skills/` (plus this contract: conversation, checkpoints, `outputs/{run_id}/`, approvals). A user’s **inputs** are natural-language goals, optional local paths or remote repositories, and any task YAML or commands **they** define. Nothing in `tests/` or `tests/fixtures/` is required to *use* the system: those exist only for **maintainers** to verify scripts and gates. The public design goal is: **drive the workflow through Skills** (and the agent reading them), not through a bundled demo tree.

## Runtime Environment

Use the shared Conda environment `ai4math`, matching `/Users/conanxu/paper-to-skill`.

Preferred command form:

```bash
conda run -n ai4math python -m <module>
```

Run tests with:

```bash
conda run -n ai4math pytest
```

Do not install this project into the user's global Python environment.

## Scope

- Phase 1 focuses on continuous optimization research code.
- Priority algorithm families: ADMM, PPA, proximal gradient, primal-dual methods, and augmented Lagrangian methods.
- Python projects are supported for automatic environment setup and execution.
- MATLAB, Julia, C++, and R are detected and reported, but are not automatically run in the MVP.

## Conversation-First Workflow

1. Human gives the coding agent a task, repository, archive, or local path.
2. The agent starts with `computational_math_reproduction_workflow_skill` for multi-stage work and states which specialist Skills it will use and why.
3. The agent uses native file/search/reasoning tools to analyze the repository or external sources.
4. The agent writes artifacts under `outputs/{run_id}/` only when durable review or reproducibility is useful.
5. The agent summarizes the checkpoint in conversation.
6. The agent asks the human for `approve`, `revise`, `reject`, or `skip`.
7. The agent records the decision with `approval_logger.py`.
8. The agent executes only the approved next step.
9. The agent reports evidence, failures, and next choices.
10. The agent asks for final review before making final conclusions.

Do not present this system as a fully automatic harness. The normal interface is human-agent dialogue.

## Required Checkpoints

- `01_task_understanding.md`: domain, algorithm family, problem type, expected goal, metrics.
- `02_run_plan_review.md`: candidate commands, reasons, timeouts, risk levels.
- `03_failure_fix_review.md`: dependency conflicts, source edits, entrypoint changes, missing data.
- `04_tuning_plan_review.md`: parameter space, search method, budget, metric, constraints.
- `05_final_review.md`: reproduction status and evidence.
- `06_algorithm_match_review.md`: external algorithm candidates, sources, match evidence, and human selection.

For external algorithm discovery, prefer the active agent's native search/browser/GitHub capabilities in conversation. Use CLI scripts only as optional helpers for structured persistence, batch querying, or reproducibility.

For repository analysis, failure diagnosis, report drafting, and tuning-plan design, also prefer agent-native reasoning and file inspection first. Scripts are helpers, not the interface.

## Approval Rules

- Low-risk read-only analysis can run without approval.
- Low-risk demo commands can run after run-plan approval.
- Execution helpers must enforce approval when they support it. Use `executor.py --require-approval run_plan` for repository reproduction runs.
- High-risk commands always require human approval.
- Source modifications require human approval.
- Dependency version changes beyond declared install files require human approval.
- Long experiments and tuning budget expansion require human approval.
- Final conclusions require `05_final_review.md`.

## Output Rules

- All artifacts must be saved under `outputs/`.
- All external command logs must be saved.
- Failed reproduction or tuning must generate `failure_analysis.md`.
- Tuning must not start until `04_tuning_plan_review.md` exists and is approved.
- Successful reproduction or tuning should generate figures under `outputs/{run_id}/figures/` when convergence or tuning data is available.

## Safety Rules

- Do not execute `sudo`.
- Do not execute `rm -rf`.
- Do not execute `curl | bash` or `wget | bash`.
- Do not read sensitive files in the user home directory.
- Do not print tokens, passwords, or API keys.
- Do not modify the user's global Python environment.
- Do not run commands indefinitely.
- All subprocess commands must set `timeout`.
- Risky README commands must be marked `risk_level=high` and must not be executed automatically.
