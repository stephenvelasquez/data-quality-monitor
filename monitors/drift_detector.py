from dataclasses import dataclass
from typing import Optional

@dataclass
class ColumnProfile:
    name: str; dtype: str; null_rate: float; distinct_count: int
    mean: Optional[float] = None; stddev: Optional[float] = None

@dataclass
class DriftAlert:
    table: str; column: str; drift_type: str; severity: str; detail: str; score: float

def detect_schema_drift(baseline: list[ColumnProfile], current: list[ColumnProfile], table: str) -> list[DriftAlert]:
    alerts = []
    base_map = {c.name: c for c in baseline}
    curr_map = {c.name: c for c in current}
    for name in curr_map:
        if name not in base_map:
            alerts.append(DriftAlert(table, name, "schema_added", "warning", f"New column '{name}'", 0.7))
    for name in base_map:
        if name not in curr_map:
            alerts.append(DriftAlert(table, name, "schema_removed", "critical", f"Column '{name}' removed", 1.0))
        elif base_map[name].dtype != curr_map[name].dtype:
            alerts.append(DriftAlert(table, name, "type_changed", "critical", f"Type: {base_map[name].dtype} -> {curr_map[name].dtype}", 0.9))
    return alerts

def compute_quality_score(alerts: list[DriftAlert]) -> float:
    if not alerts: return 100.0
    penalty = sum(a.score * (3.0 if a.severity == "critical" else 1.0) for a in alerts)
    return max(0.0, 100.0 - penalty * 10)

if __name__ == "__main__":
    baseline = [ColumnProfile("order_id","varchar",0.0,50000), ColumnProfile("amount","decimal",0.02,4800,85.5,42.0)]
    current = [ColumnProfile("order_id","varchar",0.0,55000), ColumnProfile("amount","decimal",0.05,5100,92.3,45.0), ColumnProfile("region","varchar",0.1,12)]
    alerts = detect_schema_drift(baseline, current, "orders")
    for a in alerts: print(f"[{a.severity.upper()}] {a.table}.{a.column}: {a.detail}")
    print(f"Quality Score: {compute_quality_score(alerts):.1f}/100")
