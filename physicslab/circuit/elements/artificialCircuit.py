"""Provide artificial circuit related functionality."""

import uuid
from physicslab import coordinate_system
from .._base import CircuitBase, Pin
from physicslab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    final,
    Tuple,
    Iterator,
    Generator,
)


class NE555(CircuitBase):
    """Represent a n e555 component."""

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
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._vcc_pin = Pin(self, 0, "vcc")
        self._dis_pin = Pin(self, 1, "dis")
        self._thr_pin = Pin(self, 2, "thr")
        self._ctrl_pin = Pin(self, 3, "ctrl")
        self._trig_pin = Pin(self, 4, "trig")
        self._out_pin = Pin(self, 5, "out")
        self._reset_pin = Pin(self, 6, "reset")
        self._ground_pin = Pin(self, 7, "ground")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "vcc", cls._get_property("vcc")
        yield "dis", cls._get_property("dis")
        yield "thr", cls._get_property("thr")
        yield "ctrl", cls._get_property("ctrl")
        yield "trig", cls._get_property("trig")
        yield "out", cls._get_property("out")
        yield "reset", cls._get_property("reset")
        yield "ground", cls._get_property("ground")

    def to_constructor_str(self) -> str:
        return (
            f"NE555("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "555定时器"

    @staticmethod
    def count_all_pins() -> int:
        return 8

    @property
    def vcc(self) -> Pin:
        """Execute the vcc routine."""
        return self._vcc_pin

    @property
    def dis(self) -> Pin:
        """Execute the dis routine."""
        return self._dis_pin

    @property
    def thr(self) -> Pin:
        """Execute the thr routine."""
        return self._thr_pin

    @property
    def ctrl(self) -> Pin:
        """Execute the ctrl routine."""
        return self._ctrl_pin

    @property
    def trig(self) -> Pin:
        """Execute the trig routine."""
        return self._trig_pin

    @property
    def out(self) -> Pin:
        """Execute the out routine."""
        return self._out_pin

    @property
    def reset(self) -> Pin:
        """Execute the reset routine."""
        return self._reset_pin

    @property
    def ground(self) -> Pin:
        """Execute the ground routine."""
        return self._ground_pin


class BasicCapacitor(CircuitBase):
    """Represent a basic capacitor component."""

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
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        """Initialize a capacitor element.

        Args:
            capacitance: Capacitance in farads (F).
            is_ideal: Whether to use ideal mode.
            peak_voltage: Peak voltage in volts (V).
            internal_resistance: Internal resistance in ohms (Ohm).
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

        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "电容"

    @staticmethod
    def count_all_pins() -> int:
        return 2

    def to_constructor_str(self) -> str:
        return (
            f"BasicCapacitor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"peak_voltage={self.peak_voltage}, "
            f"capacitance={self.capacitance}, "
            f"internal_resistance={self.internal_resistance}, "
            f"is_ideal={self.is_ideal}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )


class BasicInductor(CircuitBase):
    """Represent a basic inductor component."""

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
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        """Initialize an inductor element.

        Args:
            rated_current: Rated current in amperes (A).
            inductance: Inductance in henries (H).
            internal_resistance: Internal resistance in ohms (Ohm).
            is_ideal: Whether to use ideal mode.
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

        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "电感"

    @staticmethod
    def count_all_pins() -> int:
        return 2

    def to_constructor_str(self) -> str:
        return (
            f"BasicInductor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"rated_current={self.rated_current}, "
            f"inductance={self.inductance}, "
            f"internal_resistance={self.internal_resistance}, "
            f"is_ideal={self.is_ideal}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )


class BasicDiode(CircuitBase):
    """Represent a basic diode component."""

    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    def to_constructor_str(self) -> str:
        return (
            f"BasicDiode("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "二极管"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class LightEmittingDiode(CircuitBase):
    """Represent a light emitting diode component."""

    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    def to_constructor_str(self) -> str:
        return (
            f"LightEmittingDiode("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "发光二极管"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class GroundComponent(CircuitBase):
    """Represent a ground component component."""

    _i_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._i_pin = Pin(self, 0, "i")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "i", cls._get_property("i")

    def to_constructor_str(self) -> str:
        return (
            f"GroundComponent("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "接地"

    @staticmethod
    def count_all_pins() -> int:
        return 1

    @property
    def i(self) -> Pin:
        """Execute the i routine."""
        return self._i_pin


class Transformer(CircuitBase):
    """Represent a transformer component."""

    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._l_up_pin = Pin(self, 0, "l_up")
        self._r_up_pin = Pin(self, 1, "r_up")
        self._l_low_pin = Pin(self, 2, "l_low")
        self._r_low_pin = Pin(self, 3, "r_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_up", cls._get_property("l_up")
        yield "r_up", cls._get_property("r_up")
        yield "l_low", cls._get_property("l_low")
        yield "r_low", cls._get_property("r_low")

    def to_constructor_str(self) -> str:
        return (
            f"Transformer("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "理想变压器"

    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin


class TappedTransformer(CircuitBase):
    """Represent a tapped transformer component."""

    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin
    _mid_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._l_up_pin = Pin(self, 0, "l_up")
        self._r_up_pin = Pin(self, 1, "r_up")
        self._l_low_pin = Pin(self, 2, "l_low")
        self._r_low_pin = Pin(self, 3, "r_low")
        self._mid_pin = Pin(self, 4, "mid")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_up", cls._get_property("l_up")
        yield "r_up", cls._get_property("r_up")
        yield "l_low", cls._get_property("l_low")
        yield "r_low", cls._get_property("r_low")
        yield "mid", cls._get_property("mid")

    def to_constructor_str(self) -> str:
        return (
            f"TappedTransformer("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "中心抽头变压器"

    @staticmethod
    def count_all_pins() -> int:
        return 5

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin


class MutualInductor(CircuitBase):
    """Represent a mutual inductor component."""

    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._l_up_pin = Pin(self, 0, "l_up")
        self._r_up_pin = Pin(self, 1, "r_up")
        self._l_low_pin = Pin(self, 2, "l_low")
        self._r_low_pin = Pin(self, 3, "r_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_up", cls._get_property("l_up")
        yield "r_up", cls._get_property("r_up")
        yield "l_low", cls._get_property("l_low")
        yield "r_low", cls._get_property("r_low")

    def to_constructor_str(self) -> str:
        return (
            f"MutualInductor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "理想互感"

    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin


class Rectifier(CircuitBase):
    """Represent a rectifier component."""

    _l_up_pin: Pin
    _r_up_pin: Pin
    _l_low_pin: Pin
    _r_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._l_up_pin = Pin(self, 0, "l_up")
        self._r_up_pin = Pin(self, 1, "r_up")
        self._l_low_pin = Pin(self, 2, "l_low")
        self._r_low_pin = Pin(self, 3, "r_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_up", cls._get_property("l_up")
        yield "r_up", cls._get_property("r_up")
        yield "l_low", cls._get_property("l_low")
        yield "r_low", cls._get_property("r_low")

    def to_constructor_str(self) -> str:
        return (
            f"Rectifier("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "全波整流器"

    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin


class Transistor(CircuitBase):
    """Represent a transistor component."""

    _b_pin: Pin
    _c_pin: Pin
    _e_pin: Pin
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
        identifier: Optional[str] = None,
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

        self._b_pin = Pin(self, 0, "B")
        self._c_pin = Pin(self, 1, "C")
        self._e_pin = Pin(self, 2, "E")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "b", cls._get_property("b")
        yield "c", cls._get_property("c")
        yield "e", cls._get_property("e")

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "三极管"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    def to_constructor_str(self) -> str:
        return (
            f"Transistor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"is_PNP={self.is_PNP}, "
            f"gain={self.gain}, "
            f"max_power={self.max_power}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @property
    def b(self) -> Pin:
        """Execute the b routine."""
        return self._b_pin

    @property
    def c(self) -> Pin:
        """Execute the c routine."""
        return self._c_pin

    @property
    def e(self) -> Pin:
        """Execute the e routine."""
        return self._e_pin


class Comparator(CircuitBase):
    """Represent a comparator component."""

    _o_pin: Pin
    _i_up_pin: Pin
    _i_low_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._o_pin = Pin(self, 0, "o")
        self._i_up_pin = Pin(self, 1, "i_up")
        self._i_low_pin = Pin(self, 2, "i_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "o", cls._get_property("o")
        yield "i_up", cls._get_property("i_up")
        yield "i_low", cls._get_property("i_low")

    def to_constructor_str(self) -> str:
        return (
            f"Comparator("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "比较器"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def o(self) -> Pin:
        """Execute the o routine."""
        return self._o_pin

    @property
    def i_up(self) -> Pin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> Pin:
        """Execute the i low routine."""
        return self._i_low_pin


class OperationalAmplifier(CircuitBase):
    """Represent a operational amplifier component."""

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
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        """Initialize an operational amplifier element.

        Args:
            gain: Gain factor.
            max_voltage: Maximum output voltage.
            min_voltage: Minimum output voltage.
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

        self._i_neg_pin = Pin(self, 0, "i_neg")
        self._i_pos_pin = Pin(self, 1, "i_pos")
        self._o_pin = Pin(self, 2, "o")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "i_neg", cls._get_property("i_neg")
        yield "i_pos", cls._get_property("i_pos")
        yield "o", cls._get_property("o")

    def to_constructor_str(self) -> str:
        return (
            f"OperationalAmplifier("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"gain={self.gain}, "
            f"max_voltage={self.max_voltage}, "
            f"min_voltage={self.min_voltage}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "运算放大器"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def i_neg(self) -> Pin:
        """Execute the i neg routine."""
        return self._i_neg_pin

    @property
    def i_pos(self) -> Pin:
        """Execute the i pos routine."""
        return self._i_pos_pin

    @property
    def o(self) -> Pin:
        """Execute the o routine."""
        return self._o_pin


class RelayComponent(CircuitBase):
    """Represent a relay component component."""

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
        identifier: Optional[str] = None,
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

        self._l_up_pin = Pin(self, 0, "l_up")
        self._l_low_pin = Pin(self, 2, "l_low")
        self._mid_pin = Pin(self, 1, "mid")
        self._r_up_pin = Pin(self, 3, "r_up")
        self._r_low_pin = Pin(self, 4, "r_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_up", cls._get_property("l_up")
        yield "l_low", cls._get_property("l_low")
        yield "mid", cls._get_property("mid")
        yield "r_up", cls._get_property("r_up")
        yield "r_low", cls._get_property("r_low")

    def to_constructor_str(self) -> str:
        return (
            f"RelayComponent("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"pull_in_current={self.pull_in_current}, "
            f"rated_current={self.rated_current}, "
            f"coil_inductance={self.coil_inductance}, "
            f"coil_resistance={self.coil_resistance}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "继电器"

    @staticmethod
    def count_all_pins() -> int:
        return 5

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin


class N_MOSFET(CircuitBase):
    """Represent a n m o s f e t component."""

    _d_pin: Pin
    _s_pin: Pin
    _g_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        beta: num_type = 0.027,
        threshold: num_type = 1.5,
        max_power: num_type = 1000,
        identifier: Optional[str] = None,
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

        self._d_pin = Pin(self, 2, "D")
        self._s_pin = Pin(self, 1, "S")
        self._g_pin = Pin(self, 0, "G")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "d", cls._get_property("d")
        yield "s", cls._get_property("s")
        yield "g", cls._get_property("g")

    def to_constructor_str(self) -> str:
        return (
            f"N_MOSFET("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"beta={self.beta}, "
            f"threshold={self.threshold}, "
            f"max_power={self.max_power}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "N-MOSFET"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def d(self) -> Pin:
        """Execute the d routine."""
        return self._d_pin

    @property
    def s(self) -> Pin:
        """Execute the s routine."""
        return self._s_pin

    @property
    def g(self) -> Pin:
        """Execute the g routine."""
        return self._g_pin


class P_MOSFET(CircuitBase):
    """Represent a p m o s f e t component."""

    _g_pin: Pin
    _s_pin: Pin
    _d_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._g_pin = Pin(self, 0, "G")
        self._d_pin = Pin(self, 1, "D")
        self._s_pin = Pin(self, 2, "S")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "g", cls._get_property("g")
        yield "d", cls._get_property("d")
        yield "s", cls._get_property("s")

    def to_constructor_str(self) -> str:
        return (
            f"P_MOSFET("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "P-MOSFET"

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def g(self) -> Pin:
        """Execute the g routine."""
        return self._g_pin

    @property
    def s(self) -> Pin:
        """Execute the s routine."""
        return self._s_pin

    @property
    def d(self) -> Pin:
        """Execute the d routine."""
        return self._d_pin


class CurrentSource(CircuitBase):
    """Represent a current source component."""

    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    def to_constructor_str(self) -> str:
        return (
            f"CurrentSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "电流源"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class _SourceElectricity(CircuitBase):
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
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    def to_constructor_str(self) -> str:
        return (
            f"_SourceElectricity("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def count_all_pins() -> int:
        return 2


class SinewaveSource(_SourceElectricity):
    """Represent a sinewave source component."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    def to_constructor_str(self) -> str:
        return (
            f"SinewaveSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "正弦波发生器"


class SquareSource(_SourceElectricity):
    """Represent a square source component."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    def to_constructor_str(self) -> str:
        return (
            f"SquareSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "方波发生器"


class TriangleSource(_SourceElectricity):
    """Represent a triangle source component."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    def to_constructor_str(self) -> str:
        return (
            f"TriangleSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "三角波发生器"


class SawtoothSource(_SourceElectricity):
    """Represent a sawtooth source component."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    def to_constructor_str(self) -> str:
        return (
            f"SawtoothSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "锯齿波发生器"


class PulseSource(_SourceElectricity):
    """Represent a pulse source component."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
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

    def to_constructor_str(self) -> str:
        return (
            f"PulseSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "尖峰波发生器"
