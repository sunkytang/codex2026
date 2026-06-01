---
name: txjcontract
description: Personal Binance USD-M futures trading playbook, analysis workflow, risk rules, and review system for the user. Use when discussing or analyzing futures trades, HYPE/BTC/DOGE/TURBO/PEPE/TRUMP watchlists, Binance contract entries/exits/stops, win-rate estimates, trade reports, automated futures reports, or updating the user's trade journal and lessons learned.
---

# TXJ Contract

## Core Rules

Use this skill as the user's personal futures trading operating manual. It is not a profit guarantee and must not override risk controls.

- Before futures analysis or live-order discussion, read the local Obsidian knowledge base when available:
  `C:\Users\sunky\Documents\Codex\TradingKnowledge\00_执行前必读\执行前检查清单.md`.
  Use it together with this skill and the latest live market/account data.
- Use Beijing time in conversation and reports. Binance/API timestamps may remain UTC internally.
- Never open, close, increase, cancel, or modify a live order without fresh explicit user confirmation.
- Treat every live order as mainnet unless clearly proven otherwise.
- Prefer small test size while the account is small. Default new trade sizing is about `5 USDT` margin, not `5 USDT` notional. At `2x` leverage this means about `10 USDT` notional unless the user explicitly asks for a different size.
- Always attach or verify a protective stop for any live position.
- If a trade closes, record it in the trade journal before continuing strategy discussion, then update this skill's review knowledge.
- Record every live order event, analysis decision, stop change, close, and review in the workspace journal/Excel when applicable, then sync the important lesson into this skill.
- Track the scaling ladder from `5U` margin toward `100U` margin. When the logged results meet the next upgrade condition, proactively remind the user before suggesting larger size.
- When BTC is strongly bearish on 15m/1h/4h, downgrade all long setups, even for strong coins.

## Standard Workflow

0. Read local knowledge first:
   - `C:\Users\sunky\Documents\Codex\TradingKnowledge\00_执行前必读\执行前检查清单.md`
   - relevant playbook notes under `C:\Users\sunky\Documents\Codex\TradingKnowledge\01_交易规则`
   - relevant symbol notes under `C:\Users\sunky\Documents\Codex\TradingKnowledge\02_币种剧本`
1. Check account state first:
   - nonzero positions
   - ordinary open orders
   - conditional/algo stop orders
2. Score the watchlist:
   - Fixed list: `BTCUSDT`, `HYPEUSDT`, `DOGEUSDT`, `TURBOUSDT`, plus Binance Life/币安人生 only if an official futures symbol is verified.
   - Hot meme list: scan active meme candidates. Report one current meme leader/dragon-one for focus, but keep the recent `3-5` meme candidates in a short comparison/watch table so a useful target is not lost just because the leaderboard rotates quickly.
3. Pull positioning and flow context for HYPE and any active trade candidate when Binance futures data is available:
   - global long/short account ratio
   - top trader long/short account ratio
   - top trader long/short position ratio
   - taker buy/sell volume ratio
4. Report:
   - price, 24h change, score 0-10
   - 15m/1h/4h trend and RSI
   - support/resistance
   - positioning/flow summary when meaningful
   - action judgment: immediate, wait, or forbidden
   - Do not clutter reports with weak meme candidates. Keep one best current meme candidate as the main focus, plus a compact retained watchlist of the recent `3-5` strongest meme candidates for continuity.
5. For a possible trade, state exact:
   - entry condition
   - entry price or trigger
   - stop/invalidation
   - target(s)
   - subjective win-rate estimate
   - main risk
6. If the user confirms, execute only the confirmed action and verify final state.
7. After a live order event, record the operation, reasoning, risk, stop, and current status in the journal/Excel when the local journal format supports it.
8. If a position closes, journal the result and update `references/reviews.md` with the new lesson.
9. If a repeated pattern emerges during discussion, add or refine a rule in this SKILL.md or `references/reviews.md`.

## Position Sizing And Scaling

Default sizing uses margin, not notional:

- Current default: about `5 USDT` margin per new test trade.
- At `2x` leverage, expected notional is about `10 USDT`.
- Special high-conviction tests may use up to `10 USDT` margin only after explicit confirmation.
- Always state margin, leverage, notional, quantity, stop distance, and estimated loss before or immediately after a confirmed trade.

