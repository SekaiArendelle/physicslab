"""Quantum-physics experiment utilities for the physicsLab package."""

import platform

import os
import json

from typing import Optional, Tuple


def get_quantum_physics_version() -> Optional[Tuple[int, int, int]]:
    """Get version of Quantum-Physics, return None if failed to get version"""
    if platform.system() != "Windows":
        return None

    from physicsLab.constant import WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR

    try:
        a_dir = os.listdir(
            os.path.join(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Unity")
        )
        if len(a_dir) != 1:
            return None

        a_file = os.path.join(
            WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR,
            "Unity",
            a_dir[0],
            "Analytics",
            "values",
        )

        with open(a_file) as f:
            ver_str: str = json.load(f)["app_ver"]
        parts = ver_str.split(".")
        if len(parts) != 3:
            return None
        major, minor, patch = parts
        return int(major), int(minor), int(patch)
    except (json.decoder.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
        return None
    except ValueError:
        return None


def get_quantum_physics_path() -> Optional[str]:
    """Get path of Quantum-Physics"""
    if platform.system() != "Windows":
        return None

    from physicsLab.constant import WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR

    with open(
        os.path.join(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Player-prev.log")
    ) as f:
        f.readline()
        f.readline()
        res = os.path.dirname(os.path.dirname(f.readline()[25:-2]))

    if res == "":
        return None
    return res
