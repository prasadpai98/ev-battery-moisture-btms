"""
==========================================================
Battery Assessment Module
Battery Pack Moisture Monitoring System
==========================================================

Purpose:
Provides battery-related recommendations using the
estimated humidity and diagnostic status.

This module DOES NOT modify:
- Calibration
- Diagnostics
- Predictive Maintenance
- History

It only interprets their outputs.
"""

# ==========================================================
# Battery Risk Weight Configuration
# ==========================================================

RISK_WEIGHTS = {

    "humidity":0.60,

    "sensor":0.20,

    "diagnostics":0.20

}


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))

def calculate_risk_score(humidity,
                             sensor_health,
                             diagnostic_confidence):

        # ==================================================
        # Humidity Contribution (0 - 60)
        # ==================================================

        humidity_score = clamp(humidity) * RISK_WEIGHTS["humidity"]

        # ==================================================
        # Sensor Health Contribution (0 - 20)
        # Sensor health is already in %
        # ==================================================

        sensor_penalty = (100 - sensor_health) * RISK_WEIGHTS["sensor"] * 5
        sensor_penalty = clamp(sensor_penalty, 0, 20)

        diagnostic_penalty = (100 - diagnostic_confidence) * RISK_WEIGHTS["diagnostics"] * 1.33
        diagnostic_penalty = clamp(diagnostic_penalty, 0, 20)

        # ==================================================
        # Final Weighted Risk
        # ==================================================

        total = (
            humidity_score +
            sensor_penalty +
            diagnostic_penalty
        )

        return round(clamp(total), 1)

