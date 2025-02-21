import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from lifelines import CoxPHFitter
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# ---------------------------
# 🚀 STEP 1: Fetch TCGA-LUAD Data
# ---------------------------
url = "https://api.gdc.cancer.gov/cases?size=100&expand=diagnoses.treatments&pretty=true"
response = requests.get(url)
data = response.json()

# Extract patient data
cases = data["data"]["hits"]
patients = []

for case in cases:
    if "diagnoses" in case and case["diagnoses"]:
        diag = case["diagnoses"][0]
        treatment = diag.get("treatments", [{}])[0]  # First treatment

        patients.append({
            "age": case.get("demographic", {}).get("age_at_index"),
            "gender": case.get("demographic", {}).get("gender"),
            "tumor_stage": diag.get("tumor_stage"),
            "treatment_type": treatment.get("treatment_type"),
            "treatment_outcome": treatment.get("treatment_outcome"),
            "days_to_last_followup": diag.get("days_to_last_follow_up"),
            "days_to_death": diag.get("days_to_death"),
            "vital_status": case.get("diagnoses", [{}])[0].get("vital_status")
        })

# Convert to DataFrame
df = pd.DataFrame(patients)
df.dropna(inplace=True)  # Drop missing values

# ---------------------------
# 🚀 STEP 2: Data Preprocessing
# ---------------------------
# Convert categorical columns to numerical
label_encoders = {}
for col in ["gender", "tumor_stage", "treatment_type", "treatment_outcome", "vital_status"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoders for future use

# Standardize numerical features
scaler = StandardScaler()
df[["age", "days_to_last_followup", "days_to_death"]] = scaler.fit_transform(df[["age", "days_to_last_followup", "days_to_death"]])

# Train-test split
X = df.drop(columns=["treatment_outcome"])  # Features
y = df["treatment_outcome"]  # Target (treatment success)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------
# 🚀 STEP 3: AI Model - Treatment Ranking (XGBoost)
# ---------------------------
xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1)
xgb_model.fit(X_train, y_train)

# Evaluate
print("XGBoost Model Accuracy:", xgb_model.score(X_test, y_test))

# Feature importance plot
plt.figure(figsize=(10, 5))
xgb.plot_importance(xgb_model)
plt.show()

# ---------------------------
# 🚀 STEP 4: Survival Analysis (DeepSurv Model)
# ---------------------------
cph = CoxPHFitter()
df_survival = df.drop(columns=["treatment_outcome"])  # Remove target variable
df_survival["event"] = (df["vital_status"] == 1).astype(int)  # 1 = Death, 0 = Alive
df_survival["time"] = df["days_to_death"].fillna(df["days_to_last_followup"])  # Survival time

cph.fit(df_survival, duration_col="time", event_col="event")
cph.print_summary()

# Survival plot
cph.plot_survival_function()
plt.show()

# ---------------------------
# 🚀 STEP 5: Tumor Growth Forecasting (LSTM)
# ---------------------------
# Prepare time-series data (simulate tumor size progression)
time_steps = 10  # Use last 10 time steps for prediction

# Generate synthetic tumor growth data
df["tumor_size"] = np.random.uniform(1, 5, size=len(df))  # Simulated initial tumor sizes
tumor_growth = []
for i in range(len(df)):
    growth = np.cumsum(np.random.normal(0.1, 0.05, size=time_steps))  # Random growth pattern
    tumor_growth.append(growth)

tumor_growth = np.array(tumor_growth)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(tumor_growth[:, :-1], tumor_growth[:, -1], test_size=0.2, random_state=42)

# LSTM Model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(50),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_data=(X_test, y_test))

# Predict future tumor behavior
predicted_tumor_size = model.predict(X_test)

# Plot actual vs predicted tumor size
plt.figure(figsize=(10, 5))
plt.plot(y_test, label="Actual Tumor Size", marker="o")
plt.plot(predicted_tumor_size, label="Predicted Tumor Size", marker="x")
plt.legend()
plt.show()
