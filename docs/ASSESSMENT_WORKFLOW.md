# 想法评估流程

当用户还没有决定是否值得投入某个想法时，可选用此流程。它适用于软件和非软件决策，不要求先有源代码。评估本身不实现功能，也不会自动转入 SDD。

# 安装官方扩展

在已初始化项目的根目录运行：

~~~bash
specify extension add assess
~~~

扩展从官方 Spec Kit 目录安装。以下技能名采用官方 Copilot 示例；其他 Agent 使用其原生集成提供的等价调用方式。Agent 在对话中逐个调用技能，审阅每个阶段产物后再继续。

# 五个阶段

对同一个想法使用同一个 slug。

## 1. Intake：记录想法

~~~text
/speckit-assess-intake "<想法>" slug=<idea-slug>
~~~

记录用户输入，保存在 .specify/assessments/<idea-slug>/intake.md。

## 2. Research：研究证据

~~~text
/speckit-assess-research slug=<idea-slug>
~~~

在 research.md 中记录支持和反对的证据。核对来源和置信度；未引用的假设不作为已确认事实。

## 3. Define：定义问题

~~~text
/speckit-assess-define slug=<idea-slug>
~~~

在 problem.md 中描述受影响用户、问题、目标、非目标、成功指标和不采取行动的代价。

## 4. Shape：比较方向

~~~text
/speckit-assess-shape slug=<idea-slug>
~~~

在 concept.md 中比较概念选项、限制、投入程度和取舍。此阶段不做详细架构、不拆实现任务、不改源代码。

## 5. Decide：记录决定

~~~text
/speckit-assess-decide slug=<idea-slug>
~~~

在 decision.md 中记录评分、理由和结果：

| 结果 | 含义 | 下一步 |
| --- | --- | --- |
| go | 证据足以支持推荐的概念 | 用户决定是否将软件想法交给 SDD |
| needs-clarification | 有明确未知事项阻碍决定 | 补充受影响的材料，再审阅后续评分和决定 |
| kill | 当前不值得继续 | 保留决定理由；停止本身是有效结果 |

五个阶段只记录评估材料，不修改源代码。评估独立运行；go 不会自动启动 specify。用户决定继续后，将 decision.md 中的交接摘要交给功能流程的 specify 阶段。

# 修改已有评估材料

材料标出待澄清项时，只补充相关事实并更新受影响的下游结论。不要自动重跑整个阶段或覆盖已有草稿；先让 Agent 判断新增证据是否改变结论。

# 上游依据

本页根据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 docs/guides/assessment.md 整理，校订日期为 2026-09-28。
