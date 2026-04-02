"""Provide logic circuit related functionality."""

import uuid
from physicslab import quantum_physics
from .._base import CircuitBase, InputPin, OutputPin
from physicslab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    final,
    Tuple,
    Iterator,
)
from physicslab import coordinate_system


class LogicInput(CircuitBase):
    """Represent a logic input component."""
    _o_pin: OutputPin
    output_status: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        output_status: bool = False,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        if not isinstance(output_status, bool):
            raise TypeError(
                f"output_status must be of type `bool`, but got value `{output_status}` of type {type(output_status).__name__}"
            )
        if low_level > high_level:
            raise ValueError(
                f"low_level ({low_level}) must be less than or equal to high_level ({high_level})"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self.output_status: bool = output_status
        self._o_pin = OutputPin(self, 0, "o")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Logic Input",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "锁定": int(self.lock_status),
                "开关": int(self.output_status),
            },
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"LogicInput("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"output_status={self.output_status}, "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "逻辑输入"

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "o", cls.o

    @property
    def o(self) -> OutputPin:
        """Execute the o routine."""
        return self._o_pin

    @staticmethod
    def count_all_pins() -> int:
        return 1


class LogicOutput(CircuitBase):
    """Represent a logic output component."""
    _i_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self._i_pin = InputPin(self, 0, "i")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Logic Output",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "状态": 0.0,
                "高电平": self.high_level,
                "低电平": self.low_level,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": "0,180,0",
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def to_constructor_str(self) -> str:
        return (
            f"LogicOutput("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "逻辑输出"

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "i", cls.i

    @property
    def i(self) -> InputPin:
        """Execute the i routine."""
        return self._i_pin

    @staticmethod
    def count_all_pins() -> int:
        return 1


class _2PinGate(CircuitBase):
    _i_pin: InputPin
    _o_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        high_level: num_type,
        low_level: num_type,
        identifier: str,
        label: Optional[str],
        lock_status: bool,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self._i_pin = InputPin(self, 0, "i")
        self._o_pin = OutputPin(self, 1, "o")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "i", cls.i
        yield "o", cls.o

    @property
    def i(self) -> InputPin:
        """Execute the i routine."""
        return self._i_pin

    @property
    def o(self) -> OutputPin:
        """Execute the o routine."""
        return self._o_pin

    @staticmethod
    def count_all_pins() -> int:
        return 2


class YesGate(_2PinGate):
    """Represent a yes gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def to_constructor_str(self) -> str:
        return (
            f"YesGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "是门"

    @staticmethod
    def count_all_pins() -> int:
        return 2

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Yes Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }


class NoGate(_2PinGate):
    """Represent a no gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "No Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"NoGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "非门"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class _3PinGate(CircuitBase):
    _i_up_pin: InputPin
    _i_low_pin: InputPin
    _o_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        high_level: num_type,
        low_level: num_type,
        identifier: str,
        label: Optional[str],
        lock_status: bool,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self._i_up_pin = InputPin(self, 0, "i_up")
        self._i_low_pin = InputPin(self, 1, "i_low")
        self._o_pin = OutputPin(self, 2, "o")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o", cls.o

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o(self) -> OutputPin:
        """Execute the o routine."""
        return self._o_pin

    @staticmethod
    def count_all_pins() -> int:
        return 3


class OrGate(_3PinGate):
    """Represent a or gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Or Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"OrGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class AndGate(_3PinGate):
    """Represent a and gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "And Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"AndGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "与门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class NorGate(_3PinGate):
    """Represent a nor gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Nor Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"NorGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "或非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class NandGate(_3PinGate):
    """Represent a nand gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Nand Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"NandGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "与非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class XorGate(_3PinGate):
    """Represent a xor gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Xor Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"XorGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "异或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class XnorGate(_3PinGate):
    """Represent a xnor gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Xnor Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"XnorGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "同或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class ImpGate(_3PinGate):
    """Represent a imp gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Imp Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"ImpGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "蕴含门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class NimpGate(_3PinGate):
    """Represent a nimp gate component."""
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Nimp Gate",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
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
            f"NimpGate("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "蕴含非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class _BigElement(CircuitBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        high_level: num_type,
        low_level: num_type,
        identifier: str,
        label: Optional[str],
        lock_status: bool,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    @staticmethod
    def count_all_pins() -> int:
        return 0


class HalfAdder(_BigElement):
    """Represent a half adder component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_low_pin = InputPin(self, 3, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Half Adder",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"HalfAdder("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "半加器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class FullAdder(_BigElement):
    """Represent a full adder component."""
    _i_up_pin: InputPin
    _i_mid_pin: InputPin
    _i_low_pin: InputPin
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_mid_pin = InputPin(self, 3, "i_mid")
        self._i_low_pin = InputPin(self, 4, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Full Adder",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_mid", cls.i_mid
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_mid(self) -> InputPin:
        """Execute the i mid routine."""
        return self._i_mid_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"FullAdder("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "全加器"

    @staticmethod
    def count_all_pins() -> int:
        return 5


class HalfSubtractor(_BigElement):
    """Represent a half subtractor component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_low_pin = InputPin(self, 3, "i_low")

    def as_dict(self) -> CircuitElementData:
        version = quantum_physics.get_quantum_physics_version()
        if version is not None and version < (2, 5, 0):
            raise NotImplementedError(
                "HalfSubtractor is not supported in Quantum Physics version below 2.5.0"
            )
        return {
            "ModelID": "Half Subtractor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"HalfSubtractor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "半减器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class FullSubtractor(_BigElement):
    """Represent a full subtractor component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_mid_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_mid_pin = InputPin(self, 3, "i_mid")
        self._i_low_pin = InputPin(self, 4, "i_low")

    def as_dict(self) -> CircuitElementData:
        # TODO get version by passing parameter from constructor
        # Maybe I should store version in class CircuitExperiment, and raise this
        # exception in some method like crt_a_element
        # TODO so as to class HalfSubtractor, SimpleInstrument
        version = quantum_physics.get_quantum_physics_version()
        if version is not None and version < (2, 5, 0):
            raise NotImplementedError(
                "FullSubtractor is not supported in Quantum Physics version below 2.5.0"
            )
        return {
            "ModelID": "Full Subtractor",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_mid", cls.i_mid
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_mid(self) -> InputPin:
        """Execute the i mid routine."""
        return self._i_mid_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"FullSubtractor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "全减器"

    @staticmethod
    def count_all_pins() -> int:
        return 5


class Multiplier(_BigElement):
    """Represent a multiplier component."""
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_upmid_pin: InputPin
    _i_lowmid_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_upmid_pin = OutputPin(self, 1, "o_upmid")
        self._o_lowmid_pin = OutputPin(self, 2, "o_lowmid")
        self._o_low_pin = OutputPin(self, 3, "o_low")
        self._i_up_pin = InputPin(self, 4, "i_up")
        self._i_upmid_pin = InputPin(self, 5, "i_upmid")
        self._i_lowmid_pin = InputPin(self, 6, "i_lowmid")
        self._i_low_pin = InputPin(self, 7, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Multiplier",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_upmid", cls.i_upmid
        yield "i_lowmid", cls.i_lowmid
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_upmid", cls.o_upmid
        yield "o_lowmid", cls.o_lowmid
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_upmid(self) -> InputPin:
        """Execute the i upmid routine."""
        return self._i_upmid_pin

    @property
    def i_lowmid(self) -> InputPin:
        """Execute the i lowmid routine."""
        return self._i_lowmid_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        """Execute the o upmid routine."""
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        """Execute the o lowmid routine."""
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"Multiplier("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "二位乘法器"

    @staticmethod
    def count_all_pins() -> int:
        return 8


class DFlipflop(_BigElement):
    """Represent a d flipflop component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_low_pin = InputPin(self, 3, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "D Flipflop",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"DFlipflop("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "D触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class TFlipflop(_BigElement):
    """Represent a t flipflop component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_low_pin = InputPin(self, 3, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "T Flipflop",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"TFlipflop("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "T'触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class RealTFlipflop(_BigElement):
    """Represent a real t flipflop component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_low_pin = InputPin(self, 3, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Real-T Flipflop",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"RealTFlipflop("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "T触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class JKFlipflop(_BigElement):
    """Represent a j k flipflop component."""
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_mid_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_low_pin = OutputPin(self, 1, "o_low")
        self._i_up_pin = InputPin(self, 2, "i_up")
        self._i_mid_pin = InputPin(self, 3, "i_mid")
        self._i_low_pin = InputPin(self, 4, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "JK Flipflop",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_mid", cls.i_mid
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_mid(self) -> InputPin:
        """Execute the i mid routine."""
        return self._i_mid_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"JKFlipflop("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "JK触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 5


class Counter(_BigElement):
    """Represent a counter component."""
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_upmid_pin = OutputPin(self, 1, "o_upmid")
        self._o_lowmid_pin = OutputPin(self, 2, "o_lowmid")
        self._o_low_pin = OutputPin(self, 3, "o_low")
        self._i_up_pin = InputPin(self, 4, "i_up")
        self._i_low_pin = InputPin(self, 5, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Counter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_upmid", cls.o_upmid
        yield "o_lowmid", cls.o_lowmid
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        """Execute the o upmid routine."""
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        """Execute the o lowmid routine."""
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"Counter("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "计数器"

    @staticmethod
    def count_all_pins() -> int:
        return 6


class RandomGenerator(_BigElement):
    """Represent a random generator component."""
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            rotation,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )
        self._o_up_pin = OutputPin(self, 0, "o_up")
        self._o_upmid_pin = OutputPin(self, 1, "o_upmid")
        self._o_lowmid_pin = OutputPin(self, 2, "o_lowmid")
        self._o_low_pin = OutputPin(self, 3, "o_low")
        self._i_up_pin = InputPin(self, 4, "i_up")
        self._i_low_pin = InputPin(self, 5, "i_low")

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Random Generator",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_upmid", cls.o_upmid
        yield "o_lowmid", cls.o_lowmid
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        """Execute the o upmid routine."""
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        """Execute the o lowmid routine."""
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"RandomGenerator("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "随机数发生器"

    @staticmethod
    def count_all_pins() -> int:
        return 6


class EightBitInput(CircuitBase):
    """Represent a eight bit input component."""
    _input_num: int
    low_level: num_type
    high_level: num_type

    _i_up_pin: InputPin
    _i_upmid_pin: InputPin
    _i_lowmid_pin: InputPin
    _i_low_pin: InputPin
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        input_num: int,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(input_num, int):
            raise TypeError(
                f"input_num must be of type `int`, but got value `{input_num}` of type {type(input_num).__name__}"
            )
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        self.input_num = input_num
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self._i_up_pin = InputPin(self, 0, "i_up")
        self._i_upmid_pin = InputPin(self, 1, "i_upmid")
        self._i_lowmid_pin = InputPin(self, 2, "i_lowmid")
        self._i_low_pin = InputPin(self, 3, "i_low")
        self._o_up_pin = OutputPin(self, 4, "o_up")
        self._o_upmid_pin = OutputPin(self, 5, "o_upmid")
        self._o_lowmid_pin = OutputPin(self, 6, "o_lowmid")
        self._o_low_pin = OutputPin(self, 7, "o_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "8bit Input",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "十进制": self.input_num,
                "高电平": self.high_level,
                "低电平": self.low_level,
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
            f"EightBitInput("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"input_num={self.input_num}, "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "i_up", cls.i_up
        yield "i_upmid", cls.i_upmid
        yield "i_lowmid", cls.i_lowmid
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_upmid", cls.o_upmid
        yield "o_lowmid", cls.o_lowmid
        yield "o_low", cls.o_low

    @property
    def input_num(self) -> int:
        """Execute the input num routine."""
        return self._input_num

    @input_num.setter
    def input_num(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"input_num must be of type `int`, but got value `{value}` of type {type(value).__name__}"
            )
        if not (0 <= value <= 0xFF):
            raise ValueError(
                f"input_num must be between 0 and 8 (inclusive), but got {value}"
            )
        self._input_num = value

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_upmid(self) -> InputPin:
        """Execute the i upmid routine."""
        return self._i_upmid_pin

    @property
    def i_lowmid(self) -> InputPin:
        """Execute the i lowmid routine."""
        return self._i_lowmid_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        """Execute the o upmid routine."""
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        """Execute the o lowmid routine."""
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "八位输入器"

    @staticmethod
    def count_all_pins() -> int:
        return 8


class EightBitDisplay(CircuitBase):
    """Represent a eight bit display component."""
    _i_up_pin: InputPin
    _i_upmid_pin: InputPin
    _i_lowmid_pin: InputPin
    _i_low_pin: InputPin
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self._i_up_pin = InputPin(self, 0, "i_up")
        self._i_upmid_pin = InputPin(self, 1, "i_upmid")
        self._i_lowmid_pin = InputPin(self, 2, "i_lowmid")
        self._i_low_pin = InputPin(self, 3, "i_low")
        self._o_up_pin = OutputPin(self, 4, "o_up")
        self._o_upmid_pin = OutputPin(self, 5, "o_upmid")
        self._o_lowmid_pin = OutputPin(self, 6, "o_lowmid")
        self._o_low_pin = OutputPin(self, 7, "o_low")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Eight Bit Display",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
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
        yield "i_up", cls.i_up
        yield "i_upmid", cls.i_upmid
        yield "i_lowmid", cls.i_lowmid
        yield "i_low", cls.i_low
        yield "o_up", cls.o_up
        yield "o_upmid", cls.o_upmid
        yield "o_lowmid", cls.o_lowmid
        yield "o_low", cls.o_low

    @property
    def i_up(self) -> InputPin:
        """Execute the i up routine."""
        return self._i_up_pin

    @property
    def i_upmid(self) -> InputPin:
        """Execute the i upmid routine."""
        return self._i_upmid_pin

    @property
    def i_lowmid(self) -> InputPin:
        """Execute the i lowmid routine."""
        return self._i_lowmid_pin

    @property
    def i_low(self) -> InputPin:
        """Execute the i low routine."""
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        """Execute the o up routine."""
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        """Execute the o upmid routine."""
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        """Execute the o lowmid routine."""
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        """Execute the o low routine."""
        return self._o_low_pin

    def to_constructor_str(self) -> str:
        return (
            f"EightBitDisplay("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "八位显示器"

    @staticmethod
    def count_all_pins() -> int:
        return 8


class SchmittTrigger(CircuitBase):
    """Represent a schmitt trigger component."""
    _i_pin: InputPin
    _o_pin: OutputPin
    high_level: num_type
    low_level: num_type
    inverted: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        high_level: num_type = 5.0,
        low_level: Optional[num_type] = None,
        inverted: bool = False,
        identifier: Optional[str] = None,
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        if not isinstance(high_level, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{high_level}` of type {type(high_level).__name__}"
            )
        if low_level is not None and not isinstance(low_level, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{low_level}` of type {type(low_level).__name__}"
            )
        if not isinstance(inverted, bool):
            raise TypeError(
                f"inverted must be of type `bool`, but got value `{inverted}` of type {type(inverted).__name__}"
            )
        self.high_level: num_type = high_level
        self.low_level: num_type = (
            low_level if low_level is not None else high_level * 0.3
        )
        self.inverted: bool = inverted
        self._i_pin = InputPin(self, 0, "i")
        self._o_pin = OutputPin(self, 1, "o")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Schmitt Trigger",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "反相": int(self.inverted),
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @final
    @staticmethod
    def zh_name() -> str:
        """Execute the zh name routine."""
        return "施密特触发器"

    def to_constructor_str(self) -> str:
        return (
            f"SchmittTrigger("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"inverted={self.inverted}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @classmethod
    def all_pins_property_iter(cls) -> Iterator[Tuple[str, property]]:
        yield "i", cls.i
        yield "o", cls.o

    @property
    def i(self) -> InputPin:
        """Execute the i routine."""
        return self._i_pin

    @property
    def o(self) -> OutputPin:
        """Execute the o routine."""
        return self._o_pin
