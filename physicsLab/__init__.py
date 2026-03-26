
"""Python API for Physics-Lab-AR"""

from .physicsLab_version import __version__

# 操作实验
from .element import search_experiment, Experiment
from ._core import (
    ElementBase,
    get_current_experiment,
    elementXYZ_to_native,
    native_to_elementXYZ,
    ElementXYZ,
)

from .coordinate_system import *

# 实验, 标签类型
from .enums import ExperimentType, Category, Tag, OpenMode, WireColor, GetUserMode

# 电学实验
from .circuit import *

# 天体物理实验
from .celestial import *

# 电与磁实验
from .electromagnetism import *

# `physicsLab`自定义异常类
from .errors import *

from physicsLab.plAR import *
from physicsLab.utils import *

from physicsLab import web

import os

if not os.path.exists(Experiment.SAV_PATH_DIR):
    os.makedirs(Experiment.SAV_PATH_DIR)

del os
