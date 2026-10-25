"""
==========================================================
Battery Pack Moisture Monitoring ECU
==========================================================

Main Controller

Features
--------
1. Live LTspice Simulation
2. Manual VPP Measurement
3. Characterization Database
4. Calibration
5. Functional Safety Diagnostics
6. Predictive Maintenance

Author : Chaitanyarani Kiragi
"""

import os
import pandas as pd

from calibration import estimate_humidity
from diagnostics import diagnose
from predictive_maintenance import predict
from dashboard import display
from history_manager import log_measurement
from ltspice_controller import simulate_measurement
from thermal_management import thermal_controller
from battery_assessment import assess_battery
from btms_controller import update_btms_hardware

# ==========================================================
# DATABASES
# ==========================================================

DATABASES = {

    1: ("Healthy",
        "../Database/healthy_database.csv"),

    2: ("Open Harness",
        "../Database/open_harness_database.csv"),

    3: ("Short Ground",
        "../Database/short_ground_database.csv"),

    4: ("Short Battery",
        "../Database/short_battery_database.csv")

}


# ==========================================================
# Header
# ==========================================================

def print_header():

    print("\n==========================================")
    print(" Battery Pack Moisture Monitoring ECU")
    print("==========================================\n")


# ==========================================================
# Live Measurement
# ==========================================================

def manual_mode():

    print("\n------ Live Measurement ------\n")

    try:

        vpp = float(input("Measured VPP (V): "))

        temperature = float(
            input("Measured Temperature (°C): ")
        )

    except ValueError:

        print("\nInvalid Input.\n")

        return

    process_measurement(vpp, temperature)


# ==========================================================
# Live LTspice Simulation
# ==========================================================

def live_ltspice_mode():

    print("\n------ Live LTspice Simulation ------\n")

    try:

        humidity = float(
            input("Relative Humidity (%): ")
        )

        temperature = float(
            input("Temperature (°C): ")
        )

    except ValueError:

        print("\nInvalid Input.\n")

        return

    print("\nRunning LTspice Simulation...")

    vpp = simulate_measurement(

        humidity,

        temperature

    )

    print(f"Measured VPP : {vpp:.6f} V")

    process_measurement(

        vpp,

        temperature

    )

# ==========================================================
# Database Mode
# ==========================================================

def database_mode():

    print("\nSelect Database\n")

    for key, value in DATABASES.items():

        print(f"{key}. {value[0]}")

    try:

        choice = int(input("\nChoice : "))

    except ValueError:

        print("Invalid Choice")

        return

    if choice not in DATABASES:

        print("Invalid Choice")

        return

    name, file = DATABASES[choice]

    if not os.path.exists(file):

        print(f"\nDatabase not found:\n{file}")

        return

    df = pd.read_csv(file)

    print(f"\nRows Available : 1 - {len(df)}")

    try:

        row = int(input("Enter Row Number : "))

    except ValueError:

        print("Invalid Row")

        return

    if row < 1 or row > len(df):

        print("Row Out Of Range")

        return

    selected = df.iloc[row - 1]

    humidity = selected["Humidity"]

    temperature = selected["Temperature"]

    reference_rh = selected["Humidity"]

    temperature = selected["Temperature"]

    FAULT_MAP = {

        "Healthy": 0,

        "Open Harness": 1,

        "Short Ground": 2,

        "Short Battery": 3

    }

    fault = FAULT_MAP[name]

    vpp = simulate_measurement(

        humidity=reference_rh,

        temperature=temperature,

        fault=fault

    )
    
    reference_vpp = float(selected["VPP"])

    print("\n--------------------------------------")

    print(f"Database     : {name}")

    print(f"Row          : {row}")

    print(f"Reference RH : {humidity:.2f} %")

    print(f"Temperature  : {temperature:.2f} °C")

    print(f"Measured VPP : {vpp:.6f} V")

    print("--------------------------------------")

    process_measurement(vpp, temperature, reference_vpp)


# ==========================================================
# Processing
# ==========================================================

def process_measurement(vpp, temperature, reference_vpp=None ):

    print("\nRunning Calibration...")

    calibration = estimate_humidity(
        vpp,
        temperature
    )

    print("Done.")

    print("\nRunning Diagnostics...")

    diagnostic = diagnose(
        calibration,
        vpp,
        temperature
    )

    print("Done.")

    print("\nRunning Predictive Maintenance...")

    maintenance = predict(
        calibration,
        diagnostic,
        reference_vpp,
        vpp
    )

    print("Done.")

    print("\nRunning Battery Assessment...")
    

    battery = assess_battery(

        calibration["humidity"],

        diagnostic,

        maintenance["sensor_health"]

    )

    print("Done.")

    print("\nRunning Thermal Management...")

    thermal = thermal_controller(

        temperature,

        calibration["humidity"],

        battery

    )
    
    update_btms_hardware(thermal)

    print("Done.")

    
    
    log_measurement(

        temperature,

        vpp,

        calibration["humidity"],

        diagnostic["status"],

        diagnostic["diagnostics_confidence"],

        maintenance["sensor_health"]

    )
    
    

    print("Done.")

    display(
        calibration,
        diagnostic,
        battery,
        thermal,
        maintenance,
        temperature,
        vpp
    )



# ==========================================================
# Main
# ==========================================================

def main():

    print_header()

    print("Select Input Source\n")

    print("1. Live LTspice Simulation")

    print("2. Manual VPP Measurement")

    print("3. Characterization Database")

    try:

        mode = int(input("\nChoice : "))

    except ValueError:

        print("Invalid Choice")

        return

    if mode == 1:

        live_ltspice_mode()

    elif mode == 2:

        manual_mode()

    elif mode == 3:

        database_mode()

    else:

        print("Invalid Choice")


if __name__ == "__main__":

    from dashboard import gui

    main()

    gui.run()