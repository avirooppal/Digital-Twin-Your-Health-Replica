# Digital Twin: Your Health Replica 👨‍⚕️

[![GitHub repo](https://badgen.net/badge/icon/github?icon=github&label=Repo)](https://github.com/avirooppal/Digital-Twin-Your-Health-Replica.git)
[![License](https://img.shields.io/github/license/avirooppal/Digital-Twin-Your-Health-Replica.git)](https://github.com/avirooppal/Digital-Twin-Your-Health-Replica.git/blob/main/LICENSE)


This project aims to create a digital twin of a patient's health, providing a personalized replica for improved healthcare management. This is a complex system with multiple components working together.


## 🚀 Usage

The application consists of three main parts:

1. **Simulation:** A Flask-based backend for simulating tumor growth using a machine learning model.  The simulation takes patient data as input and generates predictions. You can run it using:

   ```bash
   python simulation/app.py 
   ```

2. **Prediction:** A machine learning model (Keras) that predicts tumor growth based on various patient-specific features.

3. **Frontend:** A Next.js frontend application that provides a user-friendly interface to interact with the simulation and visualize results.  This frontend uses various UI components to create a clear and comprehensive user experience. You can start the development server with:

   ```bash
   cd FrontendDT
   npm run dev
   ```


The Frontend allows users to input patient data (through a wizard/form), submit it to the simulation backend, and view the simulated tumor growth in an interactive visualization.

## ⚙️ Installation

**Backend (Python):**

The simulation backend requires Python and several dependencies.  A virtual environment is recommended for managing dependencies:

```bash
cd simulation
python3 -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment (Linux/macOS)
.\venv\Scripts\activate   # Activate the virtual environment (Windows)
pip install -r requirements.txt  # Install dependencies
```

**Frontend (Next.js):**

The frontend requires Node.js and npm (or yarn). Navigate to the Frontend directory and install dependencies:

```bash
cd FrontendDT
npm install  # Or yarn install
```


This project's structure is designed for modularity and scalability. Each component (simulation, prediction, frontend) is contained in its own directory and can be developed and deployed independently.  Note that the frontend relies on the backend for processing simulation requests.

**Note:** A detailed project structure is available within the respective subdirectories (`simulation/`, `prediction/`, `FrontendDT/`).  The given file listing provides a comprehensive overview of the files and folders.  Deployment instructions will vary based on the chosen platform and require additional configuration steps.
