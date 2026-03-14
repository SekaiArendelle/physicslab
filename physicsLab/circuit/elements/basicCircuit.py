# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab._tools import round_data
from physicsLab._core import _Experiment
from .._circuit_core import CircuitBase, Pin, _deprecated_register_element_in_stack
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Self,
    Generate,
    override,
    final,
    Iterator,
    Tuple,
    Literal,
)


class _SwitchBase(CircuitBase):
    """开关基类"""

    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate,
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"开关": 0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def turn_off_switch(self) -> Self:
        """断开开关"""
        self.data["Properties"]["开关"] = 0
        return self


class _SimpleSwitch(_SwitchBase):
    """简单开关"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        _SwitchBase.__init__(self, x, y, z)
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "Simple Switch"

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

    @final
    @staticmethod
    def zh_name() -> str:
        return "简单开关"

    def __repr__(self) -> str:
        res = (
            f"Simple_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ})"
        )

        if self.data["Properties"]["开关"] == 1:
            res += ".turn_on_switch()"
        return res

    def turn_on_switch(self) -> Self:
        """闭合开关"""
        self.data["Properties"]["开关"] = 1
        return self


def Simple_Switch(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _SimpleSwitch:
    result = _SimpleSwitch(
        x, y, z
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


class _SPDTSwitch(_SwitchBase):
    """单刀双掷开关"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        super().__init__(x, y, z)
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "SPDT Switch"

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "单刀双掷开关"

    def __repr__(self) -> str:
        res = (
            f"SPDT_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ})"
        )

        if self.data["Properties"]["开关"] == 1:
            res += ".left_turn_on_switch()"
        elif self.data["Properties"]["开关"] == 2:
            res += ".right_turn_on_switch()"
        return res

    def left_turn_on_switch(self) -> Self:
        """向左闭合开关"""
        self.data["Properties"]["开关"] = 1
        return self

    def right_turn_on_switch(self) -> Self:
        """向右闭合开关"""
        self.data["Properties"]["开关"] = 2
        return self

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin

    @staticmethod
    def count_all_pins() -> int:
        return 3


