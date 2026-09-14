import numpy as np
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# =====================================================
# VEHICLE PARAMETERS
# =====================================================

rho = 1.225
Cd = 0.16
A = 1.5
Crr = 0.015
m = 260
g = 9.81
motor_eff = 0.75        # realistic total losses
aux_power = 400         # realistic electronics load
battery_Wh = 4960

solar_area = 3.51
solar_eff = 0.22


# =====================================================
# PHYSICS ENERGY MODEL
# =====================================================

def power_required(v):
    aero = 0.5 * rho * Cd * A * v**3
    roll = Crr * m * g * v
    return (aero + roll + aux_power) / motor_eff

def energy_per_km(speed_kmh):
    v = speed_kmh / 3.6
    return power_required(v) / speed_kmh


# =====================================================
# 1️⃣ ENERGY vs SPEED
# =====================================================

full_speeds = np.linspace(10, 70, 300)
full_energies = np.array([energy_per_km(s) for s in full_speeds])

opt_idx = np.argmin(full_energies)
opt_speed = full_speeds[opt_idx]
opt_energy = full_energies[opt_idx]

print(f"\nOptimal Speed = {opt_speed:.2f} km/h")
print(f"Minimum Energy = {opt_energy:.2f} Wh/km\n")

speeds = np.linspace(opt_speed, 70, 200)
energies = np.array([energy_per_km(s) for s in speeds])

plt.figure(figsize=(7,5))
plt.plot(speeds, energies)
plt.scatter(opt_speed, opt_energy)
plt.xlabel("Speed (km/h)")
plt.ylabel("Energy (Wh/km)")
plt.title("Energy Consumption vs Speed")
plt.grid()
plt.show()


# =====================================================
# 2️⃣ RANGE vs SOLAR IRRADIANCE
# =====================================================

irr = np.linspace(200, 1000, 80)
ranges = []

for G in irr:
    solar_Wh = solar_eff * solar_area * G * 3
    total = battery_Wh + solar_Wh
    ranges.append(total / opt_energy)

plt.figure(figsize=(7,5))
plt.plot(irr, ranges)
plt.xlabel("Solar Irradiance (W/m²)")
plt.ylabel("Range (km)")
plt.title("Range vs Solar Irradiance")
plt.grid()
plt.show()


# =====================================================
# 3️⃣ METHOD COMPARISON
# =====================================================

def range_for(speed):
    return battery_Wh / energy_per_km(speed)

vals = [range_for(40), range_for(30), range_for(opt_speed)]
plt.figure(figsize=(6,5))
plt.bar(["40 km/h", "30 km/h", "Optimized"], vals)
for i, v in enumerate(vals):
    plt.text(i, v+1, f"{v:.1f}", ha='center')
plt.ylabel("Range (km)")
plt.title("Method Comparison")
plt.show()


# =====================================================
# 4️⃣ SOC PREDICTION (Physics + Classical vs QNN)
# =====================================================

time = np.linspace(0, 36000, 1200)   # 10 hours

speed_profile = 30 + 6*np.sin(time/600)

energy_used = []
E = 0

for v in speed_profile:
    E += energy_per_km(v) * (v/3600)
    energy_used.append(E)

energy_used = np.array(energy_used)

true_soc = 100 * (1 - energy_used/battery_Wh)

# realistic nonlinear battery effects
true_soc += 0.4*np.sin(time/500)
true_soc += 0.3*np.cos(time/900)
true_soc += np.random.normal(0, 0.15, len(time))

true_soc = np.clip(true_soc, 0, 100)


# =====================================================
# FEATURES
# =====================================================

X = np.vstack([
    speed_profile,
    energy_used,
    time/3600
]).T

y = true_soc


# =====================================================
# ⭐ SCALE FEATURES (CRITICAL — fixes your error)
# =====================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# =====================================================
# Classical baseline (linear)
# =====================================================

baseline = LinearRegression()
baseline.fit(X_scaled, y)
baseline_pred = np.clip(baseline.predict(X_scaled), 0, 100)


# =====================================================
# QNN proxy (tuned)
# =====================================================

qnn = MLPRegressor(hidden_layer_sizes=(64,64),
                   alpha=0.0005,
                   max_iter=6000,
                   random_state=0)

qnn.fit(X_scaled, y)
qnn_pred = np.clip(qnn.predict(X_scaled), 0, 100)


# =====================================================
# METRICS
# =====================================================

rmse_base = np.sqrt(mean_squared_error(y, baseline_pred))
rmse_qnn = np.sqrt(mean_squared_error(y, qnn_pred))

print(f"Baseline RMSE = {rmse_base:.3f}")
print(f"QNN Proxy RMSE = {rmse_qnn:.3f}")


# =====================================================
# PLOT SOC COMPARISON
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(time/60, y, label="True SOC", linewidth=3)
plt.plot(time/60, baseline_pred, "--", label="Classical Estimator")
plt.plot(time/60, qnn_pred, label="QNN Prediction")

plt.xlabel("Time (min)")
plt.ylabel("SOC (%)")
plt.title("SOC Prediction Comparison")
plt.legend()
plt.grid(alpha=0.3)

plt.xlim(0, 600)
plt.ylim(94, 100)
plt.tight_layout()

plt.show()
