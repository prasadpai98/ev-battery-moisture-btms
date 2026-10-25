"""
==========================================================
Calibration Module
Battery Pack Moisture Monitoring System
==========================================================

Author : Chaitanyarani Kiragi

Features
--------
1. Database-driven Temperature Compensation
2. Humidity Estimation
3. Confidence Calculation
4. Error Handling

No hardcoded calibration constants are used.
"""

import numpy as np
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

DATABASE = "../Database/healthy_database.csv"

REFERENCE_TEMPERATURE = 20      # Nominal characterization reference

# ==========================================================
# Load Database
# ==========================================================

df = pd.read_csv(DATABASE)

required_columns = {"Humidity", "Temperature", "VPP"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "Database must contain Humidity, Temperature and VPP columns."
    )

temperatures = sorted(df["Temperature"].unique())

# ==========================================================
# Helper Functions
# ==========================================================

def get_temperature_table(temp):
    """
    Returns calibration table for one characterized temperature.
    """

    table = (
        df[df["Temperature"] == temp]
        .sort_values("Humidity")
        .reset_index(drop=True)
    )

    return table


def find_temperature_bounds(temp):
    """
    Finds neighbouring characterization temperatures.
    """

    if temp <= temperatures[0]:
        return temperatures[0], temperatures[0]

    if temp >= temperatures[-1]:
        return temperatures[-1], temperatures[-1]

    for i in range(len(temperatures) - 1):

        t_low = temperatures[i]
        t_high = temperatures[i + 1]

        if t_low <= temp <= t_high:
            return t_low, t_high

    raise ValueError("Temperature out of range.")


# ==========================================================
# Temperature Compensation
# ==========================================================

def compensate_temperature(measured_temperature):
    """
    Generates the temperature-compensated calibration curve.

    Returns
    -------
    humidity_curve
    vpp_curve
    """

    t_low, t_high = find_temperature_bounds(measured_temperature)

    table_low = get_temperature_table(t_low)
    table_high = get_temperature_table(t_high)

    humidity_curve = table_low["Humidity"].to_numpy()

    vpp_low = table_low["VPP"].to_numpy()
    vpp_high = table_high["VPP"].to_numpy()
    

    # Exactly characterized temperature

    if t_low == t_high:

        return humidity_curve, vpp_low

    alpha = (measured_temperature - t_low) / (t_high - t_low)

    compensated_vpp = vpp_low + alpha * (vpp_high - vpp_low)

    return humidity_curve, compensated_vpp


# ==========================================================
# Humidity Estimation
# ==========================================================

def estimate_humidity(measured_vpp, measured_temperature):
    """
    Estimate humidity using temperature compensated calibration.

    Returns
    -------
    dict
    {
        humidity
        confidence
        valid
    }
    """

    humidity_curve, vpp_curve = compensate_temperature(
        measured_temperature
    )

    # Sort before interpolation

    order = np.argsort(vpp_curve)

    vpp_curve = vpp_curve[order]
    humidity_curve = humidity_curve[order]

    min_vpp = float(np.min(vpp_curve))
    max_vpp = float(np.max(vpp_curve))
    
    print("DEBUG VPP:", measured_vpp)
    print("DEBUG calibrated VPP range:", min_vpp, "to", max_vpp)

    # Outside characterized region

    if measured_vpp < min_vpp or measured_vpp > max_vpp:

        return {

            "humidity": None,

            "valid": False

        }

    humidity = np.interp(

        measured_vpp,

        vpp_curve,

        humidity_curve

    )

    # --------------------------------------------
    # Confidence Calculation
    # --------------------------------------------

    center = (min_vpp + max_vpp) / 2

    half_span = (max_vpp - min_vpp) / 2



    return {

        "humidity": round(float(humidity), 2),
        
       


        "valid": True

    }


