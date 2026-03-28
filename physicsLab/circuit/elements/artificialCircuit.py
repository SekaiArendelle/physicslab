import uuid
from physicsLab import coordinate_system
from .._base import CircuitBase
from ..pin import Pin
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Self,
    override,
    final,
    Tuple,
    Iterator,
    Literal,
)


class NE555(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_vcc_pin"], Pin],
        Tuple[Literal["_dis_pin"], Pin],
        Tuple[Literal["_thr_pin"], Pin],
        Tuple[Literal["_ctrl_pin"], Pin],
        Tuple[Literal["_trig_pin"], Pin],
        Tuple[Literal["_out_pin"], Pin],
        Tuple[Literal["_reset_pin"], Pin],
        Tuple[Literal["_ground_pin"], Pin],
    ]
    _vcc_pin: Pin
    _dis_pin: Pin
    _thr_pin: Pin
    _ctrl_pin: Pin
    _trig_pin: Pin
    _out_pin: Pin
    _reset_pin: Pin
    _ground_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_vcc_pin", Pin(self, 0, "vcc")),
            ("_dis_pin", Pin(self, 1, "dis")),
            ("_thr_pin", Pin(self, 2, "thr")),
            ("_ctrl_pin", Pin(self, 3, "ctrl")),
            ("_trig_pin", Pin(self, 4, "trig")),
            ("_out_pin", Pin(self, 5, "out")),
            ("_reset_pin", Pin(self, 6, "reset")),
            ("_ground_pin", Pin(self, 7, "ground")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "555 Timer",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": int(self.lock_status)},
            "Statistics": {
                "供电": 10,
                "放电": 0.0,
                "阈值": 4,
                "控制": 6.6666666666666666,
                "触发": 4,
                "输出": 0,
                "重设": 10,
                "接地": 0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "555定时器"

    @staticmethod
    def count_all_pins() -> int:
        return 8

    @property
    def VCC(self) -> Pin:
        return self._vcc_pin

    @property
    def Dis(self) -> Pin:
        return self._dis_pin

    @property
    def Thr(self) -> Pin:
        return self._thr_pin

    @property
    def Ctrl(self) -> Pin:
        return self._ctrl_pin

    @property
    def Trig(self) -> Pin:
        return self._trig_pin

    @property
    def Out(self) -> Pin:
        return self._out_pin

    @property
    def Reset(self) -> Pin:
        return self._reset_pin

    @property
    def Ground(self) -> Pin:
        return self._ground_pin


class BasicCapacitor(CircuitBase):
    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin
    peak_voltage: num_type
    capacitance: num_type
    internal_resistance: num_type
    is_ideal: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        peak_voltage: num_type = 16,
        capacitance: num_type = 1e-06,
        internal_resistance: num_type = 5,
        is_ideal: bool = False,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        """@param capacitance: 电容, 单位为F
        @param is_ideal: 是否为理想模式
        @param peak_voltage: 峰值电压, 单位为V
        @param internal_resistance: 内阻, 单位为Ω
        """
        if not isinstance(peak_voltage, (int, float)):
            raise TypeError(
                f"peak_voltage must be of type `int | float`, but got value `{peak_voltage}` of type {type(peak_voltage).__name__}"
            )
        if not isinstance(capacitance, (int, float)):
            raise TypeError(
                f"capacitance must be of type `int | float`, but got value `{capacitance}` of type {type(capacitance).__name__}"
            )
        if not isinstance(internal_resistance, (int, float)):
            raise TypeError(
                f"internal_resistance must be of type `int | float`, but got value `{internal_resistance}` of type {type(internal_resistance).__name__}"
            )
        if not isinstance(is_ideal, bool):
            raise TypeError(
                f"is_ideal must be of type `bool`, but got value `{is_ideal}` of type {type(is_ideal).__name__}"
            )

        self.peak_voltage: num_type = peak_voltage
        self.capacitance: num_type = capacitance
        self.internal_resistance: num_type = internal_resistance
        self.is_ideal: bool = is_ideal

        self._all_pins = (
            ("_red_pin", Pin(self, 0, "red")),
            ("_black_pin", Pin(self, 1, "black")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Basic Capacitor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "耐压": self.peak_voltage,
                "电容": self.capacitance,
                "内阻": self.internal_resistance,
                "理想模式": int(self.is_ideal),
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "电容"

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @override
    def __repr__(self) -> str:
        return (
            f"Basic_Capacitor({self.position.x}, {self.position.y}, {self.position.z}, "
            f"peak_voltage={self.peak_voltage}, "
            f"capacitance={self.capacitance}, "
            f"internal_resistance={self.internal_resistance}, "
            f"is_ideal={self.is_ideal})"
        )


class BasicInductor(CircuitBase):
    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin
    rated_current: num_type
    inductance: num_type
    internal_resistance: num_type
    is_ideal: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        rated_current: num_type = 1,
        inductance: num_type = 0.05,
        internal_resistance: num_type = 1,
        is_ideal: bool = False,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        """@param rated_current: 电感额定电流，单位为 A
        @param inductance: 电感，单位为 Henry
        @param internal_resistance: 电感内部阻抗，单位为 Ohm
        @param is_ideal: 是否为理想模式
        """
        if not isinstance(rated_current, (int, float)):
            raise TypeError(
                f"rated_current must be of type `int | float`, but got value `{rated_current}` of type {type(rated_current).__name__}"
            )
        if not isinstance(inductance, (int, float)):
            raise TypeError(
                f"inductance must be of type `int | float`, but got value `{inductance}` of type {type(inductance).__name__}"
            )
        if not isinstance(internal_resistance, (int, float)):
            raise TypeError(
                f"internal_resistance must be of type `int | float`, but got value `{internal_resistance}` of type {type(internal_resistance).__name__}"
            )
        if not isinstance(is_ideal, bool):
            raise TypeError(
                f"is_ideal must be of type `bool`, but got value `{is_ideal}` of type {type(is_ideal).__name__}"
            )

        self.rated_current: num_type = rated_current
        self.inductance: num_type = inductance
        self.internal_resistance: num_type = internal_resistance
        self.is_ideal: bool = is_ideal

        self._all_pins = (
            ("_red_pin", Pin(self, 0, "red")),
            ("_black_pin", Pin(self, 1, "black")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Basic Inductor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电流": self.rated_current,
                "电感": self.inductance,
                "内阻": self.internal_resistance,
                "锁定": int(self.lock_status),
                "理想模式": int(self.is_ideal),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "电感"

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @override
    def __repr__(self) -> str:
        return (
            f"Basic_Inductor({self.position.x}, {self.position.y}, {self.position.z}, "
            f"rated_current={self.rated_current}, "
            f"inductance={self.inductance}, "
            f"internal_resistance={self.internal_resistance}, "
            f"is_ideal={self.is_ideal})"
        )


class BasicDiode(CircuitBase):
    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0, "red")),
            ("_black_pin", Pin(self, 1, "black")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Basic Diode",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "击穿电压": 0.0,
                "前向压降": 0.6,
                "额定电流": 1.0,
                "工作电压": 3.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "二极管"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class LightEmittingDiode(CircuitBase):
    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0, "red")),
            ("_black_pin", Pin(self, 1, "black")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Light-Emitting Diode",
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
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "亮度1": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "发光二极管"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class GroundComponent(CircuitBase):
    _all_pins: Tuple[Tuple[Literal["_i_pin"], Pin]]
    _i_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (("_i_pin", Pin(self, 0, "i")),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Ground Component",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"锁定": int(self.lock_status)},
            "Statistics": {"电流": 0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "接地"

    @staticmethod
    def count_all_pins() -> int:
        return 1

    @property
    def i(self) -> Pin:
        return self._i_pin


class Transformer(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
    ]
    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0, "l_up")),
            ("_r_up_pin", Pin(self, 1, "r_up")),
            ("_l_low_pin", Pin(self, 2, "l_low")),
            ("_r_low_pin", Pin(self, 3, "r_low")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Transformer",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "输入电压": 3.0,
                "输出电压": 36.0,
                "额定功率": 20.0,
                "耦合系数": 1.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
                "功率2": 0.0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "理想变压器"

    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin


class TappedTransformer(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
    ]
    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin
    _mid_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0, "l_up")),
            ("_r_up_pin", Pin(self, 1, "r_up")),
            ("_l_low_pin", Pin(self, 2, "l_low")),
            ("_r_low_pin", Pin(self, 3, "r_low")),
            ("_mid_pin", Pin(self, 4, "mid")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Tapped Transformer",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "输入电压": 3.0,
                "输出电压": 36.0,
                "额定功率": 20.0,
                "耦合系数": 1.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "中心抽头变压器"

    @staticmethod
    def count_all_pins() -> int:
        return 5

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin


class MutualInductor(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
    ]
    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0, "l_up")),
            ("_r_up_pin", Pin(self, 1, "r_up")),
            ("_l_low_pin", Pin(self, 2, "l_low")),
            ("_r_low_pin", Pin(self, 3, "r_low")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Mutual Inductor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电感1": 4.0,
                "电感2": 1.0,
                "耦合系数": 1.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
                "功率2": 0.0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "理想互感"

    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin


class Rectifier(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
    ]
    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0, "l_up")),
            ("_r_up_pin", Pin(self, 1, "r_up")),
            ("_l_low_pin", Pin(self, 2, "l_low")),
            ("_r_low_pin", Pin(self, 3, "r_low")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Rectifier",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "前向压降": 0.8,
                "额定电流": 1.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "全波整流器"

    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin


class Transistor(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_B_pin"], Pin],
        Tuple[Literal["_C_pin"], Pin],
        Tuple[Literal["_E_pin"], Pin],
    ]
    _B_pin: Pin
    _C_pin: Pin
    _E_pin: Pin
    is_PNP: bool
    gain: num_type
    max_power: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        is_PNP: bool = True,
        gain: num_type = 100,
        max_power: num_type = 1000,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(is_PNP, bool):
            raise TypeError(
                f"is_PNP must be of type `bool`, but got value `{is_PNP}` of type `{type(is_PNP).__name__}`"
            )
        if not isinstance(gain, (int, float)):
            raise TypeError(
                f"gain must be of type `int | float`, but got value `{gain}` of type `{type(gain).__name__}`"
            )
        if not isinstance(max_power, (int, float)):
            raise TypeError(
                f"max_power must be of type `int | float`, but got value `{max_power}` of type `{type(max_power).__name__}`"
            )

        self.is_PNP: bool = is_PNP
        self.gain: num_type = gain
        self.max_power: num_type = max_power

        self._all_pins = (
            ("_B_pin", Pin(self, 0, "B")),
            ("_C_pin", Pin(self, 1, "C")),
            ("_E_pin", Pin(self, 2, "E")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Transistor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "PNP": int(self.is_PNP),
                "放大系数": self.gain,
                "最大功率": self.max_power,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电压BC": 0.0, "电压BE": 0.0, "电压CE": 0.0, "功率": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "三极管"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    def __repr__(self) -> str:
        res = (
            f"Transistor({self.position.x}, {self.position.y}, {self.position.z}, "
            f"is_PNP={self.is_PNP}"
        )

        # TODO 不论是否是默认参数都显示写到res里
        if self.gain != 100.0:
            res += f", gain={self.gain}"
        if self.max_power != 5.0:
            res += f", max_power={self.max_power}"
        return res + ")"

    @property
    def B(self) -> Pin:
        return self._B_pin

    @property
    def C(self) -> Pin:
        return self._C_pin

    @property
    def E(self) -> Pin:
        return self._E_pin


class Comparator(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_o_pin"], Pin],
        Tuple[Literal["_i_up_pin"], Pin],
        Tuple[Literal["_i_low_pin"], Pin],
    ]
    _o_pin: Pin
    _i_up_pin: Pin
    _i_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_o_pin", Pin(self, 0, "o")),
            ("_i_up_pin", Pin(self, 1, "i_up")),
            ("_i_low_pin", Pin(self, 2, "i_low")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Comparator",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": int(self.lock_status)},
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "比较器"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def o(self) -> Pin:
        return self._o_pin

    @property
    def i_up(self) -> Pin:
        return self._i_up_pin

    @property
    def i_low(self) -> Pin:
        return self._i_low_pin


class OperationalAmplifier(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_i_neg_pin"], Pin],
        Tuple[Literal["_i_pos_pin"], Pin],
        Tuple[Literal["_o_pin"], Pin],
    ]
    _i_neg_pin: Pin
    _i_pos_pin: Pin
    _o_pin: Pin
    gain: num_type
    max_voltage: num_type
    min_voltage: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        gain: num_type = 10_000_000,
        max_voltage: num_type = 1000,
        min_voltage: num_type = -1000,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        """@param gain: 增益系数
        @param max_voltage: 最大电压
        @param min_voltage: 最小电压
        """
        if not isinstance(gain, (int, float)):
            raise TypeError(
                f"gain must be of type `int | float`, but got value `{gain}` of type `{type(gain).__name__}`"
            )
        if not isinstance(max_voltage, (int, float)):
            raise TypeError(
                f"max_voltage must be of type `int | float`, but got value `{max_voltage}` of type `{type(max_voltage).__name__}`"
            )
        if not isinstance(min_voltage, (int, float)):
            raise TypeError(
                f"min_voltage must be of type `int | float`, but got value `{min_voltage}` of type `{type(min_voltage).__name__}`"
            )
        if min_voltage >= max_voltage:
            raise ValueError("min_voltage must less than max_voltage")

        self.gain: num_type = gain
        self.max_voltage: num_type = max_voltage
        self.min_voltage: num_type = min_voltage

        self._all_pins = (
            ("_i_neg_pin", Pin(self, 0, "i_neg")),
            ("_i_pos_pin", Pin(self, 1, "i_pos")),
            ("_o_pin", Pin(self, 2, "o")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Operational Amplifier",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "增益系数": self.gain,
                "最大电压": self.max_voltage,
                "最小电压": self.min_voltage,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电压-": 0,
                "电压+": 0,
                "输出电压": 0,
                "输出电流": 0,
                "输出功率": 0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @override
    def __repr__(self) -> str:
        return (
            f"Operational_Amplifier({self.position.x}, {self.position.y}, {self.position.z}, "
            f"gain={self.gain}, "
            f"max_voltage={self.max_voltage}, "
            f"min_voltage={self.min_voltage})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        return "运算放大器"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def i_neg(self) -> Pin:
        return self._i_neg_pin

    @property
    def i_pos(self) -> Pin:
        return self._i_pos_pin

    @property
    def o(self) -> Pin:
        return self._o_pin


class RelayComponent(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
    ]
    _l_up_pin: Pin
    _l_low_pin: Pin
    _mid_pin: Pin
    _r_up_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        pull_in_current: num_type = 0.02,
        rated_current: num_type = 10,
        coil_inductance: num_type = 0.2,
        coil_resistance: num_type = 20,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(pull_in_current, (int, float)):
            raise TypeError(
                f"pull_in_current must be of type `int | float`, but got value `{self.pull_in_current}` of type `{type(self.pull_in_current).__name__}`"
            )
        if not isinstance(rated_current, (int, float)):
            raise TypeError(
                f"rated_current must be of type `int | float`, but got value `{self.rated_current}` of type `{type(self.rated_current).__name__}`"
            )
        if not isinstance(coil_inductance, (int, float)):
            raise TypeError(
                f"coil_inductance must be of type `int | flaot`, but got value `{self.coil_inductance}` of type `{type(self.coil_inductance).__name__}`"
            )
        if not isinstance(coil_resistance, (int, float)):
            raise TypeError(
                f"coil_resistance must be of type `int | flaot`, but got value `{self.coil_resistance}` of type `{type(self.coil_resistance).__name__}`"
            )

        self.pull_in_current: num_type = pull_in_current
        self.rated_current: num_type = rated_current
        self.coil_inductance: num_type = coil_inductance
        self.coil_resistance: num_type = coil_resistance

        self._all_pins = (
            ("_l_up_pin", Pin(self, 0, "l_up")),
            ("_l_low_pin", Pin(self, 2, "l_low")),
            ("_mid_pin", Pin(self, 1, "mid")),
            ("_r_up_pin", Pin(self, 3, "r_up")),
            ("_r_low_pin", Pin(self, 4, "r_low")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Relay Component",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": 0.0,
                "线圈电感": self.coil_inductance,
                "线圈电阻": self.coil_resistance,
                "接通电流": self.pull_in_current,
                "额定电流": self.rated_current,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "继电器"

    @staticmethod
    def count_all_pins() -> int:
        return 5

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin


class N_MOSFET(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_D_pin"], Pin],
        Tuple[Literal["_S_pin"], Pin],
        Tuple[Literal["_G_pin"], Pin],
    ]
    _D_pin: Pin
    _S_pin: Pin
    _G_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        beta: num_type = 0.027,
        threshold: num_type = 1.5,
        max_power: num_type = 1000,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(beta, (int, float)):
            raise TypeError(
                f"beta must be of type `int | float`, but got value `{self.beta}` of type {type(self.beta).__name__}"
            )
        if not isinstance(threshold, (int, float)):
            raise TypeError(
                f"threshold must be of type `int | float`, but got value `{self.threshold}` of type {type(self.threshold).__name__}"
            )
        if not isinstance(max_power, (int, float)):
            raise TypeError(
                f"max_power must be of type `int | float`, but got value `{self.max_power}` of type {type(self.max_power).__name__}"
            )

        self.beta: num_type = beta
        self.threshold: num_type = threshold
        self.max_power: num_type = max_power

        self._all_pins = (
            ("_D_pin", Pin(self, 2, "D")),
            ("_S_pin", Pin(self, 1, "S")),
            ("_G_pin", Pin(self, 0, "G")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "N-MOSFET",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "PNP": 1.0,
                "放大系数": self.beta,
                "阈值电压": self.threshold,
                "最大功率": self.max_power,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电压GS": 0.0,
                "电压": 0.0,
                "电流": 0.0,
                "功率": 0.0,
                "状态": 0.0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "N-MOSFET"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def D(self) -> Pin:
        return self._D_pin

    @property
    def S(self) -> Pin:
        return self._S_pin

    @property
    def G(self) -> Pin:
        return self._G_pin


class P_MOSFET(CircuitBase):
    _all_pins: Tuple[
        Tuple[Literal["_G_pin"], Pin],
        Tuple[Literal["_D_pin"], Pin],
        Tuple[Literal["_S_pin"], Pin],
    ]
    _G_pin: Pin
    _S_pin: Pin
    _D_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_G_pin", Pin(self, 0, "G")),
            ("_D_pin", Pin(self, 1, "D")),
            ("_S_pin", Pin(self, 2, "S")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "P-MOSFET",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "PNP": 1.0,
                "放大系数": 0.027,
                "阈值电压": 1.5,
                "最大功率": 100.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "电压GS": 0.0,
                "电压": 0.0,
                "电流": 0.0,
                "功率": 0.0,
                "状态": 1.0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "P-MOSFET"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def G(self) -> Pin:
        return self._G_pin

    @property
    def S(self) -> Pin:
        return self._S_pin

    @property
    def D(self) -> Pin:
        return self._D_pin


class CurrentSource(CircuitBase):
    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0, "red")),
            ("_black_pin", Pin(self, 1, "black")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Current Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电流": 0.0099999997764825821,
                "内阻": 1000000000.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "电流源"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class _SourceElectricity(CircuitBase):
    _all_pins: Tuple[Tuple[str, Pin], Tuple[str, Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        identifier: str,
        label: Optional[str],
        lock_status: bool,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0, "red")),
            ("_black_pin", Pin(self, 1, "black")),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, rotation, identifier, lock_status, label)

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @staticmethod
    def count_all_pins() -> int:
        return 2


class SinewaveSource(_SourceElectricity):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        super().__init__(position, rotation, identifier, label, lock_status)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Sinewave Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电压": 3.0,
                "内阻": 0.5,
                "频率": 20000.0,
                "偏移": 0.0,
                "占空比": 0.5,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "正弦波发生器"


class SquareSource(_SourceElectricity):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        super().__init__(position, rotation, identifier, label, lock_status)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Square Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电压": 3.0,
                "内阻": 0.5,
                "频率": 20000.0,
                "偏移": 0.0,
                "占空比": 0.5,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "方波发生器"


class TriangleSource(_SourceElectricity):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        super().__init__(position, rotation, identifier, label, lock_status)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Triangle Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电压": 3.0,
                "内阻": 0.5,
                "频率": 20000.0,
                "偏移": 0.0,
                "占空比": 0.5,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "三角波发生器"


class SawtoothSource(_SourceElectricity):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        super().__init__(position, rotation, identifier, label, lock_status)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Sawtooth Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电压": 3.0,
                "内阻": 0.5,
                "频率": 20000.0,
                "偏移": 0.0,
                "占空比": 0.5,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "锯齿波发生器"


class PulseSource(_SourceElectricity):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        super().__init__(position, rotation, identifier, label, lock_status)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Pulse Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电压": 3.0,
                "内阻": 0.5,
                "频率": 20000.0,
                "偏移": 0.0,
                "占空比": 0.5,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "尖峰波发生器"
