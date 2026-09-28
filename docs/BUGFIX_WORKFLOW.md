# 缺陷修复流程

已知行为出错时使用本流程。它独立于功能 SDD，不需要先运行 Constitution、specify 或 plan。Agent 每次单独运行一个官方技能，审阅结果后再继续。

# 安装官方扩展

在已初始化项目的根目录运行：

~~~bash
specify extension add bug
~~~

扩展从官方 Spec Kit 目录安装。后续由官方 CLI 更新；不要从本地路径安装同名扩展。

以下技能名采用官方 Copilot 示例。其他 Agent 使用其原生集成提供的等价技能名称和调用方式。

# 1. Assess：诊断问题

提供症状、复现步骤和预期行为，并选一个简短、可复用的 slug。Issue 描述或堆栈信息也可作为线索。

~~~text
/speckit-bug-assess "<症状、复现步骤和预期行为>" slug=<bug-slug>
~~~

Agent 调查代码并写入 .specify/bugs/<bug-slug>/assessment.md，不修改源代码。审阅原因分析和建议修复范围。若证据不支持该诊断，或问题并非缺陷，先停止，不进入 fix。

# 2. Fix：修复已评估原因

沿用完全相同的 slug：

~~~text
/speckit-bug-fix slug=<bug-slug>
~~~

Agent 按已审阅的诊断实施修复，并写入 .specify/bugs/<bug-slug>/fix.md。这是本流程中唯一修改源代码的阶段。如果新证据要求超出已评估范围，先记录偏差，不要悄悄扩大修复。

# 3. Test：验证修复

沿用相同的 slug：

~~~text
/speckit-bug-test slug=<bug-slug>
~~~

Agent 重新执行原始复现和相关测试，并写入 .specify/bugs/<bug-slug>/test.md。此阶段记录证据，不修改源代码来修复失败测试。

| 结果 | 含义 | 下一步 |
| --- | --- | --- |
| verified | 原始复现和要求的验证均已实际成功执行 | 审阅补丁和验证记录 |
| partial | 部分验证因环境或证据不足而无法完成 | 补足环境或复现证据后重新验证 |
| failed | 验证发现问题仍然存在 | 根据证据回到诊断或修复，再运行 Test |

只通过测试套件但没有重新执行原始复现，不足以证明缺陷已修复。

# 上游依据

本页根据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 docs/guides/bugfix.md 整理，校订日期为 2026-09-28。
