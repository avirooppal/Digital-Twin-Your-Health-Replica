import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier  # ML model

# Load Dataset
df = pd.read_csv("dataset.csv")

# Drop non-numeric columns
df = df.drop(columns=['Name', 'Surname'])

# Rename columns
df.columns = ['Age', 'Smokes', 'AreaQ', 'Alkhol', 'Lung_Cancer']

# Convert target labels (Result) to binary
df['Lung_Cancer'] = df['Lung_Cancer'].map({1: 1, 0: 0})

# Split features & labels
X = df.drop(columns=['Lung_Cancer'])  # Features
y = df['Lung_Cancer']                 # Target variable

# Normalize data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split into training & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print preprocessed data
print("Preprocessed Data (First 5 Rows):\n", df.head())

# Train ML Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
