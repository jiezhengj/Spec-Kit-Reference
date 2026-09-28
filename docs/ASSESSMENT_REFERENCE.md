> 阅读对象：本仓库维护者或希望了解官方 Assessment 流程的读者。这是中文参考摘要，不会安装到目标项目；目标项目 Agent 依项目 `AGENTS.md` 和已安装的官方技能执行，不需要读取 Reference。

# 适用范围

用户尚未决定一个想法是否值得投入时，可选官方 Assessment。它适用于软件和非软件想法，不要求已有源代码，也不实现功能或自动启动 Feature SDD。

# 安装扩展

Assessment 材料保存在已初始化的 Spec Kit 项目中。若当前项目尚未初始化，先为评估材料选择合适的项目，再按[新项目初始化说明](PROJECT_INITIALIZATION.md)建立 Spec Kit 项目。项目缺少 `assess` 扩展时，先按项目 `AGENTS.md` 询问是否安装；获准后在项目根目录运行：

~~~bash
specify extension add assess
~~~

通过官方 CLI 安装官方扩展。当前 CLI 若随包提供 `assess`，会优先使用该副本；否则按 CLI 的官方目录解析结果安装。

以下命令采用 GitHub Copilot 的技能写法；其他 Agent 使用原生集成提供的对应调用方式。对同一想法沿用同一 slug，逐阶段调用并审阅产物。

# Intake：记录想法

~~~text
/speckit-assess-intake "<想法>" slug=<idea-slug>
~~~

记录用户输入到 `.specify/assessments/<idea-slug>/intake.md`。也可提供 URL、工单或代码库位置作为线索。

# Research：研究证据

~~~text
/speckit-assess-research slug=<idea-slug>
~~~

在 `research.md` 中记录支持与反对的证据。核对来源和置信度；没有来源支持的假设不能视为已证实。

# Define：定义问题

~~~text
/speckit-assess-define slug=<idea-slug>
~~~

在 `problem.md` 中描述受影响用户、问题、目标、非目标、成功指标和不采取行动的代价。

# Shape：比较方向

~~~text
/speckit-assess-shape slug=<idea-slug>
~~~

在 `concept.md` 中比较概念选项、约束、投入程度和取舍。本阶段不做详细架构、不拆实现任务、不改源代码。

# Decide：记录决定

~~~text
/speckit-assess-decide slug=<idea-slug>
~~~

在 `decision.md` 中记录评分、理由和结果：

| 结果 | 含义 | 下一步 |
| --- | --- | --- |
| `go` | 证据支持推荐的概念 | 用户决定是否把软件想法交给 Feature SDD |
| `needs-clarification` | 未知事项阻碍决定 | 补充证据，再审阅评分和决定 |
| `kill` | 当前不值得继续 | 保留理由并停止；这是有效结果 |

# 上游依据

本页依据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 `docs/guides/assessment.md` 和 `src/specify_cli/extensions/command_add.py` 整理。