Scaling ladder uses margin as the main unit. Leverage may be upgraded later, but it must lag behind evidence from the journal and never increase just because a few trades worked.

| Stage | Default Margin | Default Leverage | Upgrade Condition |
|---|---:|---:|---|
| Test | `5U` | `2x` | Current stage. Build clean execution and complete records. |
| Small upgrade | `10U` | `2x` | At least `20-30` logged trades, net PnL positive, max losing streak no more than `3`, no repeated execution mistakes. |
| Medium test | `20-30U` | `2x-3x` | At least `50` logged trades, win rate about `55%+`, average win / average loss at least `1.2`, drawdown controlled. |
| Pre-100U | `50U` | `3x` | At least `80-100` logged trades, stable equity curve, two weeks of disciplined execution. |
| Full target | `100U` | `3x-5x max` | At least `100` logged trades, win rate about `58%-62%+`, average win / average loss at least `1.2`, max losing streak and drawdown acceptable. |

Do not upgrade size or leverage based on one or two good trades. Upgrade only after journal statistics support it, and remind the user when a milestone is reached. If both margin and leverage are upgraded, total notional and stop-loss USDT risk increase multiplicatively, so report the new expected loss before any confirmed trade.

## HYPE Playbook

HYPE is treated as the priority strong coin, but it often does fake breakouts, washes late longs, then resumes. Do not chase one-minute candles.

Use these rules:

- Do not short HYPE just because BTC is weak unless HYPE also breaks structure and fails a retest.
- A HYPE long during BTC 15m/1h/4h strong-down requires two-step confirmation:
  1. 5m candle reclaims the key level.
  2. Either price reclaims the next confirmation level or retests the reclaimed level without breaking.
- A single 5m reclaim is not enough after repeated stop-outs.
- After a stop-out, avoid immediate revenge re-entry. Wait for a new structure.
- Prefer:
  - breakout and retest holds
  - deep pullback with volume stop
  - BTC no longer accelerating down
- Avoid:
  - chasing a 1m pump
  - buying the middle of a range
  - buying after a fake breakout unless retest proves support

Important learned levels from the current campaign:

- `62.80`: reclaim/watch level, not sufficient alone in weak BTC conditions.
- `63.10`: higher-quality confirmation level after reclaim.
- `63.34-63.60`: breakout/previous pressure area.
- `61.44-61.98`: pullback/structure support zone from recent data.

Refresh levels from live Binance data every time; do not blindly reuse stale levels.

## Meme Playbook

Meme trades can move fast and then pull back violently. Treat them as momentum trades with strict re-entry discipline.

- A first breakout/reclaim trade can be valid when meme momentum, volume, and BTC environment agree.
- If a meme winner rises quickly, expect a normal pullback. Do not move the stop directly into the active 1m pullback zone just because the position is green.
- Protect meme winners in stages:
  1. first near break-even or entry-plus-fees
  2. then below a confirmed 5m higher-low, VWAP/reclaim area, or other structure that has actually held
- If stopped out of a meme winner, do not immediately buy back from regret. Require a fresh setup:
  - 1m/3m reclaim EMA and hold
  - or a key level such as `0.000558` for the current MEME campaign is reclaimed and holds
  - or a stronger reclaim such as `0.000565` then a successful retest
- A low-volume pause after a stop-out is not enough. Weak rebound plus mixed 1m/3m/5m structure means wait.

Current MEME lesson:

- First MEME trade was acceptable; the mistake was moving the stop up too fast after a rapid pump and getting washed out by normal pullback.
- Second MEME trade was too fast, not cautious enough, and too optimistic; it treated a weak rebound after the first stop-out as a true re-strengthening.
- 2026-06-01 MEME momentum test confirmed a broader rule for all strong coins and hot meme trades: do not buy the late part of a vertical move just because 1m/5m keeps rising. After a breakout, require a pullback-hold or a fresh micro-structure unless using an explicitly smaller momentum test. When BTC is weak and long positioning is crowded, downgrade chase entries even if the symbol is the meme leader.

## BTC Filter

BTC is the market filter.

- BTC 15m/1h/4h strong-down: do not chase alt longs; require two-step confirmation.
- BTC short setups should usually be taken on failed retests, not at stretched lows.
- If BTC is near 15m RSI oversold after a sharp drop, do not chase short without a retest.

## Positioning And Flow Filter

Use Binance futures positioning and flow data as an emotion/crowding filter, not as a standalone trading signal.

