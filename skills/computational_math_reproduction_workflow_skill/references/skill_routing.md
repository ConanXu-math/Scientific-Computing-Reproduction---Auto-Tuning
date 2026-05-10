# Skill Routing

Use `computational_math_reproduction_workflow_skill` as the default entrypoint for end-to-end computational math research-code reproduction workflows. Route to specialist Skills as follows:

| User Intent / Stage | Specialist Skill |
| --- | --- |
| Search papers, project pages, GitHub implementations, or external algorithm candidates | `algorithm_discovery_skill` |
| Analyze a repository, fetch source, plan commands, run approved reproduction, collect results | `repo_reproduction_skill` |
| Detect ADMM, PPA, proximal gradient, primal-dual, augmented Lagrangian, or related continuous optimization algorithms | `continuous_optimization_skill` |
| Identify dependency files, deployment strategy, Python environment choices, and installation risks | `environment_deployment_skill` |
| Create checkpoints, record decisions, check approval gates, or enforce human-in-the-loop pauses | `human_review_skill` |
| Diagnose errors, timeouts, dependency failures, numerical failures, missing data, or unsafe commands | `failure_diagnosis_skill` |
| Design parameter spaces, choose grid/random search, and run approved tuning experiments | `auto_tuning_skill` |
| Plot convergence histories, residuals, tuning runtime, and best-so-far curves | `visualization_skill` |
| Generate environment, reproduction, tuning, failure, visualization, and final Markdown reports | `report_generation_skill` |

## Routing Rules

- Start with `computational_math_reproduction_workflow_skill` when more than one stage is involved.
- Add `human_review_skill` whenever a checkpoint, approval log, or approval gate is needed.
- Add `continuous_optimization_skill` for first-phase optimization repositories unless the algorithm family is already known.
- Add `failure_diagnosis_skill` immediately after a failed or blocked run.
- Add `report_generation_skill` after reproduction, tuning, or failure diagnosis.

## Artifact Contracts

| Specialist Skill | Input artifacts | Output artifacts | Failure route |
| --- | --- | --- | --- |
| `algorithm_discovery_skill` | task understanding, algorithm family, problem type, optional query terms | external search results, ranked candidates, `checkpoints/06_algorithm_match_review.md` | `human_review_skill` for candidate selection or `failure_diagnosis_skill` for search failures |
| `repo_reproduction_skill` | source path or fetched repository, approved run plan when executing | `repo_analysis.json`, `run_plan.json`, `execution_log.jsonl`, `run_log.txt`, collected results | `failure_diagnosis_skill` |
| `continuous_optimization_skill` | repository files, paper notes, README, scripts | algorithm-family evidence and default parameter-space hint | `human_review_skill` when evidence is ambiguous |
| `environment_deployment_skill` | dependency files, repo analysis, runtime constraints | environment report and installation-risk summary | `human_review_skill` before dependency changes |
| `human_review_skill` | checkpoint context, active `pending_checkpoint`, human decision | checkpoint Markdown, approval log, approval-gate result | workflow state `blocked_actions` |
| `failure_diagnosis_skill` | failed command, stdout, stderr, logs, traceback, blocked action | `failure_analysis.md`, classified failure, proposed fix | `human_review_skill` before any fix |
| `auto_tuning_skill` | approved tuning plan, parameter space, execution command, metric | tuning results, best parameters, tuning logs | `failure_diagnosis_skill` |
| `visualization_skill` | convergence CSV, tuning CSV, result metrics | figures under `figures/` and report assets | `report_generation_skill` with a missing-figure note |
| `report_generation_skill` | environment report, execution logs, tuning results, figures, checkpoints | final Markdown report and final-review context | `human_review_skill` for final conclusion |

After each specialist Skill finishes, update `workflow_state.json` with new `evidence_artifacts`, the next `current_stage`, and any required `pending_checkpoint`.
