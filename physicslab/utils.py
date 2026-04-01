"""Utility helpers for working with Physics-Lab-AR save files."""

import uuid
import json
import pathlib
from datetime import datetime
from physicslab import constant
from physicslab._typing import Optional


def id_to_time(id: str) -> datetime:
    """Convert a user ID or experiment ID into its encoded creation time."""
    seconds = int(id[0:8], 16)
    return datetime.fromtimestamp(seconds)


def generate_a_new_sav_path() -> pathlib.Path:
    """Generate a unique ``.sav`` file path inside the experiment directory."""
    return pathlib.Path(
        constant.QUANTAM_PHYSICS_EXPERIMENT_DIR / str(uuid.uuid4())
    ).with_suffix(".sav")


def find_path_of_sav_name(sav_name: str) -> Optional[pathlib.Path]:
    """Search for the ``.sav`` file whose experiment subject matches *sav_name*.

    Args:
        sav_name: The experiment name to look up (as displayed in Physics-Lab-AR).

    Returns:
        The path to the matching save file, or ``None`` if not found.

    Raises:
        TypeError: If *sav_name* is not a string.
    """
    if not isinstance(sav_name, str):
        raise TypeError(
            f"sav_name must be of type `str`, but got value {sav_name} of type {type(sav_name).__name__}"
        )

    for file in constant.QUANTAM_PHYSICS_EXPERIMENT_DIR.glob("*.sav"):
        if not file.is_file():
            continue

        with open(file, encoding="utf-8") as f:
            try:
                plsav_dict: dict = json.load(f)
            except (json.decoder.JSONDecodeError, UnicodeDecodeError, OSError):
                continue
        if "Summary" not in plsav_dict.keys():
            continue
        summary_dict: Optional[dict] = plsav_dict["Summary"]
        if summary_dict is None:
            continue
        if "Subject" in summary_dict.keys():
            if summary_dict["Subject"] == sav_name:
                return file
        elif "Subject" in plsav_dict.keys():
            if plsav_dict["Subject"] == sav_name:
                return file

    return None
