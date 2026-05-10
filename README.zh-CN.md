# 计算数学科研代码复现与调参 Skills

本仓库是一个 Skill-first、Codex-native 的计算数学科研代码复现工作区。它为 coding agent 提供一组可阅读、可执行的 Skills，用来理解用户目标、检查科研代码仓库、规划最小复现、收集证据、提出修复、调参、生成图表，并写出紧凑总结。

第一阶段重点覆盖 Python 连续优化，尤其是 ADMM、proximal methods、primal-dual methods、PPA 和 augmented Lagrangian workflows。

## 工作方式

你用自然语言和 Codex 对话。Codex 读取 `skills/` 下的 Skill 文档，检查目标源码，写出紧凑计划，在关键步骤前请求确认，然后把证据记录到 `outputs/{run_id}/`。

端到端复现任务从 `skills/computational_math_reproduction_workflow_skill/SKILL.md` 开始。人类始终是审批节点的决策者；scripts 是 Codex 在需要时调用的小工具，用来让执行、日志、绘图或审批记录更容易验证。

## Codex-Native 用法

直接把目标告诉当前 coding agent。计算数学科研代码复现类端到端任务应先让 agent 使用 `computational_math_reproduction_workflow_skill`，再由它选择具体专项 Skill、查代码、搜索资料、总结证据，并在关键节点停下来确认。

示例 prompt：

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Search for an ADMM/LASSO Python implementation, reproduce the minimal serial demo,
and after it runs, optionally propose a small tuning plan.

Output policy:
- keep outputs compact;
- write plan.md before execution;
- write repair_plan.md only when source/dependency changes are needed;
- write RUN_SUMMARY.md at the end;
- put tuning artifacts under tuning/ only when tuning is approved;
- use scripts only as optional tools, not as the workflow driver.
```

其他常用 prompt：

```text
请分析我提供的本地路径或 Git 仓库，判断它是什么连续优化问题，
写出 plan.md 供我审核，先不要执行。
```

```text
请帮我搜索适合 LASSO / ADMM 任务的外部算法候选，
优先看论文、项目主页和 GitHub，实现证据讲清楚后让我选择。
```

```text
这个 demo 已经复现了，请提出 tuning/tuning_plan.md：
参数空间、预算、目标指标和约束都说明清楚，等我确认。
```

## Skills

- `computational_math_reproduction_workflow_skill`：本计算数学科研代码复现系统的默认入口，负责选择专项 Skill，并让 Codex 保持 operator 角色。
- `repo_reproduction_skill`：仓库分析、运行计划、复现执行、结果收集。
- `environment_deployment_skill`：环境部署方案、依赖识别和环境报告。
- `continuous_optimization_skill`：识别 ADMM、PPA、proximal gradient、primal-dual 等算法。
- `algorithm_discovery_skill`：搜索外部公开算法候选。
- `auto_tuning_skill`：生成调参计划，运行 grid/random search。
- `visualization_skill`：生成收敛曲线和调参图。
- `failure_diagnosis_skill`：分类运行失败并提出修复建议。
- `human_review_skill`：可选 checkpoint 和人工确认日志。
- `report_generation_skill`：生成 plan、复现、调参、失败和总结报告。

## 默认产物

紧凑默认工作流把产物写到 `outputs/{run_id}/`：

- 执行前写 `plan.md`；
- 只有需要源码或依赖修改时才写 `repair_plan.md`；
- 结束时写 `RUN_SUMMARY.md`；
- 只有提出调参时才写 `tuning/tuning_plan.md`；
- 只有调参被批准后才写 `tuning/tuning_results.csv`、`tuning/best_parameters.json`、`tuning/tuning.log`、`tuning/tuning_figures/` 和 `tuning/TUNING_SUMMARY.md`。

`outputs/{run_id}/checkpoints/` 下的 checkpoint 文件和 `outputs/{run_id}/approvals/` 下的 approval log 仍可作为可选的持久审核机制使用。

## 环境

本项目使用和 `/Users/conanxu/paper-to-skill` 相同的 Conda 环境：`ai4math`。

```bash
conda create -y -n ai4math python=3.13 pip
conda run -n ai4math python -m pip install -e ".[dev]"
```

更多说明见 `docs/environment.md`。

## 维护者测试

```bash
conda run -n ai4math pytest
```

Pytest 覆盖 helper tools。端到端复现行为通过 Codex smoke runs 验证。
