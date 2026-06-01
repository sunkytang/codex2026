# 合约交易复盘表

规则：每一笔合约结束后都追加一行，并补充复盘。盈利不等于好交易，亏损也不等于坏交易；重点看是否符合计划、风险是否受控、下次能不能规避同类错误。

## 总表

| 编号 | 操作时间(北京时间) | 币种 | 方向 | 数量 | 入场 | 平仓/止损 | 结果 | 净PnL(USDT) | 账户影响 | 评分 | 核心结论 | 成功/失败原因 | 下次规则 |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---|---|---|
| T001 | 开仓 2026-05-28 22:55:33；平仓 2026-05-29 00:18:24 | HYPEUSDT | SHORT | 0.17 | 57.30 | 58.00 | 失败但风控合格 | -0.1254 | 约 -0.63% | 6/10 | 亏钱但流程合格：小仓、止损、退出都正确；主要问题是方向和入场确认不够 | 保护止损正确，亏损很小；但逆强势币过早做空，缺少确认的跌破/反抽失败 | 强势币优先找回踩多；若做空，必须等 15m 转弱、跌破关键位后反抽失败，并最好有 BTC 同向配合 |

| T002 | 开仓 2026-05-29 11:25:03；平仓 2026-05-29 11:31:05 | HYPEUSDT | LONG | 0.17 | 62.012 | 61.673 / 止损 61.70 | 失败但风控合格 | -0.06814322 | 约 -0.34% | 7/10 | 方向判断有逻辑，HYPE 确实修复并冲上 62；但入场点偏追，止损距离太近，62 上方未站稳就回落，属于突破确认不足的小亏试错。 | 成功点：等待 HYPE 站回 61.50 后才考虑多，保护止损提前挂好，亏损受控。失败点：在 62.0 附近追入，未等回踩 61.85-61.90 守住后再上，且止损 61.70 被正常波动扫掉。 | 突破单必须等 5m 收在关键位上方并回踩不破；若追高，止损不能贴得太近，或等 61.85-61.90 回踩确认后再入。 |

| T003 | 开仓 2026-05-29 16:28:53；平仓 2026-05-29 16:46:10 | HYPEUSDT | LONG | 0.17 | 63.139 | 62.770 / 止损 62.78 | 失败但风控有效 | -0.07343226 | 约 -0.37% | 5/10 | HYPE大方向仍强，但这笔是冲高回落后的反抽试多，入场没有等5m重新站稳63.10/63.20，也没有突破63.34确认。 | 失败原因是把1m拉回当作5m修复，前一根5m已从63.341回落到62.879，假突破后买盘并不稳；止损放在62.78使亏损可控。 | HYPE后续只做两类单：5m收上63.34且回踩不破的突破单，或回踩62.45-62.60放量止跌后的低吸单；不再在63附近来回拉扯时追。 |

| T004 | 开仓 2026-05-29 14:18:08；平仓 2026-05-29 18:24:11 | TURBOUSDT | LONG | 8000 | 0.0010761 | 0.0010752 / 止损 0.0010766 | 失败但保本管理有效 | -0.01528930 | 约 -0.08% | 7/10 | TURBO方向一度正确，最高浮盈超过0.24U，后续按计划把止损从原始风险位上移到保本附近，最终回落触发保护，亏损主要来自手续费和轻微滑点。 | 成功点是及时把亏损风险降到接近零，避免从浮盈单变成大亏；失败点是没有在放量冲高后进一步上移止损锁定利润，导致盈利回吐。 | 以后浮盈达到1.5R或突破后不能继续站稳时，止损分两步上移：先到保本，再到前一根5m低点或关键突破位下方，避免盈利单完全回吐。 |