def SPDT_Switch(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _SPDTSwitch:
    result = _SPDTSwitch(
        x, y, z
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


class _DPDTSwitch(_SwitchBase):
    """双刀双掷开关"""

    _all_pins: Tuple[
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_mid_low_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_mid_up_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
    ]
    _l_low_pin: Pin
    _mid_low_pin: Pin
    _r_low_pin: Pin
    _l_up_pin: Pin
    _mid_up_pin: Pin
    _r_up_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        super().__init__(x, y, z)
        self._all_pins = (
            ("_l_low_pin", Pin(self, 0)),
            ("_mid_low_pin", Pin(self, 1)),
            ("_r_low_pin", Pin(self, 2)),
            ("_l_up_pin", Pin(self, 3)),
            ("_mid_up_pin", Pin(self, 4)),
            ("_r_up_pin", Pin(self, 5)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data["ModelID"] = "DPDT Switch"

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "双刀双掷开关"

    def __repr__(self) -> str:
        res = (
            f"DPDT_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ})"
        )

        if self.data["Properties"]["开关"] == 1:
            res += ".left_turn_on_switch()"
        elif self.data["Properties"]["开关"] == 2:
            res += ".right_turn_on_switch()"
        return res

    # TODO 改为enum是否会更好
    def left_turn_on_switch(self) -> Self:
        """向左闭合开关"""
        self.data["Properties"]["开关"] = 1
        return self

    def right_turn_on_switch(self) -> Self:
        """向右闭合开关"""
        self.data["Properties"]["开关"] = 2
        return self

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def mid_up(self) -> Pin:
        return self._mid_up_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def mid_low(self) -> Pin:
        return self._mid_low_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin

    @staticmethod
    def count_all_pins() -> int:
        return 6


def DPDT_Switch(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _DPDTSwitch:
    result = _DPDTSwitch(
        x, y, z
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


class _PushSwitch(CircuitBase):
    """按钮开关"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Push Switch",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"开关": 0.0, "默认开关": 0.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0},
            "Position": Generate,
            "Rotation": Generate,
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
        return "按钮开关"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


def Push_Switch(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _PushSwitch:
    result = _PushSwitch(
        x, y, z
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


class _AirSwitch(CircuitBase):
    """空气开关"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Air Switch",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"开关": 0.0, "额定电流": 10.0, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
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
        return "空气开关"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    @override
    def __repr__(self) -> str:
        res = (
            f"Air_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ})"
        )

        if self.data["Properties"]["开关"] == 1:
            res += ".turn_on_switch()"
        return res

    def turn_off_switch(self) -> Self:
        """断开开关"""
        self.data["Properties"]["开关"] = 0
        return self

    def turn_on_switch(self) -> Self:
        """闭合开关"""
        self.data["Properties"]["开关"] = 1
        return self


def Air_Switch(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _AirSwitch:
    result = _AirSwitch(
        x, y, z
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


class _IncandescentLamp(CircuitBase):
    """白炽灯泡"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Incandescent Lamp",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"额定电压": 3.0, "额定功率": 0.85, "锁定": 1.0},
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
            "Position": Generate,
            "Rotation": Generate,
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
        return "白炽灯泡"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


def Incandescent_Lamp(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _IncandescentLamp:
    result = _IncandescentLamp(
        x, y, z
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


class _BatterySource(CircuitBase):
    """一节电池"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        voltage: num_type = 1.5,
        internal_resistance: num_type = 0,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Battery Source",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "最大功率": 16.2,
                "电压": Generate,
                "内阻": Generate,
                "锁定": 1.0,
            },
            "Statistics": {"电流": 0, "功率": 0, "电压": 0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

        self.voltage = voltage
        self.internal_resistance = internal_resistance

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @property
    def voltage(self) -> num_type:
        result = self.properties["电压"]
        errors.assert_true(result is not Generate)
        return result

    @voltage.setter
    def voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"voltage must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["电压"] = value
        return value

    @property
    def internal_resistance(self) -> num_type:
        result = self.properties["内阻"]
        errors.assert_true(result is not Generate)
        return result

    @internal_resistance.setter
    def internal_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"internal_resistance must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["内阻"] = value
        return value

    @final
    @staticmethod
    def zh_name() -> str:
        return "一节电池"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


def Battery_Source(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    voltage: num_type = 1.5,
    internal_resistance: num_type = 0,
) -> _BatterySource:
    result = _BatterySource(
        x, y, z,
        voltage=voltage, internal_resistance=internal_resistance
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


class _StudentSource(CircuitBase):
    """学生电源"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_l_mid_pin"], Pin],
        Tuple[Literal["_r_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _l_mid_pin: Pin
    _r_mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_l_mid_pin", Pin(self, 1)),
            ("_r_mid_pin", Pin(self, 2)),
            ("_r_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Student Source",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "交流电压": 3.0,
                "直流电压": 3.0,
                "开关": 0.0,
                "频率": 50.0,
                "锁定": 1.0,
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
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "学生电源"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def l_mid(self) -> Pin:
        return self._l_mid_pin

    @property
    def r_mid(self) -> Pin:
        return self._r_mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin


def Student_Source(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _StudentSource:
    result = _StudentSource(
        x, y, z
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


class _Resistor(CircuitBase):
    """电阻"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        resistance: num_type = 10,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Resistor",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "最大电阻": 10_000_000.0,
                "最小电阻": 0.1,
                "电阻": Generate,
                "锁定": 1.0,
            },
            "Statistics": {
                "瞬间功率": 0,
                "瞬间电流": 0,
                "瞬间电压": 0,
                "功率": 0,
                "电压": 0,
                "电流": 0,
            },
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }
        self.resistance = resistance

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
        return "电阻"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    @property
    def resistance(self) -> num_type:
        result = self.properties["电阻"]
        errors.assert_true(result is not Generate)
        return result

    @resistance.setter
    def resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"resistance must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["电阻"] = value
        return value

    def fix_resistance(self) -> Self:
        """修正电阻值的浮点误差"""
        self.properties["电阻"] = round_data(self.properties["电阻"])
        return self

    def __repr__(self) -> str:
        return (
            f"Resistor({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}, "
            f"resistance={self.properties['电阻']})"
        )


def Resistor(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    resistance: num_type = 10,
) -> _Resistor:
    result = _Resistor(
        x, y, z,
        resistance=resistance
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


class _FuseComponent(CircuitBase):
    """保险丝"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Fuse Component",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"开关": 1.0, "额定电流": 0.3, "熔断电流": 0.5, "锁定": 1.0},
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
            },
            "Position": Generate,
            "Rotation": Generate,
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
        return "保险丝"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


def Fuse_Component(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _FuseComponent:
    result = _FuseComponent(
        x, y, z
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


class _SlideRheostat(CircuitBase):
    """滑动变阻器"""

    _all_pins: Tuple[
        Tuple[Literal["_l_low_pin"], Pin],
        Tuple[Literal["_r_low_pin"], Pin],
        Tuple[Literal["_l_up_pin"], Pin],
        Tuple[Literal["_r_up_pin"], Pin],
    ]
    _l_low_pin: Pin
    _r_low_pin: Pin
    _l_up_pin: Pin
    _r_up_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_low_pin", Pin(self, 0)),
            ("_r_low_pin", Pin(self, 1)),
            ("_l_up_pin", Pin(self, 2)),
            ("_r_up_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Slide Rheostat",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电阻": 10.0,
                "滑块位置": 0.0,
                "电阻1": 10,
                "电阻2": 10.0,
                "锁定": 1.0,
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
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "滑动变阻器"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l_low(self) -> Pin:
        return self._l_low_pin

    @property
    def r_low(self) -> Pin:
        return self._r_low_pin

    @property
    def l_up(self) -> Pin:
        return self._l_up_pin

    @property
    def r_up(self) -> Pin:
        return self._r_up_pin


def Slide_Rheostat(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _SlideRheostat:
    result = _SlideRheostat(
        x, y, z
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


class _Multimeter(CircuitBase):
    """多用电表"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Multimeter",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"状态": 0.0, "锁定": 1.0},
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
            },
            "Position": Generate,
            "Rotation": Generate,
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
        return "多用电表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


def Multimeter(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _Multimeter:
    result = _Multimeter(
        x, y, z
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


class _Galvanometer(CircuitBase):
    """灵敏电流计"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Galvanometer",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 3.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "灵敏电流计"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin


def Galvanometer(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _Galvanometer:
    result = _Galvanometer(
        x, y, z
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


class _Microammeter(CircuitBase):
    """微安表"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Microammeter",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 0.1, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "微安表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin


def Microammeter(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _Microammeter:
    result = _Microammeter(
        x, y, z
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


class _ElectricityMeter(CircuitBase):
    """电能表"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_l_mid_pin"], Pin],
        Tuple[Literal["_r_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _l_mid_pin: Pin
    _r_mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_l_mid_pin", Pin(self, 2)),
            ("_r_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Electricity Meter",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"示数": 0.0, "额定电流": 6.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "电能表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 4

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def l_mid(self) -> Pin:
        return self._l_mid_pin

    @property
    def r_mid(self) -> Pin:
        return self._r_mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin


def Electricity_Meter(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _ElectricityMeter:
    result = _ElectricityMeter(
        x, y, z
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


class _ResistanceBox(CircuitBase):
    """电阻箱"""

    _all_pins: Tuple[Tuple[Literal["_l_pin"], Pin], Tuple[Literal["_r_pin"], Pin]]
    _l_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        resistance: num_type = 10,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_r_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Resistance Box",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "最大电阻": 10000.0,
                "最小电阻": 0.1,
                "电阻": Generate,
                "锁定": 1.0,
            },
            "Statistics": {
                "瞬间功率": 0.0,
                "瞬间电流": 0.0,
                "瞬间电压": 0.0,
                "功率": 0.0,
                "电压": 0.0,
                "电流": 0.0,
            },
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

        self.resistance = resistance

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "电阻箱"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def r(self) -> Pin:
        return self._r_pin

    @property
    def resistance(self) -> num_type:
        """电阻"""
        result = self.properties["电阻"]
        errors.assert_true(result is not Generate)
        return result

    @resistance.setter
    def resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"resistance must be of type `int | float`, but got {type(value).__name__}"
            )

        self.properties["电阻"] = value
        return value


def Resistance_Box(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    resistance: num_type = 10,
) -> _ResistanceBox:
    result = _ResistanceBox(
        x, y, z,
        resistance=resistance
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


class _SimpleAmmeter(CircuitBase):
    """直流安培表"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Simple Ammeter",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 0.007, "内阻": 0.007, "名义量程": 3.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "直流安培表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin


def Simple_Ammeter(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _SimpleAmmeter:
    result = _SimpleAmmeter(
        x, y, z
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


class _SimpleVoltmeter(CircuitBase):
    """直流电压表"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_mid_pin"], Pin],
        Tuple[Literal["_r_pin"], Pin],
    ]
    _l_pin: Pin
    _mid_pin: Pin
    _r_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Simple Voltmeter",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 0.001, "名义量程": 15.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
        return "直流电压表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def l(self) -> Pin:
        return self._l_pin

    @property
    def mid(self) -> Pin:
        return self._mid_pin

    @property
    def r(self) -> Pin:
        return self._r_pin


def Simple_Voltmeter(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _SimpleVoltmeter:
    result = _SimpleVoltmeter(
        x, y, z
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
