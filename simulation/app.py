import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app title
st.title("Digital Twin for Tumor Treatment Simulation")
st.markdown("### AI-Powered Tumor Growth Prediction and Drug Simulation")

# User input for patient parameters
st.sidebar.header("Patient Parameters")
tumor_size = st.sidebar.number_input("Initial Tumor Size (cm³)", min_value=0.1, value=5.0)
carrying_capacity = st.sidebar.number_input("Tumor Carrying Capacity", min_value=1.0, value=10.0)
growth_rate = st.sidebar.number_input("Tumor Growth Rate", min_value=0.01, value=0.02, format="%.3f")
body_weight = st.sidebar.number_input("Patient Body Weight (kg)", min_value=30, value=70)

# Drug selection
st.sidebar.header("Treatment Selection")
drug_types = st.sidebar.multiselect("Select Drug Types", ["Chemotherapy", "Immunotherapy", "Targeted Therapy"], default=["Chemotherapy"])
drug_doses = [st.sidebar.slider(f"Dose for {drug} (mg/kg)", min_value=0, max_value=100, value=50) for drug in drug_types]

# API request payload
patient_data = {
    "tumor_size": tumor_size,
    "tumor_carrying_capacity": carrying_capacity,
    "tumor_growth_rate": growth_rate,
    "body_weight": body_weight,
    "drug_types": drug_types,
    "drug_doses": drug_doses
}

# API endpoint
API_URL = "http://127.0.0.1:5000/simulate"

if st.sidebar.button("Simulate Treatment"):
    with st.spinner("Running Simulation..."):
        response = requests.post(API_URL, json=patient_data)
        
        if response.status_code == 200:
            data = response.json()
            best_treatment = data["best_treatment"]
            all_results = data["all_results"]
            
            # Extract data for visualization
            st.success(f"Best Treatment: {best_treatment['drug']} with {best_treatment['dose']} mg/kg")
            tumor_sizes = [result["final_tumor_size"] for result in all_results]
            drug_names = [result["drug"] for result in all_results]
            
            # Plot results
            fig, ax = plt.subplots()
            ax.bar(drug_names, tumor_sizes, color=['blue', 'green', 'red'])
            ax.set_xlabel("Drug Type")
            ax.set_ylabel("Final Tumor Size (cm³)")
            ax.set_title("Effectiveness of Different Drug Treatments")
            st.pyplot(fig)
        else:
            st.error("Error: Unable to fetch simulation results.")

# Digital Twin Features
st.markdown("## Features of Our Digital Twin")
st.markdown("### 1. **Prediction Model**")
st.markdown("- Uses AI-based models to forecast tumor growth based on patient data.")
st.markdown("- Considers patient-specific parameters like tumor size, growth rate, and drug response.")

st.markdown("### 2. **Simulation Model**")
st.markdown("- Simulates different drug treatments to analyze their impact on tumor reduction.")
st.markdown("- Provides a ranking score based on effectiveness, side effects, and tumor reduction speed.")

st.markdown("### 3. **Visualization & Decision Support**")
st.markdown("- Interactive visual charts to compare treatment options.")
st.markdown("- Helps doctors and researchers make data-driven decisions for personalized medicine.")