| T005 | 开仓 2026-05-29 21:59:10；平仓 2026-05-29 22:07:09 | HYPEUSDT | LONG | 0.17 | 62.878 | 62.424 / 止损 62.50 | 失败但风控执行 | -0.08783067 | 约 -0.44% | 5/10 | HYPE 5m 确实收回 62.80 上方，但没有继续站稳，BTC 仍三周期强空，导致强币修复试多很快失败。 | 失败原因是把一次5m收回62.80当作足够确认，但下一步没有等63.10确认；同时BTC持续走弱，HYPE被大盘拖回，止损触发且成交滑到62.424。 | 以后HYPE在BTC三周期强空时，多单必须等两步确认：先5m收回关键位，再站稳63.10或回踩62.80不破；仅一根5m收回不再开试单。 |

| T006 | 开仓 2026-05-29 22:16:40；平仓 2026-05-29 22:25:39 | HYPEUSDT | LONG | 0.17 | 63.450 | 62.908 / 止损 62.95 | 失败但风控执行 | -0.10288043 | 约 -0.52% | 6/10 | HYPE完成两步确认后突破追多，一度浮盈约0.05U，但BTC三周期强空继续加速下跌，HYPE未能守住入场区，最终触发保护止损。 | 失败原因不是没有确认，而是确认后没有在浮盈接近目标区时及时上移止损；同时BTC环境过弱，突破追随单抗不住大盘下压。 | BTC三周期强空时，HYPE突破多如果浮盈达到0.05U或接近第一目标但未突破63.96，必须主动上移保护到63.10-63.20或至少减少回撤，不能让浮盈单回到原始止损。 |

| T007 | 开仓 2026-05-30 09:32:33；平仓 2026-05-30 12:07:01 | HYPEUSDT | LONG | 0.17 | 65.640 | 64.697 / 止损 64.84 | LOSS | -0.17155311 | small test loss; stop slipped below trigger | 45 | HYPE remained a strong 1h/4h coin, but BTC rolled from recovery into three-cycle weakness; entry near resistance without later reclaim failed. | Failed because 66.04 was never reclaimed, 65.64 entry was not regained, BTC turned down, and the protective stop slipped from 64.84 trigger to 64.697 execution. | After a stop, do not immediately re-enter. For HYPE longs, require BTC not in 15m/1h/4h strong-down and require reclaim of entry/confirmation level or deep support absorption before a new trade. |

| T008 | 开仓 2026-05-30 22:15:47；平仓 2026-05-30 22:43:05 | MEMEUSDT | LONG | 9200 | 0.0005520 | 0.0005570 / 止损 0.000558 | PROFIT_PROTECTED_TOO_TIGHT | 0.04089860 | small profit; protected winner | 7/10 | MEME direction and momentum selection were correct; small 5U chase caught the strongest meme move, but protective stop was moved too close after a sharp spike and closed the trade before giving the trend enough room. | Successful because entry followed reclaim/strength and risk was small; imperfect because after MEME expanded quickly, stop was raised from 0.000542 to 0.000558 inside normal meme pullback range, causing early exit at 0.000557 while the broader momentum had not clearly failed. | For fast meme winners, protect profit in two stages: first to break-even/entry-plus-fees, then trail below the last confirmed 5m higher-low or below VWAP/reclaim zone; do not move stop directly into the active 1m pullback zone unless choosing to scalp out. |

| T009 | 开仓 2026-05-30 23:03:26；平仓 2026-05-30 23:09:07 | MEMEUSDT | LONG | 9200 | 0.0005578 | 0.0005439 / 止损 0.000545 | LOSS_STOPPED | -0.13294781 | 2x杠杆，约5.13U名义仓位，约2.56U保证金；按新规则以后默认约5U保证金，本笔仍属旧口径小仓 | 53 | MEME大周期仍强，但二次上车点只是在回落后的弱反抽，1m/3m/5m没有重新转强，量能不足，入场后很快跌破止损。 | 失败原因是把0.000545-0.000555区间的短暂停顿当成稳住，未等0.000558/0.000565重新站稳；止损本身执行了风险控制，但成交滑到0.0005439。 | MEME被洗出后再上车必须等1m/3m收回EMA且站稳0.000558，或站上0.000565后回踩不破；弱反抽和低量混合结构不再立刻追。 |

