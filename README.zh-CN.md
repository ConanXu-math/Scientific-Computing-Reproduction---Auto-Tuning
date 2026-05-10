# 计算数学科研代码复现与调参 Skills

本仓库提供一组给 coding agent 使用的 Skills，用来辅助计算数学科研代码的自动复现、自动部署、自动调参、可视化分析和报告生成。Codex 是主要参考 operator，但这些 workflow artifacts 设计上面向通用 coding agent。

当前 MVP 重点覆盖 Python 连续优化。

### 开源给公众用时，真正要依赖什么

**使用者侧接口**就是 `skills/` 里的 **Skills**（端到端从 `computational_math_reproduction_workflow_skill` 进入）。你在对话里说明任务；agent 按 Skill 路由、检查点和可选脚本执行；**待复现代码由你提供**（本地路径、克隆地址、压缩包等），并对高风险步骤做人工确认。  
`tests/`、`tests/fixtures/` 仅服务于**维护者跑 CI/回归**，**不是**使用本系统的必要组成部分，也不应写进「用户必须照做的流程」。

## 怎么使用

你不需要记命令。直接把目标告诉当前使用的 coding agent。计算数学科研代码复现类端到端任务应先让 agent 使用 `computational_math_reproduction_workflow_skill`，再由它选择具体专项 Skill、查代码、搜索资料、总结证据，并在关键节点停下来确认。

示例：

```text
请分析我提供的代码路径或 Git 仓库，判断它是什么连续优化问题，
给我一个可审核的运行计划，先不要执行。
```

```text
请帮我搜索适合 LASSO / ADMM 任务的外部算法候选，
优先看论文、项目主页和 GitHub，实现证据讲清楚后让我选择。
```

```text
这个 demo 已经复现了，请提出调参计划：
参数空间、预算、目标指标和约束都说明清楚，等我确认。
```

## 全流程交互测试 Prompt

如果想测试完整的 search-first conversation workflow，可以在本仓库里开启一个新的 agent 会话，然后发送下面这段 prompt：

```text
请使用 computational_math_reproduction_workflow_skill 作为入口。
把这次任务当作 coding-agent Skill protocol 的全流程 smoke test。

搜索主题：用于 LASSO / sparse linear regression 的 ADMM 或相近 splitting methods，
领域是 continuous optimization。
Run id：outputs/full_workflow_search_first_admm_lasso

目标：
1. 把任务理解为 search-first 的计算数学代码复现流程，识别问题类型、
   算法族、预期指标和复现目标。
2. 写入 task-understanding checkpoint，然后停下来等我决策。
3. 我 approve 后，从公开来源搜索外部算法候选，包括论文、项目主页和
   GitHub 仓库。优先选择有可运行 Python 代码、优化指标清楚、且和
   ADMM / LASSO 匹配度高的候选。
4. 对候选进行排序，列出 source URL、匹配证据、代码可用性、可能入口和风险。
   写入 algorithm-match checkpoint，然后停下来等我决策。
5. 我 approve 某个候选后，只 fetch 或 inspect 已批准的 source。
   如果没有足够安全的外部候选，就停下来向我要一个可用于 smoke 的本地路径，
   或等我补充路径；不要假设本仓库里自带 demo 目录。
6. 分析已选择仓库或 fallback source 的代码和环境。
7. 提出 run plan，列出候选命令、理由、风险等级、timeout 和预期输出。
   写入 run-plan checkpoint，然后停下来等我决策。
8. 我 approve 后，只执行已批准的低风险 run，使用 ai4math 环境，
   并把日志保存在 run 目录下。
9. 如果运行成功，提出一个适合 smoke test 的小预算 tuning plan。
   写入 tuning-plan checkpoint，然后停下来等我决策。
10. 我 approve 后，执行已批准的 tuning，生成可用图表或摘要，
    并起草 final review checkpoint。
11. 在接受最终结论前停下来，问我 approve、revise、reject 或 skip。

请遵守 agent-neutral workflow contract：
- 维护 workflow_state.json；
- 使用 pending_checkpoint 和 pending_user_decision；
- 把 approval 记录到 approvals/approval_log.jsonl；
- 把可复查证据保存在 outputs/full_workflow_search_first_admm_lasso/；
- 不执行高风险命令；
- 不修改源码或依赖。
```

之后在每个 checkpoint 回复：

```text
approve
```

或者：

```text
revise: <需要修改什么>
reject: <拒绝原因>
skip: <为什么跳过这个可选阶段>
```

完成 smoke test 后，预期能在 `outputs/full_workflow_search_first_admm_lasso/` 下看到 `workflow_state.json`、checkpoint Markdown、`approvals/approval_log.jsonl`、搜索/发现记录、执行日志和 final-review 材料。

Agent 应该在这些节点停下来：

- 任务理解是否正确。
- 运行计划是否可以执行。
- 是否允许安装或修改依赖。
- 是否允许创建 adapter、wrapper 或修改源码。
- 失败修复是否安全。
- 调参目标和预算是否合理。
- 外部算法候选是否值得复现。
- 最终结论是否可以接受。

