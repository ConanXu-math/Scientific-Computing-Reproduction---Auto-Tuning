---
name: computational-math-reproduction-workflow-skill
description: Use when a user starts an end-to-end computational math research-code reproduction, deployment, tuning, visualization, or reporting workflow with a coding agent.
version: 0.1.0
---

# Computational Math Reproduction Workflow Skill

This is the default entrypoint for open-source users of the computational math research-code reproduction system. It coordinates the specialist Skills while keeping an agent-mediated conversation as the main interface. Specialist Skills do not communicate directly; the coding agent uses `outputs/{run_id}/workflow_state.json`, checkpoints, reports, and approval logs as the shared state.

Codex is the primary reference operator for this protocol, but the artifact contract is agent-neutral. Other coding agents can follow the same state, checkpoint, approval, and evidence rules. Codex-native behavior is documented as one implementation profile, not a requirement of the core workflow.

## When To Use

Use this Skill before any end-to-end task involving:

- computational math code reproduction or repository analysis
- external algorithm discovery
- environment deployment
- experiment execution
- failure diagnosis
- automatic tuning
- convergence or tuning visualization
- final report generation

For a narrow one-off task, an agent may use a specialist Skill directly. For any workflow that crosses stages, return here first.

## Required Start Sequence

1. Understand the user goal: search, reproduce, deploy, tune, report, or a combination.
2. Create or read `outputs/{run_id}/workflow_state.json`.
3. Select specialist Skills using `references/skill_routing.md`.
4. Generate the current checkpoint using `human_review_skill`.
5. Summarize the checkpoint in conversation and wait for `approve / revise / reject / skip`.

## Conversation Playbook

Use this Skill as a coding-agent conversation protocol, not as a fully automatic batch runner.

1. Generate a stable `run_id` when the user has not provided one. Prefer a short descriptive name plus date or a numbered `run_###` directory under `outputs/`.
2. Call or mirror `scripts/workflow_state.py create` before any consequential stage. If `workflow_state.json` already exists, resume from it instead of restarting.
3. Inspect the source and route to specialist Skills. Record the selected Skills in `selected_skills`.
4. Write the stage checkpoint and set `pending_checkpoint`, `pending_user_decision`, `allowed_next_actions`, `next_action_for_agent`, and `next_prompt_to_user`.
5. Summarize evidence in conversation. Ask for exactly one of `approve`, `revise`, `reject`, or `skip`.
6. When the user responds, apply the decision to the pending checkpoint. If there is no `pending_checkpoint`, do not infer approval; ask which checkpoint the decision applies to.
7. Execute only actions listed in `allowed_next_actions`. If an action is blocked, add it to `blocked_actions` and route to failure diagnosis or human review.
8. Add every durable file, log, report, figure, and checkpoint that supports a decision to `evidence_artifacts`.

## Stage Artifact Protocol

| Stage | Required Inputs | Required Outputs | Pending Checkpoint |
| --- | --- | --- | --- |
| `task_understanding` | user task, source hint, local files or external source summary | `checkpoints/01_task_understanding.md`, `workflow_state.json` | `task_understanding` |
| `algorithm_discovery` | task understanding, algorithm keywords, optional external search results | `checkpoints/06_algorithm_match_review.md`, ranked candidates | `algorithm_match` |
| `repo_analysis` | source path or fetched repository | `repo_analysis.json`, candidate entrypoints, dependency summary | none unless uncertainty requires review |
| `environment_plan` | repo analysis and dependency files | environment report, install-risk notes | `failure_fix` when dependency changes are needed |
| `run_plan` | repo analysis and environment report | `checkpoints/02_run_plan_review.md`, `run_plan.json` | `run_plan` |
| `reproduction` | approved run plan | `execution_log.jsonl`, `run_log.txt`, collected outputs | none; failed runs route to `failure_fix` |
| `failure_fix` | failed execution evidence | `checkpoints/03_failure_fix_review.md`, `failure_analysis.md` | `failure_fix` |
| `tuning_plan` | successful or partially successful reproduction evidence | `checkpoints/04_tuning_plan_review.md`, parameter space and budget | `tuning_plan` |
| `tuning` | approved tuning plan | tuning results, tuning logs, optional best parameters | none; failures route to `failure_fix` |
| `visualization` | convergence or tuning metrics | figures under `figures/` | none unless conclusions change |
| `reporting` | logs, reports, figures, checkpoints | final Markdown report | `final` |
| `final_review` | full evidence chain | `checkpoints/05_final_review.md` | `final` |

## Stage Order

`task_understanding -> algorithm_discovery? -> repo_analysis -> environment_plan -> run_plan -> reproduction -> failure_fix? -> tuning_plan? -> tuning? -> visualization -> reporting -> final_review`

Optional stages are used only when the task needs them.

## Human Gates

Pause for human confirmation before you:

- execute external code
- install or upgrade dependencies
- create an adapter or wrapper
- modify source
- replace an entrypoint or data
- start tuning
- expand tuning budget
- accept a final conclusion

Repository execution must use `executor.py --require-approval run_plan`. Tuning execution must use `experiment_runner.py --require-approval tuning_plan`.

## Shared State

Use `scripts/workflow_state.py` or equivalent agent-native file editing to keep `workflow_state.json` current with:

- `schema_version`
- `run_id`
- `source`
- `current_stage`
- `last_completed_stage`
- `selected_skills`
- `approved_checkpoints`
- `pending_checkpoint`
- `pending_user_decision`
- `blocked_actions`
- `allowed_next_actions`
- `evidence_artifacts`
- `next_action_for_agent`
- `next_action_for_codex`
- `next_prompt_to_user`

`next_action_for_agent` is the protocol field. `next_action_for_codex` is retained as a backward-compatible alias for existing Codex-oriented scripts and documentation.

## References

- `references/skill_routing.md`: map user intent and stages to specialist Skills.
- `references/checkpoint_contract.md`: checkpoint and approval rules.

## Acceptance

A coding agent can restart from `workflow_state.json`, route to the right specialist Skills, block unapproved execution, and produce reports under `outputs/{run_id}/`.