Prefer these data points when available:

- Global long/short account ratio: broad account-side crowding.
- Top trader long/short account ratio: whether large-account counts lean long or short.
- Top trader long/short position ratio: whether large-account position size leans long or short.
- Taker buy/sell volume ratio: whether recent aggressive flow is buying or selling.

Interpretation guide:

- Price up while account ratios lean short: possible short fuel; supports long setups if structure confirms.
- Price down while account ratios lean long: crowded longs may be trapped; downgrade longs.
- Top trader positions long while account counts are short: larger size may be supporting the trend, but still require price confirmation.
- Taker buy volume rises but price cannot advance: overhead supply; downgrade chase longs.
- Taker sell volume rises but price holds support: absorption; upgrade confirmed bounce/reclaim setups.
- Extreme one-sided positioning increases liquidation and wick risk; widen structural invalidation or wait for retest.

Do not open, close, or modify trades only because positioning data looks bullish or bearish.

## Stop And Profit Management

- Initial stop must sit beyond the setup invalidation, not at a random round number.
- Floating profit protection is mandatory. A position that has moved meaningfully in favor must be managed as a live asset, not left with only the original stop.
- If a position reaches about `1.5R` unrealized profit or breaks out then stalls, move protection:
  1. first to break-even or near break-even
  2. then to the prior 5m low or below the confirmed breakout level
- For small HYPE test size, if unrealized profit reaches about `0.05 USDT` while BTC remains 15m/1h/4h strong-down, immediately evaluate moving the stop up to protect structure, usually near `63.10-63.20` or the latest valid 5m higher-low.
- Do not let a meaningful winner fully round-trip because the stop stayed at break-even.
- If stop execution slips, record the actual exit price and lesson.

## Win-Rate Estimate

Use subjective win-rate only as a decision aid. It is not a measured probability until enough logged trades exist.

Current heuristic:

```text
base 40
+ trend alignment
+ 5m/15m structure confirmation
+ relative strength vs BTC and watchlist
+ liquidity/volume/hot narrative
+ positioning/flow support when it agrees with price structure
- BTC environment risk
- fake-breakout history
- poor entry location
- stop too tight or too wide
- crowded positioning against the trade
= subjective win-rate
```

When reporting a win-rate, state it is subjective unless backed by journal statistics.

## Trade Journal

Use the workspace journal files when available:

- `trade_journal.csv`
- `trade_journal.md`
- `trade_journal.xlsx`
- `src/trade_journal.py`
- `src/export_trade_journal_xlsx.py`

On every closed trade, record:

- operation time
- symbol, side, size
- margin, leverage, notional when known
- entry, exit, stop
- gross PnL, costs, net PnL
- core conclusion
- success/failure reason
- next rule to avoid repeating the error

On every active trade event, record or preserve enough context to later review:

- pre-trade analysis and subjective win-rate
- entry reason and trigger
- confirmed order details
- stop placement or stop modification reason
- market context at the time

If a local Python lacks `openpyxl`, use the Codex bundled Python runtime if available, or tell the user Excel export could not be refreshed.

## Skill Memory Update

Maintain this skill as the living operating manual. Do not wait for the user to ask.

After every meaningful trading event, update both the journal and the skill memory:

- Closed trade: append to journal files, export Excel, then add a concise lesson to `references/reviews.md`.
- Important new rule or durable lesson: also update the local Obsidian vault under
  `C:\Users\sunky\Documents\Codex\TradingKnowledge`.
- New repeated mistake: add a hard rule or warning in the relevant section.
- New effective behavior: add it as a positive pattern.
- New risk rule: add it to `Core Rules`, `BTC Filter`, `HYPE Playbook`, or `Stop And Profit Management`.
- New reporting requirement: update `references/report-template.md`.

Keep skill updates concise. Do not store secrets, API keys, webhook URLs, or raw private account payloads in this skill.

Use `scripts/sync_reviews_from_journal.py` when the journal has changed and `references/reviews.md` should be regenerated from `trade_journal.csv`.

## References

- Read `references/reviews.md` for the current campaign's closed-trade lessons.
- Read `references/report-template.md` when producing a complex futures report.
- Use `scripts/journal_summary.py` to summarize the journal when a numeric performance snapshot is needed.
- Use `scripts/sync_reviews_from_journal.py` to refresh skill review memory from the workspace journal.
