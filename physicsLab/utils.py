# -*- coding: utf-8 -*-
import uuid
import pathlib
from datetime import datetime
from physicsLab import constant


def id_to_time(id: str) -> datetime:
    """从 用户id/实验id 中获取其对应的时间"""
    seconds = int(id[0:8], 16)
    return datetime.fromtimestamp(seconds)


def generate_a_new_sav_path() -> pathlib.Path:
    return pathlib.Path(
        constant.QUANTAM_PHYSICS_EXPERIMENT_DIR / str(uuid.uuid4())
    ).with_suffix(".sav")
