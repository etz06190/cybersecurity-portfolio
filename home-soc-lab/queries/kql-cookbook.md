# KQL Cookbook

Reusable KQL queries with notes on what each one teaches.

The goal: by Week 13, this contains 80-100+ queries representing fluency across Sentinel tables, KQL operators, and threat hunting patterns.

## Conventions

- Queries are commented at the top with purpose and any prerequisites
- Time windows use `ago()` or `between()` rather than hard-coded dates where possible
- Each query is runnable copy-paste in the Sentinel Logs blade or Azure Data Explorer
- Sandbox queries (against `StormEvents`, `PopulationData`, etc.) note that they require the `help/Samples` cluster context

## Organization

Queries grouped by primary operator or pattern, in roughly learning order:

1. **Basics** — `take`, `project`, `where`, `project-away`
2. **Time** — `ago`, `between`, `bin`, `render timechart`
3. **String operations** — `has`, `contains`, `startswith`, `endswith`
4. **Aggregations** — `summarize`, `count`, `dcount`, `make_set`
5. **Joins and unions** — `join`, `union`, `let`
6. **Parsing** — `extend`, `parse`, `parse_json`
7. **Real data queries** — against `AzureActivity` in `law-homesoc`

---

## 1. Basics

### Q1: Sample N rows from a table

Quick way to inspect what's in a table.

