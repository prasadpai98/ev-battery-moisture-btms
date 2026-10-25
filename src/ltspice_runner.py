"""
==========================================================
LTspice Runner
Battery Pack Moisture Monitoring System
==========================================================

Runs LTspice in batch mode.

Author : Chaitanyarani Kiragi
"""

from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
import subprocess
import os


# ==========================================================
# LTspice Executable
# ==========================================================

LTSPICE_EXE = _os.environ.get("LTSPICE_EXE", r"C:\Program Files\ADI\LTspice\LTspice.exe")


# ==========================================================
# Run Simulation
# ==========================================================

def run_simulation(asc_file):

    if not os.path.exists(LTSPICE_EXE):

        raise FileNotFoundError(
            f"LTspice executable not found:\n{LTSPICE_EXE}"
        )

    if not os.path.exists(asc_file):

        raise FileNotFoundError(
            f"ASC file not found:\n{asc_file}"
        )

    print("\n========================================")
    print("Running LTspice Simulation...")
    print("========================================")

    result = subprocess.run(

        [

            LTSPICE_EXE,

            "-b",

            asc_file

        ],

        capture_output=True,

        text=True

    )

    if result.returncode != 0:

        print("\nLTspice returned an error.\n")

        if result.stdout.strip():

            print("STDOUT")
            print("--------------------------------")
            print(result.stdout)

        if result.stderr.strip():

            print("STDERR")
            print("--------------------------------")
            print(result.stderr)

        raise RuntimeError(
            "LTspice simulation failed."
        )

    print("Simulation Finished Successfully.")

    return True


# ==========================================================
# Standalone Test
# ==========================================================

if __name__ == "__main__":

    ASC_FILE = str(_ROOT / "LTSpice" / "HumiditySensor_AFE_v5.asc")

    run_simulation(ASC_FILE)