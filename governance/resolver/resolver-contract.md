# Resolver contract

Resolver 只使用 Python 标准库和当前项目 runtime。允许解析的 integration CLI 机器输出只有 `specify integration status --json`；不得解析 Rich list/search/info、导入私有 API、扫描磁盘或创建临时项目查询 registry。

身份声明优先级为：当前用户 key、宿主 runtime metadata、显式环境变量、Agent 自声明。任意冲突返回 `IDENTITY_CONFLICT`；只有 display name 返回 `KEY_REQUIRED`。安装健康不等于 runtime 匹配；fresh-session binding 验证后才是 `EXACT_NATIVE_INSTALLED`。
