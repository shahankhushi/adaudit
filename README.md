# adaudit

> **Zero-login ad account auditor that runs on CSV exports. Drop in a Meta or Google Ads export and get back wasted spend, creative fatigue, and a prioritized fix list in 5 seconds.**

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero OAuth](https://img.shields.io/badge/OAuth-None%20Required-brightgreen.svg)](#)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## The Problem: The Credentials Wall

Every performance marketing tool wants OAuth access, full admin rights, or live API tokens before doing anything. 

According to EMARKETER research, **52% of marketers do not control their company's API access**, and enterprise security teams take months to approve ad account permissions. Meanwhile, every media buyer and agency strategist has an ad export CSV sitting on their desktop right now.

`adaudit` has **no login, no OAuth, and no API keys**. You run it locally on your export. Your client's financial data never leaves your computer.

---

## 5-Second Quickstart

### 1. Install
```bash
pip install adaudit
```

### 2. Run Audit
```bash
adaudit analyze meta-export.csv --target-cpa 30
```

### 3. Instant Terminal Output

```markdown
# adaudit — Ad Account Audit Report
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

1. **Zero-Conversion Wasted Spend:** Identifies ads and ad sets that have burned $>2\times$ the target CPA without generating a single customer.
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
adaudit analyze meta-export.csv --json
```

---

## License
MIT © [Haider (@darimamhaider)](https://github.com/darimamhaider)
