import requests

URL = "http://127.0.0.1:5000/simulate"

patient_data = {
    "tumor_size": 5.0,
    "tumor_carrying_capacity": 10.0,
    "tumor_growth_rate": 0.02,
    "body_weight": 70,
    "drug_types": ["Chemotherapy", "Immunotherapy"],
    "drug_doses": [50, 30]
}

response = requests.post(URL, json=patient_data)
print(response.json())
