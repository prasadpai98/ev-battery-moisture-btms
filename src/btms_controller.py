"""
====================================================
BTMS Hardware Controller
Python ECU -> LTspice
====================================================
"""

from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
from pathlib import Path
import subprocess
import time

# ----------------------------------------------------
# PATHS (resolved relative to the repository; set LTSPICE_EXE to override)
# ----------------------------------------------------

LTSPICE_EXE = _os.environ.get("LTSPICE_EXE", r"C:\Program Files\ADI\LTspice\LTspice.exe")

BTMS_ASC = Path(
    str(_ROOT / "LTSpice" / "BTMS_Controller.asc")
)

CONTROL_FILE = Path(
    str(_ROOT / "LTSpice" / "btms_control.inc")
)

# ----------------------------------------------------


def update_btms_hardware(thermal):

    cool = 5 if thermal["fan"] else 0
    heat = 5 if thermal["heater"] else 0

    print("\n========================================")
    print(" ECU -> BTMS Hardware")
    print("========================================")

    print(f"Mode        : {thermal['mode']}")
    print(f"COOL_CMD    : {cool} V")
    print(f"HEAT_CMD    : {heat} V")

    print("\nUpdating BTMS Control File...")

    CONTROL_FILE.write_text(
        f".param COOL_CMD={cool}\n"
        f".param HEAT_CMD={heat}\n",
        encoding="ascii"
    )

    print("Done.")

    print("\nLaunching LTspice...")

    subprocess.Popen(
        [
            LTSPICE_EXE,
            str(BTMS_ASC)
        ]
    )

    time.sleep(1)

    print("LTspice Started Successfully.")