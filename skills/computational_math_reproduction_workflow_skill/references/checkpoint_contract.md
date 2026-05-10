# Checkpoint Contract

The active coding agent must use checkpoints to keep the human in control of computational math workflows.

## Required Stages

| Stage | Checkpoint | Pause Before |
| --- | --- | --- |
| `task_understanding` | `01_task_understanding.md` | accepting the task interpretation |
| `algorithm_discovery` | `06_algorithm_match_review.md` | selecting external code to pursue |
| `run_plan` | `02_run_plan_review.md` | execute external code |
| `failure_fix` | `03_failure_fix_review.md` | install or upgrade dependencies, create an adapter, modify source, replace entrypoint, replace data |
| `tuning_plan` | `04_tuning_plan_review.md` | start tuning or expand tuning budget |
| `final_review` | `05_final_review.md` | accept a final conclusion |

## Approval Decisions

Ask for exactly one decision: `approve`, `revise`, `reject`, or `skip`.

Record decisions in `outputs/{run_id}/approvals/approval_log.jsonl`.

Tie every decision to the active `pending_checkpoint` in `workflow_state.json`.

- `approve`: record approval, add the checkpoint to `approved_checkpoints`, clear `pending_checkpoint`, and continue only with the next allowed stage.
- `revise`: record the request, keep `pending_checkpoint` active, rewrite the checkpoint with the requested changes, and ask again.
- `reject`: record the rejection, clear the pending checkpoint, add the proposed action to `blocked_actions`, and stop or reroute.
- `skip`: record the skip, clear the pending checkpoint, and continue only if the stage is optional.

If a user says `approve`, `revise`, `reject`, or `skip` when no `pending_checkpoint` exists, the agent must ask which checkpoint the decision applies to instead of logging it.

## Gates

- Repository reproduction uses `executor.py --require-approval run_plan`.
- Tuning uses `experiment_runner.py --require-approval tuning_plan`.
- If approval is missing, tools must return `blocked` and record the blocked action in either `failure_analysis.md` or `workflow_state.json`.

## Checkpoint Content

Each checkpoint must include:

- `Decision Needed`: the exact decision vocabulary.
- A human-readable evidence summary for the checkpoint type.
- Candidate commands, fixes, tuning budgets, external candidates, or final conclusions when applicable.
- `Raw Context`: the structured JSON used to render the checkpoint.
- Safety notes for high-risk commands, source changes, dependency changes, long runs, and budget expansion.
