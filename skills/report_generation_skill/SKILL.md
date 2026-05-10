---
name: report-generation-skill
description: This skill should be used when the user asks to generate a report, summarize results, write up findings, or create documentation for a computational math reproduction or tuning experiment.
version: 0.1.0
---

# Report Generation Skill

Aggregates all run artifacts into structured Markdown reports.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### report_writer
Input: `--run <path>` — run directory with repo_analysis.json, execution_log.jsonl, best_parameters.json, tuning_results.csv, figures/

Output: environment_report.md, reproduce_report.md, tuning_report.md, failure_analysis.md, final_summary.md

```bash
python -m skills.report_generation_skill.scripts.report_writer --run /path/to/output
```

## Workflow

1. After experiments complete, run `report_writer`
2. Review generated reports
3. Ask user if they want sections expanded or additional context included
