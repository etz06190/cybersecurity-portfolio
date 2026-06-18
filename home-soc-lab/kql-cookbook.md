## Session: `let` and `join` operators

_Added during Week 3 — KQL intermediate. Tables used: SigninLogs, AzureActivity, OfficeActivity._

---

### `let` — scalar binding
Names a single value so it can be reused. Surprised me: nothing fancy, but a `let` at the top makes a long query read top-to-bottom instead of burying the time window deep in a `where`.
```kql
let lookback = ago(24h);
SigninLogs
| where TimeGenerated > lookback
| limit 20
```

### `let` — sub-table binding
Names a whole query result so it can be referenced like a table. Surprised me: you filter once, then treat the named result as a real table for the rest of the query.
```kql
let failedSignins =
    SigninLogs
    | where ResultType != 0;
failedSignins
| summarize count() by UserPrincipalName
| sort by count_ desc
```

### `let` — successful sign-ins per user (micro-exercise)
Counts successful sign-ins per user in the last 24h via a named sub-table. Surprised me: `ResultType == 0` means success, non-zero means a failure code — counterintuitive until you see it once.
```kql
let successfulSignins =
    SigninLogs
    | where TimeGenerated > ago(24h)
    | where ResultType == 0;
successfulSignins
| summarize count() by UserPrincipalName
| sort by count_ desc
```

### `join` — basic inner join (skeleton)
Matches rows from two tables where a key agrees; right table goes in parentheses. Surprised me: the right-hand table has to be wrapped in `( )`, the left is just whatever precedes the pipe.
```kql
LeftTable
| join kind=inner (
    RightTable
    | where Field == "value"
) on KeyColumn
```

### `let` + `join` — new-geography sign-in detection
Finds last-24h sign-ins from a country a user has NOT used in the prior 30 days. Surprised me: `make_set` collapses all a user's historical countries into one set per user, so a single `!in` check does the whole comparison.
```kql
let knownLocations =
    SigninLogs
    | where TimeGenerated between (ago(30d) .. ago(24h))
    | where ResultType == 0
    | summarize knownCountries = make_set(Location) by UserPrincipalName;
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType == 0
| join kind=inner knownLocations on UserPrincipalName
| where Location !in (knownCountries)
| project TimeGenerated, UserPrincipalName, Location, knownCountries
```

### `join` — case-normalized (THE TRAP fix)
Same join, but `tolower()` on BOTH sides of the key so case differences don't silently kill the match. Surprised me: a case mismatch returns an empty result with NO error — the query lies instead of failing. Default to normalizing join keys from now on.
```kql
let knownLocations =
    SigninLogs
    | where TimeGenerated between (ago(30d) .. ago(24h))
    | where ResultType == 0
    | extend joinkey = tolower(UserPrincipalName)
    | summarize knownCountries = make_set(Location) by joinkey;
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType == 0
| extend joinkey = tolower(UserPrincipalName)
| join kind=inner knownLocations on joinkey
| where Location !in (knownCountries)
| project TimeGenerated, joinkey, Location, knownCountries
```

---

**`join kind=` quick reference**
- `inner` — only rows matching on both sides (default, most common)
- `leftouter` — all left rows, right data where matched, nulls otherwise
- `rightouter` — mirror of leftouter
- `fullouter` — everything from both sides
- `leftanti` — left rows with NO match on the right ("in A, not in B" — good for hunting gaps)

**Diagnostic rule:** join returns empty but you expected matches → suspect case first (`tolower()` both sides), then check for differing column names, trailing spaces, or type mismatch.

**Semicolon rule:** every `let` statement ends with `;`. The final query does not.
