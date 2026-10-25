import matplotlib.pyplot as plt


# ==========================================================
# Test Condition
# ==========================================================

humidity = 40
temperature = 26


# ==========================================================
# Actual Measured Sensor Health Results
# ==========================================================

fault_conditions = [
    "Healthy",
    "Open Harness",
    "STG",
    "STB"
]

sensor_health = [
    99.67,
    44.00,
    43.74,
    44.00
]


# ==========================================================
# Average Sensor Health
# ==========================================================

average_health = 66.18


# ==========================================================
# Create Plot
# ==========================================================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    fault_conditions,
    sensor_health,
    label=f"Test condition: {humidity}%RH, {temperature}°C"
)


# ==========================================================
# Axis Labels and Title
# ==========================================================

plt.xlabel("Operating / Fault Condition")

plt.ylabel("Sensor Health (%)")

plt.title(
    "Sensor Health Under Fault Injection\n"
    f"Humidity = {humidity}%RH | Temperature = {temperature}°C"
)


# ==========================================================
# Y-axis
# ==========================================================

plt.ylim(0, 105)


# ==========================================================
# Display Values Above Bars
# ==========================================================

for bar, value in zip(bars, sensor_health):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{value:.2f}%",
        ha="center",
        va="bottom"
    )


# ==========================================================
# Average Health Line
# ==========================================================

plt.axhline(
    average_health,
    linestyle="--",
    label=f"Average Sensor Health = {average_health:.2f}%"
)


# ==========================================================
# Grid and Legend
# ==========================================================

plt.grid(
    axis="y",
    alpha=0.3
)

plt.legend()


# ==========================================================
# Layout
# ==========================================================

plt.tight_layout()

plt.show()