# TXJ Contract Git Backup

这是合约交易系统的本地 Git 备份目录。

包含：

- `TradingKnowledge/`：Obsidian 本地知识库，保存规则、剧本、复盘和指标方法。
- `workspace/`：交易工作区中的脚本、交易日志、Excel 和示例配置。
- `skills/txjcontract/`：Codex 使用的合约交易 skill。

不包含：

- `.env`
- Binance API key / secret
- 微信机器人 webhook
- 虚拟环境、缓存、运行状态

换电脑时：

1. 新电脑安装 Git、Obsidian、Codex。
2. 克隆这个仓库。
3. 用 Obsidian 打开 `TradingKnowledge/`。
4. 把 `skills/txjcontract/` 放回 Codex skills 目录。
5. 在新电脑重新创建 `.env`，不要把密钥提交到 Git。

