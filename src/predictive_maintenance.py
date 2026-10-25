"""
==========================================================
Predictive Maintenance Module
Battery Pack Moisture Monitoring System
==========================================================

Features
--------
1. Sensor Health Index (SHI)
2. Health Classification
3. Maintenance Recommendation

Author : Chaitanyarani Kiragi
"""

from history_manager import load_history

# ==========================================================
# Calculate Trend
# ==========================================================

def calculate_trend(samples=10):

    history = load_history()   # Read enough history

    history = load_history()

    history = history.tail(samples).reset_index(drop=True)
    if len(history) < 2:

        return {

            "average_health": None,

            "trend_value": 0,

            "trend": "INSUFFICIENT DATA",

            "samples": len(history)

        }

    health = history["Sensor_Health"]

    average = round(health.mean(), 2)

    trend_value = round(

        health.iloc[-1] - health.iloc[0],

        2

    )

    if trend_value >= -1:

        trend = "STABLE"

    elif trend_value >= -5:

        trend = "SLOW DEGRADATION"

    elif trend_value >= -10:

        trend = "MODERATE DEGRADATION"

    else:

        trend = "RAPID DEGRADATION"

    return {

        "average_health": average,

        "trend_value": trend_value,

        "trend": trend,

        "samples": len(history)

    }
    
# ==========================================================
# Configuration
# ==========================================================

CONFIDENCE_WEIGHT = 0.50
SEVERITY_WEIGHT = 0.30
VALIDITY_WEIGHT = 0.20

# ==========================================================
# Severity Scores
# ==========================================================

SEVERITY_SCORE = {

    "NORMAL": 100,

    "WARNING": 70,

    "CRITICAL": 20

}

# ==========================================================
# Health Classification
# ==========================================================

def classify_health(shi):

    if shi >= 90:
        return "EXCELLENT"

    elif shi >= 75:
        return "GOOD"

    elif shi >= 50:
        return "WARNING"

    elif shi >= 25:
        return "POOR"

    else:
        return "CRITICAL"


# ==========================================================
# Maintenance Recommendation
# ==========================================================

def maintenance_action(shi):

    if shi >= 75:
        return "NOT REQUIRED"

    elif shi >= 50:
        return "INSPECT SENSOR"

    elif shi >= 25:
        return "SERVICE SOON"

    else:
        return "REPLACE SENSOR"


# ==========================================================
# Predictive Maintenance
# ==========================================================

def predict(
    calibration_result,
    diagnostic_result,
    reference_vpp,
    measured_vpp
):

    diagnostics_confidence = diagnostic_result["diagnostics_confidence"]
    # ==========================================================
    # VPP Accuracy
    # ==========================================================

    if reference_vpp is None:

        accuracy = diagnostics_confidence

        severity = diagnostic_result["severity"].upper()

        if severity == "CRITICAL":
            accuracy *= 0.20

        elif severity == "WARNING":
            accuracy *= 0.60

    else:

        vpp_error = abs(reference_vpp - measured_vpp)

        # Convert voltage error into an accuracy score
        accuracy = max(
            0,
            100 - (vpp_error * 50)
        )
    # ==========================================================
    # Sensor Health Index
    # ==========================================================
    if reference_vpp is None:

        print("Reference VPP : Live Mode")
        print("Measured VPP  :", measured_vpp)
        print("Accuracy      :", accuracy)

    else:

        print("Reference VPP :", reference_vpp)
        print("Measured VPP  :", measured_vpp)
        print("VPP Error     :", vpp_error)
        print("Accuracy      :", accuracy)
    sensor_health = round(

        0.70 * accuracy +

        0.30 * diagnostics_confidence,

        2

    )

    trend = calculate_trend()

    health_state = classify_health(sensor_health)

    maintenance = maintenance_action(sensor_health)

    return {

        "sensor_health": sensor_health,

        "health_state": health_state,

        "maintenance": maintenance,

        "average_health": trend["average_health"],

        "trend": trend["trend"],

        "trend_value": trend["trend_value"],

        "samples": trend["samples"]

    }


