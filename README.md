# 📘 Quant Spec Document: Step Index 100 Sniper AI Bot (Hybrid Mode Enabled)

## Objective:

Design and implement a high-precision, rule-based trading bot that executes sniper Smart Money Concept (SMC) trades on **Step Index 100** to grow accounts aggressively, targeting **$1k → $3k per day**, and transitioning into a swing-trading mode to compound profits toward **$10k–$30k+ weekly**, all while using tight risk control and flawless execution.

---

## 🔁 Dual Mode Strategy

### 1. **Normal Day-Trade Mode**

- Short-term sniper trades (M15 time frame)
- $1k starting capital → $3k target via multiple high-RRR trades
- Tight stop-loss (5–15 pips)
- Up to 5 trades/day (max risk: 10–20% per trade)

### 2. **Hybrid Swing Mode (Runs in Parallel)**

- Bot continues day trading until a valid swing setup is found
- When swing trade is detected (H1/H4 confluence), bot enters it using profit only
- Once swing trade is placed, day trade engine pauses
- Swing trades target 300–1000+ pip moves with extended holding period

---

## 🧠 Strategy Overview

### ✅ Core Logic:

- Trade only when **all SMC conditions** are met:
    1. **Break of Structure (BOS)**
    2. **Valid Order Block (OB)**
    3. **Liquidity Sweep**
    4. **OB within 61.8–78.6% Fibonacci retracement**
    5. **Clean price structure above/below OB**
    6. **Impulse from OB caused BOS**

### ✅ Entry Type:

- **Sniper LIMIT order at OB wick**
- **Stop-loss (SL)**: 5–15 pips (day), 100–300 pips (swing)
- **Take-profit (TP)**: Minimum 1:3 RRR

---

## 🔍 Perfect OB Filter Module

### 🎯 Purpose:

Filter out weak or fake OBs. Only execute high-confluence sniper setups.

### ✅ Filter Scoring Logic (max score = 6):

- +1: OB caused a clean displacement
- +1: OB is unmitigated
- +1: Liquidity sweep occurred just before OB
- +1: OB aligns with Fib retracement zone (61.8–78.6%)
- +1: Clean structure around OB (no wick chaos)
- +1: OB impulse caused BOS

### 🧪 Acceptance Threshold:

- Only accept OBs with **score ≥ 5**

---

## 📈 Swing Trade Detection Logic (High Precision)

### 🔹 Requirements for Swing Trade Entry:

- Timeframe: 4H (structure), 1H/4H (entry logic)
- Confirmed BOS on 4H timeframe (major structural break)
- Identify last unmitigated OB that caused BOS
- OB must sit within 61.8–78.6% Fib retracement zone
- Liquidity must have been swept just before OB formation
- Clean price action and minimal traffic around OB zone
- Confluence score must be ≥ 5/6

### 🔹 Execution:

- Entry: Limit order at OB wick
- SL: Just outside OB sweep (100–300 pips)
- TP: Swing high/low or 1:3 to 1:6 RRR target (300–1000+ pips)
- Risk: Only use profit buffer from day trades (never principal)

---

## 🤖 Bot Execution Flow

### 🔹 Day Trade Mode

```
if detect_bos():
    ob = detect_order_block()
    if is_perfect_ob(ob, bos, candles, liquidity_zones, fib_zone):
        lot_size = calculate_lot_size(account_balance, sl)
        place_limit_order(entry, sl, tp, lot_size)
        monitor_trade()
        update_profit_tracker()
```

### 🔹 Swing Mode Scanner (Runs in Parallel)

```
if detect_bos(tf='H4'):
    ob = detect_order_block(tf='H4')
    if is_perfect_ob(ob, bos, candles_h4, liquidity_zones, fib_zone):
        lot = calculate_lot_size(day_profit_buffer, swing_sl)
        place_limit_order(entry, swing_sl, swing_tp, lot)
        pause_day_trading()
```

---

## 💸 Risk Management Rules

| Rule | Value |
| --- | --- |
| Per trade risk (Day) | 10–20% of current balance |
| SL size (Day) | 5–15 pips |
| TP ratio (Day) | Minimum 1:3 RRR |
| Max trades/day | 3–5 |
| Swing risk | Use only profit from Day mode |
| SL size (Swing) | 100–300 pips |
| TP ratio (Swing) | 1:3 – 1:6 |

---

## 📊 Trade Frequency Estimates

| Trade Type | Frequency |
| --- | --- |
| 100–300 pip sniper trade | 2–4 times daily |
| 300–500 pip swing trade | 1–3 times weekly |
| 500–1000 pip multi-leg trade | 1x per week |

---

## 🔐 Profit Allocation & Swing Trigger

- Bot tracks daily profit growth
- Continues day mode until high-confluence swing OB appears
- When swing setup detected:
    - Uses **profit buffer only** as capital (e.g., $3k)
    - Pauses day trades
    - Monitors swing trade until TP or SL is hit
    - Resets logic next session

---

## 🧱 Modules Required

### 1. **Market Scanner**

- Detect BOS, swing highs/lows, OB candidates on multiple TFs

### 2. **Perfect OB Filter**

- Score OB validity, reject weak setups

### 3. **Risk Engine**

- Auto-calculate lot sizes from SL + risk %

### 4. **Trade Engine**

- Place LIMIT orders with SL/TP logic for day + swing modes

### 5. **Performance Tracker**

- Track daily profits, monitor buffer, activate swing scan

---

## 🧠 Quant Notes:

- Use Python + MT5 SDK (or Deriv API)
- Separate `day_engine()` and `swing_engine()` modules
- Enable parallel monitoring of swing conditions
- Trade log should mark: `[type: day]` or `[type: swing]`

## 🔁 Learning & Optimization Module (Self-Training Logic)

### 🔹 Purpose:

Continuously improve entry accuracy, filter tuning, and SL/TP logic by learning from live and historical performance.

### 🔹 Core Features:

- **Trade Logger**: Save full trade context (TF, entry zone, SL/TP, confluence score, outcome)
- **Accuracy Monitor**: Calculate win rate, RRR, stop-out behavior per setup type
- **Filter Optimizer**: Adjust confluence thresholds based on win/loss streaks
- **OB Replay Evaluator**: Re-analyze all trades post-close to identify what changed between entry and exit

### 🔹 Future Extensions:

- Integrate LSTM or attention-based model to learn which confluence mixes produce the best results
- Enable semi-supervised fine-tuning of OB filters from large datasets
- Build heatmaps of successful OB zones and structure types

---

---

## 🏁 Final Notes:

This hybrid sniper bot runs **day mode continuously** until a valid swing trade is found. Once detected, it redirects profit into the swing setup and pauses intraday trades.

**Day builds margin → swing scales the gains.**

This approach maximizes trade frequency, efficiency, and capital scaling within 24/7 synthetic markets.

## Video:
https://youtu.be/wVqb9xmCOuk?si=g8-rs2Ro5_X7fHXb
