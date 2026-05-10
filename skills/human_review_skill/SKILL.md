---
name: human-review-skill
description: This skill should be used when the user wants to set up checkpoints, record approval decisions, gate execution pending human confirmation, or manage human-in-the-loop review points in a computational math workflow.
version: 0.1.0
---

# Human Review Skill

Manages checkpoints and approval state for human-in-the-loop workflows.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Scripts

### checkpoint_writer
Input: `--type <checkpoint_type>`, `--run <path>`, `--context-json <json>`
Types: task_understanding, run_plan, failure_fix, tuning_plan, final, algorithm_match, all

```bash
python -m skills.human_review_skill.scripts.checkpoint_writer --type all --run /path/to/output
```

### approval_gate
Input: `--run <path>`, `--checkpoint <name>`, `--risk-level <low|high>`
Exits 0 if allowed, exits 2 if blocked.

### approval_logger
Records an approval decision to `approvals/approval_log.jsonl`.

## Workflow

1. After analysis or planning, write a checkpoint for human review
2. Present the checkpoint to user and ask for decision
3. Log the user's decision with `approval_logger`
4. Before high-risk steps, use `approval_gate` to confirm approval

## Agent Conversation Semantics

Use `workflow_state.json` as the source of truth for pending decisions.

- When writing a checkpoint, set `pending_checkpoint` to the checkpoint name and `pending_user_decision` to `true`.
- Ask for exactly one decision: `approve`, `revise`, `reject`, or `skip`.
- If the user approves, record the approval and clear `pending_checkpoint`.
- If the user asks to revise, keep the same checkpoint pending and rewrite it with the requested change.
- If the user rejects, record the rejection, clear the pending checkpoint, and add the proposed action to `blocked_actions`.
- If the user skips, clear the pending checkpoint only when the stage is optional.
- Do not log a decision when no checkpoint is pending; ask which checkpoint the decision applies to.

Checkpoint files are decision artifacts, not just raw data dumps. Each checkpoint should include a concise human-readable summary plus the raw JSON context used to produce it.
