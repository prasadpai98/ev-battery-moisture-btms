"""
==========================================================
Diagnostics Module
Battery Pack Moisture Monitoring System
==========================================================

Features
--------
1. Functional Safety
2. Fault Detection
3. DTC Generation
4. Severity Classification

Author : Chaitanyarani Kiragi
"""

import numpy as np
import pandas as pd

from calibration import estimate_humidity

# ==========================================================
# DATABASES
# ==========================================================

HEALTHY_DB = "../Database/healthy_database.csv"
OPEN_DB = "../Database/open_harness_database.csv"
GROUND_DB = "../Database/short_ground_database.csv"
BATTERY_DB = "../Database/short_battery_database.csv"

healthy = pd.read_csv(HEALTHY_DB)
open_harness = pd.read_csv(OPEN_DB)
short_ground = pd.read_csv(GROUND_DB)
short_battery = pd.read_csv(BATTERY_DB)

# ==========================================================
# DTC TABLE
# ==========================================================

DTC = {

    "HEALTHY": "HUM000",

    "OPEN_HARNESS": "HUM001",

    "SHORT_GROUND": "HUM002",

    "SHORT_BATTERY": "HUM003",

    "INVALID": "HUM004"

}

# ==========================================================
# SEVERITY
# ==========================================================

SEVERITY = {

    "HEALTHY": "NORMAL",

    "OPEN_HARNESS": "CRITICAL",

    "SHORT_GROUND": "CRITICAL",

    "SHORT_BATTERY": "CRITICAL",

    "INVALID": "WARNING"

}

# ==========================================================
# Helper
# ==========================================================

def get_curve(database, temperature):

    temperatures = sorted(database["Temperature"].unique())

    if temperature <= temperatures[0]:
        temperature = temperatures[0]

    if temperature >= temperatures[-1]:
        temperature = temperatures[-1]

    lower = max([t for t in temperatures if t <= temperature])
    upper = min([t for t in temperatures if t >= temperature])

    table_low = database[database["Temperature"] == lower].sort_values("Humidity")
    table_high = database[database["Temperature"] == upper].sort_values("Humidity")

    vpp_low = table_low["VPP"].to_numpy()
    vpp_high = table_high["VPP"].to_numpy()

    humidity = table_low["Humidity"].to_numpy()

    if lower == upper:

        return humidity, vpp_low

    alpha = (temperature - lower) / (upper - lower)

    vpp = vpp_low + alpha * (vpp_high - vpp_low)

    return humidity, vpp


# ==========================================================
# Error Calculation
# ==========================================================

def curve_error(database, measured_vpp, temperature):

    humidity, curve = get_curve(database, temperature)

    return np.min(np.abs(curve - measured_vpp))


# ==========================================================
# Diagnostics
# ==========================================================

def diagnose(calibration, measured_vpp, measured_temperature):

    errors = {

        "HEALTHY":
            curve_error(
                healthy,
                measured_vpp,
                measured_temperature
            ),

        "OPEN_HARNESS":
            curve_error(
                open_harness,
                measured_vpp,
                measured_temperature
            ),

        "SHORT_GROUND":
            curve_error(
                short_ground,
                measured_vpp,
                measured_temperature
            ),

        "SHORT_BATTERY":
            curve_error(
                short_battery,
                measured_vpp,
                measured_temperature
            )

    }

    ordered = sorted(
        errors.items(),
        key=lambda x: x[1]
    )

    best = ordered[0]
    second = ordered[1]

    best_fault = best[0]

    best_error = best[1]

    second_error = second[1]

    if second_error == 0:

        diagnostics_confidence = 100.0

    else:

        diagnostics_confidence = (
            1 -
            best_error / second_error
        ) * 100

    diagnostics_confidence = max(
        0.0,
        min(100.0, diagnostics_confidence)
    )

    return {

        "humidity":
            calibration.get("humidity"),

        "status":
            best_fault,

        "fault":
            best_fault,

        "dtc":
            DTC[best_fault],

        "severity":
            SEVERITY[best_fault],

        "diagnostics_confidence":
            round(diagnostics_confidence,2)

    }


