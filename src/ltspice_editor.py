"""
==========================================================
LTspice Parameter Editor
==========================================================
"""

from pathlib import Path as _Path
import os as _os
_ROOT = _Path(__file__).resolve().parent.parent  # repository root
import re


def update_parameters(
    asc_file,
    humidity,
    temperature,
    fault
):

    with open(asc_file, "r") as f:
        text = f.read()

    text = re.sub(
        r"(!\.param RH=).*",
        rf"\g<1>{humidity}",
        text
    )

    text = re.sub(
        r"(!\.param TENV=).*",
        rf"\g<1>{temperature}",
        text
    )

    text = re.sub(
        r"(!\.param FAULT=).*",
        rf"\g<1>{fault}",
        text
    )

    with open(asc_file, "w") as f:
        f.write(text)
        
if __name__ == "__main__":

    update_parameters(

        str(_ROOT / "LTSpice" / "HumiditySensor_AFE_v5.asc"),

        humidity=60,

        temperature=40,

        fault=2

    )

    print("Done")