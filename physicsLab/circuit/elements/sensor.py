# -*- coding: utf-8 -*-
from physicsLab import errors
from .._circuit_core import CircuitBase, Pin, _deprecated_register_element_in_stack
from physicsLab._core import _Experiment
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Generate,
    final,
    Iterator,
    Tuple,
    Literal,
)


class _MemsBase(CircuitBase):
    """三引脚集成式传感器基类"""

    _all_pins: Tuple[
        Tuple[Literal["_x_pin"], Pin],
        Tuple[Literal["_y_pin"], Pin],
        Tuple[Literal["_z_pin"], Pin],
    ]
    _x_pin: Pin
    _y_pin: Pin
    _z_pin: Pin

    def __init__(self, x: num_type, y: num_type, z: num_type, /) -> None:
        self.data: CircuitElementData = {
            "ModelID": Generate,
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": Generate,
                "输出阻抗": 10000,
                "偏移": Generate,
                "响应系数": Generate,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }
        self._all_pins = (
            ("_x_pin", Pin(self, 0)),
            ("_y_pin", Pin(self, 1)),
            ("_z_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 3

    @property
    def x(self) -> Pin:
        return self._x_pin

    @property
    def y(self) -> Pin:
        return self._y_pin

    @property
    def z(self) -> Pin:
        return self._z_pin

    @property
    @final
    def ranges(self) -> num_type:
        """量程"""
        result = self.properties["量程"]
        errors.assert_true(result is not Generate)
        return result

    @ranges.setter
    @final
    def ranges(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"ranges must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )

        self.properties["量程"] = value
        return value

    @property
    @final
    def shifting(self) -> num_type:
        """偏移"""
        result = self.properties["偏移"]
        errors.assert_true(result is not Generate)
        return result

    @shifting.setter
    @final
    def shifting(self, value: num_type) -> num_type:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"shifting must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )

        self.properties["偏移"] = value
        return value

    @property
    @final
    def response_factor(self) -> num_type:
        result = self.properties["响应系数"]
        errors.assert_true(result is not Generate)
        return result

    @response_factor.setter
    @final
    def response_factor(self, value: num_type) -> num_type:
        """响应系数"""
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"response_factor must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )

        self.properties["响应系数"] = value
        return value


class _Accelerometer(_MemsBase):
    """加速度计"""

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
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.2290000021457672,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Accelerometer"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> str:
        return "加速度计"


def Accelerometer(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    ranges: num_type = 2,
    shifting: num_type = 0.75,
    response_factor: num_type = 0.2290000021457672,
) -> _Accelerometer:
    result = _Accelerometer(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment,
        ranges=ranges, shifting=shifting, response_factor=response_factor
    )
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


class _AnalogJoystick(CircuitBase):
    """模拟摇杆"""

    _all_pins: Tuple[
        Tuple[Literal["_x1_pin"], Pin],
        Tuple[Literal["_x2_pin"], Pin],
        Tuple[Literal["_x3_pin"], Pin],
        Tuple[Literal["_y1_pin"], Pin],
        Tuple[Literal["_y2_pin"], Pin],
        Tuple[Literal["_y3_pin"], Pin],
    ]
    _x1_pin: Pin
    _x2_pin: Pin
    _x3_pin: Pin
    _y1_pin: Pin
    _y2_pin: Pin
    _y3_pin: Pin

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
        self.data: CircuitElementData = {
            "ModelID": "Analog Joystick",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"额定电阻": 10000, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }
        self._all_pins = (
            ("_x1_pin", Pin(self, 0)),
            ("_x2_pin", Pin(self, 1)),
            ("_x3_pin", Pin(self, 2)),
            ("_y1_pin", Pin(self, 3)),
            ("_y2_pin", Pin(self, 4)),
            ("_y3_pin", Pin(self, 5)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 6

    @final
    @staticmethod
    def zh_name() -> str:
        return "模拟摇杆"

    @property
    def x1(self) -> Pin:
        return self._x1_pin

    @property
    def x2(self) -> Pin:
        return self._x2_pin

    @property
    def x3(self) -> Pin:
        return self._x3_pin

    @property
    def y1(self) -> Pin:
        return self._y1_pin

    @property
    def y2(self) -> Pin:
        return self._y2_pin

    @property
    def y3(self) -> Pin:
        return self._y3_pin


def Analog_Joystick(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _AnalogJoystick:
    result = _AnalogJoystick(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment
    )
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


class _AttitudeSensor(_MemsBase):
    """姿态传感器"""

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
        ranges: num_type = 180,
        shifting: num_type = 2.5,
        response_factor: num_type = 0.0125,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Attitude Sensor"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> str:
        return "姿态传感器"


def Attitude_Sensor(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    ranges: num_type = 180,
    shifting: num_type = 2.5,
    response_factor: num_type = 0.0125,
) -> _AttitudeSensor:
    result = _AttitudeSensor(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment,
        ranges=ranges, shifting=shifting, response_factor=response_factor
    )
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


class _GravitySensor(_MemsBase):
    """重力加速计"""

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
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.229,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Gravity Sensor"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> str:
        return "重力加速计"


def Gravity_Sensor(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    ranges: num_type = 2,
    shifting: num_type = 0.75,
    response_factor: num_type = 0.229,
) -> _GravitySensor:
    result = _GravitySensor(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment,
        ranges=ranges, shifting=shifting, response_factor=response_factor
    )
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


class _Gyroscope(_MemsBase):
    """陀螺仪传感器"""

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
        ranges: num_type = 150,
        shifting: num_type = 2.5,
        response_factor: num_type = 0.0125,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Gyroscope"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> str:
        return "陀螺仪传感器"


def Gyroscope(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    ranges: num_type = 150,
    shifting: num_type = 2.5,
    response_factor: num_type = 0.0125,
) -> _Gyroscope:
    result = _Gyroscope(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment,
        ranges=ranges, shifting=shifting, response_factor=response_factor
    )
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


class _LinearAccelerometer(_MemsBase):
    """线性加速度计"""

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
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.229,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Linear Accelerometer"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> str:
        return "线性加速度计"


def Linear_Accelerometer(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    ranges: num_type = 2,
    shifting: num_type = 0.75,
    response_factor: num_type = 0.229,
) -> _LinearAccelerometer:
    result = _LinearAccelerometer(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment,
        ranges=ranges, shifting=shifting, response_factor=response_factor
    )
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


class _MagneticFieldSensor(_MemsBase):
    """磁场传感器"""

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
        ranges: num_type = 0.04,
        shifting: num_type = 3.2,
        response_factor: num_type = 80,
    ) -> None:
        super().__init__(x, y, z)
        self.data["ModelID"] = "Magnetic Field Sensor"
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor

    @final
    @staticmethod
    def zh_name() -> str:
        return "磁场传感器"


def Magnetic_Field_Sensor(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
    ranges: num_type = 0.04,
    shifting: num_type = 3.2,
    response_factor: num_type = 80,
) -> _MagneticFieldSensor:
    result = _MagneticFieldSensor(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment,
        ranges=ranges, shifting=shifting, response_factor=response_factor
    )
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


class _Photodiode(CircuitBase):
    """光电二极管"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

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
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Photodiode",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "前向压降": 0.6,
                "击穿电压": 0,
                "额定电流": 1,
                "响应系数": 0.1,
                "响应时间": 0.03,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "光电二极管"


def Photodiode(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _Photodiode:
    result = _Photodiode(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment
    )
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


class _Photoresistor(CircuitBase):
    """光敏电阻"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

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
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Photoresistor",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "亮电阻": 10000,
                "暗电阻": 1000000,
                "响应时间": 0.03,
                "最大电压": 150,
                "响应系数": 0.6,
                "锁定": 1.0,
            },
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 2

    @property
    def red(self) -> Pin:
        return self._red_pin

    @property
    def black(self) -> Pin:
        return self._black_pin

    @final
    @staticmethod
    def zh_name() -> str:
        return "光敏电阻"


def Photoresistor(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _Photoresistor:
    result = _Photoresistor(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment
    )
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


class _ProximitySensor(CircuitBase):
    """临近传感器"""

    _all_pins: Tuple[Tuple[Literal["_o_pin"], Pin]]
    _o_pin: Pin

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
        self._all_pins = (("_o_pin", Pin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.data: CircuitElementData = {
            "ModelID": "Proximity Sensor",
            "Identifier": Generate,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"高电平": 3, "低电平": 0, "输出阻抗": 10000, "锁定": 1.0},
            "Statistics": {},
            "Position": Generate,
            "Rotation": Generate,
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @staticmethod
    def count_all_pins() -> int:
        return 1

    @final
    @staticmethod
    def zh_name() -> str:
        return "临近传感器"

    @property
    def o(self) -> Pin:
        return self._o_pin


def Proximity_Sensor(
    x: num_type,
    y: num_type,
    z: num_type,
    /,
    *,
    elementXYZ: Optional[bool] = None,
    identifier: Optional[str] = None,
    experiment: Optional[_Experiment] = None,
) -> _ProximitySensor:
    result = _ProximitySensor(
        x, y, z, elementXYZ=elementXYZ, identifier=identifier, experiment=experiment
    )
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
