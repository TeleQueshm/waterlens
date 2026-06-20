# 💧 Smart Water Quality Monitoring System

An end-to-end, real-time AI-powered dashboard designed to monitor and predict water potability at the output stage of water treatment plants. Built using **XGBoost** for precise machine learning predictions and **Flask** with a modern **Tailwind CSS** dashboard for operations.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-v3.0-green.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-Latest-orange.svg)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-v3.0-cyan.svg)

---

## 🚀 Project Overview

Water quality metrics often present complex, non-linear relationships. Standard threshold rules can fail to detect systemic issues. This system bridges the gap by leveraging machine learning to evaluate **9 chemical and physical parameters** simultaneously, providing operators with an instant safety assessment and an explicit confidence score.

### Key Features
- **Robust Preprocessing (`preprocess.py`):** Automatically sanitizes data types, isolates noise, and handles missing values using robust statistical imputation.
- **Advanced Machine Learning (`train.py`):** Utilizes **XGBoost Classification** calibrated with dynamic class-weight metrics to counteract data imbalance.
- **Custom Decision Thresholding:** Calibrated to handle realistic environmental data ranges without over-rejecting pristine water profiles.
- **Modern Industrial UI (`index.html`):** Glassmorphism dashboard style engineered in Tailwind CSS with intuitive visual alerts and built-in World Health Organization (WHO) benchmarks.
- **IoT-Ready API Endpoints:** Includes a fully functional JSON POST API designed to ingest real-time telemetry from live SCADA or hardware sensors.

---

## 🌍 Open Source Mission & Regional Impact

This software is specifically developed to kickstart open-source initiatives and build a dynamic framework for solving critical regional needs. By bringing passionate professionals and community members together around open-source software, we aim to bridge technical gaps in resource-constrained environments. 

Our ultimate hope is that this open-source tool serves as a practical asset to actively solve localized challenges—particularly in water sanitation—improving safety and infrastructure for the community. We welcome developers, data scientists, and environmental engineers to contribute and scale this system together.

---

## 📊 Feature Set & Architecture

The system evaluates water potability based on the following structural criteria:

| Feature Name | Description | Units / Standards |
| :--- | :--- | :--- |
| `ph` | Acid-base balance evaluation | WHO Standard: 6.5 – 8.5 |
| `Hardness` | Calcium and magnesium concentration | mg/L |
| `Solids` | Total Dissolved Solids (TDS) | ppm |
| `Chloramines` | Residual chlorine disinfection compounds | ppm (Max 4 mg/L) |
| `Sulfate` | Dissolved sulfate minerals | mg/L (Max 250 mg/L) |
| `Conductivity` | Electrical conductivity of water | μS/cm |
| `Organic_carbon` | Total Organic Carbon (TOC) levels | ppm |
| `Trihalomethanes` | Disinfection byproducts | μg/L |
| `Turbidity` | Visual clarity and suspended solids | NTU (Max 5 NTU) |

---

## 🛠️ Installation & Setup

### 1. Clone & Organize the Workspace
Ensure your folder structure matches the layout below:
```text
water-monitoring-system/
│
├── water_potability.csv       # Raw Dataset
├── preprocess.py              # Step 1: Data Cleansing Script
├── train.py                   # Step 2: Model Training Script
├── app.py                     # Step 3: Flask Deployment Application
└── templates/
    └── index.html             # UI Front-end Layout

```

### 2. Install Dependencies

Run the following command to install required modules:

```bash
pip install Flask joblib scikit-learn numpy xgboost pandas

```

---

## 🏃‍♂️ Step-by-Step Execution

### Step 1: Preprocess the Dataset

Run the preprocessing script to clean text anomalies, impute missing entries via median analysis, and export sanitized structures.

```bash
python preprocess.py

```

*Output: Generates `cleaned_water_data.csv*`

### Step 2: Train the ML Intelligence Model

Train the advanced XGBoost network. The script applies an optimized `scale_pos_weight` ratio and exports saved artifacts.

```bash
python train.py

```

*Output: Generates `final_water_model.pkl` and `final_scaler.pkl` alongside diagnostic metrics (Accuracy, F1-Score, Recall).*

### Step 3: Launch the Production Web Dashboard

Fire up the Flask web server to spin up the edge UI monitoring client:

```bash
python app.py

```

Once initialized, navigate to **`http://localhost:5005`** via any modern web browser.

---

## 🌐 API Reference (IoT Hardware Integration)

Smart sensors, microcontrollers (ESP32/Raspberry Pi), or PLC systems can easily push live metrics directly to the model's background endpoint.

### Endpoint:

`POST /api/predict`

### Payload Format (JSON):

```json
{
  "ph": 7.2,
  "Hardness": 204.8,
  "Solids": 20791.3,
  "Chloramines": 7.3,
  "Sulfate": 368.5,
  "Conductivity": 564.3,
  "Organic_carbon": 10.3,
  "Trihalomethanes": 86.9,
  "Turbidity": 2.9
}

```

### Success Response (JSON):

```json
{
  "applied_threshold": 0.35,
  "message": "Water is potable",
  "potability": 1,
  "potability_probability": 0.5482,
  "status": "success"
}

```

---

## ⚙️ Calibration Note: Tuning Safety Sensitivity

Industrial real-world data distributions rarely split perfectly down a standard 50% line. In `app.py`, you can manipulate the decision boundaries using the custom threshold variable:

```python
CUSTOM_THRESHOLD = 0.35

```

* Lowering this threshold reduces strictness (useful if the model flags clean water as contaminated due to unharmful mineral spikes).
* Raising this threshold forces maximum strictness for tight chemical margins.

```
---

