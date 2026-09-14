# Energy Management & Cruising Speed Optimization in Solar EVs (Indian Patent IN202541126599 A1)

[![Patent Status](https://img.shields.io/badge/Patent%20Status-Published%20(IN202541126599%20A1)-success)](file:///C:/Users/Anvesha/.gemini/antigravity/scratch/solar_patent/patent.pdf)
[![Applicant](https://img.shields.io/badge/Applicant-MAHE%20Manipal-blue)](https://www.manipal.edu/)
[![IPC Classification](https://img.shields.io/badge/IPC-G06N%20%7C%20G01R-orange)]()
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

> **Official Repository for Indian Patent Application:**  
> *"A system and method for energy management and cruising speed optimization in solar electric vehicles"*  
> **Application No:** `202541126599` | **Publication No:** `IN202541126599 A1`  
> **Filing Date:** December 14, 2025 | **Publication Date:** June 26, 2026 (Journal No: 26/2026)

---

## 📌 Patent Metadata & Inventorship

* **Inventor:** **Anvesha Singh**
* **Applicant:** **Manipal Academy of Higher Education (MAHE)**, Madhav Nagar, Manipal, 576104, Karnataka, India.
* **Patent Agent:** Adv. Pranav Bhat (`IN/PA 4580`)
* **International Patent Classification (IPC):** `G06N 3/08`, `G06N 3/04`, `G01R 31/367`, `G01R 31/392`, `G01R 31/382`

---

## 📖 Abstract & Technological Overview

This invention discloses a unified **Solar Electric Vehicle Energy Management System (101)** that solves the coupled challenges of non-linear State-of-Charge (SOC) estimation and dynamic range optimization.

Existing battery management systems suffer from cumulative numerical drift and errors when modeling complex non-linear interactions between intermittent photovoltaic (PV) generation, fluctuating traction loads, regenerative braking, and temperature variations. Simultaneously, traditional driving strategies rely on fixed speeds or heuristic rules, leading to suboptimal energy consumption.

The present system addresses these deficiencies through two core innovations:
1. **Hybrid Quantum-Classical Neural Network (QNN) Framework:** Employs parameterized quantum circuits to capture high-dimensional non-linear feature entanglements, improving short-horizon SOC prediction accuracy (**7.7% RMSE reduction** over classical estimators).
2. **Deterministic Newton-Raphson Cruising Speed Optimizer:** An electronic controller (311) executing an iterative root-finding algorithm to converge on the exact minimum-energy cruising speed (**39.90 km/h at 34.22 Wh/km**), expanding driving range by **16.8 km**.

---

## 🏗️ System Architecture & Sub-Modules

The central electronic controller (**311**) comprises five specialized computational sub-modules (**311A – 311E**) operating in sequence:

```mermaid
flowchart TD
    subgraph Data Acquisition
        S1["Traction Battery Telemetry (301)"] 
        S2["Photovoltaic Array Sensors (303)"] 
        S3["Vehicle Speed & Road Sensors"] 
    end

    Data Acquisition --> Input["Input Interface (309)<br>& Feature Normalization"]

    subgraph Electronic Controller (311)
        Input --> A["311A: Resistive-Force Computation Module<br>(Rolling, Aero, Gradient, Inertia)"]
        A --> B["311B: Torque & Power Estimation Module<br>(Wheel Torque, Motor RPM, Gross Power)"]
        B --> C["311C: Motor-Efficiency Estimation Module<br>(Multi-D Efficiency Map Interpolation)"]
        Input --> D["311D: Solar Contribution Determination Module<br>(PV Output Accounting & Irradiance Mapping)"]
        
        B & C & D --> E["311E: Energy Management Module<br>(Newton-Raphson Iterative Optimization)"]
    end

    subgraph Output & Actuation
        E --> Command["Optimized Cruising Speed Command<br>v_opt = 39.90 km/h"]
        Command --> MC["Motor Controller (307)<br>& BLDC Traction Motor (305)"]
        E --> QNN["Quantum Neural Network Engine<br>Short-Horizon SOC Forecast (RMSE 0.346)"]
    end
```

### Module Functional Breakdown:

| Module | Reference | Primary Function & Mathematical Description |
| :--- | :---: | :--- |
| **Resistive-Force Computation** | `311A` | Computes total resistive force $F_{\text{res}} = F_{\text{roll}} + F_{\text{aero}} + F_{\text{grad}} + F_{\text{inertial}}$. <br> $F_{\text{roll}} = C_{\text{rr}} \cdot m \cdot g = 0.015 \times 260 \times 9.81 = 38.26\text{ N}$. <br> $F_{\text{aero}} = 0.5 \cdot \rho \cdot C_d \cdot A \cdot v^2 = 0.5 \times 1.225 \times 0.16 \times 1.5 \times v^2$. |
| **Torque & Power Estimation** | `311B` | Calculates required wheel torque $T_{\text{wheel}} = F_{\text{res}} \cdot r_{\text{wheel}}$ ($r = 224.06\text{ mm}$), motor speed (direct drive 1:1, rated 898 RPM, peak 1017 RPM), and gross electrical power demand $P_{\text{gross}} = P_{\text{mech}} / \eta_{\text{motor}}$. |
| **Motor-Efficiency Estimation** | `311C` | Interpolates real-time operating efficiency $\eta_{\text{motor}}$ from stored 2D torque-speed maps for a 72V, 3000W rated / 6000W peak BLDC hub motor (nominal efficiency 92%). |
| **Solar Contribution Determination**| `311D` | Calculates PV harvesting power $P_{\text{solar}} = G \cdot A_{\text{pv}} \cdot \eta_{\text{pv}}$ ($A_{\text{pv}} = 3.51\text{ m}^2, \eta_{\text{pv}} = 20\%$). Generates $421\text{ W}$ at $600\text{ W/m}^2$ and $561\text{ W}$ at $800\text{ W/m}^2$, extending range by up to **31%**. |
| **Energy Management (Optimizer)** | `311E` | Applies Newton-Raphson root-finding to solve $\frac{d}{dv}\left( \frac{P_{\text{gross}}(v) - P_{\text{solar}}}{v} \right) = 0$, converging on **$v_{\text{opt}} = 39.90\text{ km/h}$** and **$E_{\text{min}} = 34.22\text{ Wh/km}$**. |

---

## 📐 Mathematical Formulation & Physics Model

### 1. Specific Energy Consumption Formulation
The net specific energy consumption $E_{\text{net}}(v)$ in $\text{Wh/km}$ for a vehicle traveling at speed $v$ ($\text{m/s}$) is given by:

$$E_{\text{net}}(v) = \frac{P_{\text{gross}}(v) - P_{\text{solar}}}{3.6 \cdot v}$$

Where gross electrical power $P_{\text{gross}}(v)$ accounts for rolling resistance, aerodynamic drag, auxiliary load, and motor efficiency:

$$P_{\text{gross}}(v) = \frac{\left( C_{\text{rr}} m g + \frac{1}{2} \rho C_d A v^2 \right) v + P_{\text{aux}}}{\eta_{\text{motor}}(v, T_{\text{motor}})}$$

### 2. Newton-Raphson Speed Optimization
Module `311E` iteratively updates the cruising speed estimate $v^{(k)}$ until convergence:

$$v^{(k+1)} = v^{(k)} - \frac{R(v^{(k)})}{J_R(v^{(k)})}$$

Where $R(v)$ is the terminal SOC residual function over the 150 km target distance, and $J_R(v)$ is its Jacobian with respect to speed.

---

## 📊 Quantifiable Validation & Benchmark Results

The system performance was validated on a 150 km target journey with a 4960 Wh traction battery pack (72V) and a 260 kg vehicle mass:

### 1. Driving Strategy Performance Comparison (Table 1 of Patent)

| Cruising Strategy | Speed (km/h) | Specific Energy (Wh/km) | Achievable Range (km) | Comparative Technical Advantage |
| :--- | :---: | :---: | :---: | :--- |
| **Fixed Speed Strategy 1** | 30.00 km/h | 35.73 Wh/km | 138.8 km | **Suboptimal:** Extended trip duration increases time-dependent auxiliary & rolling losses. |
| **Fixed Speed Strategy 2** | 40.00 km/h | 34.22 Wh/km | 144.9 km | Near minimum, but static; cannot adapt to mass, slope, or solar irradiance changes. |
| **Optimized System (Invention)**| **39.90 km/h** | **34.22 Wh/km** | **144.9 km** | **Optimal & Adaptive:** Achieves minimum energy point, saving **9.7 Wh/km** & adding **16.8 km** range over non-optimized baselines. |

### 2. Quantum Neural Network (QNN) SOC Prediction Accuracy

| Estimator Model | Root Mean Square Error (RMSE) | Performance vs. True SOC Trace |
| :--- | :---: | :--- |
| **Classical Estimator (EKF / Linear)** | `0.375` | Diverges after ~200 mins; fails to capture short-term PV/braking transients. |
| **QNN Proxy / Quantum Circuit (Ours)** | **`0.346`** | **7.7% Accuracy Improvement:** Accurately tracks dynamic transients across 550+ mins. |

---

## 📂 Repository Structure

```
solar_patent/
├── patent.pdf              # Official Indian Patent Journal Publication (IN202541126599 A1)
├── anvesha_patent.py       # Python simulation script (Energy vs Speed, QNN vs Classical SOC)
├── MI106.docx              # Complete Patent Specification Manuscript
├── MI106 FORM 1.docx       # Official Patent Application Form 1
└── MI106_DRAWINGS.pptx     # Patent Engineering Schematics & Diagrams (FIGs 1 to 5D)
```

---

## 🚀 Running the Python Simulation

### Installation
Ensure Python 3.9+ and required packages are installed:
```bash
pip install numpy matplotlib scikit-learn
```

### Execution
Run the full optimization and SOC benchmark script:
```bash
python anvesha_patent.py
```

---

## 📜 Patent Citation

To reference this patent application or legal specification:

```bibtex
@patent{singh2026solarev,
  title        = {A system and method for energy management and cruising speed optimization in solar electric vehicles},
  author       = {Singh, Anvesha},
  number       = {IN202541126599 A1},
  year         = {2026},
  month        = jun,
  day          = {26},
  holder       = {Manipal Academy of Higher Education (MAHE)},
  url          = {https://github.com/ASingh2425/solar_patent}
}
```

---
*Maintained by Anvesha Singh, Manipal Academy of Higher Education (MAHE), Manipal.*
