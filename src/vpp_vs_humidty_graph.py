from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Load characterization database
# --------------------------------------------------

df = pd.read_csv(
    str(_ROOT / "Database" / "characterization_database.csv")
)

# --------------------------------------------------
# Plot VPP vs Humidity for each temperature
# --------------------------------------------------

temperatures = sorted(df["Temperature"].unique())

plt.figure(figsize=(10, 6))

for temperature in temperatures:

    data = df[df["Temperature"] == temperature]

    plt.plot(
        data["Humidity"],
        data["VPP"],
        marker="o",
        label=f"{temperature} °C"
    )

# --------------------------------------------------
# Labels
# --------------------------------------------------

plt.xlabel("Humidity (%RH)")
plt.ylabel("Peak-to-Peak Voltage (V)")
plt.title("Humidity Sensor Characterization: VPP vs Humidity")

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.show()