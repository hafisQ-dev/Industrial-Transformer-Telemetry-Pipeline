
# Industrial Transformer Telemetry Pipeline

An end-to-end, production-ready Industrial IoT (IIoT) telemetry and anomaly detection system. This project simulates real-time thermal and electrical behavior of grid transformers, streams high-frequency data using the MQTT protocol, stores time-series metrics in InfluxDB, and provides a fully visualized dashboard with automated Telegram alerting mechanisms.



##  System Architecture

The architecture relies on a fully containerized, microservices-based pipeline designed for high scalability and low latency:

1. **Telemetry Simulator (Python):** Generates multi-variable physical metrics mimicking realistic grid transformer loading cycles and ambient temperature effects.
2. **MQTT Broker (Eclipse Mosquitto):** Handles lightweight, asynchronous pub/sub telemetry transport layer.
3. **ETL Data Bridge (Python):** Consumes raw MQTT payloads, structuralizes data points, and handles batch writing over the network.
4. **Time-Series Database (InfluxDB v2):** Optimized storage for high-frequency time-stamped parameters.
5. **Visualization & Analytics Engine (Grafana):** Serves analytical panels using Flux queries and acts as the root alerting manager.

```text
[Simulator (Python)] ──(MQTT)──> [Mosquitto Broker] ──> [Data Bridge] ──> [InfluxDB] ──> [Grafana & Telegram]

```

---

##  Tech Stack & Keywords

* **Infrastructure:** Docker, Docker Compose, Linux Server Management
* **Protocols:** MQTT (Message Queuing Telemetry Transport)
* **Data Tier:** InfluxDB v2, Flux Query Language
* **Visualization:** Grafana Labs, Analytical Dashboards
* **Languages & Core Libs:** Python 3.10+, Paho-MQTT, InfluxDB-Client, Bash Scripting
* **Notification Integration:** Telegram Bot API (HTTP Webhooks)

---

## Core Technical Achievements

### 1. Robust Multi-Container Dockerization

The entire stack is deployed via an optimized `docker-compose.yml` manifest, ensuring total environment isolation, declarative storage volume bounds, and internal network bridging without port collision.

### 2. Time-Series Data Modeling (Flux Queries)

Raw unstructured sensory data is queried out of InfluxDB buckets natively. High-frequency data point parsing is structured dynamically using structural functional logic:

```flux
from(bucket: "YOUR_INFLUX_BUCKET")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "transformer_telemetry")
  |> filter(fn: (r) => r["_field"] == "temperature")
  |> filter(fn: (r) => r["transformer_id"] == "TX_Silo_01")

```

### 3. Smart Edge Alerting Mechanism

Configured dual-tier alarm rules directly within Grafana-managed alert infrastructure.

* **Visual Thresholding:** Implemented real-time conditional color shading schemas (`From thresholds`) mapping critical zones ($> 65^\circ\text{C}$).
* **Alert Fatigue Prevention:** Built custom routing trees using specific label matching (`telegram=true`) integrated with specialized `Repeat Interval` windows to throttle redundant push notifications during prolonged critical status periods.

---

##  Quick Start

### Prerequisites

* Docker & Docker Compose installed on your host machine.

### Installation & Deployment

1. Clone this repository:
```bash
git clone [https://github.com/hafisQ-dev/Industrial-Transformer-Telemetry-Pipeline.git]
cd industrial-transformer-telemetry-pipeline

```

2. Fire up the infrastructure stack:
```bash
docker compose up -d

```


3. Verify running containers:
```bash
docker ps

```


4. Run the Python simulator & bridge scripts to feed live telemetry data into the pipeline.

---

##  Visualizations & Dashboards

The monitoring panel includes:

* **Real-time Temperature Analytics:** Gauge charts and time-series graphs tracking thermal degradation.
* **Threshold Indicators:** Clear static and dynamic lines showing safety boundaries.
* **System Integrity Logs:** Direct visibility into individual transformer IDs across distinct industrial zones.

```

