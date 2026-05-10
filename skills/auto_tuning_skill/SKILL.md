---
name: auto-tuning-skill
description: This skill should be used when the user asks to tune parameters, run hyperparameter search, optimize algorithm settings, or find the best configuration for a computational math method.
version: 0.1.0
---

# Auto Tuning Skill

Runs parameter tuning experiments using grid search or random search.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### experiment_runner
Input: `--source <path>`, `--task <task.yaml>`, `--budget <n>`, `--out <path>`, `--method <grid_search|random_search>`

Output: `tuning_results.csv`, `best_parameters.json`

```bash
python -m skills.auto_tuning_skill.scripts.experiment_runner --source /path/to/repo --param-space task.yaml --budget 20 --out /path/to/output --require-approval tuning_plan
```

## Workflow

1. Define parameter space in `task.yaml`
2. Propose tuning budget and method to user for approval
3. Run `experiment_runner --require-approval tuning_plan`
4. Present results and best parameters to user
5. Ask if user wants to refine the parameter space and repeat
