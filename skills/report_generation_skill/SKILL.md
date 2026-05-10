---
name: report-generation-skill
description: This skill should be used when the user asks to generate a report, summarize results, write up findings, or create documentation for a computational math reproduction or tuning experiment.
version: 0.1.0
---

# Report Generation Skill

Aggregates run artifacts into compact Markdown reports for the Skill-first Codex workflow.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Optional Helper

### report_writer
Input: `--run <path>` — run directory with repo analysis, execution logs, optional tuning outputs, and figures.

Output includes `plan.md`, `RUN_SUMMARY.md`, optional legacy reports, and `tuning/TUNING_SUMMARY.md`.

```bash
python -m skills.report_generation_skill.scripts.report_writer --run /path/to/output
```

## Workflow

1. Draft `plan.md` before execution when a durable plan is useful.
2. After reproduction, write `RUN_SUMMARY.md` with status, evidence, limits, and next options.
3. If tuning was approved and run, write `tuning/TUNING_SUMMARY.md`.
4. Ask the user if conclusions are acceptable or if sections need revision.
