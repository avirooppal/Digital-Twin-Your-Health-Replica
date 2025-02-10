from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Drug effectiveness coefficients based on type
DRUG_COEFFICIENTS = {
    "Chemotherapy": {
        "direct_kill": 0.8,
        "growth_inhibition": 0.3,
        "half_life": 24  # hours
    },
    "Immunotherapy": {
        "direct_kill": 0.4,
        "growth_inhibition": 0.6,
        "half_life": 48  # hours
    },
    "Targeted Therapy": {
        "direct_kill": 0.6,
        "growth_inhibition": 0.5,
        "half_life": 36  # hours
    }
}

def tumor_growth(state, t, params):
    """Enhanced tumor growth model with drug-specific effects"""
    tumor_size, drug_conc = state
    
    if tumor_size <= 0.1:
        return [0, 0]
    
    # Unpack parameters
    carrying_capacity = params['tumor_carrying_capacity']
    base_growth_rate = params['tumor_growth_rate']
    drug_type = params['drug_type']
    
    # Calculate drug effects
    drug_coef = DRUG_COEFFICIENTS[drug_type]
    growth_inhibition = drug_coef['growth_inhibition'] * drug_conc
    direct_kill = drug_coef['direct_kill'] * drug_conc
    
    # Modified growth rate based on drug presence
    effective_growth_rate = base_growth_rate * (1 / (1 + growth_inhibition))
    
    # Tumor growth with drug effects
    dTdt = effective_growth_rate * tumor_size * (1 - tumor_size / carrying_capacity) - direct_kill * tumor_size
    
    # Drug clearance based on half-life
    dDdt = -np.log(2) / DRUG_COEFFICIENTS[drug_type]['half_life'] * drug_conc
    
    return [max(dTdt, -tumor_size), dDdt]

def simulate_treatment(patient, drug_type, dose):
    """Improved treatment simulation with realistic pharmacokinetics"""
    # Simulation parameters
    days = 150
    steps_per_day = 24
    time = np.linspace(0, days, days * steps_per_day)
    
    # Initial conditions
    initial_state = [patient['tumor_size'], 0.0]  # [tumor size, drug concentration]
    
    # Parameters for the ODE solver
    params = {
        'tumor_carrying_capacity': patient['tumor_carrying_capacity'],
        'tumor_growth_rate': patient['tumor_growth_rate'],
        'drug_type': drug_type
    }
    
    # Storage for results
    results = []
    current_state = initial_state.copy()
    
    # Simulate with daily dosing for first 5 days
    for t_start, t_end in zip(time[:-1], time[1:]):
        # Add drug dose at the start of each day for first 5 days
        if int(t_start) < 5 and abs(t_start - int(t_start)) < 1/steps_per_day:
            current_state[1] += dose / patient['body_weight']
        
        # Solve for this time step
        solution = odeint(
            tumor_growth,
            current_state,
            [t_start, t_end],
            args=(params,)
        )
        
        current_state = [
            max(0.1, solution[-1, 0]),  # Tumor size
            max(0, solution[-1, 1])     # Drug concentration
        ]
        results.append(current_state.copy())
    
    results = np.array(results)
    return time[1:], results[:, 0], results[:, 1]  # time, tumor sizes, drug concentrations

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        patient = request.json
        logging.debug(f"Received request: {patient}")
        
        results = []
        for dose, drug in zip(patient["drug_doses"], patient["drug_types"]):
            # Run simulation
            time, tumor_sizes, drug_concentrations = simulate_treatment(patient, drug, dose)
            
            # Calculate metrics
            initial_size = patient["tumor_size"]
            final_size = float(tumor_sizes[-1])  # Convert to Python float
            
            # Calculate reduction percentage
            reduction_percentage = float(max(0, ((initial_size - final_size) / initial_size) * 100))
            
            # Find time to half size
            time_to_half = next(
                (float(t) for t, s in zip(time, tumor_sizes) if s <= initial_size / 2),
                float('inf')
            )
            
            # Calculate effectiveness score
            reduction_speed = 1 / (time_to_half + 1) if time_to_half != float('inf') else 0
            sustained_effect = bool(np.mean(tumor_sizes[-len(tumor_sizes)//4:]) < initial_size / 2)  # Convert to Python bool
            side_effects_factor = 1 - (dose / max(patient["drug_doses"]) * 0.3)
            
            ranking_score = float(
                reduction_percentage * 0.4 +
                reduction_speed * 40 +
                (sustained_effect * 20) +
                side_effects_factor * 10
            )
            
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
        
        # Sort by ranking score
        results.sort(key=lambda x: -x["ranking_score"])
        best_treatment = results[0]
        
        return jsonify({
            "best_treatment": best_treatment,
            "all_results": results
        })
        
    except KeyError as e:
        logging.error(f"Missing key in request: {e}")
        return jsonify({"error": f"Missing required parameter: {str(e)}"}), 400
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)