正常交互里，agent 不应该直接跳到执行。它应该先说清楚：

```text
我将使用 repo_reproduction_skill 和 human_review_skill。
我已经生成运行计划，请你回复 approve / revise / reject / skip。
```

只有记录 approval 后，执行工具才应该继续运行。项目中的 `executor.py` 支持 approval gate，agent 在真实复现时应使用 `--require-approval run_plan`。

## Skills

- `computational_math_reproduction_workflow_skill`：本计算数学科研代码复现系统的开源用户默认入口，负责选择专项 Skill、维护 `workflow_state.json`、执行人机 checkpoint。
- `repo_reproduction_skill`：仓库分析、运行计划、复现执行、结果收集。
- `environment_deployment_skill`：环境部署方案、依赖识别和环境报告。
- `continuous_optimization_skill`：识别 ADMM、PPA、proximal gradient、primal-dual 等算法。
- `algorithm_discovery_skill`：搜索外部公开算法候选。
- `auto_tuning_skill`：生成调参计划，运行 grid/random search。
- `visualization_skill`：生成收敛曲线、调参曲线和可视化报告。
- `failure_diagnosis_skill`：分类运行失败并提出修复建议。
- `human_review_skill`：生成 checkpoint 和记录人工确认。
- `report_generation_skill`：生成环境、复现、调参、失败和最终报告。

## Checkpoints

运行过程中可能生成这些审核文件：

- `01_task_understanding.md`
- `02_run_plan_review.md`
- `03_failure_fix_review.md`
- `04_tuning_plan_review.md`
- `05_final_review.md`
- `06_algorithm_match_review.md`

这些文件保存在 `outputs/{run_id}/checkpoints/`。人工决策记录保存在：

```text
outputs/{run_id}/approvals/approval_log.jsonl
```

跨 Skill 的流程状态保存在：

```text
outputs/{run_id}/workflow_state.json
```

## 环境

本项目使用和 `/Users/conanxu/paper-to-skill` 相同的 Conda 环境：`ai4math`。

```bash
conda create -y -n ai4math python=3.13 pip
conda run -n ai4math python -m pip install -e ".[dev]"
```

更多说明见 `docs/environment.md`。

## 可选命令

批处理 CLI（`computational_math_skills.cli`）可选；**以 Skills + 对话为主的流程通常不必跑这些**。

`--task` 指向**你自己写的 YAML**（领域、指标、调参空间等）。仅为 **CI/维护者** 提供一份字段示例：`tests/fixtures/tasks/admm_tuning_task.yaml`，可复制改编；**正常使用不依赖该路径**。

生成分析和 checkpoint，然后暂停：

```bash
conda run -n ai4math python -m computational_math_skills.cli run \
  --task path/to/my_task.yaml \
  --out outputs/run_001
```

结构化外部算法搜索：

```bash
conda run -n ai4math python -m computational_math_skills.cli discover-algorithms \
  --task path/to/my_task.yaml \
  --out outputs/run_001 \
  --sources arxiv,github \
  --max-results 5
```

若任务 YAML 支持 demo 自动运行：

```bash
conda run -n ai4math python -m computational_math_skills.cli run \
  --task path/to/my_task.yaml \
  --out outputs/run_demo \
  --demo-auto-run
```

## 维护者：测试用 fixtures（最终用户可忽略）

以下内容仅用于 **`pytest` / 仓库内回归**，**不构成**对外发布时的使用前提。

ADMM（LASSO 形式）：

```bash
conda run -n ai4math python tests/fixtures/minimal_admm_lasso/main.py \
  --rho 1.0 \
  --tol 1e-5 \
  --max-iter 500 \
  --seed 0
```

PPA（强凸二次）：

```bash
conda run -n ai4math python tests/fixtures/minimal_ppa_quadratic/main.py \
  --proximal-parameter 1.0 \
  --max-iter 500 \
  --seed 0
```

## 输出

复现和调参完成后，`outputs/{run_id}/` 下会保存：

- `environment_report.md`
- `reproduce_report.md`
- `tuning_report.md`
- `failure_analysis.md`
- `final_summary.md`
- `visualization_report.md`
- `figures/`
- `run_log.txt`
- `tuning_results.csv`

## 安全规则

- 不执行 `sudo`、`rm -rf`、`curl | bash`、`wget | bash`。
- 不读取用户 home 目录中的敏感文件。
- 不打印 token、password、API key。
- 不修改用户全局 Python 环境。
- 所有外部命令必须设置 timeout。
- 高风险步骤必须人工确认。
- 外部仓库执行前必须有 `run_plan` approval；依赖安装、adapter、源码修改需要在对话中单独说明。

## 测试（维护者）

```bash
conda run -n ai4math pytest
```

最终用户开箱可用的是 **Skills**，不依赖在本仓库执行测试。
