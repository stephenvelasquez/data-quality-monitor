from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class FreshnessConfig:
    table: str; warn_hours: int; error_hours: int

@dataclass
class FreshnessResult:
    table: str; hours_since: float; status: str

def check_freshness(configs, now, timestamps):
    results = []
    for c in configs:
        latest = timestamps.get(c.table)
        if not latest: results.append(FreshnessResult(c.table, -1, "unknown")); continue
        hours = (now - latest).total_seconds() / 3600
        status = "error" if hours > c.error_hours else "warn" if hours > c.warn_hours else "ok"
        results.append(FreshnessResult(c.table, round(hours,1), status))
    return results

if __name__ == "__main__":
    now = datetime(2025,12,15,14,0,0)
    ts = {"raw.orders": datetime(2025,12,15,10,0,0), "raw.events": datetime(2025,12,15,8,0,0)}
    for r in check_freshness([FreshnessConfig("raw.orders",6,12), FreshnessConfig("raw.events",1,3)], now, ts):
        print(f"  {r.table}: {r.status.upper()} ({r.hours_since}h)")
