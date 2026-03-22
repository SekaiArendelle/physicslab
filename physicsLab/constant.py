import os
import platform

if platform.system() == "Windows":
    WIN_QUANTAM_PHYSICS_STORAGE_DIR = (
        f"{os.environ['USERPROFILE']}\\AppData\\LocalLow\\CIVITAS\\Quantum Physics"
    )

    WIN_QUANTAM_PHYSICS_EXPERIMENT_DIR = os.path.join(
        WIN_QUANTAM_PHYSICS_STORAGE_DIR, "Circuit"
    )