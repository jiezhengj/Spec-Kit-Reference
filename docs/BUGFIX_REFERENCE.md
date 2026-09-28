> 阅读对象：本仓库维护者或希望了解官方 Bug Fix 流程的读者。这是中文参考摘要，不会安装到目标项目；目标项目 Agent 依项目 `AGENTS.md` 和已安装的官方技能执行，不需要读取 Reference。

# 适用范围

已有行为不符合预期时使用官方 Bug Fix 流程。它独立于 Feature SDD，不要求先运行 Constitution、specify 或 plan。尚未初始化的项目先按[新项目初始化说明](PROJECT_INITIALIZATION.md)接入 Spec Kit；初始化后按 assess → fix → test 顺序逐步调用技能，并审阅每阶段结果。

# 安装扩展

在已初始化的目标项目中，如果 `bug` 扩展缺失，先按该项目的 `AGENTS.md` 询问是否安装；获准后在项目根目录运行：

~~~bash
specify extension add bug
~~~

通过官方 CLI 安装官方扩展。当前 CLI 若随包提供 `bug`，会优先使用该副本；否则按 CLI 的官方目录解析结果安装。以下命令采用 GitHub Copilot 的技能写法；其他 Agent 使用原生集成提供的对应调用方式。

# Assess：诊断问题

提供症状、复现步骤和预期行为，可附 Issue 或堆栈信息。使用一个简短、可复用的 slug：

~~~text
/speckit-bug-assess "<症状、复现步骤和预期行为>" slug=<bug-slug>
~~~

技能调查代码并写入 `.specify/bugs/<bug-slug>/assessment.md`，不修改源代码。先审阅诊断和建议修复范围；证据不支持诊断或问题并非缺陷时，不进入 fix。

# Fix：修复已评估原因

沿用同一 slug：

~~~text
/speckit-bug-fix slug=<bug-slug>
~~~

技能按已审阅诊断实施修复，并写入 `fix.md`。这是流程中唯一修改源代码的阶段；若新证据要求扩大范围，先记录偏差并交由用户审阅。

# Test：验证修复

沿用同一 slug：

~~~text
/speckit-bug-test slug=<bug-slug>
~~~

技能重新执行原始复现和相关验证，并写入 `test.md`。此阶段记录证据，不修改源代码来修复失败验证。

| 结果 | 含义 | 下一步 |
| --- | --- | --- |
| `verified` | 原始复现和要求的验证均已成功执行 | 审阅补丁和验证记录 |
| `partial` | 部分验证因环境或证据不足无法完成 | 补足环境或复现证据后重新验证 |
| `failed` | 验证发现问题仍存在 | 根据证据回到诊断或修复，再运行 Test |

仅测试套件通过、但没有重新执行原始复现，不足以证明缺陷已修复。

# 上游依据

本页依据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 `docs/guides/bugfix.md` 和 `src/specify_cli/extensions/command_add.py` 整理。
