import matplotlib.pyplot as plt

humidity = 10
temperature = 26

healthy_vpp = 1.08311       # <-- put actual fault_mode=0 VPP here
fault_vpp = 0.014419

conditions = [
    "Healthy Sensor",
    "Open Harness"
]

vpp_values = [
    healthy_vpp,
    fault_vpp
]

plt.figure(figsize=(8, 5))

bars = plt.bar(conditions, vpp_values)

plt.ylabel("Measured VPP (V)")
plt.xlabel("Sensor Condition")

plt.title(
    f"Sensor Output Under Fault Injection\n"
    f"RH = {humidity}%RH, T = {temperature}°C"
)

# Show exact values above bars
for bar, value in zip(bars, vpp_values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.4f} V",
        ha="center",
        va="bottom"
    )

plt.grid(axis="y")
plt.tight_layout()
plt.show()