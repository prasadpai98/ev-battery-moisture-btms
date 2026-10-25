"""
==========================================================
History Manager
Battery Pack Moisture Monitoring System
==========================================================

Creates and updates history.csv

Author : Chaitanyarani Kiragi
"""

import os
import pandas as pd
from datetime import datetime


# ==========================================================
# File Location
# ==========================================================

HISTORY_FILE = "../Results/history.csv"


# ==========================================================
# Create History File
# ==========================================================

def initialize_history():

    if os.path.exists(HISTORY_FILE):
        return

    df = pd.DataFrame({

        "Timestamp": pd.Series(dtype="str"),

        "Temperature": pd.Series(dtype="float"),

        "Measured_VPP": pd.Series(dtype="float"),

        "Humidity": pd.Series(dtype="float"),

        "Status": pd.Series(dtype="str"),

        "Diagnostic_Confidence": pd.Series(dtype="float"),

        "Sensor_Health": pd.Series(dtype="float")

    })

    df.to_csv(HISTORY_FILE, index=False)

    print("History file created.")


# ==========================================================
# Append New Entry
# ==========================================================

def log_measurement(

    temperature,

    vpp,

    humidity,

    status,

    confidence,

    sensor_health

):

    initialize_history()

    df = load_history()

    new_row = pd.DataFrame([{

        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "Temperature": temperature,

        "Measured_VPP": vpp,

        "Humidity": humidity,

        "Status": status,

        "Diagnostic_Confidence": confidence,

        "Sensor_Health": sensor_health

    }])

    if df.empty:

        df = new_row

    else:

        df.loc[len(df)] = new_row.iloc[0]

    df.to_csv(HISTORY_FILE, index=False)


# ==========================================================
# Read History
# ==========================================================

def load_history():

    initialize_history()

    return pd.read_csv(HISTORY_FILE)
    
# ==========================================================
# Get Last N Measurements
# ==========================================================

def get_recent_history(samples=10):

    df = load_history()

    if df.empty:

        return df

    return df.tail(samples).reset_index(drop=True)


# ==========================================================
# Number of Stored Measurements
# ==========================================================

def history_size():

    return len(load_history())
    
if __name__ == "__main__":

    initialize_history()

    log_measurement(
        20,
        1.826,
        50,
        "HEALTHY",
        98.5,
        99.2
    )

    print(load_history())