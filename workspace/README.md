# Binance Futures Trading Lab

一个默认安全的币安 U 本位合约交易实验框架。第一版只启用公共行情和纸面交易，用来讨论、验证和复盘策略，不会直接下真实订单。

## 当前能力

- 读取 Binance USD-M Futures 公共行情和 K 线
- 使用 EMA + RSI 的示例策略生成 `LONG` / `SHORT` / `FLAT`
- 根据账户规模、单笔风险和止损距离计算仓位
- 纸面交易执行、止损、止盈、日志记录
- 默认 `paper` 模式；`live` 模式入口暂时锁定

## 快速开始

```powershell
python -m src.bot --config config.example.json --once
```

循环运行：

```powershell
python -m src.bot --config config.example.json
```

## 建议的 100U 初始设置

- 交易对：`BTCUSDT`
- 周期：`15m`
- 杠杆：`1x` 到 `3x`
- 单笔风险：账户 `1%`，也就是 100U 亏损上限约 1U
- 每天最多少量交易，没有信号就空仓

## 安全说明

- 不要把 API key 写进代码或提交到版本库
- 实盘 key 不要开提现权限
- 先跑测试网或纸面交易
- 合约高风险，任何策略都可能亏损

