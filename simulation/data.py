import pandas as pd
import requests

# 🚀 Step 1: Load the real-world lung cancer dataset
LUAD_URL = "https://raw.githubusercontent.com/cBioPortal/datahub/master/public/luad_tcga_pan_can_atlas_2018/data_clinical_patient.txt"
LUSC_URL = "https://raw.githubusercontent.com/cBioPortal/datahub/master/public/lusc_tcga_pan_can_atlas_2018/data_clinical_patient.txt"

# Choose either LUAD (Lung Adenocarcinoma) or LUSC (Lung Squamous Cell Carcinoma)
DATA_URL = LUAD_URL  # Change to LUSC_URL if needed

# Load dataset
data = pd.read_csv(DATA_URL, sep='\t', comment='#')

# 🚀 Step 2: Map Clinical Data to Simulation Parameters

# Define tumor sizes based on staging
stage_to_size = {
    'Stage I': 3.0,   # Tumor size ≤ 3 cm
    'Stage II': 4.5,  # Tumor size 3–5 cm
    'Stage III': 6.0, # Tumor size 5–7 cm
    'Stage IV': 8.0   # Tumor size > 7 cm (or metastatic)
}

# Map tumor stages to estimated tumor sizes
data['tumor_size'] = data['AJCC_PATHOLOGIC_TUMOR_STAGE'].map(stage_to_size)

# Assume a standard body weight (not provided in dataset)
data['body_weight'] = 70  # kg (adjust based on demographics)

# Assign tumor growth rate and carrying capacity
data['tumor_growth_rate'] = 0.02  # Per day, hypothetical value
data['tumor_carrying_capacity'] = 120  # Arbitrary units

# 🚀 Step 3: Assign Drug Types and Doses
standard_doses = {
    'Chemotherapy': 50,  # mg/kg
    'Immunotherapy': 3,  # mg/kg
    'Targeted Therapy': 7  # mg/kg
}

# Assign a combination of treatments to each patient
data['drug_types'] = [['Chemotherapy', 'Immunotherapy', 'Targeted Therapy']] * len(data)
data['drug_doses'] = [[standard_doses[drug] for drug in data['drug_types'].iloc[0]]] * len(data)

# 🚀 Step 4: Select a Patient for Simulation
patient = data.iloc[0].to_dict()  # Select first patient

# Prepare the data for the simulation API
simulation_input = {
    'tumor_size': patient['tumor_size'],
    'tumor_growth_rate': patient['tumor_growth_rate'],
    'tumor_carrying_capacity': patient['tumor_carrying_capacity'],
    'body_weight': patient['body_weight'],
    'drug_types': patient['drug_types'],
    'drug_doses': patient['drug_doses']
}

# 🚀 Step 5: Send Data to Flask API for Treatment Simulation
API_URL = "http://127.0.0.1:5000/simulate"  # Make sure your Flask app is running!

try:
    response = requests.post(API_URL, json=simulation_input)

    if response.status_code == 200:
        print("\n✅ Simulation Successful!")
        print(response.json())  # Print results
    else:
        print("\n❌ Error:", response.json())
except Exception as e:
    print("\n🚨 Failed to connect to API:", e)

