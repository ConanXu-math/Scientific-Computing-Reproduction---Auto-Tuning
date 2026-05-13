---
name: matlab-runtime-skill
description: Use when a computational math repository or task uses MATLAB files, MATLAB README commands, MATLAB toolboxes, or MATLAB MCP execution tools.
version: 0.1.0
---

# MATLAB Runtime Skill

MATLAB is a runtime backend, not the workflow driver. The workflow remains Skill-first and conversation-first: `computational_math_reproduction_workflow_skill` writes plans, records evidence under `outputs/{run_id}/`, and pauses for human approval before consequential execution.

This Skill defines how to inspect, plan, and optionally execute MATLAB code in computational math reproduction tasks.

## When To Use

- Source contains `.m`, `.mlx`, `.mat`, MATLAB project files, or MATLAB README commands.
- A repository depends on MATLAB toolboxes.
- The user wants MATLAB execution, tests, static analysis, or toolbox detection.
- MATLAB MCP tools are available or need to be checked.

## When Not To Use

- The task is a pure Python, Julia, C++, or R repository with no MATLAB artifacts.
- The user wants MATLAB Agentic Toolkit installation itself. In that case, use the official MATLAB Agentic Toolkit setup guidance as a reference and ask for approval before changing global Codex configuration.

## Execution Boundary

- Do static file inspection without approval.
- Before executing MATLAB code, write or update the run plan and ask for approval.
- Use MATLAB MCP tools only when available in the current agent session.
- If MCP tools are unavailable, produce a MATLAB runtime plan and verification instructions instead of pretending execution happened.
- Save external execution logs to `outputs/{run_id}/logs/run.log`.
- Do not install MATLAB, install toolboxes, or change global MCP configuration without explicit approval.

## Preferred MCP Tools

| Capability | Use |
| --- | --- |
| `detect_matlab_toolboxes` | Confirm MATLAB version and installed toolboxes. |
| `check_matlab_code` | Static Code Analyzer checks for `.m` files. |
| `run_matlab_file` | Run scripts or programs from files. Prefer this over long inline code. |
| `run_matlab_test_file` | Run MATLAB unit tests with structured results. |
| `evaluate_matlab_code` | Short diagnostics and quick variable/toolbox checks only. |

## Workflow

1. Inspect MATLAB files, README commands, project files, and toolbox references.
2. Read `references/INDEX.md`.
3. Determine whether MATLAB MCP tools are available.
4. If unavailable, report a plan and setup reference.
5. If available, include the exact MATLAB action in `plan.md` and wait for approval.
6. Execute only the approved action, capture logs, and summarize evidence.
7. Route failures to `failure_diagnosis_skill`.

## Codex MCP Setup Reference

The official MATLAB Agentic Toolkit recommends registering MATLAB MCP with Codex using:

```bash
codex mcp add matlab -- "<MCP_SERVER_PATH>" --matlab-root "<MATLAB_ROOT>" --matlab-display-mode "<DISPLAY_MODE>"
```

After registration, the MATLAB MCP server should have a longer timeout such as `tool_timeout_sec = 600` in the Codex config. Treat setup as a user-approved environment change, not an automatic reproduction step.

