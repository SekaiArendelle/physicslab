"""Enumerations used across the physicslab package."""

from enum import Enum, unique


@unique
class ExperimentType(Enum):
    """Experiment type."""

    # Circuit experiment
    Circuit = 0


@unique
class Category(Enum):
    """Community content categories."""

    Experiment = "Experiment"
    Discussion = "Discussion"


@unique
class Tag(Enum):
    """Community tags."""

    # TODO: Submission tags
    # Experiment area
    Circuit = "Type-0"
    Celestial = "Type-3"
    Electromagnetism = "Type-4"
    KnowledgeBase = "知识库"
    Featured = "精选"
    ElementarySchool = "小学"
    HighSchool = "高中"
    MiddleSchool = "初中"
    College = "大学"
    Professional = "专科"
    FunExperiment = "娱乐实验"
    SmallProject = "小作品"
    Curricular = "教学实验"
    NoRemixes = "禁止改编"
    ApplyForFeature = "精选申请"
    # Discussion area
    BUG = "BUG"
    Discussion = "交流"
    Stories = "小说专区"
    Charroom = "聊天"
    Q_A = "问与答"
    # Legacy tags
    Logic_Circuit = "逻辑电路"
    DC_Circuit = "直流电路"
    AC_Circuit = "交流电路"
    Electronic = "电子电路"
    Interest = "兴趣"


@unique
class OpenMode(Enum):
    """Modes for opening an experiment with ``Experiment`` APIs."""

    load_by_sav_name = 0  # Save name as shown in Physics-Lab-AR.
    load_by_filepath = 1  # Full path provided by the user.
    load_by_plar_app = 2  # Load via network request from Physics-Lab-AR.
    crt = 3  # Create a new save.


@unique
class ColorOfWire(Enum):
    """Wire color options for circuit connections."""

    black = "黑"
    blue = "蓝"
    red = "红"
    green = "绿"
    yellow = "黄"


@unique
class GetUserMode(Enum):
    """Mode for looking up a community user account."""

    by_id = 0
    by_name = 1


@unique
class SwitchState(Enum):
    """On/off state for a two-position switch element."""

    OFF = 0
    ON = 1


@unique
class PDTSwitchState(Enum):
    """State for a three-position (PDT) switch element."""

    OFF = 0
    LEFT = 1
    RIGHT = 2
