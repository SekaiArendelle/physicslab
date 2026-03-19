# -*- coding: utf-8 -*-
from physicsLab import plAR
from physicsLab import _warn
from physicsLab import errors
from physicsLab._core import _Experiment
from .._circuit_core import (
    CircuitBase,
    InputPin,
    OutputPin,
    _deprecated_init_attr_experiment,
    _deprecated_assign_element_to_experiment,
)
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


class _LogicInput(CircuitBase):
    """逻辑输入"""

    _all_pins: Tuple[Tuple[Literal["_o_pin"], OutputPin]]
    _o_pin: OutputPin
    output_status: bool

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        output_status: bool = False,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        self.high_level: num_type = high_level
        self.low_level: num_type = low_level
        self.output_status: bool = output_status
        self._all_pins = (("_o_pin", OutputPin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Logic Input",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "锁定": 1.0,
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
            f"elementXYZ={self.is_elementXYZ}, "
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


class Logic_Input(_LogicInput):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        output_status: bool = False,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            output_status=output_status,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _LogicOutput(CircuitBase):
    """逻辑输出"""

    _all_pins: Tuple[Tuple[Literal["_i_pin"], InputPin]]
    _i_pin: InputPin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Logic Output",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "状态": 0.0,
                "高电平": self.high_level,
                "低电平": self.low_level,
                "锁定": 1.0,
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


class Logic_Output(_LogicOutput):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _2PinGate(CircuitBase):
    """2引脚门电路基类"""

    _all_pins: Tuple[
        Tuple[Literal["_i_pin"], InputPin], Tuple[Literal["_o_pin"], OutputPin]
    ]
    _i_pin: InputPin
    _o_pin: OutputPin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type,
        low_level: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        super().__init__(x, y, z, elementXYZ, identifier)

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


class _YesGate(_2PinGate):
    """是门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @final
    @staticmethod
    def zh_name() -> str:
        return "是门"

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Yes Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }


class Yes_Gate(_YesGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _NoGate(_2PinGate):
    """非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "No Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class No_Gate(_NoGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _3PinGate(CircuitBase):
    """3引脚门电路基类"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type,
        low_level: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        super().__init__(x, y, z, elementXYZ, identifier)

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


class _OrGate(_3PinGate):
    """或门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Or Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Or_Gate(_OrGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _AndGate(_3PinGate):
    """与门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "And Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class And_Gate(_AndGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _NorGate(_3PinGate):
    """或非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Nor Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Nor_Gate(_NorGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _NandGate(_3PinGate):
    """与非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Nand Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Nand_Gate(_NandGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _XorGate(_3PinGate):
    """异或门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Xor Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Xor_Gate(_XorGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _XnorGate(_3PinGate):
    """同或门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Xnor Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Xnor_Gate(_XnorGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _ImpGate(_3PinGate):
    """蕴含门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Imp Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Imp_Gate(_ImpGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _NimpGate(_3PinGate):
    """蕴含非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Nimp Gate",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "最大电流": 0.1,
                "锁定": 1.0,
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


class Nimp_Gate(_NimpGate):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _BigElement(CircuitBase):
    """2体积元件父类"""

    is_bigElement = True

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type,
        low_level: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        super().__init__(x, y, z, elementXYZ, identifier)

    @staticmethod
    def count_all_pins() -> int:
        return 0


class _HalfAdder(_BigElement):
    """半加器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Half Adder",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Half_Adder(_HalfAdder):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _FullAdder(_BigElement):
    """全加器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Full Adder",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Full_Adder(_FullAdder):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _HalfSubtractor(_BigElement):
    """半减器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
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

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Half Subtractor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Half_Subtractor(_HalfSubtractor):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _FullSubtractor(_BigElement):
    """全减器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Full Subtractor is not supported in this version of plAR")
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Full Subtractor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Full_Subtractor(_FullSubtractor):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _Multiplier(_BigElement):
    """二位乘法器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
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

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Multiplier",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Multiplier(_Multiplier):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _DFlipflop(_BigElement):
    """D触发器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "D Flipflop",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class D_Flipflop(_DFlipflop):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _TFlipflop(_BigElement):
    """T'触发器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "T Flipflop",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class T_Flipflop(_TFlipflop):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _RealTFlipflop(_BigElement):
    """T触发器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Real-T Flipflop",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Real_T_Flipflop(_RealTFlipflop):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _JKFlipflop(_BigElement):
    """JK触发器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "JK Flipflop",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class JK_Flipflop(_JKFlipflop):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _Counter(_BigElement):
    """计数器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
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

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Counter",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Counter(_Counter):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _RandomGenerator(_BigElement):
    """随机数发生器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level, elementXYZ, identifier)
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

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Random Generator",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Random_Generator(_RandomGenerator):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _EightBitInput(CircuitBase):
    """八位输入器"""

    is_bigElement: bool = True

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Eight Bit Input",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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
            f"elementXYZ={self.is_elementXYZ})"
        )

    # TODO 改为@property
    def set_num(self, num: int):
        pass

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


class Eight_Bit_Input(_EightBitInput):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _EightBitDisplay(CircuitBase):
    """八位显示器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Eight Bit Display",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": self.high_level, "低电平": self.low_level, "锁定": 1.0},
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


class Eight_Bit_Display(_EightBitDisplay):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _SchmittTrigger(CircuitBase):
    """施密特触发器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 5.0,
        low_level: Optional[num_type] = None,
        inverted: bool = False,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
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
        self.low_level: num_type = low_level if low_level is not None else high_level * 0.3
        self.inverted: bool = inverted
        self._all_pins = (
            ("_i_pin", InputPin(self, 0)),
            ("_o_pin", OutputPin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Schmitt Trigger",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": self.high_level,
                "低电平": self.low_level,
                "反相": int(self.inverted),
                "锁定": 1.0,
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
            f"elementXYZ={self.is_elementXYZ}, "
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


class Schmitt_Trigger(_SchmittTrigger):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        experiment: Optional[_Experiment] = None,
        high_level: num_type = 5.0,
        low_level: Optional[num_type] = None,
        inverted: bool = False,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            high_level=high_level,
            low_level=low_level,
            inverted=inverted,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)
