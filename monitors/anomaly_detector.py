from dataclasses import dataclass
import math

@dataclass
class Anomaly:
    metric: str; timestamp: str; value: float; expected: float; z_score: float; severity: str

def detect_anomalies(values, timestamps, metric_name, z_threshold=2.5, window=7):
    if len(values) < window + 1: return []
    anomalies = []
    for i in range(window, len(values)):
        w = values[i-window:i]
        mean = sum(w)/len(w)
        std = math.sqrt(sum((v-mean)**2 for v in w)/len(w)) or 0.001
        z = (values[i]-mean)/std
        if abs(z) > z_threshold:
            anomalies.append(Anomaly(metric_name, timestamps[i], values[i], mean, z, "critical" if abs(z)>4 else "warning"))
    return anomalies

if __name__ == "__main__":
    orders = [1200,1180,1210,1195,1220,1205,1190,1230,1215,1240,1225,1250,1235,1220,1260,1245,1270,1255,1280,1265,1250,1290,1275,400,1295,1310,1300,1285]
    ts = [f"2025-12-{i+1:02d}" for i in range(len(orders))]
    for a in detect_anomalies(orders, ts, "daily_orders"):
        print(f"[{a.severity.upper()}] {a.metric} {a.timestamp}: val={a.value:.0f} exp={a.expected:.0f} z={a.z_score:.1f}")
