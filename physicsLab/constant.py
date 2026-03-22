import os
import pathlib
import platform

if platform.system() != "Windows":
    QUANTAM_PHYSICS_STORAGE_DIR = pathlib.Path("physicsLabSav")

    QUANTAM_PHYSICS_EXPERIMENT_DIR = QUANTAM_PHYSICS_STORAGE_DIR
else:
    QUANTAM_PHYSICS_STORAGE_DIR = pathlib.Path(
        f"{os.environ['USERPROFILE']}\\AppData\\LocalLow\\CIVITAS\\Quantum Physics"
    )

    QUANTAM_PHYSICS_EXPERIMENT_DIR = QUANTAM_PHYSICS_STORAGE_DIR / "Circuit"
