import tensorflow as tf
import numpy as np
import pandas as pd
import joblib

def load_model(model_path):
    """Load the trained Keras model."""
    return tf.keras.models.load_model(model_path)

def load_preprocessing_tools(scaler_path, encoder_path, categorical_cols):
    """Load the pre-fitted scaler and encoder."""
    scaler = joblib.load(scaler_path)
    encoder = joblib.load(encoder_path)
    encoder_categories = encoder.get_feature_names_out(categorical_cols)
    return scaler, encoder, encoder_categories

def get_user_input(categorical_cols, num_cols):
    """Prompt user for input values and preprocess them accordingly."""
    user_data = {}
    
    # Collect numerical input
    for col in num_cols:
        while True:
            try:
                user_data[col] = float(input(f"Enter {col} (numeric value): "))
                break
            except ValueError:
                print(f"Invalid input! Please enter a numeric value for {col}.")
    
    # Collect categorical input
    for col in categorical_cols:
        user_data[col] = input(f"Enter {col} (choose a valid category): ")
    
    return user_data

def preprocess_input(user_data, categorical_cols, num_cols, scaler, encoder, encoder_categories):
    """Convert user input into a format suitable for model prediction."""
    user_df = pd.DataFrame([user_data])
    
    # Encode categorical features
    encoded_cats = pd.DataFrame(encoder.transform(user_df[categorical_cols]), columns=encoder_categories)
    
    # Scale numerical features
    user_df[num_cols] = scaler.transform(user_df[num_cols])
    
    # Combine both numerical and encoded categorical features
    user_df = user_df.drop(columns=categorical_cols)
    user_df = pd.concat([user_df, encoded_cats], axis=1)
    
    return user_df

def interpret_result(prediction):
    """Interpret model output for cancer prediction."""
    return "🔴 High Risk of Lung Cancer" if prediction >= 0.5 else "🟢 Low Risk of Lung Cancer"

def main():
    model_path = "lung_cancer_model.keras"
    scaler_path = "scaler.pkl"
    encoder_path = "encoder.pkl"
    
    categorical_cols = ["Gender", "Smoking_History", "Physical_Activity_Level", "Dietary_Habits", "Treatment_Type"]
    num_cols = ["Age", "Years_Smoked", "Pack_Years", "BMI", "Lung_Function_Test_Result", "Air_Quality_Index"]
    
    model = load_model(model_path)
    scaler, encoder, encoder_categories = load_preprocessing_tools(scaler_path, encoder_path, categorical_cols)
    
    print("\n🚀 Lung Cancer Prediction System 🚀")
    print("Provide the required information below:")
    
    while True:
        user_data = get_user_input(categorical_cols, num_cols)
        processed_input = preprocess_input(user_data, categorical_cols, num_cols, scaler, encoder, encoder_categories)
        prediction = model.predict(processed_input)[0][0]
        
        print("\n🧪 Prediction Result:")
        print(interpret_result(prediction))
        
        again = input("\nDo you want to make another prediction? (yes/no): ").strip().lower()
        if again not in ["yes", "y"]:
            print("\n📌 Exiting... Stay healthy! 💙")
            break

if __name__ == "__main__":
    main()
