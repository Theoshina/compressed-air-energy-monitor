# AI-Assisted Compressed-Air Energy Monitoring

A Python proof-of-concept for AI-assisted monitoring of compressed-air energy use in an industrial environment.

## What this prototype does

The prototype generates **simulated** industrial sensor data containing:

- Production demand
- Compressed-air pressure
- Airflow
- Compressor power
- Simulated leak periods

It then:

1. Detects abnormal operating patterns using **Isolation Forest**.
2. Estimates simplified excess power.
3. Applies transparent rules to generate maintenance recommendations.
4. Produces a CSV summary and an anomaly plot.

### Architecture

```text
Simulated sensor data
        ↓
Data generation / input
        ↓
Isolation Forest anomaly detection
        ↓
Energy-impact estimation
        ↓
Rule-based reasoning
        ↓
Maintenance recommendation
        ↓
CSV + visualization
```

## Important limitation

This is a **proof-of-concept using simulated data**. It is not connected to a real factory, PLC, compressor, or industrial sensor.

The estimated energy values and detection results should not be presented as validated industrial performance.

## Run locally

Use Python 3.11 or newer.

```bash
python -m venv .venv
```

Activate the environment.

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python src/main.py
```

## Generated files

After running, the project creates:

```text
data/sensor_data.csv
results/anomaly_summary.csv
results/anomaly_plot.png
```

## GitHub Actions

The repository includes a GitHub Actions workflow at:

```text
.github/workflows/run-prototype.yml
```

Whenever the workflow is triggered, GitHub creates a Python environment, installs the requirements, runs the prototype, and uploads the generated `results/` folder as an artifact.

Go to:

**GitHub → Actions → Run Compressed-Air Energy Prototype**

## Future development

A later version could:

- Replace simulated data with real sensor/public industrial data.
- Add real-time monitoring.
- Add a dashboard.
- Add an agentic AI layer for maintenance reasoning.
- Validate energy-saving estimates using measured industrial data.
- Integrate with IoT/PLC data where appropriate.

## Honest project description

> I developed a Python proof-of-concept for AI-assisted compressed-air energy monitoring. It analyzes simulated pressure, flow, production and compressor-power data to detect abnormal consumption and generate maintenance recommendations, with the goal of reducing unnecessary energy use.
