import physicsLab.plAR as plar
from physicsLab import _warn
from physicsLab import coordinate_system

from physicsLab._core import _Experiment
from .._circuit_core import (
    CircuitBase,
    Pin,
    _deprecated_init_attr_experiment,
    _deprecated_assign_element_to_experiment,
)
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Union,
    List,
    override,
    Tuple,
    final,
    Literal,
    Iterator,
)


class _Buzzer(CircuitBase):
    """蜂鸣器"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Buzzer",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电压": 3.0,
                "额定功率": 0.3,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "嗡鸣器"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Buzzer(_Buzzer):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _SparkGap(CircuitBase):
    """火花隙"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Spark Gap",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "击穿电压": 1000.0,
                "击穿电阻": 1.0,
                "维持电流": 0.001,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "火花隙"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Spark_Gap(_SparkGap):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _TeslaCoil(CircuitBase):
    """特斯拉线圈"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Tesla Coil",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "击穿电压": 30000.0,
                "次级电容": 2.5e-11,
                "次级电阻": 1.0,
                "电感1": 0.1,
                "电感2": 90.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"瞬间功率": 0.0, "瞬间电流": 0.0, "瞬间电压": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "特斯拉线圈"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Tesla_Coil(_TeslaCoil):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _ColorLightEmittingDiode(CircuitBase):
    """彩色发光二极管"""

    _all_pins: Tuple[
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_l_mid_pin"], Pin],
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_up_pin: Pin
    _l_mid_pin: Pin
    _l_low_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0)),
            ("_l_mid_pin", Pin(self, 1)),
            ("_l_low_pin", Pin(self, 2)),
            ("_r_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Color Light-Emitting Diode",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "反向耐压": 6.0,
                "击穿电压": 0.0,
                "前向压降": 2.1024259,
                "工作电流": 0.01,
                "工作电压": 3.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "亮度1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
                "功率2": 0.0,
                "亮度2": 0.0,
                "电流3": 0.0,
                "电压3": 0.0,
                "功率3": 0.0,
                "亮度3": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "彩色发光二极管"

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def l_mid(self) -> Pin:
        return self._l_mid_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def r(self) -> Pin:
        return self._r_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 4


class Color_Light_Emitting_Diode(_ColorLightEmittingDiode):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _DualLightEmittingDiode(CircuitBase):
    """演示发光二极管"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Dual Light-Emitting Diode",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "反向耐压": 6.0,
                "击穿电压": 0.0,
                "前向压降": 2.1024259,
                "工作电流": 0.01,
                "工作电压": 3.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "亮度1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
                "功率2": 0.0,
                "亮度2": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "演示发光二极管"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Dual_Light_Emitting_Diode(_DualLightEmittingDiode):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _ElectricBell(CircuitBase):
    """电铃"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Electric Bell",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电压": 3.0,
                "额定功率": 0.3,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "电铃"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Electric_Bell(_ElectricBell):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _MusicalBox(CircuitBase):
    """八音盒"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Musical Box",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电压": 3.0,
                "额定功率": 0.3,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "八音盒"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Musical_Box(_MusicalBox):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _ResistanceLaw(CircuitBase):
    """电阻定律实验"""

    _all_pins: Tuple[
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_l_lowmid_pin"], Pin],
        Tuple[Literal["_l_upmid_pin"], Pin],
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
        Tuple[Literal["_r_lowmid_pin"], Pin],
        Tuple[Literal["_r_upmid_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
    ]
    _l_low_pin: Pin
    _l_lowmid_pin: Pin
    _l_upmid_pin: Pin
    _l_up_pin: Pin
    _r_low_pin: Pin
    _r_lowmid_pin: Pin
    _r_upmid_pin: Pin
    _r_up_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_l_low_pin", Pin(self, 0)),
            ("_l_lowmid_pin", Pin(self, 1)),
            ("_l_upmid_pin", Pin(self, 2)),
            ("_l_up_pin", Pin(self, 3)),
            ("_r_low_pin", Pin(self, 4)),
            ("_r_lowmid_pin", Pin(self, 5)),
            ("_r_upmid_pin", Pin(self, 6)),
            ("_r_up_pin", Pin(self, 7)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Resistance Law",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电阻率": 1.0,
                "电阻率2": 4.0,
                "电阻率3": 1.0,
                "最大长度": 2.0,
                "最小长度": 0.1,
                "长度": 1.0,
                "最大半径": 0.01,
                "最小半径": 0.0001,
                "半径": 0.0005,
                "电阻": 1.4,
                "电阻2": 0.56,
                "电阻3": 0.02,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
                "瞬间功率1": 0.0,
                "瞬间电流1": 0.0,
                "瞬间电压1": 0.0,
                "功率1": 0.0,
                "电压1": 0.0,
                "电流1": 0.0,
                "瞬间功率2": 0.0,
                "瞬间电流2": 0.0,
                "瞬间电压2": 0.0,
                "功率2": 0.0,
                "电压2": 0.0,
                "电流2": 0.0,
                "瞬间功率3": 0.0,
                "瞬间电流3": 0.0,
                "瞬间电压3": 0.0,
                "功率3": 0.0,
                "电压3": 0.0,
                "电流3": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "电阻定律实验"

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def l_lowmid(self) -> Pin:
        return self._l_lowmid_pin

    @property
    def l_upmid(self) -> Pin:
        return self._l_upmid_pin

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin

    @property
    def r_lowmid(self) -> Pin:
        return self._r_lowmid_pin

    @property
    def r_upmid(self) -> Pin:
        return self._r_upmid_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 8


class Resistance_Law(_ResistanceLaw):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _Solenoid(CircuitBase):
    """通电螺线管"""

    _all_pins: Tuple[
        Tuple[Literal["_subred_pin"], Pin],
        Tuple[Literal["_subblack_pin"], Pin],
        Tuple[Literal["_red_pin"], Pin],
        Tuple[Literal["_black_pin"], Pin],
    ]
    _subred_pin: Pin
    _subblack_pin: Pin
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_subred_pin", Pin(self, 0)),
            ("_subblack_pin", Pin(self, 1)),
            ("_red_pin", Pin(self, 2)),
            ("_black_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Solenoid",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "插入铁芯": 1.0,
                "内圈状态": 0.0,
                "切割速度": 1.0,
                "锁定": int(self.lock_status),
                "线圈匝数": 100.0,
                "线圈位置": 0.0,
                "内线圈半径": 0.1,
                "磁通量": 0.0,
            },
            "Statistics": {
                "电流-内线圈": 0.0,
                "功率-内线圈": 0.0,
                "电压-内线圈": 0.0,
                "磁感应强度": 0.0,
                "磁通量": 0.0,
                "电压-外线圈": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "通电螺线管"

    @property
    def subred(self) -> Pin:
        return self._subred_pin

    @property
    def subblack(self) -> Pin:
        return self._subblack_pin

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 4


class Solenoid(_Solenoid):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _ElectricFan(CircuitBase):
    """小电扇"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Electric Fan",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电阻": 1.0,
                "马达常数": 0.1,
                "转动惯量": 0.01,
                "电感": 5e-05,
                "负荷扭矩": 0.01,
                "反电动势系数": 0.001,
                "粘性摩擦系数": 0.01,
                "角速度": 0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0,
                "瞬间电流": 0,
                "瞬间电压": 0,
                "功率": 0,
                "电压": 0,
                "电流": 0,
                "摩擦扭矩": 0,
                "角速度": 0,
                "反电动势": 0,
                "转速": 0,
                "输入功率": 0,
                "输出功率": 0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "小电扇"

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Electric_Fan(_ElectricFan):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            identifier,
            label,
            lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _SimpleInstrument(CircuitBase):
    """简单乐器"""

    _all_pins: Tuple[Tuple[Literal["_i_pin"], Pin], Tuple[Literal["_o_pin"], Pin]]
    _i_pin: Pin
    _o_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        /,
        *,
        pitches: Union[List[int], Tuple[int]],
        experiment: Optional[_Experiment] = None,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        rated_oltage: num_type = 3.0,
        volume: num_type = 1,
        bpm: int = 100,
        instrument: int = 0,
        is_ideal: bool = False,
        is_pulse: bool = True,
        lock_status: bool = True,
    ) -> None:
        """@param rated_oltage: 额定电压
        @param volume: 音量 (响度)
        @param pitch: 音高
        @param instrument: 演奏的乐器，暂时只支持传入数字
        @param bpm: 节奏
        @param is_ideal: 是否为理想模式
        @param is_pulse: 简单乐器是否只响一次
        """
        self._all_pins = (
            ("_i_pin", Pin(self, 0)),
            ("_o_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.pitches: List[int] = list(pitches)
        self.set_rated_oltage(rated_oltage)
        self.set_volume(volume)
        self.set_bpm(bpm)
        self.set_instrument(instrument)
        self.set_is_ideal(is_ideal)
        self.set_is_pulse(is_pulse)
        super().__init__(position, identifier, lock_status, label)

    @final
    @staticmethod
    def zh_name() -> str:
        return "简单乐器"

    def as_dict(self) -> CircuitElementData:
        if not all(isinstance(a_pitch, int) for a_pitch in self.pitches):
            raise TypeError
        if not all(0 <= a_pitch < 128 for a_pitch in self.pitches):
            raise ValueError

        plar_version = plar.get_plAR_version()
        if plar_version is not None and plar_version < (2, 4, 7):
            _warn.warning("Physics-Lab-AR's version less than 2.4.7")

        properties = {
            "额定电压": self._rated_oltage,
            "额定功率": 0.3,
            "音量": self._volume,
            "节拍": self._bpm,
            "锁定": int(self.lock_status),
            "乐器": self._instrument,
            "理想模式": int(self._is_ideal),
            "脉冲": int(self._is_pulse),
            "电平": 0.0,
        }
        for i, a_pitch in enumerate(self.pitches):
            if i == 0:
                properties["音高"] = a_pitch
            else:
                properties[f"音高{i}"] = a_pitch
        properties["和弦"] = len(self.pitches)

        return {
            "ModelID": "Simple Instrument",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": properties,
            "Statistics": {
                "瞬间功率": 0,
                "瞬间电流": 0,
                "瞬间电压": 0,
                "功率": 0,
                "电压": 0,
                "电流": 0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def set_rated_oltage(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"rated_oltage must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self._rated_oltage = value

    def set_volume(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"volume must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        if not 0 <= value <= 1:
            raise ValueError(f"volume must be in range [0, 1], but got {value}")
        self._volume = value

    def set_bpm(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"bpm must be of type `int`, but got value {value} of type `{type(value).__name__}`"
            )
        if not 20 <= value <= 240:
            raise ValueError(f"bpm must be in range [20, 240], but got {value}")
        self._bpm = value

    def set_instrument(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"instrument must be of type `int`, but got value {value} of type `{type(value).__name__}`"
            )
        if not 0 <= value <= 128:
            raise ValueError(f"instrument must be in range [0, 128], but got {value}")
        self._instrument = value

    def set_is_ideal(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_ideal must be of type `bool`, but got value {value} of type `{type(value).__name__}`"
            )
        self._is_ideal = value

    def set_is_pulse(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_pulse must be of type `bool`, but got value {value} of type `{type(value).__name__}`"
            )
        self._is_pulse = value

    @property
    def i(self) -> Pin:
        return self._i_pin

    @property
    def o(self) -> Pin:
        return self._o_pin

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @override
    def __repr__(self) -> str:
        return (
            f"Simple_Instrument({self._position.x}, {self._position.y}, {self._position.z}, "
            f""
            f"pitches={self.pitches}, "
            f"instrument={self._instrument}, "
            f"bpm={self._bpm}, "
            f"volume={self._volume}, "
            f"rated_oltage={self._rated_oltage}, "
            f"is_ideal={self._is_ideal}, "
            f"is_pulse={self._is_pulse}"
            f")"
        )

    @staticmethod
    def str2num_pitch(pitch: str, rising_falling: Optional[bool] = None) -> int:
        """输入格式：
            pitch: C4, A5 ...
            rising_falling = True 时，为升调，为 False 时降调

        输入范围：
            C0 ~ C8
            注: C0: 24, C1: 36, C2: 48, C3: 60, ..., C8: 120
        """
        if not isinstance(pitch, str) or not isinstance(
            rising_falling, (bool, type(None))
        ):
            raise TypeError
        if (
            len(pitch) != 2
            or pitch.upper()[0] not in "ABCDEFG"
            or pitch[1] not in "012345678"
        ):
            raise ValueError

        var = 1 if rising_falling is True else 0 if rising_falling is None else -1

        res = (
            {
                "A": 22,
                "B": 23,
                "C": 24,
                "D": 25,
                "E": 26,
                "F": 27,
                "G": 28,
            }[pitch.upper()[0]]
            + 12 * int(pitch[1])
            + var
        )

        return res

    @staticmethod
    def count_all_pins() -> int:
        return 2


class Simple_Instrument(_SimpleInstrument):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        pitches: Union[List[int], Tuple[int]],
        experiment: Optional[_Experiment] = None,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        rated_oltage: num_type = 3.0,
        volume: num_type = 1,
        bpm: int = 100,
        instrument: int = 0,
        is_ideal: bool = False,
        is_pulse: bool = True,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            pitches=pitches,
            identifier=identifier,
            experiment=experiment,
            label=label,
            rated_oltage=rated_oltage,
            volume=volume,
            bpm=bpm,
            instrument=instrument,
            is_ideal=is_ideal,
            is_pulse=is_pulse,
            lock_status=lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()