| T014 | 开仓 2026-05-31 20:57:05；平仓 2026-05-31 22:02:36 | 1000PEPEUSDT | LONG | 2900 | 0.0034415 | 0.0034190 / 止损 0.003420 | 失败止损 | -0.07519771 | 2x杠杆 约9.98U名义仓位 约4.99U保证金 小仓meme试单止损退出 | 5/10 | 1000PEPE作为当时meme候选龙一 15m/1h结构较强 但入场后没有站稳0.003445 反而回落触发保护止损 | 失败原因是突破确认不够扎实 多头账户拥挤且taker卖压切换明显 入场后未能快速打到第一目标 说明这笔属于试单失败而非策略大错 | 热点meme小试可以做 但已有卖压警告时必须等0.003445真正站稳或回踩确认；止损后不立刻追回 除非重新站回关键位并形成新结构 |

## 单笔复盘

### T001 HYPEUSDT SHORT

- 计划：限价做空 HYPE，止损 58.00。
- 执行：入场后保护止损成功挂上，触发后退出，没有扩大亏损。
- 做对的地方：流程走通；实盘订单、成交、止损、复盘完整；单笔亏损控制在小范围。
- 做错的地方：HYPE 当时相对强势，做空属于逆强势币；入场确认偏早，没有等明确反转结构。
- 下次规则：强势币优先找回踩多，不优先摸顶空；如果要空，必须满足“15m 跌破关键支撑 + 反抽失败 + 大盘不强”。

### T002 HYPEUSDT LONG

- 结果：失败但风控合格，净PnL -0.06814322 USDT。
- 核心结论：方向判断有逻辑，HYPE 确实修复并冲上 62；但入场点偏追，止损距离太近，62 上方未站稳就回落，属于突破确认不足的小亏试错。
- 成功/失败原因：成功点：等待 HYPE 站回 61.50 后才考虑多，保护止损提前挂好，亏损受控。失败点：在 62.0 附近追入，未等回踩 61.85-61.90 守住后再上，且止损 61.70 被正常波动扫掉。
- 下次规避：突破单必须等 5m 收在关键位上方并回踩不破；若追高，止损不能贴得太近，或等 61.85-61.90 回踩确认后再入。

### T003 HYPEUSDT LONG

- 结果：失败但风控有效，净PnL -0.07343226 USDT。
- 核心结论：HYPE大方向仍强，但这笔是冲高回落后的反抽试多，入场没有等5m重新站稳63.10/63.20，也没有突破63.34确认。
- 成功/失败原因：失败原因是把1m拉回当作5m修复，前一根5m已从63.341回落到62.879，假突破后买盘并不稳；止损放在62.78使亏损可控。
- 下次规避：HYPE后续只做两类单：5m收上63.34且回踩不破的突破单，或回踩62.45-62.60放量止跌后的低吸单；不再在63附近来回拉扯时追。

### T004 TURBOUSDT LONG

- 结果：失败但保本管理有效，净PnL -0.01528930 USDT。
- 核心结论：TURBO方向一度正确，最高浮盈超过0.24U，后续按计划把止损从原始风险位上移到保本附近，最终回落触发保护，亏损主要来自手续费和轻微滑点。
- 成功/失败原因：成功点是及时把亏损风险降到接近零，避免从浮盈单变成大亏；失败点是没有在放量冲高后进一步上移止损锁定利润，导致盈利回吐。
- 下次规避：以后浮盈达到1.5R或突破后不能继续站稳时，止损分两步上移：先到保本，再到前一根5m低点或关键突破位下方，避免盈利单完全回吐。

### T005 HYPEUSDT LONG

