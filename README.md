# adaudit

> **Zero-login ad account auditor that runs on CSV exports. Drop in a Meta or Google Ads export and get back wasted spend, creative fatigue, and a prioritized fix list in 5 seconds.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero OAuth](https://img.shields.io/badge/OAuth-None%20Required-brightgreen.svg)](#)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## The Problem: The Credentials Wall

Most performance marketing SaaS platforms demand OAuth access, admin permissions, or live API credentials before doing anything. 

In agency and multi-client environments, clients are often hesitant to grant third-party apps direct access to their ad accounts, and enterprise security approvals can take weeks. Meanwhile, media buyers and strategists have ad account CSV exports sitting on their desktop.

`adaudit` has **no login, no OAuth, and no API keys**. It parses standard CSV exports locally in your terminal. Your client's financial and ad account data never leaves your computer.

---

## 5-Second Quickstart

### 1. Install from Source
```bash
git clone https://github.com/darhaiderimam/adaudit.git
cd adaudit
pip install .
```

### 2. Run Audit
```bash
adaudit analyze examples/sample_meta_export.csv --target-cpa 30
```
*(Or run directly without installation: `python -m adaudit.cli analyze examples/sample_meta_export.csv --target-cpa 30`)*

### 3. Instant Terminal Output *(Synthetic Sample Data)*

```markdown
# adaudit — Ad Account Audit Report
*(Synthetic sample demonstration output)*

**Account Health Score:** `62/100` | **Total Analyzed Spend:** `$22,800.00`

> **IMMEDIATE RECOVERABLE CASH:** `$4,950.00` (21.7% of total spend)

## 1. High-Level Performance Metrics
| Metric | Value |
| :--- | :--- |
| **Total Ad Spend** | `$22,800.00` |
| **Total Conversions** | `605` |
| **Blended Account CPA** | `$37.69` |
| **Target CPA Benchmark** | `$30.00` |
| **Wasted Spend (0 Conversions)** | `$4,950.00` |

## 2. Top Zero-Conversion Wasted Spend Leaks
| Campaign | Ad / Asset Name | Spend Wasted | Clicks | Impressions | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TOF_BROAD_US | AD_02_LOSING_LIFESTYLE | `$3,100.00` | 900 | 180,000 | **PAUSE IMMEDIATELY** |
| TOF_BROAD_US | AD_03_DEAD_ANIMATION | `$1,850.00` | 475 | 95,000 | **PAUSE IMMEDIATELY** |

## 3. Creative Fatigue Warnings (High Frequency + Low CTR)
| Campaign | Ad Name | Spend | Frequency | CTR | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| MOF_RETARGET_30D | AD_04_FATIGUED_REVIEW | `$5,200.00` | `4.60` | `0.70%` | **REFRESH CREATIVE** |

## 4. Top Scale Opportunities (Proven Winners)
| Campaign | Ad Name | Spend | Conversions | CPA | ROAS | Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TOF_BROAD_US | AD_01_WINNING_HOOK_A | `$8,450.00` | 340 | `$24.85` | `3.02x` | **SCALE +20% BUDGET** |
| BOF_CATALOG_SALES | AD_05_DPA_CAROUSEL | `$4,200.00` | 190 | `$22.11` | `3.39x` | **SCALE +20% BUDGET** |

## 5. Prioritized 24-Hour Action Plan
1. **Pause the top zero-conversion ads** listed in Section 2 to immediately stop cash bleed.
2. **Refresh fatigued assets** in Section 3 with 3 new hook variations.
3. **Reallocate recovered dollars ($4,950.00)** into top scaling winners.
```

---

## What `adaudit` Detects

1. **Zero-Conversion Wasted Spend:** Identifies ads and ad sets that have spent $>2\times$ the target CPA without generating a single customer.
2. **Creative Fatigue Decay:** Flags ads where frequency exceeds 3.2 and CTR has decayed below 1.0%, indicating audience burnout.
3. **High-CPA Bleeders:** Detects campaigns generating purchases at $>1.5\times$ target CPA, eroding contribution margin.
4. **Scale Candidates:** Isolates winning assets with CPA $<0.85\times$ target benchmark ready for budget expansion.
5. **Naming Convention & UTM Hygiene:** Catches ads missing standard campaign tagging delimiters.

---

## Supported File Formats
- Meta Ads Manager raw CSV exports (`Columns: Performance and Clicks`)
- Google Ads Campaign and Ad Group CSV reports
- Custom CSVs containing standard columns (`Spend`, `Impressions`, `Clicks`, `Conversions`, `Revenue`)

---

## Machine-Readable Output (JSON)
For automated agent workflows:
```bash
adaudit analyze examples/sample_meta_export.csv --json
```

---

## License
MIT © [Imam Haider (@darhaiderimam)](https://github.com/darhaiderimam) • [LinkedIn](https://www.linkedin.com/in/darhaiderimam)
