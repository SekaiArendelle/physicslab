# -*- coding: utf-8 -*-
from physicsLab import plAR
from physicsLab import _warn
from physicsLab import errors
from physicsLab._core import _Experiment
from .._circuit_core import CircuitBase, InputPin, OutputPin, _deprecated_register_element_in_stack
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Generate,
    final,
    Tuple,
    Iterator,
    Union,
    Literal,
)


class _LogicBase(CircuitBase):
    @property
    @final
    def high_level(self) -> num_type:
        """高电平的值"""
        result = self.properties["高电平"]
        errors.assert_true(result is not Generate)
        return result

    @high_level.setter
    @final
    def high_level(self, value) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )
        if self.properties["低电平"] is not Generate and self.low_level > value:
            raise ValueError(f"high_level is smaller than low_level")

        self.properties["高电平"] = value
        return value

    @property
    @final
    def low_level(self) -> num_type:
        """低电平的值"""
        result = self.properties["低电平"]
        errors.assert_true(result is not Generate)
        return result

    @low_level.setter
    @final
    def low_level(self, value) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"low_level must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )
        if self.properties["高电平"] is not Generate and value > self.high_level:
            raise ValueError(f"high_level is smaller than low_level")

        self.properties["低电平"] = value
        return value


class _LogicInput(_LogicBase):
    """逻辑输入"""

    _all_pins: Tuple[Tuple[Literal["_o_pin"], OutputPin]]
    _o_pin: OutputPin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        output_status: bool = False,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        self._all_pins = (("_o_pin", OutputPin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Logic Input",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": Generate,
                "低电平": Generate,
                "锁定": 1.0,
                "开关": Generate,
            },
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.output_status = output_status
        self.high_level = high_level
        self.low_level = low_level

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @property
    @final
    def output_status(self) -> bool:
        """设置开关的状态"""
        if "开关" not in self.properties:
            self.properties["开关"] = 0

        result = self.properties["开关"]
        errors.assert_true(result is not Generate)
        return bool(result)

    @output_status.setter
    @final
    def output_status(self, value: bool) -> bool:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"output_status must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self.properties["开关"] = int(value)
        return value

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


def Logic_Input(
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
) -> _LogicInput:
    result = _LogicInput(
        x, y, z,
        output_status=output_status, high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _LogicOutput(_LogicBase):
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
    ) -> None:
        self._all_pins = (("_i_pin", InputPin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Logic Output",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "状态": 0.0,
                "高电平": Generate,
                "低电平": Generate,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": "0,180,0",
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level

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


def Logic_Output(
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
) -> _LogicOutput:
    result = _LogicOutput(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _2PinGate(_LogicBase):
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
        /,
    ) -> None:
        self._all_pins = (
            ("_i_pin", InputPin(self, 0)),
            ("_o_pin", OutputPin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": Generate,
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": Generate,
                "低电平": Generate,
                "最大电流": 0.1,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level

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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Yes Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "是门"

    @staticmethod
    def count_all_pins() -> int:
        return 2


def Yes_Gate(
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
) -> _YesGate:
    result = _YesGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _NoGate(_2PinGate):
    """非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "No Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "非门"

    @staticmethod
    def count_all_pins() -> int:
        return 2


def No_Gate(
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
) -> _NoGate:
    result = _NoGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _3PinGate(_LogicBase):
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
        /,
    ) -> None:
        self._all_pins = (
            ("_i_up_pin", InputPin(self, 0)),
            ("_i_low_pin", InputPin(self, 1)),
            ("_o_pin", OutputPin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": Generate,
                "低电平": Generate,
                "最大电流": 0.1,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level

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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Or Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Or_Gate(
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
) -> _OrGate:
    result = _OrGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _AndGate(_3PinGate):
    """与门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "And Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "与门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def And_Gate(
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
) -> _AndGate:
    result = _AndGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _NorGate(_3PinGate):
    """或非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Nor Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "或非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Nor_Gate(
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
) -> _NorGate:
    result = _NorGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _NandGate(_3PinGate):
    """与非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Nand Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "与非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Nand_Gate(
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
) -> _NandGate:
    result = _NandGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _XorGate(_3PinGate):
    """异或门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Xor Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "异或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Xor_Gate(
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
) -> _XorGate:
    result = _XorGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _XnorGate(_3PinGate):
    """同或门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Xnor Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "同或门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Xnor_Gate(
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
) -> _XnorGate:
    result = _XnorGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _ImpGate(_3PinGate):
    """蕴含门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Imp Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "蕴含门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Imp_Gate(
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
) -> _ImpGate:
    result = _ImpGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _NimpGate(_3PinGate):
    """蕴含非门"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 3,
        low_level: num_type = 0,
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self.data["ModelID"] = "Nimp Gate"

    @final
    @staticmethod
    def zh_name() -> str:
        return "蕴含非门"

    @staticmethod
    def count_all_pins() -> int:
        return 3


def Nimp_Gate(
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
) -> _NimpGate:
    result = _NimpGate(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _BigElement(_LogicBase):
    """2体积元件父类"""

    is_bigElement = True

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type,
        low_level: num_type,
        /,
    ) -> None:
        self.data: CircuitElementData = {
            "ModelID": "",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": Generate, "低电平": Generate, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level

    @staticmethod
    def count_all_pins() -> int:
        return 4


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "Half Adder"

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


def Half_Adder(
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
) -> _HalfAdder:
    result = _HalfAdder(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "Full Adder"

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


def Full_Adder(
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
) -> _FullAdder:
    result = _FullAdder(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Physics-Lab-AR's version less than 2.5.0")

        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "Half Subtractor"

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


def Half_Subtractor(
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
) -> _HalfSubtractor:
    result = _HalfSubtractor(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        plAR_version = plAR.get_plAR_version()
        if plAR_version is not None and plAR_version < (2, 5, 0):
            _warn.warning("Physics-Lab-AR's version less than 2.5.0")

        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "Full Subtractor"

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


def Full_Subtractor(
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
) -> _FullSubtractor:
    result = _FullSubtractor(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
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
        self.data["ModelID"] = "Multiplier"

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


def Multiplier(
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
) -> _Multiplier:
    result = _Multiplier(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "D Flipflop"

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


def D_Flipflop(
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
) -> _DFlipflop:
    result = _DFlipflop(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "T Flipflop"

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


def T_Flipflop(
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
) -> _TFlipflop:
    result = _TFlipflop(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_low_pin", InputPin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "Real-T Flipflop"

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


def Real_T_Flipflop(
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
) -> _RealTFlipflop:
    result = _RealTFlipflop(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
        self._all_pins = (
            ("_o_up_pin", OutputPin(self, 0)),
            ("_o_low_pin", OutputPin(self, 1)),
            ("_i_up_pin", InputPin(self, 2)),
            ("_i_mid_pin", InputPin(self, 3)),
            ("_i_low_pin", InputPin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "JK Flipflop"

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


def JK_Flipflop(
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
) -> _JKFlipflop:
    result = _JKFlipflop(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
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
        self.data["ModelID"] = "Counter"

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


def Counter(
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
) -> _Counter:
    result = _Counter(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


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
    ) -> None:
        super().__init__(x, y, z, high_level, low_level)
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
        self.data["ModelID"] = "Random Generator"

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


def Random_Generator(
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
) -> _RandomGenerator:
    result = _RandomGenerator(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _EightBitInput(_LogicBase):
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
    ) -> None:
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
        self.data: CircuitElementData = {
            "ModelID": "8bit Input",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": Generate,
                "低电平": Generate,
                "十进制": 0.0,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level

    def __repr__(self) -> str:
        res = (
            f"Eight_Bit_Input({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ})"
        )

        if self.data["Properties"]["十进制"] != 0:
            res += f".set_num({self.data['Properties']['十进制']})"
        return res

    # TODO 改为@property
    def set_num(self, num: int):
        if 0 <= num <= 255:
            self.data["Properties"]["十进制"] = num
        else:
            raise RuntimeError("The number range entered is incorrect")

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


def Eight_Bit_Input(
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
) -> _EightBitInput:
    result = _EightBitInput(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _EightBitDisplay(_LogicBase):
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
    ) -> None:
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
        self.data: CircuitElementData = {
            "ModelID": "8bit Display",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": Generate,
                "低电平": Generate,
                "状态": 0.0,
                "锁定": 1.0,
            },
            "Statistics": {
                "7": 0.0,
                "6": 0.0,
                "5": 0.0,
                "4": 0.0,
                "3": 0.0,
                "2": 0.0,
                "1": 0.0,
                "0": 0.0,
                "十进制": 0.0,
            },
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level

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


def Eight_Bit_Display(
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
) -> _EightBitDisplay:
    result = _EightBitDisplay(
        x, y, z,
        high_level=high_level, low_level=low_level
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result


class _SchmittTrigger(CircuitBase):
    """施密特触发器"""

    _all_pins: Tuple[
        Tuple[Literal["_i_pin"], InputPin],
        Tuple[Literal["_o_pin"], OutputPin],
    ]
    _i_pin: InputPin
    _o_pin: OutputPin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        high_level: num_type = 5.0,
        low_level: Optional[num_type] = None,
        inverted: bool = False,
    ) -> None:
        self._all_pins = (
            ("_i_pin", InputPin(self, 0)),
            ("_o_pin", OutputPin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Schmitt Trigger",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "工作模式": Generate,
                "切变速率": 0.5,
                "高电准位": Generate,
                "锁定": 1.0,
                "正向阈值": 3.3333332538604736,
                "低电准位": Generate,
                "负向阈值": 1.6666666269302368,
            },
            "Statistics": {"输入电压": 0.0, "输出电压": 0.0, "1": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.high_level = high_level
        self.low_level = low_level
        self.inverted = inverted

    def all_pins(
        self,
    ) -> Iterator[Tuple[str, Union[InputPin, OutputPin]]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @property
    def high_level(self) -> num_type:
        """高电准位"""
        result = self.properties["高电准位"]
        errors.assert_true(result is not Generate)
        return result

    @high_level.setter
    def high_level(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"high_level must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        if self.properties["低电准位"] is not Generate and self.low_level >= value:
            raise ValueError("The high level must be greater than the low level")

        self.properties["高电准位"] = value
        return value

    @property
    def low_level(self) -> num_type:
        """低电准位"""
        result = self.properties["低电准位"]
        errors.assert_true(result is not Generate)
        return result

    @low_level.setter
    def low_level(self, value: Optional[num_type]) -> num_type:
        # None means auto derivation
        # TODO maybe we should use physicsLab.auto instead of None
        if not isinstance(value, (int, float, type(None))):
            raise TypeError(
                f"low_level must be of type `Optional[int | float]`, but got value `{value}` of type `{type(value).__name__}`"
            )

        if value is None:
            self.properties["低电准位"] = min(self.high_level, 0)
        else:
            self.properties["低电准位"] = value

        if (
            self.properties["高电准位"] is not Generate
            and self.properties["高电准位"] < self.properties["低电准位"]
        ):
            raise ValueError("The high level must be greater than the low level")
        return value

    @property
    def inverted(self) -> bool:
        """是否翻转"""
        errors.assert_true(self.properties["工作模式"] is not Generate)
        return bool(self.properties["工作模式"])

    @inverted.setter
    def inverted(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise TypeError(
                f"inverted must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["工作模式"] = int(value)
        return value

    @final
    @staticmethod
    def zh_name() -> str:
        return "施密特触发器"

    def __repr__(self) -> str:
        res = (
            f"Schmitt_Trigger({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}"
        )

        # TODO 显示指明而非使用默认值
        if self.properties["高电准位"] != 5.0:
            res += f", high_level={self.properties['高电准位']}"
        if self.properties["低电准位"] != 0.0:
            res += f", low_level={self.properties['低电准位']}"
        if self.properties["工作模式"] != 0.0:
            res += f", inverted=True"
        return res + ")"

    @property
    def i(self) -> InputPin:
        return self._i_pin

    @property
    def o(self) -> OutputPin:
        return self._o_pin


def Schmitt_Trigger(
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
) -> _SchmittTrigger:
    result = _SchmittTrigger(
        x, y, z,
        high_level=high_level, low_level=low_level, inverted=inverted
    )
    # deprecate
    _deprecated_register_element_in_stack(
        result,
        x,
        y,
        z,
        elementXYZ=elementXYZ,
        identifier=identifier,
        experiment=experiment,
    )
    return result
