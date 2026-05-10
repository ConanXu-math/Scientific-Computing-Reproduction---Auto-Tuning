---
name: computational-math-reproduction-workflow-skill
description: Use when a user starts an end-to-end computational math research-code reproduction, deployment, tuning, visualization, or reporting workflow with a coding agent.
version: 0.1.0
---

# Computational Math Reproduction Workflow Skill

This is the default entrypoint for open-source users of the computational math research-code reproduction system. The repository is Skill-first and Codex-native: Codex reads the relevant Skills, inspects the source, explains evidence in conversation, writes compact review artifacts, and waits for human approval before consequential execution.

Codex is the primary reference operator for this protocol, but the artifact contract is agent-neutral. Other coding agents can follow the same Skill documents, review artifacts, approval records, and evidence rules.

Scripts are tools, not drivers. They may help with local execution, logging, plotting, approval records, or repeatable toy checks, but there is no user-facing CLI pipeline and no command-line orchestrator that defines the workflow.

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

For a narrow one-off task, Codex may use a specialist Skill directly. For any workflow that crosses stages, return here first.

## Default Flow

The default workflow is compact and conversation-led:

```text
user goal
  -> Codex reads relevant Skills
  -> Codex inspects/searches source
  -> Codex writes plan.md
  -> human approves
  -> Codex runs minimal reproduction
  -> repair_plan.md only if needed
  -> RUN_SUMMARY.md
  -> optional tuning/tuning_plan.md
  -> tuning/TUNING_SUMMARY.md
```

Default output locations:

- `outputs/{run_id}/plan.md`
- `outputs/{run_id}/repair_plan.md` only when source edits, dependency changes, adapters, or entrypoint changes are needed
- `outputs/{run_id}/RUN_SUMMARY.md`
- `outputs/{run_id}/tuning/tuning_plan.md` only after reproduction succeeds or partially succeeds and tuning is proposed
- `outputs/{run_id}/tuning/tuning_results.csv`
- `outputs/{run_id}/tuning/best_parameters.json`
- `outputs/{run_id}/tuning/tuning.log`
- `outputs/{run_id}/tuning/tuning_figures/`
- `outputs/{run_id}/tuning/TUNING_SUMMARY.md`

Debug checkpoints may still be written under `outputs/{run_id}/checkpoints/` when a durable review trail is useful, but they are optional documentation, not the default workflow mechanism.

## Required Start Sequence

1. Understand the user goal: search, reproduce, deploy, tune, report, or a combination.
2. Select specialist Skills using `references/skill_routing.md`.
3. Inspect the source or search candidates with Codex-native tools first.
4. Write `outputs/{run_id}/plan.md` with the task interpretation, candidate command, risks, timeout, and expected evidence.
5. Summarize the plan in conversation and wait for `approve / revise / reject / skip`.

Use `outputs/{run_id}/workflow_state.json` when durable resume state is useful. It is a state helper, not a workflow driver.

## Conversation Playbook

Use this Skill as a coding-agent conversation protocol, not as a fully automatic batch runner.

1. Generate a stable `run_id` when the user has not provided one. Prefer a short descriptive name plus date or a numbered `run_###` directory under `outputs/`.
2. Inspect files, dependency manifests, candidate entrypoints, metrics, and algorithm evidence directly.
3. Route to specialist Skills. Record selected Skills in conversation and, when useful, in `workflow_state.json`.
4. Write `plan.md` before execution. Include the minimal reproduction command, why it is selected, risk level, timeout, expected outputs, and what will be logged.
5. Ask for exactly one of `approve`, `revise`, `reject`, or `skip`.
6. After approval, execute only the approved minimal reproduction. If using the executor helper, call it with `--require-approval run_plan`.
7. If execution fails or repair is needed, write `repair_plan.md`, explain the evidence, and ask for approval before source edits, dependency changes, adapters, or entrypoint changes.
8. Write `RUN_SUMMARY.md` with reproduction status, logs, metrics, limitations, and next options.
9. Propose tuning only after reproduction succeeds or partially succeeds. Write `tuning/tuning_plan.md`, ask for approval, and only then run tuning. If using the tuning helper, call it with `--require-approval tuning_plan`.
10. Write `tuning/TUNING_SUMMARY.md` after approved tuning. Ask for final review before accepting conclusions.

## Optional State Fields

When `workflow_state.json` is useful, keep it current with:

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
- `next_prompt_to_user`

`pending_checkpoint` and `pending_user_decision` may refer to compact artifacts such as `plan.md`, `repair_plan.md`, or `tuning/tuning_plan.md`, not only numbered checkpoint files.

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

## Specialist Routing

- Use `algorithm_discovery_skill` when the user asks Codex to search for external algorithms or implementations.
- Use `repo_reproduction_skill` for repository analysis, run planning, execution, and result collection.
- Use `environment_deployment_skill` for dependency and runtime reports.
- Use `failure_diagnosis_skill` when a run fails or repair is needed.
- Use `auto_tuning_skill` only after reproduction succeeds or partially succeeds and the human approves tuning.
- Use `visualization_skill` when convergence or tuning metrics can be plotted.
- Use `report_generation_skill` for `plan.md`, `RUN_SUMMARY.md`, and tuning summaries.
- Use `human_review_skill` when durable approval logs or numbered checkpoints are useful.

## References

- `references/skill_routing.md`: map user intent and stages to specialist Skills.
- `references/checkpoint_contract.md`: optional checkpoint and approval rules.

## Acceptance

A coding agent can start from a natural-language goal, read the Skills, inspect or search the source, write `plan.md`, wait for approval, run a minimal reproduction, produce `RUN_SUMMARY.md`, and optionally run approved tuning under `tuning/` without invoking a user-facing CLI pipeline.