\`\`\`kql
StormEvents
| take 5
\`\`\`

**Teaches:** `take` returns N rows in non-deterministic order. Use it to peek at data without scanning the whole table. Note: `take` does NOT sort — for sorted top-N use `top`.

**Sandbox:** `help/Samples`

---

### Q2: Select specific columns with project

Cut down a wide table to just the columns you care about.

\`\`\`kql
StormEvents
| project EventType, State, DamageProperty, DamageCrops, InjuriesDirect, InjuriesIndirect
| take 10
\`\`\`

**Teaches:** `project` selects which columns appear in the output. Order in the `project` statement determines column order in the result. Essential for keeping result sets readable when tables have 30+ columns.

**Sandbox:** `help/Samples`

---

### Q3: Rename and compute columns with project

Build new columns from existing data in one step.

\`\`\`kql
StormEvents
| project US_State=State, EventType, Injuries=InjuriesDirect+InjuriesIndirect, Damage=DamageCrops+DamageProperty
| take 10
\`\`\`

**Teaches:** `project` does double duty as renaming (`US_State=State`) and computation (`Injuries=InjuriesDirect+InjuriesIndirect`). This is how you reshape data for reporting in a single operator. Compare to SQL's `SELECT ... AS ...` with computed columns.

**Sandbox:** `help/Samples`

---

### Q4: Drop columns with project-away

Inverse of project — keep everything except what you name.

\`\`\`kql
StormEvents
| project-away EpisodeId, EventId
| take 10
\`\`\`

**Teaches:** Use `project-away` when you want to keep most columns but strip out a few. Common pattern: removing internal IDs or PII from results. Cleaner than listing 30 columns in a `project`.

**Sandbox:** `help/Samples`

---

## 2. Filtering

### Q5: Filter rows with where (numeric)

The most common operator in real-world KQL.

\`\`\`kql
StormEvents
| where DamageProperty > 0
| project State, EventType, DamageProperty
| take 10
\`\`\`

**Teaches:** `where` drops rows that don't match the predicate. Numeric operators: `>`, `>=`, `<`, `<=`, `==`, `!=`. Apply `where` early in your pipeline to reduce data volume before expensive operations.

**Sandbox:** `help/Samples`

---

### Q6: Chain multiple where filters (string equality)

Combine filters by stacking `where` clauses.

\`\`\`kql
StormEvents
| where DamageCrops > 0
| where State == "FLORIDA"
| project State, EventType, DamageCrops
\`\`\`

**Teaches:** String comparison uses `==` (case-sensitive) or `=~` (case-insensitive). Each `where` further restricts the result set. The query engine optimizes the order, so logical clarity matters more than performance ordering.

**Sandbox:** `help/Samples`

---

### Q7: String substring matching with has

Find rows where a column contains a specific word.

\`\`\`kql
StormEvents
| where DamageProperty > 0
| where State == "FLORIDA"
| where EventType has "wind"
| project StartTime, EventType, DamageProperty
\`\`\`

**Teaches:** `has` searches for a full word (token) inside a string column. Much faster than `contains` for indexed columns because it can use the inverted index. Use `has` when looking for whole-word matches; use `contains` for substring anywhere in the string.

Operators worth knowing:
- `has` / `!has` — whole-word match
- `contains` / `!contains` — substring match
- `startswith` / `endswith` — prefix/suffix match
- `has_any (...)` — match against a list of values

**Sandbox:** `help/Samples`

---

### Q8: Filter by datetime range with between

Restrict results to a specific time window.

\`\`\`kql
StormEvents
| where StartTime between (datetime(2007-01-01)..datetime(2007-06-01))
| where DamageProperty > 0
| where State == "FLORIDA"
| project StartTime, EventType, DamageProperty
| take 50
\`\`\`

**Teaches:** Time filtering is fundamental in security — every SIEM query needs a time bound. `between` is inclusive on both ends. The `datetime()` function parses ISO-style date strings. For "last N days" use `ago(Nd)` instead; for absolute ranges use `between`.

**Sandbox:** `help/Samples`

---

## 3. Time-based queries

### Q9: Last N hours/days with ago

Most common time filter in security work.

\`\`\`kql
StormEvents
| where StartTime > ago(365d)
| project StartTime, EventType, State
| take 20
\`\`\`

**Teaches:** `ago(7d)`, `ago(1h)`, `ago(30m)` — all return "now minus N units." Combine with `where TimeGenerated > ago(...)` for nearly every Sentinel query. Helps the query engine prune partitions before scanning.

**Sandbox:** `help/Samples`

---

### Q10: Bin time into buckets for time-series

Group events into time intervals for charting.

\`\`\`kql
StormEvents
| where StartTime > datetime(2007-01-01)
| summarize event_count = count() by bin(StartTime, 1d)
| render timechart
\`\`\`

**Teaches:** `bin(timestamp, 1d)` rounds each timestamp down to the nearest day. Combined with `summarize`, this produces time-series data. `render timechart` renders it as a line chart in the result pane. Use `bin(time, 1h)` for hourly, `bin(time, 5m)` for 5-minute buckets, etc.

**Sandbox:** `help/Samples`

---

## 4. Aggregations

### Q11: Count rows with summarize

The KQL equivalent of SQL's `GROUP BY ... COUNT`.

\`\`\`kql
StormEvents
| summarize event_count = count() by EventType
| order by event_count desc
\`\`\`

**Teaches:** `summarize` aggregates rows into groups defined by the `by` clause. `count()` returns the number of rows in each group. `order by ... desc` sorts the result. This pattern — `summarize by X | order by count desc` — is your most common analytical query.

**Sandbox:** `help/Samples`

---

### Q12: Multiple aggregates in one summarize

Compute several stats per group at once.

\`\`\`kql
StormEvents
| where DamageProperty > 0
| summarize total_damage = sum(DamageProperty),
            event_count = count(),
            avg_damage = avg(DamageProperty)
            by State
| order by total_damage desc
| take 10
\`\`\`

**Teaches:** A single `summarize` can produce many aggregates: `sum()`, `count()`, `avg()`, `min()`, `max()`, `dcount()` (distinct count). Much more efficient than multiple queries. Output column names come from the assignment (`total_damage =`).

**Sandbox:** `help/Samples`

---

### Q13: Distinct count with dcount

Count unique values, not all rows.

\`\`\`kql
StormEvents
| summarize unique_event_types = dcount(EventType),
            unique_states = dcount(State)
\`\`\`

**Teaches:** `dcount()` returns approximate distinct count (uses HyperLogLog under the hood — extremely fast even on huge datasets). Use `dcount_hll` for exact count when accuracy matters. Common security use: "how many unique users tried to log in?" or "how many distinct IPs attacked us?"

**Sandbox:** `help/Samples`

---

## 5. String operations

### Q14: Case-insensitive matching

Most real-world string matching needs to be case-insensitive.

\`\`\`kql
StormEvents
| where State =~ "florida"
| project State, EventType
| take 5
\`\`\`

**Teaches:** `=~` is case-insensitive equality. The case-sensitive `==` would miss "Florida" or "FLORIDA". For substring matching, use `contains` (case-insensitive by default) vs `contains_cs` (case-sensitive).

**Sandbox:** `help/Samples`

---

### Q15: Match against a list with has_any

Filter where a column matches any of N values.

\`\`\`kql
StormEvents
| where State has_any ("FLORIDA", "GEORGIA", "MISSISSIPPI", "ALABAMA")
| summarize event_count = count() by State
\`\`\`

**Teaches:** Cleaner than chaining `or` statements for many values. Common security pattern: "alert on logins from any of these high-risk countries" or "look for these specific malware filenames." Combine with `dynamic([...])` to define the list once and reuse.

**Sandbox:** `help/Samples`

---

## 6. Parsing and extending

### Q16: Add a computed column with extend

Add a column without dropping existing ones (unlike `project`).

\`\`\`kql
StormEvents
| extend TotalInjuries = InjuriesDirect + InjuriesIndirect
| where TotalInjuries > 0
| project StartTime, State, EventType, TotalInjuries
| take 10
\`\`\`

**Teaches:** `extend` adds new columns; `project` selects which ones to keep. Use `extend` early in the pipeline to compute derived fields, then `project` at the end to choose your final output shape. Together they cover most data-reshaping needs.

**Sandbox:** `help/Samples`

---

### Q17: Conditional column with iff

Add a column based on a condition.

\`\`\`kql
StormEvents
| extend Severity = iff(DamageProperty > 1000000, "High", iff(DamageProperty > 10000, "Medium", "Low"))
| project StartTime, State, EventType, DamageProperty, Severity
| take 20
\`\`\`

**Teaches:** `iff(condition, then_value, else_value)` is KQL's ternary. Nest for multi-way branching (or use `case()` which is cleaner for 3+ branches). Common security use: categorizing alerts by severity based on detection criteria.

**Sandbox:** `help/Samples`

---

## 7. let bindings

### Q18: Define a variable with let

Make queries readable and reusable.

\`\`\`kql
let TargetState = "FLORIDA";
let StartDate = datetime(2007-01-01);
StormEvents
| where State == TargetState
| where StartTime > StartDate
| project StartTime, EventType, DamageProperty
| take 10
\`\`\`

**Teaches:** `let` defines a constant or even a function at the top of a query. Makes parameters explicit and the query self-documenting. Multiple `let` statements stack — each ends with a semicolon. Essential for building reusable detection rules.

**Sandbox:** `help/Samples`

---

### Q19: let with a subquery result

Compute something once, use it many times.

\`\`\`kql
let HighDamageThreshold = toscalar(
    StormEvents
    | summarize percentile(DamageProperty, 95)
);
StormEvents
| where DamageProperty > HighDamageThreshold
| project StartTime, State, EventType, DamageProperty
| take 10
\`\`\`

**Teaches:** `toscalar()` extracts a single value from a subquery. Pattern: compute a threshold (like "95th percentile damage"), then filter the main query by it. This is how you write rules that adapt to changing data without hardcoded thresholds.

**Sandbox:** `help/Samples`

---

## 8. Real data: AzureActivity

These queries run against your own `law-homesoc` Sentinel workspace (not the sandbox).

### Q20: Verify AzureActivity is flowing

The basic "is my data connector working?" check.

\`\`\`kql
AzureActivity
| take 10
\`\`\`

**Teaches:** If this returns rows, your Azure Activity connector is working. If empty, either the connector isn't enabled or no activity has been logged yet (wait 15 minutes or generate some by creating a resource).

**Workspace:** `law-homesoc`

---

### Q21: Recent activity over the last hour

Sanity check that recent data is flowing.

\`\`\`kql
AzureActivity
| where TimeGenerated > ago(1h)
| project TimeGenerated, OperationNameValue, Caller, ResourceGroup, ActivityStatusValue
| order by TimeGenerated desc
| take 20
\`\`\`

**Teaches:** `TimeGenerated` is the standard timestamp column for nearly every Sentinel/Log Analytics table. Always filter by `TimeGenerated > ago(...)` as the first operation when querying real data — it prunes partitions and dramatically reduces query cost.

**Workspace:** `law-homesoc`

---

### Q22: Top operations in the last day

What's actually happening in my Azure subscription?

\`\`\`kql
AzureActivity
| where TimeGenerated > ago(1d)
| summarize event_count = count() by OperationNameValue
| order by event_count desc
| take 20
\`\`\`

**Teaches:** First aggregation query on real data. Tells you what activities are most common in your subscription — useful for spotting unusual operations later. Bookmark this query — you'll run it often.

**Workspace:** `law-homesoc`

---

## Open questions to revisit

- When should I use `project` early vs late in the pipeline? Performance impact?
- Difference between `has` and `contains` on indexed vs non-indexed string columns?
- When does `dcount()` accuracy matter and how do I know when to switch to `dcount_hll(col, 4)`?
- How do `join` strategies (`innerunique`, `inner`, `leftouter`, etc.) affect performance on big tables?

## What to add in Week 3

- 3-5 `join` queries (joining `SigninLogs` with `AuditLogs`, etc.)
- More `parse_json` examples once M365 connector is online
- First detection-style queries (looking for anomalies, not just describing data)

// ===========================================================================
// Time-series and trend analysis
// ===========================================================================

// Q27 — Activity volume over time, 15-minute buckets
// Teaches: bin(), render timechart, summarize with time grouping
AzureActivity
| where TimeGenerated > ago(24h)
| summarize event_count = count() by bin(TimeGenerated, 15m)
| render timechart

// Q28 — Activity by hour of day (find unusual time patterns)
// Teaches: hourofday(), pattern recognition for off-hours activity
AzureActivity
| where TimeGenerated > ago(7d)
| extend hour_of_day = hourofday(TimeGenerated)
| summarize event_count = count() by hour_of_day
| order by hour_of_day asc
| render columnchart

// Q29 — Detect activity spikes (operations 2x average)
// Teaches: let, percentiles, comparison against baseline
let baseline_avg = toscalar(
    AzureActivity
    | where TimeGenerated between (ago(7d) .. ago(1d))
    | summarize avg_per_hour = count() / 144.0  // 144 ten-minute buckets in 24h
);
AzureActivity
| where TimeGenerated > ago(1d)
| summarize event_count = count() by bin(TimeGenerated, 10m)
| where event_count > (baseline_avg * 2)
| order by TimeGenerated desc

// ===========================================================================
// String parsing and extraction
// ===========================================================================

// Q30 — Extract just the operation name (last segment of OperationNameValue)
// Teaches: split() and array indexing
AzureActivity
| where TimeGenerated > ago(1h)
| extend op_name = tostring(split(OperationNameValue, "/")[-1])
| project TimeGenerated, op_name, Caller
| take 50

// Q31 — Parse the resource provider from operations
// Teaches: tostring, split for hierarchical strings
AzureActivity
| where TimeGenerated > ago(1d)
| extend provider = tostring(split(OperationNameValue, "/")[0])
| summarize event_count = count() by provider
| order by event_count desc

// Q32 — Parse JSON properties (works on any table with JSON columns)
// Teaches: parse_json, dynamic typing
AzureActivity
| where TimeGenerated > ago(1d)
| where isnotempty(Properties)
| extend props = parse_json(Properties)
| extend status_code = tostring(props.statusCode)
| project TimeGenerated, OperationNameValue, status_code
| where isnotempty(status_code)
| take 20

// ===========================================================================
// Aggregation patterns common in detection
// ===========================================================================

// Q33 — Most active callers with the operations they perform
// Teaches: make_set() to aggregate distinct values into an array
AzureActivity
| where TimeGenerated > ago(1d)
| summarize 
    total_ops = count(),
    operations_performed = make_set(OperationNameValue, 10)
    by Caller
| order by total_ops desc
| take 10

// Q34 — First and last activity time per caller
// Teaches: min(), max(), and computing duration
AzureActivity
| where TimeGenerated > ago(7d)
| summarize 
    first_seen = min(TimeGenerated),
    last_seen = max(TimeGenerated),
    total_ops = count()
    by Caller
| extend duration = last_seen - first_seen
| order by total_ops desc

// ===========================================================================
// Detection patterns (templates for future real detections)
// ===========================================================================

// Q35 — Failed operations grouped by caller (potential auth issues or scanning)
// Teaches: filtering by status, summarize with where
AzureActivity
| where TimeGenerated > ago(7d)
| where ActivityStatusValue == "Failed"
| summarize 
    failure_count = count(),
    failed_operations = make_set(OperationNameValue, 5)
    by Caller
| where failure_count > 3
| order by failure_count desc

// Q36 — Operations on sensitive resource types (template detection)
// Teaches: has_any, watchlist-style filtering
let sensitive_ops = dynamic([
    "Microsoft.KeyVault",
    "Microsoft.Authorization/roleAssignments",
    "Microsoft.Authorization/policyAssignments"
]);
AzureActivity
| where TimeGenerated > ago(7d)
| where OperationNameValue has_any (sensitive_ops)
| project TimeGenerated, OperationNameValue, Caller, ResourceGroup
| order by TimeGenerated desc
