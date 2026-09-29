from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"

def generate_sensor_data(n_hours=720, seed=42):
    """Generate simulated industrial compressed-air sensor data."""
    rng = np.random.default_rng(seed)
    time = pd.date_range("2026-01-01", periods=n_hours, freq="h")

    production = np.clip(
        60 + 25 * np.sin(np.arange(n_hours) / 24 * 2 * np.pi)
        + rng.normal(0, 8, n_hours), 5, 100
    )
    pressure = np.clip(
        7.0 - 0.008 * production + rng.normal(0, 0.12, n_hours),
        5.5, 8.0
    )
    airflow = np.clip(
        120 + 2.0 * production + rng.normal(0, 12, n_hours),
        50, None
    )
    compressor_power = np.clip(
        18 + 0.16 * airflow + rng.normal(0, 2, n_hours),
        10, None
    )

    # Simulated leak periods (labels are for evaluation only).
    leak = np.zeros(n_hours, dtype=int)
    for start, duration in [(145, 18), (330, 24), (520, 20), (650, 15)]:
        leak[start:start + duration] = 1

    airflow += leak * rng.normal(80, 10, n_hours)
    compressor_power += leak * rng.normal(12, 2, n_hours)
    pressure -= leak * rng.normal(0.35, 0.08, n_hours)

    return pd.DataFrame({
        "timestamp": time,
        "production_demand_pct": np.round(production, 2),
        "pressure_bar": np.round(pressure, 2),
        "airflow_cfm": np.round(airflow, 2),
        "compressor_power_kw": np.round(compressor_power, 2),
        "simulated_leak_label": leak
    })

def detect_anomalies(df):
    features = [
        "production_demand_pct",
        "pressure_bar",
        "airflow_cfm",
        "compressor_power_kw",
    ]

    model = IsolationForest(
        n_estimators=200,
        contamination=0.08,
        random_state=42
    )
    df["anomaly"] = (model.fit_predict(df[features]) == -1).astype(int)
    df["anomaly_score"] = -model.decision_function(df[features])
    return df

def add_reasoning(df):
    """Transparent rule-based explanation layer."""
    recommendations = []

    for row in df.itertuples():
        if row.anomaly == 0:
            recommendations.append("Normal operation")
        elif row.production_demand_pct < 45 and row.airflow_cfm > 220:
            recommendations.append(
                "Inspect for compressed-air leak; demand is low but airflow is high"
            )
        elif row.pressure_bar < 6.4:
            recommendations.append(
                "Inspect downstream leaks or pressure drop"
            )
        else:
            recommendations.append(
                "Investigate abnormal compressed-air consumption"
            )

    df["recommendation"] = recommendations

    # Simplified excess-power estimate for the prototype only.
    expected_airflow = 120 + 2.0 * df["production_demand_pct"]
    excess_airflow = np.maximum(df["airflow_cfm"] - expected_airflow, 0)
    df["estimated_excess_power_kw"] = np.round(
        excess_airflow * 0.08, 2
    )
    return df

def save_outputs(df):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(DATA_DIR / "sensor_data.csv", index=False)

    summary = (
        df[df["anomaly"] == 1][
            ["timestamp", "anomaly_score", "estimated_excess_power_kw",
             "recommendation"]
        ]
        .sort_values("anomaly_score", ascending=False)
    )
    summary.to_csv(RESULTS_DIR / "anomaly_summary.csv", index=False)

    plt.figure(figsize=(12, 5))
    plt.plot(
        df["timestamp"], df["compressor_power_kw"],
        label="Compressor power (kW)"
    )
    anomaly_rows = df[df["anomaly"] == 1]
    plt.scatter(
        anomaly_rows["timestamp"],
        anomaly_rows["compressor_power_kw"],
        label="Detected anomaly",
        s=18
    )
    plt.xlabel("Time")
    plt.ylabel("Power (kW)")
    plt.title("AI-Assisted Compressed-Air Energy Monitoring")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "anomaly_plot.png", dpi=150)
    plt.close()

def main():
    print("AI-Assisted Compressed-Air Energy Monitoring")
    print("NOTE: This prototype uses simulated industrial sensor data.\n")

    df = generate_sensor_data()
    df = detect_anomalies(df)
    df = add_reasoning(df)
    save_outputs(df)

    anomalies = int(df["anomaly"].sum())
    simulated_leaks = int(df["simulated_leak_label"].sum())

    print(f"Records analyzed : {len(df)}")
    print(f"Anomalies found  : {anomalies}")
    print(f"Simulated leaks  : {simulated_leaks}")
    print("\nOutputs:")
    print("  data/sensor_data.csv")
    print("  results/anomaly_summary.csv")
    print("  results/anomaly_plot.png")

if __name__ == "__main__":
    main()
