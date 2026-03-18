# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab._core import _Experiment
from physicsLab._tools import round_data
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
    Generate,
    Self,
    override,
    final,
    Tuple,
    Iterator,
    Literal,
)


class _NE555(CircuitBase):
    """555定时器"""

    is_bigElement = True

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_vcc_pin", Pin(self, 0)),
            ("_dis_pin", Pin(self, 1)),
            ("_thr_pin", Pin(self, 2)),
            ("_ctrl_pin", Pin(self, 3)),
            ("_trig_pin", Pin(self, 4)),
            ("_out_pin", Pin(self, 5)),
            ("_reset_pin", Pin(self, 6)),
            ("_ground_pin", Pin(self, 7)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "555 Timer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class NE555(_NE555):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _BasicCapacitor(CircuitBase):
    """电容"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        peak_voltage: num_type = 16,
        capacitance: num_type = 1e-06,
        internal_resistance: num_type = 5,
        is_ideal: bool = False,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        """@param capacitance: 电容, 单位为F
        @param is_ideal: 是否为理想模式
        @param peak_voltage: 峰值电压, 单位为V
        @param internal_resistance: 内阻, 单位为Ω
        """
        self.peak_voltage = peak_voltage
        self.capacitance = capacitance
        self.internal_resistance = internal_resistance
        self.is_ideal = is_ideal
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Basic Capacitor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "耐压": Generate,
                "电容": Generate,
                "内阻": Generate,
                "理想模式": Generate,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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

    @property
    @final
    def peak_voltage(self) -> num_type:
        """峰值电压属性, 单位为V"""
        result = self.properties["耐压"]
        errors.assert_true(result is not Generate)
        return result

    @peak_voltage.setter
    @final
    def peak_voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"peak_voltage must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["耐压"] = value
        return value

    @property
    @final
    def capacitance(self) -> num_type:
        """电容属性, 单位为F"""
        result = self.properties["电容"]
        errors.assert_true(result is not Generate)
        return result

    @capacitance.setter
    @final
    def capacitance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"capacitance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["电容"] = value
        return value

    @property
    @final
    def internal_resistance(self) -> num_type:
        """内阻属性, 单位为Ω"""
        result = self.properties["内阻"]
        errors.assert_true(result is not Generate)
        return result

    @internal_resistance.setter
    @final
    def internal_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"internal_resistance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["内阻"] = value
        return value

    @property
    @final
    def is_ideal(self) -> bool:
        """元件是否为理想模式"""
        if "理想模式" not in self.properties:
            self.properties["理想模式"] = 0
        result = bool(self.properties["理想模式"])
        errors.assert_true(result is not Generate)
        return result

    @is_ideal.setter
    @final
    def is_ideal(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_ideal must be of type `bool`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["理想模式"] = int(value)
        return value

    @override
    def __repr__(self) -> str:
        return (
            f"Basic_Capacitor({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}, "
            f"peak_voltage={self.peak_voltage}, "
            f"capacitance={self.capacitance}, "
            f"internal_resistance={self.internal_resistance}, "
            f"is_ideal={self.is_ideal})"
        )


class Basic_Capacitor(_BasicCapacitor):
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
        peak_voltage: num_type = 16,
        capacitance: num_type = 1e-06,
        internal_resistance: num_type = 5,
        is_ideal: bool = False,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            peak_voltage=peak_voltage,
            capacitance=capacitance,
            internal_resistance=internal_resistance,
            is_ideal=is_ideal,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _BasicInductor(CircuitBase):
    """电感"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        rated_current: num_type = 1,
        inductance: num_type = 0.05,
        internal_resistance: num_type = 1,
        is_ideal: bool = False,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        """@param rated_current: 电感额定电流，单位为 A
        @param inductance: 电感，单位为 Henry
        @param internal_resistance: 电感内部阻抗，单位为 Ohm
        @param is_ideal: 是否为理想模式
        """
        self.rated_current = rated_current
        self.inductance = inductance
        self.internal_resistance = internal_resistance
        self.is_ideal = is_ideal
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Basic Inductor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "额定电流": Generate,
                "电感": Generate,
                "内阻": Generate,
                "锁定": 1.0,
                "理想模式": Generate,
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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

    @property
    @final
    def rated_current(self) -> num_type:
        """电感额定电流，单位为 A"""
        result = self.properties["额定电流"]
        errors.assert_true(result is not Generate)
        return result

    @rated_current.setter
    @final
    def rated_current(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"rated_current must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["额定电流"] = value
        return value

    @property
    @final
    def inductance(self) -> num_type:
        """电感，单位为 Henry"""
        result = self.properties["电感"]
        errors.assert_true(result is not Generate)
        return result

    @inductance.setter
    @final
    def inductance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"inductance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["电感"] = value
        return value

    @property
    @final
    def internal_resistance(self) -> num_type:
        """电感内部阻抗, 单位为Ohm"""
        result = self.properties["内阻"]
        errors.assert_true(result is not Generate)
        return result

    @internal_resistance.setter
    @final
    def internal_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"internal_resisitance must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["内阻"] = value
        return value

    @property
    @final
    def is_ideal(self) -> bool:
        """元件是否为理想模式"""
        if "理想模式" not in self.properties:
            self.properties["理想模式"] = 0
        result = self.properties["理想模式"]
        errors.assert_true(result is not Generate)
        return bool(result)

    @is_ideal.setter
    @final
    def is_ideal(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_ideal must be of type `bool`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["理想模式"] = int(value)
        return value

    def fix_inductance(self) -> Self:
        """修正电感值的浮点误差"""
        self.properties["电感"] = round_data(self.properties["电感"])
        return self

    @override
    def __repr__(self) -> str:
        return (
            f"Basic_Inductor({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}, "
            f"rated_current={self.rated_current}, "
            f"inductance={self.inductance}, "
            f"internal_resistance={self.internal_resistance}, "
            f"is_ideal={self.is_ideal})"
        )


class Basic_Inductor(_BasicInductor):
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
        rated_current: num_type = 1,
        inductance: num_type = 0.05,
        internal_resistance: num_type = 1,
        is_ideal: bool = False,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            rated_current=rated_current,
            inductance=inductance,
            internal_resistance=internal_resistance,
            is_ideal=is_ideal,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _BasicDiode(CircuitBase):
    """二极管"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Basic Diode",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "击穿电压": 0.0,
                "前向压降": 0.6,
                "额定电流": 1.0,
                "工作电压": 3.0,
                "锁定": 1.0,
            },
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Basic_Diode(_BasicDiode):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _LightEmittingDiode(CircuitBase):
    """发光二极管"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Light-Emitting Diode",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "反向耐压": 6.0,
                "击穿电压": 0.0,
                "前向压降": 2.1024259,
                "工作电流": 0.01,
                "工作电压": 3.0,
                "锁定": 1.0,
            },
            "Statistics": {"电流1": 0.0, "电压1": 0.0, "功率1": 0.0, "亮度1": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Light_Emitting_Diode(_LightEmittingDiode):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _GroundComponent(CircuitBase):
    """接地元件"""

    _all_pins: Tuple[Tuple[Literal["_i_pin"], Pin]]
    _i_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (("_i_pin", Pin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Ground Component",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"锁定": 1.0},
            "Statistics": {"电流": 0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Ground_Component(_GroundComponent):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _Transformer(CircuitBase):
    """理想变压器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0)),
            ("_r_up_pin", Pin(self, 1)),
            ("_l_low_pin", Pin(self, 2)),
            ("_r_low_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Transformer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "输入电压": 3.0,
                "输出电压": 36.0,
                "额定功率": 20.0,
                "耦合系数": 1.0,
                "锁定": 1.0,
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
                "功率2": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Transformer(_Transformer):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _TappedTransformer(CircuitBase):
    """中心抽头变压器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0)),
            ("_r_up_pin", Pin(self, 1)),
            ("_l_low_pin", Pin(self, 2)),
            ("_r_low_pin", Pin(self, 3)),
            ("_mid_pin", Pin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Tapped Transformer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "输入电压": 3.0,
                "输出电压": 36.0,
                "额定功率": 20.0,
                "耦合系数": 1.0,
                "锁定": 1.0,
            },
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Tapped_Transformer(_TappedTransformer):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _MutualInductor(CircuitBase):
    """理想互感"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0)),
            ("_r_up_pin", Pin(self, 1)),
            ("_l_low_pin", Pin(self, 2)),
            ("_r_low_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Mutual Inductor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"电感1": 4.0, "电感2": 1.0, "耦合系数": 1.0, "锁定": 1.0},
            "Statistics": {
                "电流1": 0.0,
                "电压1": 0.0,
                "功率1": 0.0,
                "电流2": 0.0,
                "电压2": 0.0,
                "功率2": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Mutual_Inductor(_MutualInductor):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _Rectifier(CircuitBase):
    """全波整流器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0)),
            ("_r_up_pin", Pin(self, 1)),
            ("_l_low_pin", Pin(self, 2)),
            ("_r_low_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Rectifier",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"前向压降": 0.8, "额定电流": 1.0, "锁定": 1.0},
            "Statistics": {"电流": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Rectifier(_Rectifier):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _Transistor(CircuitBase):
    """三极管"""

    _all_pins: Tuple[
        Tuple[Literal["_B_pin"], Pin],
        Tuple[Literal["_C_pin"], Pin],
        Tuple[Literal["_E_pin"], Pin],
    ]
    _B_pin: Pin
    _C_pin: Pin
    _E_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        is_PNP: bool = True,
        gain: num_type = 100,
        max_power: num_type = 1000,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self.is_PNP = is_PNP
        self.gain = gain
        self.max_power = max_power
        self._all_pins = (
            ("_B_pin", Pin(self, 0)),
            ("_C_pin", Pin(self, 1)),
            ("_E_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Transistor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "PNP": Generate,
                "放大系数": Generate,
                "最大功率": Generate,
                "锁定": 1.0,
            },
            "Statistics": {"电压BC": 0.0, "电压BE": 0.0, "电压CE": 0.0, "功率": 0.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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

    @property
    def is_PNP(self) -> bool:
        """是PNP还是NPN, True时为PNP"""
        result = self.properties["PNP"]
        errors.assert_true(result is not Generate)
        return bool(result)

    @is_PNP.setter
    def is_PNP(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise TypeError(
                f"is_PNP must be of type `bool`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["PNP"] = int(value)
        return value

    @property
    def gain(self) -> num_type:
        result = self.properties["放大系数"]
        errors.assert_true(result is not Generate)
        return result

    @gain.setter
    def gain(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"gain must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["放大系数"] = value
        return value

    @property
    def max_power(self) -> num_type:
        result = self.properties["最大功率"]
        errors.assert_true(result is not Generate)
        return result

    @max_power.setter
    def max_power(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"max_power must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["最大功率"] = value
        return value

    def __repr__(self) -> str:
        res = (
            f"Transistor({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}, is_PNP={bool(self.properties['PNP'])}"
        )

        # TODO 不论是否是默认参数都显示写到res里
        if self.properties["放大系数"] != 100.0:
            res += f", gain={self.properties['放大系数']}"
        if self.properties["最大功率"] != 5.0:
            res += f", max_power={self.properties['最大功率']}"
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


class Transistor(_Transistor):
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
        is_PNP: bool = True,
        gain: num_type = 100,
        max_power: num_type = 1000,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            is_PNP=is_PNP,
            gain=gain,
            max_power=max_power,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _Comparator(CircuitBase):
    """比较器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_o_pin", Pin(self, 0)),
            ("_i_up_pin", Pin(self, 1)),
            ("_i_low_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Comparator",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": 3.0, "低电平": 0.0, "锁定": 1.0},
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Comparator(_Comparator):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _OperationalAmplifier(CircuitBase):
    """运算放大器"""

    _all_pins: Tuple[
        Tuple[Literal["_i_neg_pin"], Pin],
        Tuple[Literal["_i_pos_pin"], Pin],
        Tuple[Literal["_o_pin"], Pin],
    ]
    _i_neg_pin: Pin
    _i_pos_pin: Pin
    _o_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        gain: num_type = 10_000_000,
        max_voltage: num_type = 1000,
        min_voltage: num_type = -1000,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        """@param gain: 增益系数
        @param max_voltage: 最大电压
        @param min_voltage: 最小电压
        """
        self.gain = gain
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self._all_pins = (
            ("_i_neg_pin", Pin(self, 0)),
            ("_i_pos_pin", Pin(self, 1)),
            ("_o_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Operational Amplifier",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "增益系数": Generate,
                "最大电压": Generate,
                "最小电压": Generate,
                "锁定": 1.0,
            },
            "Statistics": {
                "电压-": 0,
                "电压+": 0,
                "输出电压": 0,
                "输出电流": 0,
                "输出功率": 0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def gain(self) -> num_type:
        """增益系数"""
        result = self.properties["增益系数"]
        errors.assert_true(result is not Generate)
        return result

    @gain.setter
    def gain(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"gain must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["增益系数"] = value
        return value

    @property
    def max_voltage(self) -> num_type:
        result = self.properties["最大电压"]
        errors.assert_true(result is not Generate)
        return result

    @max_voltage.setter
    def max_voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"max_voltage must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )
        if self.properties["最小电压"] is not Generate and self.min_voltage >= value:
            raise ValueError(f"min_voltage must must less than max_voltage")

        self.properties["最大电压"] = value
        return value

    @property
    def min_voltage(self) -> num_type:
        result = self.properties["最小电压"]
        errors.assert_true(result is not Generate)
        return result

    @min_voltage.setter
    def min_voltage(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"min_voltage must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )
        if self.properties["最大电压"] is not Generate and self.max_voltage <= value:
            raise ValueError("min_voltage must less than max_voltage")

        self.properties["最小电压"] = value
        return value

    @override
    def __repr__(self) -> str:
        return (
            f"Operational_Amplifier({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}, "
            f"gain={self.properties['增益系数']}, "
            f"max_voltage={self.properties['最大电压']}, "
            f"min_voltage={self.properties['最小电压']})"
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


class Operational_Amplifier(_OperationalAmplifier):
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
        gain: num_type = 10_000_000,
        max_voltage: num_type = 1000,
        min_voltage: num_type = -1000,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            gain=gain,
            max_voltage=max_voltage,
            min_voltage=min_voltage,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _RelayComponent(CircuitBase):
    """继电器"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        pull_in_current: num_type = 0.02,
        rated_current: num_type = 10,
        coil_inductance: num_type = 0.2,
        coil_resistance: num_type = 20,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self.pull_in_current = pull_in_current
        self.rated_current = rated_current
        self.coil_inductance = coil_inductance
        self.coil_resistance = coil_resistance
        self._all_pins = (
            ("_l_up_pin", Pin(self, 0)),
            ("_l_low_pin", Pin(self, 2)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_up_pin", Pin(self, 3)),
            ("_r_low_pin", Pin(self, 4)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Relay Component",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": 0.0,
                "线圈电感": Generate,
                "线圈电阻": Generate,
                "接通电流": Generate,
                "额定电流": Generate,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def pull_in_current(self) -> num_type:
        """接通电流"""
        result = self.properties["接通电流"]
        errors.assert_true(result is not Generate)
        return result

    @pull_in_current.setter
    def pull_in_current(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"pull_in_current must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["接通电流"] = value
        return value

    @property
    def rated_current(self) -> num_type:
        """额定电流"""
        result = self.properties["额定电流"]
        errors.assert_true(result is not Generate)
        return result

    @rated_current.setter
    def rated_current(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"rated_current must be of type `int | float`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["额定电流"] = value
        return value

    @property
    def coil_inductance(self) -> num_type:
        """线圈电感"""
        result = self.properties["线圈电感"]
        errors.assert_true(result is not Generate)
        return result

    @coil_inductance.setter
    def coil_inductance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"coil_inductance must be of type `int | flaot`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["线圈电感"] = value
        return value

    @property
    def coil_resistance(self) -> num_type:
        """线圈电阻"""
        result = self.properties["线圈电阻"]
        errors.assert_true(result is not Generate)
        return result

    @coil_resistance.setter
    def coil_resistance(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"coil_resistance must be of type `int | flaot`, but got value `{value}` of type `{type(value).__name__}`"
            )

        self.properties["线圈电阻"] = value
        return value

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


class Relay_Component(_RelayComponent):
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
        pull_in_current: num_type = 0.02,
        rated_current: num_type = 10,
        coil_inductance: num_type = 0.2,
        coil_resistance: num_type = 20,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            pull_in_current=pull_in_current,
            rated_current=rated_current,
            coil_inductance=coil_inductance,
            coil_resistance=coil_resistance,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _N_MOSFET(CircuitBase):
    """N-MOSFET"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        beta: num_type = 0.027,
        threshold: num_type = 1.5,
        max_power: num_type = 1000,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self.beta = beta
        self.threshold = threshold
        self.max_power = max_power
        self._all_pins = (
            ("_D_pin", Pin(self, 2)),
            ("_S_pin", Pin(self, 1)),
            ("_G_pin", Pin(self, 0)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "N-MOSFET",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "PNP": 1.0,
                "放大系数": Generate,
                "阈值电压": Generate,
                "最大功率": Generate,
                "锁定": 1.0,
            },
            "Statistics": {
                "电压GS": 0.0,
                "电压": 0.0,
                "电流": 0.0,
                "功率": 0.0,
                "状态": 0.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def beta(self) -> num_type:
        """放大系数"""
        result = self.properties["放大系数"]
        errors.assert_true(result is not Generate)
        return result

    @beta.setter
    def beta(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"beta must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["放大系数"] = value
        return value

    @property
    def threshold(self) -> num_type:
        """阈值电压"""
        result = self.properties["阈值电压"]
        errors.assert_true(result is not Generate)
        return result

    @threshold.setter
    def threshold(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"threshold must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["阈值电压"] = value
        return value

    @property
    def max_power(self) -> num_type:
        """最大功率"""
        result = self.properties["最大功率"]
        errors.assert_true(result is not Generate)
        return result

    @max_power.setter
    def max_power(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"max_power must be of type `int | float`, but got value `{value}` of type {type(value).__name__}"
            )

        self.properties["最大功率"] = value
        return value

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


class N_MOSFET(_N_MOSFET):
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
        beta: num_type = 0.027,
        threshold: num_type = 1.5,
        max_power: num_type = 1000,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            beta=beta,
            threshold=threshold,
            max_power=max_power,
            elementXYZ=elementXYZ,
            identifier=identifier,
        )
        _deprecated_assign_element_to_experiment(self)


class _P_MOSFET(CircuitBase):
    """P-MOSFET"""

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
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_G_pin", Pin(self, 0)),
            ("_D_pin", Pin(self, 1)),
            ("_S_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "P-MOSFET",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "PNP": 1.0,
                "放大系数": 0.027,
                "阈值电压": 1.5,
                "最大功率": 100.0,
                "锁定": 1.0,
            },
            "Statistics": {
                "电压GS": 0.0,
                "电压": 0.0,
                "电流": 0.0,
                "功率": 0.0,
                "状态": 1.0,
            },
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class P_MOSFET(_P_MOSFET):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _CurrentSource(CircuitBase):
    """电流源"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": "Current Source",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电流": 0.0099999997764825821,
                "内阻": 1000000000.0,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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


class Current_Source(_CurrentSource):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _SourceElectricity(CircuitBase):
    """波形发生器基类"""

    _all_pins: Tuple[Tuple[str, Pin], Tuple[str, Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier)

    @property
    def data(self) -> CircuitElementData:
        return {
            "ModelID": Generate,
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "电压": 3.0,
                "内阻": 0.5,
                "频率": 20000.0,
                "偏移": 0.0,
                "占空比": 0.5,
                "锁定": 1.0,
            },
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": -3.0},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
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

    @staticmethod
    def count_all_pins() -> int:
        return 2


class _SinewaveSource(_SourceElectricity):
    """正弦波发生器"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(x, y, z, elementXYZ, identifier)
        self.data["ModelID"] = "Sinewave Source"

    @final
    @staticmethod
    def zh_name() -> str:
        return "正弦波发生器"


class Sinewave_Source(_SinewaveSource):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _SquareSource(_SourceElectricity):
    """方波发生器"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(x, y, z, elementXYZ, identifier)
        self.data["ModelID"] = "Square Source"

    @final
    @staticmethod
    def zh_name() -> str:
        return "方波发生器"


class Square_Source(_SquareSource):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _TriangleSource(_SourceElectricity):
    """三角波发生器"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(x, y, z, elementXYZ, identifier)
        self.data["ModelID"] = "Triangle Source"

    @final
    @staticmethod
    def zh_name() -> str:
        return "三角波发生器"


class Triangle_Source(_TriangleSource):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _SawtoothSource(_SourceElectricity):
    """锯齿波发生器"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(x, y, z, elementXYZ, identifier)
        self.data["ModelID"] = "Sawtooth Source"

    @final
    @staticmethod
    def zh_name() -> str:
        return "锯齿波发生器"


class Sawtooth_Source(_SawtoothSource):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)


class _PulseSource(_SourceElectricity):
    """尖峰波发生器"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(x, y, z, elementXYZ, identifier)
        self.data["ModelID"] = "Pulse Source"

    @final
    @staticmethod
    def zh_name() -> str:
        return "尖峰波发生器"


class Pulse_Source(_PulseSource):
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
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(x, y, z, elementXYZ, identifier)
        _deprecated_assign_element_to_experiment(self)
