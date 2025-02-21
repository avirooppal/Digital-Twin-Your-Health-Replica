import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# 🚀 Step 1: Load Dataset
df = pd.read_csv("lung_cancer_data.csv")

# 🚀 Step 2: Create Binary Target Column from 'Stage_of_Cancer'
df['Has_Lung_Cancer'] = df['Stage_of_Cancer'].apply(lambda x: 1 if x != 'Stage 0' else 0)

# 🚀 Step 3: Feature Selection
features = [
    "Age", "Gender", "Smoking_History", "Years_Smoked", "Pack_Years", "Family_History_Cancer",
    "Exposure_to_Toxins", "BMI", "Lung_Function_Test_Result", "Chest_Pain_Symptoms",
    "Shortness_of_Breath", "Weight_Loss", "Physical_Activity_Level", "Dietary_Habits",
    "Air_Quality_Index", "Metastasis_Status", "Previous_Cancer_Diagnosis", "Treatment_Type"
]

target = "Has_Lung_Cancer"

df = df[features + [target]]

# 🚀 Step 4: Encode Categorical Variables
categorical_cols = ["Gender", "Smoking_History", "Physical_Activity_Level", "Dietary_Habits", "Treatment_Type"]

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoded_cats = pd.DataFrame(encoder.fit_transform(df[categorical_cols]), columns=encoder.get_feature_names_out())

# Save the encoder
joblib.dump(encoder, "encoder.pkl")

df.drop(columns=categorical_cols, inplace=True)
df = pd.concat([df, encoded_cats], axis=1)

# 🚀 Step 5: Normalize Numerical Features
num_cols = ["Age", "Years_Smoked", "Pack_Years", "BMI", "Lung_Function_Test_Result", "Air_Quality_Index"]
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Save the scaler
joblib.dump(scaler, "scaler.pkl")

# 🚀 Step 6: Train-Test Split (80% Train, 20% Test)
X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🚀 Step 7: Define the Neural Network Model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Output layer for binary classification
])

# 🚀 Step 8: Compile the Model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 🚀 Step 9: Train the Model
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2)

# 🚀 Step 10: Evaluate Model on Test Data
y_pred = (model.predict(X_test) > 0.5).astype("int32")

accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2f}")

# 🚀 Step 11: Confusion Matrix & Classification Report
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 🚀 Step 12: Plot ROC Curve
fpr, tpr, _ = roc_curve(y_test, model.predict(X_test))
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, color="blue", label=f"ROC curve (area = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")
plt.show()

# 🚀 Step 13: Save the Model
model.save("lung_cancer_model.keras")
print("Model and preprocessing tools saved successfully!")
