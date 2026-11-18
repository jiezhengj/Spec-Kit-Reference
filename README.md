# 仓库用途

本仓库维护 GitHub Spec Kit 的中文政策和操作参考。下游项目的流程与组件来自官方 CLI、目录和项目内 `.agents/skills` 技能；本仓库不提供目标项目运行时组件。

新项目初始化由个人全局规则引导。初始化后，目标项目提交的根目录 `AGENTS.md` 规则块和 Spec Kit 状态构成项目基线；后续工作不依赖个人全局规则或本仓库。

# 查找文档

按使用阶段查看[文档索引](SPEC_KIT_REFERENCE.md)：新项目初始化 Agent 只在首次接入时读取初始化步骤和项目规则模板；目标项目后续会话不依赖本仓库。其他流程摘要是本仓库维护者或读者的参考资料，不是目标项目 Agent 的运行时文档。

# 仓库维护

- [全局政策来源](GLOBAL_POLICY.md)由用户人工部署；[人工更新说明](docs/GLOBAL_POLICY_DEPLOYMENT.md)记录部署步骤。
- 仓库维护规则见根目录 `AGENTS.md`；上游依赖处理规则见[上游依赖兼容性规则](docs/UPSTREAM_UPDATE_POLICY.md)。
- `scripts/check_cli_contract.py` 和每月运行的 GitHub Actions 校验官方 CLI 输出契约；本仓库不逐提交跟踪上游，文档使用 CLI 版本锚点。
