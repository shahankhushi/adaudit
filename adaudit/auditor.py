import csv
import re
from typing import Dict, Any, List

def clean_float(val: Any) -> float:
    if val is None:
        return 0.0
    s = str(val).strip().replace("$", "").replace(",", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return 0.0

class AdRow:
    def __init__(self, campaign: str, ad_set: str, ad_name: str, spend: float, impressions: int, clicks: int, conversions: int, revenue: float, frequency: float, ctr: float):
        self.campaign = campaign
        self.ad_set = ad_set
        self.ad_name = ad_name
        self.spend = spend
        self.impressions = impressions
        self.clicks = clicks
        self.conversions = conversions
        self.revenue = revenue
        self.frequency = frequency
        self.ctr = ctr
        self.cpa = (spend / conversions) if conversions > 0 else 0.0
        self.roas = (revenue / spend) if spend > 0 else 0.0

def parse_csv_export(file_path: str) -> List[AdRow]:
    rows = []
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Map column names dynamically
            campaign = r.get("Campaign Name") or r.get("Campaign") or r.get("campaign") or "Unknown Campaign"
            ad_set = r.get("Ad Set Name") or r.get("Ad Group") or r.get("ad_set") or "Unknown Group"
            ad_name = r.get("Ad Name") or r.get("Ad") or r.get("Keyword") or r.get("ad_name") or "Unknown Ad"
            
            spend = clean_float(r.get("Amount Spent (USD)") or r.get("Amount Spent") or r.get("Spend") or r.get("Cost") or 0)
            impressions = int(clean_float(r.get("Impressions") or 0))
            clicks = int(clean_float(r.get("Clicks (All)") or r.get("Clicks") or r.get("Link Clicks") or 0))
            conversions = int(clean_float(r.get("Purchases") or r.get("Conversions") or r.get("Results") or 0))
            revenue = clean_float(r.get("Purchases Conversion Value") or r.get("Conversion Value") or r.get("Total Conversion Value") or 0)
            frequency = clean_float(r.get("Frequency") or 1.0)
            ctr = clean_float(r.get("CTR (All)") or r.get("CTR") or (clicks / impressions * 100 if impressions > 0 else 0))

            if spend > 0 or impressions > 0:
                rows.append(AdRow(
                    campaign=campaign,
                    ad_set=ad_set,
                    ad_name=ad_name,
                    spend=spend,
                    impressions=impressions,
                    clicks=clicks,
                    conversions=conversions,
                    revenue=revenue,
                    frequency=frequency,
                    ctr=ctr
                ))
    return rows

def audit_account(rows: List[AdRow], target_cpa: float = None) -> Dict[str, Any]:
    total_spend = sum(r.spend for r in rows)
    total_conversions = sum(r.conversions for r in rows)
    total_revenue = sum(r.revenue for r in rows)
    blended_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0.0
    effective_target_cpa = target_cpa if target_cpa and target_cpa > 0 else (blended_cpa if blended_cpa > 0 else 30.0)

    # 1. Wasted Spend: Ads that spent > $50 with ZERO conversions
    wasted_ads = [r for r in rows if r.conversions == 0 and r.spend >= 50.0]
    total_wasted_spend = sum(r.spend for r in wasted_ads)

    # 2. Creative Fatigue: Frequency > 3.2 and CTR < 1.0% with spend > $100
    fatigued_ads = [r for r in rows if r.frequency >= 3.2 and r.ctr < 1.0 and r.spend >= 100.0]
    fatigue_spend = sum(r.spend for r in fatigued_ads)

    # 3. High CPA Bleeders: Conversions > 0, but CPA > 1.5x target_cpa and spend > $100
    bleeder_ads = [r for r in rows if r.conversions > 0 and r.cpa > (1.5 * effective_target_cpa) and r.spend >= 100.0]
    bleeder_spend = sum(r.spend for r in bleeder_ads)

    # 4. Naming Convention Breaks (missing standard delimiters like '_' or lack of funnel stage prefix)
    naming_breaks = [r for r in rows if "_" not in r.campaign and not any(tag in r.campaign.upper() for tag in ["TOF", "MOF", "BOF", "COLD", "RETARGET", "BRAND"])]

    # 5. Top Scaling Winners: CPA <= 0.85 * target_cpa and spend > $150
    winners = [r for r in rows if r.conversions > 0 and r.cpa <= (0.85 * effective_target_cpa) and r.spend >= 150.0]
    winners = sorted(winners, key=lambda x: x.conversions, reverse=True)

    # Health score (0-100)
    waste_ratio = (total_wasted_spend / total_spend) if total_spend > 0 else 0.0
    health_score = max(10, min(100, int(100 - (waste_ratio * 150) - (len(fatigued_ads) * 5))))

    return {
        "summary": {
            "total_spend": total_spend,
            "total_conversions": total_conversions,
            "total_revenue": total_revenue,
            "blended_cpa": blended_cpa,
            "target_cpa": effective_target_cpa,
            "health_score": health_score,
            "total_wasted_spend": total_wasted_spend,
            "waste_percentage": (total_wasted_spend / total_spend * 100) if total_spend > 0 else 0.0
        },
        "wasted_ads": wasted_ads,
        "fatigued_ads": fatigued_ads,
        "bleeder_ads": bleeder_ads,
        "naming_breaks": naming_breaks,
        "top_winners": winners
    }

def render_audit_markdown(audit: Dict[str, Any]) -> str:
    s = audit["summary"]
    md = []
    md.append("# adaudit — Ad Account Audit Report")
    md.append(f"**Account Health Score:** `{s['health_score']}/100` | **Total Analyzed Spend:** `${s['total_spend']:,.2f}`\n")
    md.append(f"> **IMMEDIATE RECOVERABLE CASH:** `${s['total_wasted_spend']:,.2f}` ({s['waste_percentage']:.1f}% of total spend)\n")

    md.append("## 1. High-Level Performance Metrics")
    md.append("| Metric | Value |")
    md.append("| :--- | :--- |")
    md.append(f"| **Total Ad Spend** | `${s['total_spend']:,.2f}` |")
    md.append(f"| **Total Conversions** | `{s['total_conversions']:,}` |")
    md.append(f"| **Blended Account CPA** | `${s['blended_cpa']:,.2f}` |")
    md.append(f"| **Target CPA Benchmark** | `${s['target_cpa']:,.2f}` |")
    md.append(f"| **Wasted Spend (0 Conversions)** | `${s['total_wasted_spend']:,.2f}` |")

    # Wasted spend table
    if audit["wasted_ads"]:
        md.append("\n## 2. Top Zero-Conversion Wasted Spend Leaks")
        md.append("| Campaign | Ad / Asset Name | Spend Wasted | Clicks | Impressions | Action |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for ad in sorted(audit["wasted_ads"], key=lambda x: x.spend, reverse=True)[:5]:
            md.append(f"| {ad.campaign[:25]} | {ad.ad_name[:30]} | `${ad.spend:,.2f}` | {ad.clicks} | {ad.impressions:,} | **PAUSE IMMEDIATELY** |")

    # Fatigued ads
    if audit["fatigued_ads"]:
        md.append("\n## 3. Creative Fatigue Warnings (High Frequency + Low CTR)")
        md.append("| Campaign | Ad Name | Spend | Frequency | CTR | Action |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for ad in audit["fatigued_ads"][:5]:
            md.append(f"| {ad.campaign[:25]} | {ad.ad_name[:30]} | `${ad.spend:,.2f}` | `{ad.frequency:.2f}` | `{ad.ctr:.2f}%` | **REFRESH CREATIVE** |")

    # Winners
    if audit["top_winners"]:
        md.append("\n## 4. Top Scale Opportunities (Proven Winners)")
        md.append("| Campaign | Ad Name | Spend | Conversions | CPA | ROAS | Action |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for ad in audit["top_winners"][:5]:
            md.append(f"| {ad.campaign[:25]} | {ad.ad_name[:30]} | `${ad.spend:,.2f}` | {ad.conversions} | `${ad.cpa:,.2f}` | `{ad.roas:.2f}x` | **SCALE +20% BUDGET** |")

    md.append("\n## 5. Prioritized 24-Hour Action Plan")
    md.append("1. **Pause the top zero-conversion ads** listed in Section 2 to immediately stop cash bleed.")
    md.append("2. **Refresh fatigued assets** in Section 3 with 3 new hook variations.")
    md.append(f"3. **Reallocate recovered dollars (${s['total_wasted_spend']:,.2f})** into top scaling winners.")

    return "\n".join(md)
