"""Provide other circuit related functionality."""

import uuid
from physicslab import quantum_physics
from physicslab import coordinate_system

from .._base import CircuitBase, Pin
from physicslab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    List,
    Tuple,
    final,
    Iterator,
    Generator,
)


class Buzzer(CircuitBase):
    """Represent a buzzer component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"Buzzer("
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
        return "嗡鸣器"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class SparkGap(CircuitBase):
    """Represent a spark gap component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"SparkGap("
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
        return "火花隙"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class TeslaCoil(CircuitBase):
    """Represent a tesla coil component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"TeslaCoil("
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
        return "特斯拉线圈"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class ColorLightEmittingDiode(CircuitBase):
    """Represent a color light emitting diode component."""

    _l_up_pin: Pin
    _l_mid_pin: Pin
    _l_low_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._l_up_pin = Pin(self, 0, "l_up")
        self._l_mid_pin = Pin(self, 1, "l_mid")
        self._l_low_pin = Pin(self, 2, "l_low")
        self._r_pin = Pin(self, 3, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"ColorLightEmittingDiode("
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
        return "彩色发光二极管"

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_up", cls._get_property("l_up")
        yield "l_mid", cls._get_property("l_mid")
        yield "l_low", cls._get_property("l_low")
        yield "r", cls._get_property("r")

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def l_mid(self) -> Pin:
        """Execute the l mid routine."""
        return self._l_mid_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin

    @staticmethod
    def count_all_pins() -> int:
        return 4


class DualLightEmittingDiode(CircuitBase):
    """Represent a dual light emitting diode component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"DualLightEmittingDiode("
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
        return "演示发光二极管"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class ElectricBell(CircuitBase):
    """Represent a electric bell component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"ElectricBell("
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
        return "电铃"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class MusicalBox(CircuitBase):
    """Represent a musical box component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"MusicalBox("
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
        return "八音盒"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class ResistanceLaw(CircuitBase):
    """Represent a resistance law component."""

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
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        self._l_low_pin = Pin(self, 0, "l_low")
        self._l_lowmid_pin = Pin(self, 1, "l_lowmid")
        self._l_upmid_pin = Pin(self, 2, "l_upmid")
        self._l_up_pin = Pin(self, 3, "l_up")
        self._r_low_pin = Pin(self, 4, "r_low")
        self._r_lowmid_pin = Pin(self, 5, "r_lowmid")
        self._r_upmid_pin = Pin(self, 6, "r_upmid")
        self._r_up_pin = Pin(self, 7, "r_up")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"ResistanceLaw("
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
        return "电阻定律实验"

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "l_low", cls._get_property("l_low")
        yield "l_lowmid", cls._get_property("l_lowmid")
        yield "l_upmid", cls._get_property("l_upmid")
        yield "l_up", cls._get_property("l_up")
        yield "r_low", cls._get_property("r_low")
        yield "r_lowmid", cls._get_property("r_lowmid")
        yield "r_upmid", cls._get_property("r_upmid")
        yield "r_up", cls._get_property("r_up")

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def l_lowmid(self) -> Pin:
        """Execute the l lowmid routine."""
        return self._l_lowmid_pin

    @property
    def l_upmid(self) -> Pin:
        """Execute the l upmid routine."""
        return self._l_upmid_pin

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin

    @property
    def r_lowmid(self) -> Pin:
        """Execute the r lowmid routine."""
        return self._r_lowmid_pin

    @property
    def r_upmid(self) -> Pin:
        """Execute the r upmid routine."""
        return self._r_upmid_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @staticmethod
    def count_all_pins() -> int:
        return 8


