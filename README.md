# Product Retention & Cohort Analysis

**Role this showcases:** Product Analyst / Growth Analyst / Data Analyst

A complete cohort retention analysis on 3,000+ simulated user events across 18 months. This project demonstrates end-to-end product analytics capabilities — from data generation to actionable A/B test recommendations.

---

## Business Questions

1. What is 7-day and 30-day retention — and is it improving over time?
2. Which signup cohort has the best lifetime value (LTV)?
3. Which acquisition channel retains users best?
4. Does completing onboarding actually improve long-term retention?

---

## Approach

This analysis uses synthetic user event data spanning January 2023 to September 2024. I built an N×N cohort retention matrix tracking user activity month-over-month, then layered on revenue analysis to compute LTV per cohort. The key insight comes from comparing retention curves across acquisition channels and onboarding completion status — identifying the highest-leverage intervention for the product team.

---

## Key Insights

1. **Retention is improving**: Cohorts from January 2024 onward show 8-12% higher 30-day retention, suggesting recent product improvements are working.

2. **Onboarding completion drives +81% retention lift**: Users who complete onboarding have 38% 30-day retention vs. 21% for those who skip it — the strongest predictor of long-term engagement.

3. **Referral channel has 2.1x better LTV than paid social**: Organic and referral channels both retain better than paid acquisition, with referral users generating $89 average LTV vs. $42 for paid social.

4. **Pro plan users rarely churn**: Pro users show 65% 30-day retention compared to 35% for free users, confirming the value of conversion-focused initiatives.

---

## Recommended Experiments

### 1. Onboarding Progress Bar
**Hypothesis:** Adding a visible progress indicator during onboarding will increase completion rate by 15-20%.  
**Metric:** Onboarding completion rate → 30-day retention  
**Expected Impact:** If completion improves by 20%, expect 30-day retention to lift from 28% to ~33% (+5pp)

### 2. Referral Incentive Program
**Hypothesis:** Offering existing users a credit for each successful referral will shift acquisition mix toward higher-LTV users.  
**Metric:** % of new users from referral channel → blended LTV  
**Expected Impact:** Each 10% shift from paid social to referral improves blended LTV by ~$4.70 per user

### 3. Day-7 Re-engagement Email
**Hypothesis:** A personalized email at day 7 highlighting unused features will prevent early churn.  
**Metric:** Day-7 retention rate  
**Expected Impact:** Industry benchmarks suggest 5-10% relative improvement in day-7 retention; if achieved, expect downstream 30-day retention lift of 3-4pp

---

## How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Generate user events data
python data/generate_user_events.py

# Step 3: Run the analysis
jupyter notebook notebooks/cohort_retention.ipynb

# Step 4: View charts
open charts/
```

---

## Project Structure

```
cohort-retention-analysis/
├── data/
│   ├── generate_user_events.py    # Data generation script
│   └── user_events.csv            # Generated dataset (3,000+ rows)
├── notebooks/
│   └── cohort_retention.ipynb     # Complete analysis notebook
├── charts/
│   ├── cohort_heatmap.png         # Retention matrix visualization
│   ├── retention_curve.png        # Survival curves by cohort
│   └── ltv_by_cohort.png          # LTV comparison chart
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

---

## Skills Demonstrated

| Skill | Evidence |
|-------|----------|
| **Cohort Analysis** | N×N retention matrix construction, cohort assignment logic |
| **LTV Modeling** | Cumulative revenue per user per cohort, monetization analysis |
| **Product Thinking** | Onboarding impact analysis, A/B test recommendations with hypothesis/expected lift |
| **Python / Pandas** | pivot_table, date math, groupby operations, data validation |
| **Seaborn / Matplotlib** | Annotated heatmaps, multi-line retention curves, bar charts |
| **Statistical Intuition** | Retention benchmarks, delta comparisons, correlation analysis |
| **Business Communication** | PM-ready insights, experiment proposals, narrative structure |

---

## Sample Output

### Cohort Retention Heatmap
The heatmap shows retention % for each signup cohort over time. Reading down a column reveals whether retention is improving (later cohorts retain better).

### Retention Curves
Line chart comparing the first 6 cohorts, with vertical markers at Day 7 and Day 30 — the standard product health benchmarks.

### LTV by Cohort
Bar chart revealing which signup periods produced the most valuable users, with cohort-level recommendations.

---

## How I Would Present This to a PM

1. **Start with the bottom line:** "30-day retention is improving — up 8-12% since January 2024 — but onboarding completion remains our biggest lever."

2. **Show the heatmap:** "This chart tells the story. Later cohorts (darker blue) retain better than early ones, especially at Month 1 and 2."

3. **Introduce the experiment:** "Users who complete onboarding have 81% better retention. If we improve onboarding completion by 20%, we expect 30-day retention to jump 5 percentage points."

4. **Address acquisition:** "Referral users are worth 2x paid social users. We should test a referral incentive to shift our acquisition mix."

5. **Close with next steps:** "I recommend we prioritize the onboarding progress bar test this sprint — highest confidence, highest impact, easiest to implement."

---

## Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | string | Unique user identifier |
| `registration_date` | date | When the user signed up |
| `event_date` | date | When this event happened |
| `event_type` | string | signup / onboarding_complete / first_purchase / return_visit / upgrade / churn |
| `revenue` | float | Non-zero on first_purchase and upgrade only |
| `plan_type` | string | free / starter / pro |
| `acquisition_channel` | string | organic / paid_social / referral |

---

*Built for portfolio demonstration. Data is synthetic but patterns reflect real SaaS benchmarks.*