- 结果：失败但风控执行，净PnL -0.08783067 USDT。
- 核心结论：HYPE 5m 确实收回 62.80 上方，但没有继续站稳，BTC 仍三周期强空，导致强币修复试多很快失败。
- 成功/失败原因：失败原因是把一次5m收回62.80当作足够确认，但下一步没有等63.10确认；同时BTC持续走弱，HYPE被大盘拖回，止损触发且成交滑到62.424。
- 下次规避：以后HYPE在BTC三周期强空时，多单必须等两步确认：先5m收回关键位，再站稳63.10或回踩62.80不破；仅一根5m收回不再开试单。

### T006 HYPEUSDT LONG

- 结果：失败但风控执行，净PnL -0.10288043 USDT。
- 核心结论：HYPE完成两步确认后突破追多，一度浮盈约0.05U，但BTC三周期强空继续加速下跌，HYPE未能守住入场区，最终触发保护止损。
- 成功/失败原因：失败原因不是没有确认，而是确认后没有在浮盈接近目标区时及时上移止损；同时BTC环境过弱，突破追随单抗不住大盘下压。
- 下次规避：BTC三周期强空时，HYPE突破多如果浮盈达到0.05U或接近第一目标但未突破63.96，必须主动上移保护到63.10-63.20或至少减少回撤，不能让浮盈单回到原始止损。

### T007 HYPEUSDT LONG

- 结果：LOSS，净PnL -0.17155311 USDT。
- 核心结论：HYPE remained a strong 1h/4h coin, but BTC rolled from recovery into three-cycle weakness; entry near resistance without later reclaim failed.
- 成功/失败原因：Failed because 66.04 was never reclaimed, 65.64 entry was not regained, BTC turned down, and the protective stop slipped from 64.84 trigger to 64.697 execution.
- 下次规避：After a stop, do not immediately re-enter. For HYPE longs, require BTC not in 15m/1h/4h strong-down and require reclaim of entry/confirmation level or deep support absorption before a new trade.

### T008 MEMEUSDT LONG

- 结果：PROFIT_PROTECTED_TOO_TIGHT，净PnL 0.04089860 USDT。
- 核心结论：MEME direction and momentum selection were correct; small 5U chase caught the strongest meme move, but protective stop was moved too close after a sharp spike and closed the trade before giving the trend enough room.
- 成功/失败原因：Successful because entry followed reclaim/strength and risk was small; imperfect because after MEME expanded quickly, stop was raised from 0.000542 to 0.000558 inside normal meme pullback range, causing early exit at 0.000557 while the broader momentum had not clearly failed.
- 下次规避：For fast meme winners, protect profit in two stages: first to break-even/entry-plus-fees, then trail below the last confirmed 5m higher-low or below VWAP/reclaim zone; do not move stop directly into the active 1m pullback zone unless choosing to scalp out.

### T009 MEMEUSDT LONG

- 结果：LOSS_STOPPED，净PnL -0.13294781 USDT。
- 核心结论：MEME大周期仍强，但二次上车点只是在回落后的弱反抽，1m/3m/5m没有重新转强，量能不足，入场后很快跌破止损。
- 成功/失败原因：失败原因是把0.000545-0.000555区间的短暂停顿当成稳住，未等0.000558/0.000565重新站稳；止损本身执行了风险控制，但成交滑到0.0005439。
- 下次规避：MEME被洗出后再上车必须等1m/3m收回EMA且站稳0.000558，或站上0.000565后回踩不破；弱反抽和低量混合结构不再立刻追。

### T014 1000PEPEUSDT LONG

- 结果：失败止损，净PnL -0.07519771 USDT。
- 核心结论：1000PEPE作为当时meme候选龙一 15m/1h结构较强 但入场后没有站稳0.003445 反而回落触发保护止损
- 成功/失败原因：失败原因是突破确认不够扎实 多头账户拥挤且taker卖压切换明显 入场后未能快速打到第一目标 说明这笔属于试单失败而非策略大错
- 下次规避：热点meme小试可以做 但已有卖压警告时必须等0.003445真正站稳或回踩确认；止损后不立刻追回 除非重新站回关键位并形成新结构
