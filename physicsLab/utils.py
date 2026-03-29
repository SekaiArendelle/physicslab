
import uuid
import json
import pathlib
from datetime import datetime
from physicsLab import constant
from physicsLab._typing import Optional


def id_to_time(id: str) -> datetime:
    """从 用户id/实验id 中获取其对应的时间"""
    seconds = int(id[0:8], 16)
    return datetime.fromtimestamp(seconds)


def generate_a_new_sav_path() -> pathlib.Path:
    return pathlib.Path(
        constant.QUANTAM_PHYSICS_EXPERIMENT_DIR / str(uuid.uuid4())
    ).with_suffix(".sav")


def find_path_of_sav_name(sav_name: str) -> Optional[pathlib.Path]:
    if not isinstance(sav_name, str):
        raise TypeError(
            f"sav_name must be of type `str`, but got value {sav_name} of type {type(sav_name).__name__}"
        )

    for file in constant.QUANTAM_PHYSICS_EXPERIMENT_DIR.glob("*.sav"):
        if not file.is_file():
            continue

        plsav_dict: dict = json.loads(file.read_text(encoding="utf-8"))
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
