import uuid
from physicsLab import plAR
from physicsLab import _warn
from physicsLab import errors
from .._circuit_core import CircuitBase, InputPin, OutputPin
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    final,
    Tuple,
    Iterator,
    Union,
    Literal,
)
from physicsLab import coordinate_system


class LogicInput(CircuitBase):

    _all_pins: Tuple[Tuple[Literal["_o_pin"], OutputPin]]
    _o_pin: OutputPin
    output_status: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        output_status: bool = False,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (("_o_pin", OutputPin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    def __repr__(self) -> str:
        res = (
            f"Logic_Input({self._position.x}, {self._position.y}, {self._position.z}, "
            f"output_status={self.output_status})"
        )
        return res

    @final
    @staticmethod
    def zh_name() -> str:
        return "逻辑输入"

    @property
    def o(self) -> OutputPin:
        return self._o_pin

    @staticmethod
    def count_all_pins() -> int:
        return 1


class LogicOutput(CircuitBase):

    _all_pins: Tuple[Tuple[Literal["_i_pin"], InputPin]]
    _i_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (("_i_pin", InputPin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": "0,180,0",
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "逻辑输出"

    @property
    def i(self) -> InputPin:
        return self._i_pin

    @staticmethod
    def count_all_pins() -> int:
        return 1


class _2PinGate(CircuitBase):

    _all_pins: Tuple[
        Tuple[Literal["_i_pin"], InputPin], Tuple[Literal["_o_pin"], OutputPin]
    ]
    _i_pin: InputPin
    _o_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type,
        low_level: num_type,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (
            ("_i_pin", InputPin(self, 0)),
            ("_o_pin", OutputPin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i(self) -> InputPin:
        return self._i_pin

    @property
    def o(self) -> OutputPin:
        return self._o_pin

    @staticmethod
    def count_all_pins() -> int:
        return 2


class YesGate(_2PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position,
            high_level,
            low_level,
            identifier,
            label,
            lock_status,
        )

    @final
    @staticmethod
    def zh_name() -> str:
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }


class NoGate(_2PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "非门"

    @staticmethod
    def count_all_pins() -> int:
        return 2


class _3PinGate(CircuitBase):

    _all_pins: Tuple[
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
        Tuple[Literal["_o_pin"], OutputPin],
    ]
    _i_up_pin: InputPin
    _i_low_pin: InputPin
    _o_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type,
        low_level: num_type,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (
            ("_i_up_pin", InputPin(self, 0)),
            ("_i_low_pin", InputPin(self, 1)),
            ("_o_pin", OutputPin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o(self) -> OutputPin:
        return self._o_pin

    @staticmethod
    def count_all_pins() -> int:
        return 3


class OrGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class AndGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "与门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class NorGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "或非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class NandGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "与非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class XorGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "异或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class XnorGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "同或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class ImpGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "蕴含门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class NimpGate(_3PinGate):

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position,
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "蕴含非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


class _BigElement(CircuitBase):

    is_bigElement = True

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type,
        low_level: num_type,
        identifier: str = str(uuid.uuid4()),
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
        super().__init__(position, identifier, lock_status, label)

    @staticmethod
    def count_all_pins() -> int:
        return 0


class HalfAdder(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "半加器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class FullAdder(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_mid_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _i_up_pin: InputPin
    _i_mid_pin: InputPin
    _i_low_pin: InputPin
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_mid(self) -> InputPin:
        return self._i_mid_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "全加器"

    @staticmethod
    def count_all_pins() -> int:
        return 5


class HalfSubtractor(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Half Subtractor is not supported in this version of plAR")
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    def as_dict(self) -> CircuitElementData:
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "半减器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class FullSubtractor(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_mid_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_mid_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Full Subtractor is not supported in this version of plAR")
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    def as_dict(self) -> CircuitElementData:
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_mid(self) -> InputPin:
        return self._i_mid_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "全减器"

    @staticmethod
    def count_all_pins() -> int:
        return 5


class Multiplier(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_upmid_pin"], OutputPin],
        Tuple[Literal["_o_lowmid_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_upmid_pin"], InputPin],
        Tuple[Literal["_i_lowmid_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
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
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_upmid_pin", OutputPin(self, 1)),
            ("_o_lowmid_pin", OutputPin(self, 2)),
            ("_o_low_pin", OutputPin(self, 3)),
            ("_i_up_pin", InputPin(self, 4)),
            ("_i_upmid_pin", InputPin(self, 5)),
            ("_i_lowmid_pin", InputPin(self, 6)),
            ("_i_low_pin", InputPin(self, 7)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_upmid(self) -> InputPin:
        return self._i_upmid_pin

    @property
    def i_lowmid(self) -> InputPin:
        return self._i_lowmid_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "二位乘法器"

    @staticmethod
    def count_all_pins() -> int:
        return 8


class DFlipflop(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "D触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class TFlipflop(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "T'触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class RealTFlipflop(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "T触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 4


class JKFlipflop(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_mid_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_mid_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_mid(self) -> InputPin:
        return self._i_mid_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "JK触发器"

    @staticmethod
    def count_all_pins() -> int:
        return 5


class Counter(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_upmid_pin"], OutputPin],
        Tuple[Literal["_o_lowmid_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_upmid_pin", OutputPin(self, 1)),
            ("_o_lowmid_pin", OutputPin(self, 2)),
            ("_o_low_pin", OutputPin(self, 3)),
            ("_i_up_pin", InputPin(self, 4)),
            ("_i_low_pin", InputPin(self, 5)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "计数器"

    @staticmethod
    def count_all_pins() -> int:
        return 6


class RandomGenerator(_BigElement):

    _all_pins: Tuple[
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_upmid_pin"], OutputPin],
        Tuple[Literal["_o_lowmid_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
    ]
    _o_up_pin: OutputPin
    _o_upmid_pin: OutputPin
    _o_lowmid_pin: OutputPin
    _o_low_pin: OutputPin
    _i_up_pin: InputPin
    _i_low_pin: InputPin

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
        label: Optional[str] = None,
        lock_status: bool = True,
    ) -> None:
        super().__init__(
            position, high_level, low_level, identifier, label, lock_status
        )
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_upmid_pin", OutputPin(self, 1)),
            ("_o_lowmid_pin", OutputPin(self, 2)),
            ("_o_low_pin", OutputPin(self, 3)),
            ("_i_up_pin", InputPin(self, 4)),
            ("_i_low_pin", InputPin(self, 5)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "随机数发生器"

    @staticmethod
    def count_all_pins() -> int:
        return 6


class EightBitInput(CircuitBase):

    is_bigElement: bool = True

    _input_num: int
    low_level: num_type
    high_level: num_type

    _all_pins: Tuple[
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_upmid_pin"], InputPin],
        Tuple[Literal["_i_lowmid_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_upmid_pin"], OutputPin],
        Tuple[Literal["_o_lowmid_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
    ]
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
        input_num: int,
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (
            ("_i_up_pin", InputPin(self, 0)),
            ("_i_upmid_pin", InputPin(self, 1)),
            ("_i_lowmid_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
            ("_o_up_pin", OutputPin(self, 4)),
            ("_o_upmid_pin", OutputPin(self, 5)),
            ("_o_lowmid_pin", OutputPin(self, 6)),
            ("_o_low_pin", OutputPin(self, 7)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def __repr__(self) -> str:
        return (
            f"Eight_Bit_Input({self._position.x}, {self._position.y}, {self._position.z}, "
            f"input_num={self.input_num})"
        )

    @property
    def input_num(self) -> int:
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

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_upmid(self) -> InputPin:
        return self._i_upmid_pin

    @property
    def i_lowmid(self) -> InputPin:
        return self._i_lowmid_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "八位输入器"

    @staticmethod
    def count_all_pins() -> int:
        return 8


class EightBitDisplay(CircuitBase):

    is_bigElement = True

    _all_pins: Tuple[
        Tuple[Literal["_i_up_pin"], InputPin],
        Tuple[Literal["_i_upmid_pin"], InputPin],
        Tuple[Literal["_i_lowmid_pin"], InputPin],
        Tuple[Literal["_i_low_pin"], InputPin],
        Tuple[Literal["_o_up_pin"], OutputPin],
        Tuple[Literal["_o_upmid_pin"], OutputPin],
        Tuple[Literal["_o_lowmid_pin"], OutputPin],
        Tuple[Literal["_o_low_pin"], OutputPin],
    ]
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
        high_level: num_type = 3,
        low_level: num_type = 0,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (
            ("_i_up_pin", InputPin(self, 0)),
            ("_i_upmid_pin", InputPin(self, 1)),
            ("_i_lowmid_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
            ("_o_up_pin", OutputPin(self, 4)),
            ("_o_upmid_pin", OutputPin(self, 5)),
            ("_o_lowmid_pin", OutputPin(self, 6)),
            ("_o_low_pin", OutputPin(self, 7)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    def i_up(self) -> InputPin:
        return self._i_up_pin

    @property
    def i_upmid(self) -> InputPin:
        return self._i_upmid_pin

    @property
    def i_lowmid(self) -> InputPin:
        return self._i_lowmid_pin

    @property
    def i_low(self) -> InputPin:
        return self._i_low_pin

    @property
    def o_up(self) -> OutputPin:
        return self._o_up_pin

    @property
    def o_upmid(self) -> OutputPin:
        return self._o_upmid_pin

    @property
    def o_lowmid(self) -> OutputPin:
        return self._o_lowmid_pin

    @property
    def o_low(self) -> OutputPin:
        return self._o_low_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "八位显示器"

    @staticmethod
    def count_all_pins() -> int:
        return 8


class SchmittTrigger(CircuitBase):

    _all_pins: Tuple[
        Tuple[Literal["_i_pin"], InputPin],
        Tuple[Literal["_o_pin"], OutputPin],
    ]
    _i_pin: InputPin
    _o_pin: OutputPin
    high_level: num_type
    low_level: num_type
    inverted: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        high_level: num_type = 5.0,
        low_level: Optional[num_type] = None,
        inverted: bool = False,
        identifier: str = str(uuid.uuid4()),
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
        self._all_pins = (
            ("_i_pin", InputPin(self, 0)),
            ("_o_pin", OutputPin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, identifier, lock_status, label)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @final
    @staticmethod
    def zh_name() -> str:
        return "施密特触发器"

    def __repr__(self) -> str:
        return (
            f"Schmitt_Trigger({self._position.x}, {self._position.y}, {self._position.z}, "
            f"high_level={self.high_level}, "
            f"low_level={self.low_level}, "
            f"inverted={self.inverted})"
        )

    @property
    def i(self) -> InputPin:
        return self._i_pin

    @property
    def o(self) -> OutputPin:
        return self._o_pin
