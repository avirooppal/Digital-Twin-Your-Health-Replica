import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import logging
import pickle

app = Flask(__name__)
CORS(app)  # Allow CORS for all origins
# CORS(app, origins=["http://localhost:5173"])  # Use this for specific frontend

logging.basicConfig(level=logging.DEBUG)

MODEL_FILE = "tumor_model.pkl"

# Drug effectiveness coefficients
DRUG_COEFFICIENTS = {
    "Chemotherapy": {"direct_kill": 0.8, "growth_inhibition": 0.3, "half_life": 24},
    "Immunotherapy": {"direct_kill": 0.4, "growth_inhibition": 0.6, "half_life": 48},
    "Targeted Therapy": {"direct_kill": 0.6, "growth_inhibition": 0.5, "half_life": 36},
}

# Tumor growth model
def tumor_growth(state, t, params):
    tumor_size, drug_conc = state
    if tumor_size <= 0.1:
        return [0, 0]

    carrying_capacity = params['tumor_carrying_capacity']
    base_growth_rate = params['tumor_growth_rate']
    drug_type = params['drug_type']
    
    drug_coef = DRUG_COEFFICIENTS[drug_type]
    growth_inhibition = drug_coef['growth_inhibition'] * drug_conc
    direct_kill = drug_coef['direct_kill'] * drug_conc

    effective_growth_rate = base_growth_rate * (1 / (1 + growth_inhibition))
    dTdt = effective_growth_rate * tumor_size * (1 - tumor_size / carrying_capacity) - direct_kill * tumor_size
    dDdt = -np.log(2) / drug_coef['half_life'] * drug_conc

    return [max(dTdt, -tumor_size), dDdt]

# Treatment simulation
def simulate_treatment(patient, drug_type, dose):
    days = 150
    steps_per_day = 24
    time = np.linspace(0, days, days * steps_per_day)
    
    initial_state = [patient['tumor_size'], 0.0]
    params = {
        'tumor_carrying_capacity': patient['tumor_carrying_capacity'],
        'tumor_growth_rate': patient['tumor_growth_rate'],
        'drug_type': drug_type
    }
    
    results = []
    current_state = initial_state.copy()
    
    for t_start, t_end in zip(time[:-1], time[1:]):
        if int(t_start) < 5 and abs(t_start - int(t_start)) < 1 / steps_per_day:
            current_state[1] += dose / patient['body_weight']
        
        solution = odeint(tumor_growth, current_state, [t_start, t_end], args=(params,))
        current_state = [max(0.1, solution[-1, 0]), max(0, solution[-1, 1])]
        results.append(current_state.copy())

    results = np.array(results)
    return time[1:], results[:, 0], results[:, 1]

# Save & Load Model
def save_model():
    with open(MODEL_FILE, "wb") as f:
        pickle.dump((tumor_growth, simulate_treatment), f)

def load_model():
    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)

# Handle OPTIONS request (CORS preflight)
@app.route('/simulate', methods=['OPTIONS'])
def handle_options():
    response = jsonify({"message": "CORS Preflight OK"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# Simulation API Route
@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        patient = request.json
        logging.debug(f"Received request: {patient}")
        results = []
        
        for dose, drug in zip(patient["drug_doses"], patient["drug_types"]):
            time, tumor_sizes, drug_concentrations = simulate_treatment(patient, drug, dose)
            initial_size, final_size = patient["tumor_size"], float(tumor_sizes[-1])
            reduction_percentage = float(max(0, ((initial_size - final_size) / initial_size) * 100))
            
            time_to_half = next((float(t) for t, s in zip(time, tumor_sizes) if s <= initial_size / 2), float('inf'))
            reduction_speed = 1 / (time_to_half + 1) if time_to_half != float('inf') else 0
            sustained_effect = bool(np.mean(tumor_sizes[-len(tumor_sizes)//4:]) < initial_size / 2)
            side_effects_factor = 1 - (dose / max(patient["drug_doses"]) * 0.3)
            ranking_score = float(reduction_percentage * 0.4 + reduction_speed * 40 + (sustained_effect * 20) + side_effects_factor * 10)
            
            results.append({
                "drug": drug,
                "dose": float(dose),
                "final_tumor_size": round(final_size, 2),
                "tumor_reduction_percent": round(reduction_percentage, 2),
                "time_to_half_size": round(time_to_half, 2) if time_to_half != float('inf') else None,
                "ranking_score": round(ranking_score, 2),
                "sustained_effect": sustained_effect,
                "side_effects_risk": round(float(1 - side_effects_factor) * 100, 2)
            })
        
        results.sort(key=lambda x: -x["ranking_score"])
        return jsonify({"best_treatment": results[0], "all_results": results})

    except KeyError as e:
        logging.error(f"Missing key in request: {e}")
        return jsonify({"error": f"Missing required parameter: {str(e)}"}), 400
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    save_model()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
