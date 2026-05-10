---
name: algorithm-discovery-skill
description: This skill should be used when the user asks to search for external algorithms, find related implementations, discover alternative approaches, or look up papers and code for computational math optimization methods.
version: 0.1.0
---

# Algorithm Discovery Skill

Searches external sources (arXiv, GitHub) for algorithm implementations relevant to a given task.

For end-to-end computational math research-code reproduction workflows, this Skill should be selected by `computational_math_reproduction_workflow_skill` rather than used as the first entrypoint.

## Script

### external_search
Input: `--task <task.yaml>`, `--out <path>`, `--sources <arxiv,github>`, `--max-results <n>`

Output: `algorithm_candidates.json` with ranked candidates

```bash
python -m skills.algorithm_discovery_skill.scripts.external_search --task task.yaml --out /path/to/output --sources arxiv,github --max-results 5
```

## Workflow

1. Prepare a `task.yaml` with domain information
2. Run `external_search` to discover candidates
3. Present ranked candidates to user
4. User selects which candidates to pursue further
