"""Storage path constants for Physics-Lab-AR save files."""

import os
import pathlib
import platform

if platform.system() != "Windows":
    QUANTAM_PHYSICS_STORAGE_DIR = pathlib.Path("physicsLabSav")

    QUANTAM_PHYSICS_EXPERIMENT_DIR = QUANTAM_PHYSICS_STORAGE_DIR
else:
    WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR = (
        f"{os.environ['USERPROFILE']}\\AppData\\LocalLow\\CIVITAS\\Quantum Physics"
    )

    QUANTAM_PHYSICS_STORAGE_DIR = pathlib.Path(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR)

    QUANTAM_PHYSICS_EXPERIMENT_DIR = QUANTAM_PHYSICS_STORAGE_DIR / "Circuit"
