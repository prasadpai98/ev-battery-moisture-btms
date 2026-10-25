from battery_assessment import assess_battery
import matplotlib.pyplot as plt

humidity_values = [
    0,
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100
]

diagnostic_result = {
    "status": "HEALTHY",
    "diagnostics_confidence": 99.9
}

sensor_health = 100

risk_scores = []

for humidity in humidity_values:

    battery = assess_battery(
        humidity,
        diagnostic_result,
        sensor_health
    )

    risk_scores.append(
        battery["risk_score"]
    )
    
print("\nRisk Score vs Humidity")
print("-----------------------")

for humidity, risk in zip(humidity_values, risk_scores):

    print(
        f"Humidity = {humidity:3d}%  "
        f"Risk Score = {risk:.2f}"
    )   
    
plt.figure(figsize=(9, 5))

plt.plot(
    humidity_values,
    risk_scores,
    marker="o"
)

plt.xlabel("Humidity (%RH)")
plt.ylabel("Risk Score")
plt.title(
    "Battery Risk Score vs Humidity\n"
    "Temperature = 26°C, Diagnostics = HEALTHY, Sensor Health = 100%"
)

plt.ylim(0, 105)

plt.grid(True)

plt.tight_layout()

plt.show()