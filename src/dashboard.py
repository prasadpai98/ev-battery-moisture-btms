"""
==========================================================
Dashboard Module
Battery Pack Moisture Monitoring System
==========================================================

Displays the complete ECU results.

Author : Chaitanyarani Kiragi
"""
from battery_assessment import assess_battery
from gui_dashboard import DashboardGUI

# ==========================================================
# Create one GUI instance
# ==========================================================

gui = DashboardGUI()

# ==========================================================
# Utility
# ==========================================================

def progress_bar(value, title):

    bar_length = 30

    value = max(0, min(100, value))

    filled = int(bar_length * value / 100)

    bar = "█" * filled + "░" * (bar_length - filled)

    print(f"{title:<20} [{bar}] {value:.2f}%")


# ==========================================================
# Dashboard
# ==========================================================

def display(
    calibration,
    diagnostic,
    battery,
    thermal,
    maintenance,
    temperature=None,
    vpp=None
):

    print("\n")
    print("=" * 60)
    print("      BATTERY PACK MOISTURE MONITORING ECU")
    print("=" * 60)

    print("\n--------------- CALIBRATION ----------------")

    print(f"Estimated Humidity      : {calibration['humidity']} %")

    print(f"Measurement Valid       : {calibration['valid']}")

    print("\n--------------- DIAGNOSTICS ----------------")

    print(f"System Status           : {diagnostic['status']}")

    print(f"DTC                     : {diagnostic['dtc']}")

    print(f"Severity                : {diagnostic['severity']}")

    print(f"Diagnostic Confidence   : {diagnostic['diagnostics_confidence']} %")

    print()


    progress_bar(
        diagnostic["diagnostics_confidence"],
        "Confidence"
    )
    
    

    print()
    print("=" * 55)
    print("BATTERY ASSESSMENT")
    print("=" * 55)

    print(f"Battery Status          : {battery['battery_status']}")

    print(f"Moisture Risk          : {battery['moisture_risk']}")

    print(f"Corrosion Risk         : {battery['corrosion_risk']}")

    print(f"Moisture Ingress       : {battery['ingress']}")

    print(f"Maintenance Priority   : {battery['maintenance_priority']}")

    print(f"Recommended Action     : {battery['recommended_action']}")
    
    print(f"Risk Score           : {battery['risk_score']:.1f}/100")

    print(f"Battery Health       : {battery['battery_health']:.1f}%")

    print(f"Safety Index         : {battery['safety_index']:.1f}%")

    print(f"Protection Stage     : {battery['protection_stage']}")

    print(f"Protection Info      : {battery['protection_description']}")

    print("\nPrimary Cause(s):")

    for cause in battery["root_causes"]:
        print(f"  • {cause}")
    
    
    print("\n--------------- BATTERY THERMAL MANAGEMENT ---------------")

    print(f"Mode                : {thermal['mode']}")

    print(f"Cooling Fan         : {'ON' if thermal['fan'] else 'OFF'}")

    print(f"Heater              : {'ON' if thermal['heater'] else 'OFF'}")

    print(f"Fan Speed           : {thermal['fan_speed']} %")

    print(f"Target Temperature  : {thermal['target_temperature']} °C")

    print(f"Predicted Temp      : {thermal['predicted_temperature']} °C")

    print(f"Charging Limited    : {'YES' if thermal['charging_limit'] else 'NO'}")
    
    print("\n----------- PREDICTIVE MAINTENANCE ----------")

    print()

    print("Sensor Health")
    
    print(f"{'Sensor Health Index':<25}: {maintenance['sensor_health']:.2f} %")

    print()
    
    if maintenance["average_health"] is None:

        print(f"{'Average Health':<25}: N/A")

    else:

        print(
            f"{'Average Health':<25}: "
            f"{maintenance['average_health']:.2f} %"
        )

    print(f"{'Health Trend':<25}: {maintenance['trend']}")

    print(f"{'History Samples':<25}: {maintenance['samples']}")

    print(f"{'Health State':<25}: {maintenance['health_state']}")

    print(f"{'Maintenance Action':<25}: {maintenance['maintenance']}")
    
    progress_bar(
        maintenance["sensor_health"],
        "Sensor Health"
    )

    if maintenance["average_health"] is not None:

        progress_bar(
            maintenance["average_health"],
            "Average Health"
        )

    print("\n" + "=" * 60)

    if diagnostic["status"] == "HEALTHY":

        print("OVERALL SYSTEM STATUS : HEALTHY")

    else:

        print("OVERALL SYSTEM STATUS : ATTENTION REQUIRED")

    print("=" * 60)
    print()
    
    gui.update_dashboard(
            calibration,
            diagnostic,
            battery,
            thermal,
            maintenance,
            temperature,
            vpp
        )
    
    