def assess_battery(humidity,
                   diagnostic_result,
                   sensor_health):

    status = diagnostic_result["status"].upper()
    diagnostic_confidence = diagnostic_result["diagnostics_confidence"]

    # --------------------------------------------------
    # Sensor Fault Overrides
    # --------------------------------------------------

    if status != "HEALTHY":

            battery_status = "SENSOR FAULT"

            moisture_risk = "UNKNOWN"

            corrosion_risk = "UNKNOWN"

            condensation_risk = "UNKNOWN"

            ingress = "UNKNOWN"

            priority = "IMMEDIATE"

            action = "Repair/Replace Humidity Sensor"

            risk_score = 100

            protection_stage = "STAGE 4"

            charging_allowed = False
            
          
            safety_index = 0
            

            battery_health = 0
            
            protection_description = "Emergency"
            
            root_causes = [
                "Sensor Fault",
                "Invalid Sensor Measurement"
            ]
            
            return {

                "battery_status": battery_status,

                "moisture_risk": moisture_risk,

                "corrosion_risk": corrosion_risk,

                "ingress": ingress,

                "maintenance_priority": priority,

                "recommended_action": action,
                
                "condensation_risk": condensation_risk,

                "risk_score": risk_score,
                
                "safety_index": safety_index,
                
                "battery_health": battery_health,

                "protection_stage": protection_stage,
                
                "protection_description": protection_description,

                "charging_allowed": charging_allowed,
                
                "root_causes": root_causes

            }

    # --------------------------------------------------
    # Moisture Risk
    # --------------------------------------------------

    if humidity < 60:

        moisture_risk = "LOW"

    elif humidity < 80:

        moisture_risk = "MODERATE"

    elif humidity < 90:

        moisture_risk = "HIGH"

    else:

        moisture_risk = "CRITICAL"

    # --------------------------------------------------
    # Corrosion Risk
    # --------------------------------------------------

    if humidity < 60:

        corrosion_risk = "LOW"

    elif humidity < 80:

        corrosion_risk = "MODERATE"

    elif humidity < 90:

        corrosion_risk = "HIGH"

    else:

        corrosion_risk = "CRITICAL"

    # --------------------------------------------------
    # Moisture Ingress
    # --------------------------------------------------

    if humidity >= 80:

        ingress = "LIKELY"

    else:

        ingress = "NO"
    
    
    # --------------------------------------------------
    # Condensation Risk
    # --------------------------------------------------

    if humidity < 60:

        condensation_risk = "LOW"

    elif humidity < 80:

        condensation_risk = "MODERATE"

    elif humidity < 90:

        condensation_risk = "HIGH"

    else:

        condensation_risk = "CRITICAL"
    
    # --------------------------------------------------
    # Battery Status
    # --------------------------------------------------

    if humidity < 60:

        battery_status = "NORMAL"

    elif humidity < 80:

        battery_status = "MONITOR"

    elif humidity < 90:

        battery_status = "WARNING"

    else:

        battery_status = "CRITICAL"

    # --------------------------------------------------
    # Maintenance Priority
    # --------------------------------------------------

    if humidity < 60:

        priority = "LOW"

    elif humidity < 80:

        priority = "MEDIUM"

    elif humidity < 90:

        priority = "HIGH"

    else:

        priority = "IMMEDIATE"
    
    
    # --------------------------------------------------
    # Overall Battery Risk Score (Weighted Model)
    # --------------------------------------------------

    diagnostic_confidence = diagnostic_result["diagnostics_confidence"]

    risk_score = calculate_risk_score(
        humidity,
        sensor_health,
        diagnostic_confidence
    )
    
    
    
    # --------------------------------------------------
    # Protection Stage
    # --------------------------------------------------

    if risk_score < 30:

        protection_stage = "STAGE 1"

    elif risk_score < 60:

        protection_stage = "STAGE 2"

    elif risk_score < 80:

        protection_stage = "STAGE 3"

    else:

        protection_stage = "STAGE 4"
    
    
    # --------------------------------------------------
    # Charging Permission
    # --------------------------------------------------

    charging_allowed = True

    if protection_stage == "STAGE 4":

        charging_allowed = False
    
    # --------------------------------------------------
    # Recommended Action
    # --------------------------------------------------

    if humidity < 60:

        action = "Normal Operation"

    elif humidity < 80:

        action = "Continue Monitoring"

    elif humidity < 90:

        action = "Inspect Battery Enclosure Seals"

    else:

        action = "Immediate Battery Inspection-Stop operation and Service battery pack"
    # ==========================================================
    # Battery Safety Index
    # ==========================================================

    safety_index = 100 - risk_score

    if safety_index < 0:
        safety_index = 0

    if safety_index > 100:
        safety_index = 100
    
    
    # ==========================================================
    # Battery Health Estimation
    # ==========================================================

    battery_health = 100 - (risk_score * 0.5)

    if battery_health < 0:
        battery_health = 0

    if battery_health > 100:
        battery_health = 100

    battery_health = round(battery_health, 1)
    
    # ==========================================================
    # Protection Level Description
    # ==========================================================

    if protection_stage == "STAGE 1":

        protection_description="Normal Operation"

    elif protection_stage=="STAGE 2":

        protection_description="Increase Monitoring"

    elif protection_stage=="STAGE 3":

        protection_description="Limit Charging"

    elif protection_stage=="STAGE 4":

        protection_description="Emergency Protection"
    
    # ==========================================================
    # Root Cause Analysis
    # ==========================================================

    root_causes = []

    if humidity >= 80:
        root_causes.append("High Humidity")

    if sensor_health < 98:
        root_causes.append("Sensor Health Degradation")

    if diagnostic_confidence < 95:
        root_causes.append("Low Diagnostic Confidence")

    if not root_causes:
        root_causes.append("Normal Operating Conditions")
    
    return {

        "battery_status": battery_status,

        "moisture_risk": moisture_risk,

        "corrosion_risk": corrosion_risk,

        "ingress": ingress,

        "maintenance_priority": priority,

        "recommended_action": action,
        
        "condensation_risk": condensation_risk,

        "risk_score": risk_score,
        
        "safety_index": safety_index,
        
        "battery_health": battery_health,

        "protection_stage": protection_stage,
        
        "protection_description": protection_description,

        "charging_allowed": charging_allowed,
        
        "root_causes": root_causes

    }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    diag = {

        "status": "HEALTHY"

    }

    print(

        assess_battery(
            humidity=84,
            diagnostic_result=diag,
            sensor_health=99.6
        )

    )