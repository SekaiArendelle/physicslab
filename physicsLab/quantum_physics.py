import os
import json
import platform

from typing import Optional, Tuple
from physicsLab.constant import WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR


def get_quantum_physics_version() -> Optional[Tuple[int, int, int]]:
    """Get version of Quantum-Physics, return None if failed to get version"""
    if platform.system() != "Windows":
        return None

    try:
        a_dir = os.listdir(os.path.join(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Unity"))
        if len(a_dir) != 1:
            return None

        a_file = os.path.join(
            WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Unity", a_dir[0], "Analytics", "values"
        )

        with open(a_file) as f:
            ver_str: str = json.load(f)["app_ver"]
        return eval(f"({ver_str.replace('.', ',')})")
    except (json.decoder.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
        return None


def get_quantum_physics_path() -> Optional[str]:
    """Get path of Quantum-Physics"""
    if platform.system() != "Windows":
        return None

    with open(os.path.join(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Player-prev.log")) as f:
        f.readline()
        f.readline()
        res = os.path.dirname(os.path.dirname(f.readline()[25:-2]))

    if res == "":
        return None
    return res
