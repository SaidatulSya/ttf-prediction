# ⏱️ Time to Failure (TTF) Prediction from Process Data

This pilot project demonstrates a practical workflow for predicting **Time to Failure (TTF)** of process equipment using **simple anomaly detection** and **linear regression** based on historical sensor data (e.g., pressure transmitters).

---

## 📌 Problem Statement

In industrial environments, anticipating equipment failure before alarms trigger can prevent unplanned downtime. This project:
- Detects early-stage anomalies before a **Low/High Alarm**.
- Labels each anomaly with the number of hours before failure (`TTF`).
- Trains a regression model to predict TTF using process values (e.g., PV).

---

## 🔧 Project Workflow

1. **Data Preprocessing**
   - Clean raw timestamped sensor values
   - Convert timestamps, remove bad data

2. **Status Labeling**
   - Label each point as:
     - `"Normal"`: within expected range
     - `"Anomaly"`: N rows before alarm
     - `"Low Alarm"` or `"High Alarm"`: outside safe limits

3. **TTF Labeling**
   - For each `"Anomaly"` row, calculate time (in hours) to the next alarm
   - Drop rows where TTF cannot be calculated

4. **Model Training**
   - Use Linear Regression on `value` → `TTF`
   - Evaluate using MAE and R²

---

## 📊 Model Results

| Metric               | Result        |
|----------------------|---------------|
| Mean Absolute Error  | ~3.01 hours   |
| R² Score             | Negative (pilot model) |

> This is an initial prototype. Future improvements will include advanced features and non-linear models.

---

## 🔍 Sample Data (Structure)

| Timestamp           | Value | Status     | TTF (hrs) |
|---------------------|-------|------------|-----------|
| 2024-07-31 17:55:00 | 76.89 | Anomaly    | 0.83      |
| 2024-07-31 19:03:00 | 65.91 | Low Alarm  | —         |

---

## 🧠 Future Improvements

- Add rolling average, rate of change, and contextual features
- Try Random Forest or XGBoost for non-linear modeling
- Build live prediction dashboard or deploy via API

---

## 🚀 How to Run

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the notebook or script to:
    - Generate anomaly & TTF labels
    - Train the regression model
    - Make predictions

## 📄 License
This project is licensed under the MIT License.

## 🙋‍♀️ Author
Saidatul Syafiqah
Data Scientist / AVEVA PI System Engineer


