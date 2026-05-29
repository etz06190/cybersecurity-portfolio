# KQL Cookbook

Reusable KQL queries organized by purpose. Each entry includes the query, what it does, and any caveats.

The goal: by Week 13, this contains 80-100+ queries representing fluency across Sentinel tables, KQL operators, and threat hunting patterns.

## Conventions

- Queries are commented at the top with purpose, intended table(s), and any prerequisites
- Time windows use `ago()` or `between()` rather than hard-coded dates
- Each query should be runnable copy-paste in the Sentinel Logs blade
- Examples that depend on lab-specific data (e.g., Pi-hole logs) note the prerequisite

## Organization

Queries grouped by primary operator or pattern, in roughly the order they appear in learning:

1. **Basics** — where, project, summarize, count
2. **Time** — ago, between, bin, render timechart
3. **Joins and unions** — join, union, let
4. **Parsing** — extend, parse, parse_json
5. **Aggregations** — make_set, dcount, percentile
6. **Hunting patterns** — anomaly detection, threshold deviations
7. **Cross-table** — multi-source correlation

---

## 1. Basics

### Q1: Recent Azure activity, last hour

Quick sanity check that data is flowing.

```kql
AzureActivity
| where TimeGenerated > ago(1h)
| project TimeGenerated, OperationNameValue, Caller, ResourceGroup
| limit 50
```

### Q2: Failed sign-ins in the last 24 hours

Aggregate failures by user to spot brute force attempts.

```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != 0
| summarize attempts = count() by UserPrincipalName, ResultDescription
| order by attempts desc
```

---

## 2. Time

### Q3: Activity volume over time, hourly buckets

Visualize event volume to spot anomalies.

```kql
AzureActivity
| where TimeGenerated > ago(24h)
| summarize events = count() by bin(TimeGenerated, 1h)
| render timechart
```

---

## 3. Joins and Unions

### Q4: Events per data source across the workspace

Useful for inventorying what's actually being collected.

```kql
union withsource=Source *
| where TimeGenerated > ago(1h)
| summarize count() by Source
| order by count_ desc
```

---

## Notes

- More queries added daily during Phase 1 KQL practice
- Counter at top of Week N entries in study log tracks total query count
- Target: 20+ queries by end of Week 2, 30+ by end of Week 3, 80-100+ by end of Phase 1
