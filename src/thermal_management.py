"""
==========================================================
Battery Thermal Management System (BTMS)
==========================================================

Author : Chaitanyarani Kiragi
"""


def thermal_controller(

    temperature,
    humidity,
    battery

):

    result = {}
    
    battery_status = battery["battery_status"]

    risk_score = battery["risk_score"]

    protection_stage = battery["protection_stage"]

    charging_allowed = battery["charging_allowed"]
    # -------------------------------------------------
    # Thermal Decision
    # -------------------------------------------------

    if temperature < 10:

        mode = "HEATING"
        heater = True
        fan = False
        target = 20

    elif (
        temperature >= 35
        or battery_status == "WARNING"
        or battery_status == "CRITICAL"
        or protection_stage in ["STAGE 3", "STAGE 4"]
    ):

        mode = "COOLING"
        heater = False
        fan = True
        target = 30

    elif temperature > 45:

        mode = "EMERGENCY"
        heater = False
        fan = True
        target = 25

    else:

        mode = "NORMAL"
        heater = False
        fan = False
        target = 25

    # ----------------------------------------
    # Fan Speed
    # ----------------------------------------

    if mode == "COOLING":

        if battery_status == "CRITICAL":

            fan_speed = 100

        elif battery_status == "WARNING":

            fan_speed = 80

        elif temperature >= 40:

            fan_speed = 80

        else:

            fan_speed = 60

    elif mode == "EMERGENCY":

        fan_speed = 100

    else:

        fan_speed = 0

    # ----------------------------------------
    # Charging Limit
    # ----------------------------------------

    charging_limit = (
        mode == "EMERGENCY"
        or battery_status == "CRITICAL"
        or protection_stage == "STAGE 4"
    )

    if (

        mode == "EMERGENCY"

        or

        protection_stage == "STAGE 4"

    ):

        charging_limit = True

    # ----------------------------------------
    # Predicted Temperature
    # ----------------------------------------

    predicted_temperature = temperature

    if fan:

        predicted_temperature -= 5

    if heater:

        predicted_temperature += 5

    result["mode"] = mode

    result["fan"] = fan

    result["heater"] = heater

    result["fan_speed"] = fan_speed

    result["target_temperature"] = target

    result["predicted_temperature"] = round(predicted_temperature,1)

    result["charging_limit"] = charging_limit
    
    result["risk_score"] = risk_score

    result["protection_stage"] = protection_stage

    result["battery_status"] = battery_status

    result["charging_allowed"] = charging_allowed

    return result