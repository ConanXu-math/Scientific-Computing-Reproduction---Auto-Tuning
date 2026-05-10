---
name: failure-diagnosis-skill
description: This skill should be used when an execution fails, an error occurs, a command times out, or the user asks to diagnose what went wrong with a computational math experiment.
version: 0.1.0
---

# Failure Diagnosis Skill

Classifies execution failures and generates fix proposals.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### failure_classifier
Input: `--stderr <text>`, `--stdout <text>`, `--out <path>`
Output: `failure_analysis.md`

Classified failure types: dependency_error, version_conflict, missing_data, missing_entrypoint, timeout, numerical_failure, permission_error, high_risk_command, readme_unclear, unknown_error

```bash
python -m skills.failure_diagnosis_skill.scripts.failure_classifier --stderr "ModuleNotFoundError" --out /path/to/output
```

## Workflow

1. When an execution fails, run `failure_classifier` with stderr/stdout
2. Review the failure analysis
3. Ask user how to proceed: attempt fix, adjust parameters, or escalate
4. Do not apply high-risk fixes without explicit user approval
