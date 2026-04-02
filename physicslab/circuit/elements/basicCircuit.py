"""Provide basic circuit related functionality."""

import uuid
from physicslab import coordinate_system
from .._base import CircuitBase, Pin
from physicslab.enums import SwitchState, PDTSwitchState
from physicslab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    final,
    Iterator,
    Tuple,
)


class _SwitchBase(CircuitBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)


class SimpleSwitch(_SwitchBase):
    """Represent a simple switch component."""
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        switch_state: SwitchState = SwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            identifier,
            lock_status,
            label,
        )
        self.switch_state = switch_state
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

    @property
    def switch_state(self) -> SwitchState:
        """Execute the switch state routine."""
        return self._switch_state

    @switch_state.setter
    def switch_state(self, value: SwitchState) -> None:
        if not isinstance(value, SwitchState):
            raise TypeError(
                f"switch_state must be of type `SwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self._switch_state = value

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

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "简单开关"

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Simple Switch",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": self.switch_state.value,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        return (
            f"SimpleSwitch("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"switch_state=SwitchState.{self.switch_state.name}, "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )


class SPDTSwitch(_SwitchBase):
    """Represent a s p d t switch component."""
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        switch_state: PDTSwitchState = PDTSwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)
        self.switch_state = switch_state
        self._l_pin = Pin(self, 0, "l")
        self._mid_pin = Pin(self, 1, "mid")
        self._r_pin = Pin(self, 2, "r")

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "mid", cls.mid
        yield "r", cls.r

    @property
    def switch_state(self) -> PDTSwitchState:
        """Execute the switch state routine."""
        return self._switch_state

    @switch_state.setter
    def switch_state(self, value: PDTSwitchState) -> None:
        if not isinstance(value, PDTSwitchState):
            raise TypeError(
                f"switch_state must be of type `PDTSwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self._switch_state = value

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "单刀双掷开关"

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "SPDT Switch",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": self.switch_state.value,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"SPDTSwitch("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"switch_state=PDTSwitchState.{self.switch_state.name}, "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin

    @staticmethod
    def count_all_pins() -> int:
        return 3


class DPDTSwitch(_SwitchBase):
    """Represent a d p d t switch component."""
    _l_low_pin: Pin
    _mid_low_pin: Pin
    _r_low_pin: Pin
    _l_up_pin: Pin
    _mid_up_pin: Pin
    _r_up_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        switch_state: PDTSwitchState = PDTSwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_low_pin = Pin(self, 0, "l_low")
        self._mid_low_pin = Pin(self, 1, "mid_low")
        self._r_low_pin = Pin(self, 2, "r_low")
        self._l_up_pin = Pin(self, 3, "l_up")
        self._mid_up_pin = Pin(self, 4, "mid_up")
        self._r_up_pin = Pin(self, 5, "r_up")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)
        self.switch_state = switch_state

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l_low", cls.l_low
        yield "mid_low", cls.mid_low
        yield "r_low", cls.r_low
        yield "l_up", cls.l_up
        yield "mid_up", cls.mid_up
        yield "r_up", cls.r_up

    @property
    def switch_state(self) -> PDTSwitchState:
        """Execute the switch state routine."""
        return self._switch_state

    @switch_state.setter
    def switch_state(self, value: PDTSwitchState) -> None:
        if not isinstance(value, PDTSwitchState):
            raise TypeError(
                f"switch_state must be of type `PDTSwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self._switch_state = value

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "双刀双掷开关"

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "DPDT Switch",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": self.switch_state.value,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"DPDTSwitch("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"switch_state=PDTSwitchState.{self.switch_state.name}, "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def mid_up(self) -> Pin:
        """Execute the mid up routine."""
        return self._mid_up_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def mid_low(self) -> Pin:
        """Execute the mid low routine."""
        return self._mid_low_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin

    @staticmethod
    def count_all_pins() -> int:
        return 6


class PushSwitch(CircuitBase):
    """Represent a push switch component."""
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Push Switch",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"开关": 0.0, "默认开关": 0.0, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

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
            f"PushSwitch("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "按钮开关"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class AirSwitch(CircuitBase):
    """Represent a air switch component."""
    _red_pin: Pin
    _black_pin: Pin
    __switch_state: SwitchState

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
        switch_state: SwitchState = SwitchState.OFF,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        self.switch_state = switch_state
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Air Switch",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": self.switch_state.value,
                "额定电流": 10.0,
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
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

    @property
    def switch_state(self) -> SwitchState:
        """Execute the switch state routine."""
        return self.__switch_state

    @switch_state.setter
    def switch_state(self, value: SwitchState) -> None:
        if not isinstance(value, SwitchState):
            raise TypeError(
                f"switch_state must be of type `SwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.__switch_state = value

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
        return "空气开关"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    def to_constructor_str(self) -> str:
        return (
            f"AirSwitch("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r}, "
            f"switch_state=SwitchState.{self.switch_state.name})"
        )


class IncandescentLamp(CircuitBase):
    """Represent a incandescent lamp component."""
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Incandescent Lamp",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电压": 3.0,
                "额定功率": 0.85,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
                "灯泡温度": 300.0,
                "电阻": 0.5,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

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
            f"IncandescentLamp("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "白炽灯泡"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class BatterySource(CircuitBase):
    """Represent a battery source component."""
    _red_pin: Pin
    _black_pin: Pin
    voltage: num_type
    internal_resistance: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        voltage: num_type = 1.5,
        internal_resistance: num_type = 0,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if not isinstance(voltage, (int, float)):
            raise TypeError(
                f"voltage must be of type `int | float`, but got value `{voltage}` of type `{type(voltage).__name__}`"
            )
        if not isinstance(internal_resistance, (int, float)):
            raise TypeError(
                f"internal_resistance must be of type `int | float`, but got value `{internal_resistance}` of type `{type(internal_resistance).__name__}`"
            )

        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")

        self.voltage = voltage
        self.internal_resistance = internal_resistance
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Battery Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "最大功率": 16.2,
                "电压": self.voltage,
                "内阻": self.internal_resistance,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0, "功率": 0, "电压": 0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

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
            f"BatterySource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"voltage={self.voltage}, "
            f"internal_resistance={self.internal_resistance}, "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "一节电池"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class StudentSource(CircuitBase):
    """Represent a student source component."""
    _l_pin: Pin
    _l_mid_pin: Pin
    _r_mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_pin = Pin(self, 0, "l")
        self._l_mid_pin = Pin(self, 1, "l_mid")
        self._r_mid_pin = Pin(self, 2, "r_mid")
        self._r_pin = Pin(self, 3, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Student Source",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "交流电压": 3.0,
                "直流电压": 3.0,
                "开关": 0.0,
                "频率": 50.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电压": 0.0,
                "瞬间电流": 0.0,
                "瞬间电阻": 0.0,
                "功率": 0.0,
                "电阻": 0.0,
                "电流": 0.0,
                "瞬间功率1": 0.0,
                "瞬间电压1": 0.0,
                "瞬间电流1": 0.0,
                "瞬间电阻1": 0.0,
                "功率1": 0.0,
                "电阻1": 0.0,
                "电流1": 0.0,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"StudentSource("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "学生电源"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 4

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "l_mid", cls.l_mid
        yield "r_mid", cls.r_mid
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def l_mid(self) -> Pin:
        """Execute the l mid routine."""
        return self._l_mid_pin

    @property
    def r_mid(self) -> Pin:
        """Execute the r mid routine."""
        return self._r_mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin


class Resistor(CircuitBase):
    """Represent a resistor component."""
    _red_pin: Pin
    _black_pin: Pin
    resistance: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        resistance: num_type = 10,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if not isinstance(resistance, (int, float)):
            raise TypeError(
                f"resistance must be of type `int | float`, but got value `{resistance}` of type `{type(resistance).__name__}`"
            )

        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        self.resistance = resistance
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Resistor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "最大电阻": 10_000_000.0,
                "最小电阻": 0.1,
                "电阻": self.resistance,
                "锁定": int(self.lock_status),
            },
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
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

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
        return "电阻"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    def to_constructor_str(self) -> str:
        return (
            f"Resistor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"resistance={self.resistance}, "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )


class FuseComponent(CircuitBase):
    """Represent a fuse component component."""
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Fuse Component",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": 1.0,
                "额定电流": 0.3,
                "熔断电流": 0.5,
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

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

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
            f"FuseComponent("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "保险丝"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class SlideRheostat(CircuitBase):
    """Represent a slide rheostat component."""
    _l_low_pin: Pin
    _r_low_pin: Pin
    _l_up_pin: Pin
    _r_up_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_low_pin = Pin(self, 0, "l_low")
        self._r_low_pin = Pin(self, 1, "r_low")
        self._l_up_pin = Pin(self, 2, "l_up")
        self._r_up_pin = Pin(self, 3, "r_up")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Slide Rheostat",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电阻": 10.0,
                "滑块位置": 0.0,
                "电阻1": 10,
                "电阻2": 10.0,
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
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"SlideRheostat("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "滑动变阻器"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 4

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l_low", cls.l_low
        yield "r_low", cls.r_low
        yield "l_up", cls.l_up
        yield "r_up", cls.r_up

    @property
    def l_low(self) -> Pin:
        """Execute the l low routine."""
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        """Execute the r low routine."""
        return self._r_low_pin

    @property
    def l_up(self) -> Pin:
        """Execute the l up routine."""
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        """Execute the r up routine."""
        return self._r_up_pin


class Multimeter(CircuitBase):
    """Represent a multimeter component."""
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._red_pin = Pin(self, 0, "red")
        self._black_pin = Pin(self, 1, "black")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Multimeter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"状态": 0.0, "锁定": int(self.lock_status)},
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

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "red", cls.red
        yield "black", cls.black

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
            f"Multimeter("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "多用电表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class Galvanometer(CircuitBase):
    """Represent a galvanometer component."""
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_pin = Pin(self, 0, "l")
        self._mid_pin = Pin(self, 1, "mid")
        self._r_pin = Pin(self, 2, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Galvanometer",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 3.0, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"Galvanometer("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "灵敏电流计"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "mid", cls.mid
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin


class Microammeter(CircuitBase):
    """Represent a microammeter component."""
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_pin = Pin(self, 0, "l")
        self._mid_pin = Pin(self, 1, "mid")
        self._r_pin = Pin(self, 2, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Microammeter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 0.1, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"Microammeter("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "微安表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "mid", cls.mid
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin


class ElectricityMeter(CircuitBase):
    """Represent a electricity meter component."""
    _l_pin: Pin
    _l_mid_pin: Pin
    _r_mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_pin = Pin(self, 0, "l")
        self._l_mid_pin = Pin(self, 2, "l_mid")
        self._r_mid_pin = Pin(self, 1, "r_mid")
        self._r_pin = Pin(self, 3, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Electricity Meter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"示数": 0.0, "额定电流": 6.0, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"ElectricityMeter("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "电能表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 4

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "l_mid", cls.l_mid
        yield "r_mid", cls.r_mid
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def l_mid(self) -> Pin:
        """Execute the l mid routine."""
        return self._l_mid_pin

    @property
    def r_mid(self) -> Pin:
        """Execute the r mid routine."""
        return self._r_mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin


class ResistanceBox(CircuitBase):
    """Represent a resistance box component."""
    _l_pin: Pin
    _r_pin: Pin
    resistance: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        resistance: num_type = 10,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if not isinstance(resistance, (int, float)):
            raise TypeError(
                f"resistance must be of type `int | float`, but got value {resistance} of type {type(resistance).__name__}"
            )

        self._l_pin = Pin(self, 0, "l")
        self._r_pin = Pin(self, 1, "r")
        self.resistance = resistance
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Resistance Box",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "最大电阻": 10000.0,
                "最小电阻": 0.1,
                "电阻": self.resistance,
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
            f"ResistanceBox("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"resistance={self.resistance}, "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "电阻箱"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin


class SimpleAmmeter(CircuitBase):
    """Represent a simple ammeter component."""
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_pin = Pin(self, 0, "l")
        self._mid_pin = Pin(self, 1, "mid")
        self._r_pin = Pin(self, 2, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Simple Ammeter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": 0.007,
                "内阻": 0.007,
                "名义量程": 3.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"SimpleAmmeter("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "直流安培表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "mid", cls.mid
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin


class SimpleVoltmeter(CircuitBase):
    """Represent a simple voltmeter component."""
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._l_pin = Pin(self, 0, "l")
        self._mid_pin = Pin(self, 1, "mid")
        self._r_pin = Pin(self, 2, "r")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Simple Voltmeter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": 0.001,
                "名义量程": 15.0,
                "锁定": int(self.lock_status),
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"SimpleVoltmeter("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"lock_status={self.lock_status}, "
            f"label={self.label!r})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "直流电压表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "l", cls.l
        yield "mid", cls.mid
        yield "r", cls.r

    @property
    def l(self) -> Pin:
        """Execute the l routine."""
        return self._l_pin

    @property
    def mid(self) -> Pin:
        """Execute the mid routine."""
        return self._mid_pin

    @property
    def r(self) -> Pin:
        """Execute the r routine."""
        return self._r_pin
