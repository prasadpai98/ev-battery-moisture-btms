"""
==========================================================
LTspice Controller
==========================================================
"""

from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
import json

from ltspice_editor import update_parameters
from ltspice_runner import run_simulation
from ltspice_runtime_parser import extract_vpp


ASC_FILE = str(_ROOT / "LTSpice" / "HumiditySensor_AFE_v5.asc")
LOG_FILE = str(_ROOT / "LTSpice" / "HumiditySensor_AFE_v5.log")

CONFIG_FILE = "simulation_config.json"


def read_fault_mode():
    """
    Reads the fault mode from simulation_config.json

    0 = Healthy
    1 = Open Harness
    2 = Short Ground
    3 = Short Battery
    """

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        return config.get("fault_mode", 0)

    except Exception:
        print("Warning: simulation_config.json not found.")
        print("Using Healthy Mode.")

        return 0


def simulate_measurement(humidity, temperature, fault=None):
    """
    Runs LTspice simulation.

    If fault is not supplied,
    it is automatically read from simulation_config.json.
    """

    if fault is None:
        fault = read_fault_mode()

    # Update LTspice parameters
    update_parameters(
        ASC_FILE,
        humidity,
        temperature,
        fault
    )

    # Run LTspice
    run_simulation(ASC_FILE)

    # Read measured VPP
    vpp = extract_vpp(
        LOG_FILE,
        humidity,
        temperature
    )

    return vpp


if __name__ == "__main__":

    vpp = simulate_measurement(
        humidity=50,
        temperature=40
    )

    print()
    print("Measured VPP :", vpp)