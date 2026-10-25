from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# Load Characterization Database
# ==========================================================

df = pd.read_csv(
    str(_ROOT / "Database" / "characterization_database.csv")
)


# ==========================================================
# Fixed Humidity Condition
# ==========================================================

target_humidity = 40


# ==========================================================
# Temperature Compensation Parameters
# ==========================================================

REFERENCE_TEMPERATURE = 25.0

K_TEMP = 0.0002525


# ==========================================================
# Select Data for 40% RH
# ==========================================================

data = df[df["Humidity"] == target_humidity].copy()


# Sort by temperature

data = data.sort_values("Temperature")


# ==========================================================
# Extract Temperature and Measured VPP
# ==========================================================

temperature = data["Temperature"].to_numpy()

measured_vpp = data["VPP"].to_numpy()


# ==========================================================
# Temperature Compensation
# ==========================================================

corrected_vpp = (
    measured_vpp
    - K_TEMP * (temperature - REFERENCE_TEMPERATURE)
)


# ==========================================================
# Print Results
# ==========================================================

print("\nTemperature Compensation Results")
print("--------------------------------")

for T, raw, corrected in zip(
    temperature,
    measured_vpp,
    corrected_vpp
):

    print(
        f"T = {T:5.1f} °C   "
        f"Measured VPP = {raw:.6f} V   "
        f"Corrected VPP = {corrected:.6f} V"
    )


# ==========================================================
# Plot
# ==========================================================

plt.figure(figsize=(10, 6))


# Raw VPP

plt.plot(
    temperature,
    measured_vpp,
    marker="o",
    label="Measured VPP"
)


# Temperature compensated VPP

plt.plot(
    temperature,
    corrected_vpp,
    marker="s",
    linestyle="--",
    label="Temperature Compensated VPP"
)


# ==========================================================
# Labels
# ==========================================================

plt.xlabel("Temperature (°C)")

plt.ylabel("VPP (V)")

plt.title(
    "Temperature Compensation of Humidity Sensor\n"
    f"Humidity = {target_humidity}%RH | "
    f"Reference Temperature = {REFERENCE_TEMPERATURE:.0f}°C"
)


# ==========================================================
# Grid and Legend
# ==========================================================

plt.grid(True)

plt.legend()


# ==========================================================
# Layout
# ==========================================================

plt.tight_layout()

plt.show()