class Solenoid(CircuitBase):
    """Represent a solenoid component."""

    _subred_pin: Pin
    _subblack_pin: Pin
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
        self._subred_pin = Pin(self, 0, "subred")
        self._subblack_pin = Pin(self, 1, "subblack")
        self._red_pin = Pin(self, 2, "red")
        self._black_pin = Pin(self, 3, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"Solenoid("
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
        return "通电螺线管"

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "subred", cls._get_property("subred")
        yield "subblack", cls._get_property("subblack")
        yield "red", cls._get_property("red")
        yield "black", cls._get_property("black")

    @property
    def subred(self) -> Pin:
        """Execute the subred routine."""
        return self._subred_pin

    @property
    def subblack(self) -> Pin:
        """Execute the subblack routine."""
        return self._subblack_pin

    @property
    def red(self) -> Pin:
        """Execute the red routine."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Execute the black routine."""
        return self._black_pin

    @staticmethod
    def count_all_pins() -> int:
        return 4


class ElectricFan(CircuitBase):
    """Represent a electric fan component."""

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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"ElectricFan("
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
        return "小电扇"

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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class SimpleInstrument(CircuitBase):
    """Represent a simple instrument component."""

    _i_pin: Pin
    _o_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        pitches: List[int],
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
        """Initialize a simple instrument.

        Args:
            rated_oltage: Rated voltage.
            volume: Playback volume.
            pitch: Pitch value.
            instrument: Instrument ID (currently numeric only).
            bpm: Tempo in beats per minute.
            is_ideal: Whether to use ideal mode.
            is_pulse: Whether the instrument plays only once per trigger.
        """
        self._i_pin = Pin(self, 0, "i")
        self._o_pin = Pin(self, 1, "o")
        self.pitches: List[int] = pitches
        self.rated_oltage = rated_oltage
        self.volume = volume
        self.bpm = bpm
        self.instrument = instrument
        self.is_ideal = is_ideal
        self.is_pulse = is_pulse
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "简单乐器"

    def as_dict(self) -> CircuitElementData:
        if not all(isinstance(a_pitch, int) for a_pitch in self.pitches):
            raise TypeError
        if not all(0 <= a_pitch < 128 for a_pitch in self.pitches):
            raise ValueError

        plar_version = quantum_physics.get_quantum_physics_version()
        if plar_version is not None and plar_version < (2, 4, 7):
            raise NotImplementedError(
                "SimpleInstrument is not supported in Quantum Physics version below 2.4.7"
            )

        properties = {
            "额定电压": self.rated_oltage,
            "额定功率": 0.3,
            "音量": self.volume,
            "节拍": self.bpm,
            "锁定": int(self.lock_status),
            "乐器": self.instrument,
            "理想模式": int(self.is_ideal),
            "脉冲": int(self.is_pulse),
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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "i", cls._get_property("i")
        yield "o", cls._get_property("o")

    @property
    def rated_oltage(self) -> num_type:
        """Execute the rated oltage routine."""
        return self.__rated_oltage

    @rated_oltage.setter
    def rated_oltage(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"rated_oltage must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__rated_oltage = value

    @property
    def volume(self) -> num_type:
        """Execute the volume routine."""
        return self.__volume

    @volume.setter
    def volume(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"volume must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        if not 0 <= value <= 1:
            raise ValueError(f"volume must be in range [0, 1], but got {value}")
        self.__volume = value

    @property
    def bpm(self) -> int:
        """Execute the bpm routine."""
        return self.__bpm

    @bpm.setter
    def bpm(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"bpm must be of type `int`, but got value {value} of type `{type(value).__name__}`"
            )
        if not 20 <= value <= 240:
            raise ValueError(f"bpm must be in range [20, 240], but got {value}")
        self.__bpm = value

    @property
    def instrument(self) -> int:
        """Execute the instrument routine."""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"instrument must be of type `int`, but got value {value} of type `{type(value).__name__}`"
            )
        if not 0 <= value <= 128:
            raise ValueError(f"instrument must be in range [0, 128], but got {value}")
        self.__instrument = value

    @property
    def is_ideal(self) -> bool:
        """Check whether the instance is ideal."""
        return self.__is_ideal

    @is_ideal.setter
    def is_ideal(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_ideal must be of type `bool`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__is_ideal = value

    @property
    def is_pulse(self) -> bool:
        """Check whether the instance is pulse."""
        return self.__is_pulse

    @is_pulse.setter
    def is_pulse(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_pulse must be of type `bool`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__is_pulse = value

    @property
    def i(self) -> Pin:
        """Execute the i routine."""
        return self._i_pin

    @property
    def o(self) -> Pin:
        """Execute the o routine."""
        return self._o_pin

    def to_constructor_str(self) -> str:
        return (
            f"SimpleInstrument("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"pitches={self.pitches!r}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"rated_oltage={self.rated_oltage}, "
            f"volume={self.volume}, "
            f"bpm={self.bpm}, "
            f"instrument={self.instrument}, "
            f"is_ideal={self.is_ideal}, "
            f"is_pulse={self.is_pulse}, "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def str2num_pitch(pitch: str, rising_falling: Optional[bool] = None) -> int:
        """Convert pitch notation to the numeric pitch value.

        Args:
            pitch: Pitch notation such as ``C4`` or ``A5``.
            rising_falling: ``True`` for sharp, ``False`` for flat, ``None`` for natural.

        Returns:
            int: Numeric pitch value.

        Notes:
            Supported range is ``C0`` to ``C8``.
            Examples: ``C0=24``, ``C1=36``, ``C2=48``, ``C3=60``, ..., ``C8=120``.
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
