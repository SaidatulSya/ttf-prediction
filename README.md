# ⏱️ Time to Failure (TTF) Estimation using Statistical Trend Detection

This project showcases a **rule-based framework** for estimating **Time to Failure (TTF)** of process equipment using **statistical feature engineering** and **linear extrapolation** based on historical sensor data (e.g., pressure transmitters, control valve positions).

---

## 📌 Problem Statement

In process industries, it is crucial to detect early signs of deviation that could lead to equipment failure. This project:
- Uses statistical methods to detect **anomalous behavior** before a failure.
- Estimates how many hours remain before a **Low or High Alarm** is triggered.
- Uses the slope of recent sensor data (`rolling_slope`) to project future behavior and calculate **TTF using y = mx + c**.

---

## 🔧 Project Workflow

### ✅ Step 1: Extract Data
- Retrieve historical sensor values from Cognite Data Fusion (CDF).
- Ensure consistent formatting and indexing.

### 📊 Step 2: Analyze Data Quality
- Detect and summarize missing values (`NaN`), outliers, and bad data.

### 🔁 Step 3: Transform & Engineer Features
- Apply rolling statistics: mean, standard deviation, MAD, slope
- Compute sigma levels, lag differences, and deviations from mean/median

### 🏷️ Step 4: Status Labeling
- Label each row as:
  - `"Normal"`: Within expected behavior
  - `"Anomaly"`: Statistically deviating from the baseline (based on sigma, slope, etc.)
  - `"Low Alarm"` / `"High Alarm"`: Breaches safe operating limits

### ⏱️ Step 5: Estimate TTF
- For each `"Anomaly"` point, calculate `Estimated TTF (hours)` using:
  
  TTF = (y_alarm - y0) / m
  
  where:
  - `y0` = current value
  - `m` = recent rolling slope
  - `y_alarm` = nearest alarm threshold (high or low)

---

## 📊 Sample Data Structure

| Timestamp           | Value | Status     | Rolling Slope | TTF (hrs) |
|---------------------|-------|------------|----------------|-----------|
| 2024-07-31 17:55:00 | 76.89 | Anomaly    | 0.03           | 0.83      |
| 2024-07-31 19:03:00 | 65.91 | Low Alarm  | -              | -         |

---

## 💡 Highlights

- No machine learning required — purely statistical and interpretable.
- Suitable for control loops or sensor diagnostics in early pilot setups.
- Framework modularized into classes:
  - `RetrieveData`
  - `FeatureEngineer`
  - `EstTTF`

---

## 📈 Future Improvements

- Integrate contextual tags (e.g., CO, OP) for smarter rule triggers
- Extend to multi-sensor correlation and event-based detection
- Deploy real-time alert system or dashboard in CDF or Power BI

---

## 🚀 How to Run

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib

---

## 📄 License
This project is licensed under the MIT License.

---

## 🙋‍♀️ Author
Saidatul Syafiqah
Data Scientist / AVEVA PI System Engineer


