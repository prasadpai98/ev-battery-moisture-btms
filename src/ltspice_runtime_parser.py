"""
==========================================================
LTspice Log Parser
Battery Pack Moisture Monitoring System
==========================================================

Extracts VPP from LTspice log file.

Author : Chaitanyarani Kiragi
"""

from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
import re
import os


# ==========================================================
# Extract VPP
# ==========================================================



def extract_vpp(log_file, humidity, temperature):

    with open(log_file, "r") as f:
        text = f.read()

    start = text.find("Measurement: vpp")

    if start == -1:
        raise ValueError("Measurement: vpp not found.")

    end = text.find("Measurement: vavg", start)

    if end == -1:
        end = len(text)

    section = text[start:end]

    pattern = r"\n\s*\d+\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"

    values = [float(x) for x in re.findall(pattern, section)]

    if len(values) != 105:
        raise ValueError(f"Expected 105 VPP values, found {len(values)}")

    rh_index = round(humidity / 5)
    temp_index = round(temperature / 20)

    step = int(temp_index * 21 + rh_index)

    return values[step]


# ==========================================================
# Standalone Test
# ==========================================================

#LOG_FILE = str(_ROOT / "LTSpice" / "HumiditySensor_AFE_v5.log")

#print(extract_vpp(LOG_FILE, 50, 40))