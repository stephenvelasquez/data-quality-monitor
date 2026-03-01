# data-quality-monitor

Data validation, schema drift detection, and pipeline observability — built for teams that ship data products, not just dashboards.

Uses **dbt** for SQL-native data tests, **Python** for anomaly detection and alerting, and **SQL** throughout because that's what data teams actually speak.

## What's Inside

- `dbt_project/` — dbt models (staging + marts), custom tests, macros for freshness and row count validation
- `monitors/` — Python-based drift detection, anomaly detection, freshness checking, and alert routing
- `sql/` — Standalone SQL for composite quality scores and completeness audits
- `configs/` — Monitor definitions and alert routing rules

## Core Capabilities

### dbt-Native Testing
- Schema tests, custom data tests, freshness SLAs, row count deltas

### Drift Detection
- Schema drift (added/removed/type-changed columns)
- Distribution drift (PSI, KL divergence on numeric columns)
- Cardinality and temporal drift detection

### Anomaly Detection
- Z-score based with rolling windows
- Seasonal decomposition (trend + seasonal + residual)
- Volume anomalies and cross-metric correlation

### Alerting
- Severity tiers with Slack/PagerDuty routing
- Deduplication and auto-escalation

## Design Principles

1. **SQL-first** — if a data person can't read it, it won't get maintained
2. **Incremental** — monitors run on deltas, not full table scans
3. **Opinionated defaults** — works out of the box, tune only when needed

## Background

Built from patterns learned across Amazon, Walmart, and Microsoft, where bad data costs millions before anyone notices. Every monitor here exists because the absence of that monitor caused a real incident.

## License

MIT
