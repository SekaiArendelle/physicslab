from physicsLab import coordinate_system
from .._circuit_core import (
    CircuitBase,
    Pin,
    _deprecated_init_attr_experiment,
    _deprecated_assign_element_to_experiment,
)
from physicsLab._core import _Experiment
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
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
    _ranges: num_type
    _shifting: num_type
    _response_factor: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type,
        shifting: num_type,
        response_factor: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self.set_ranges(ranges)
        self.set_shifting(shifting)
        self.set_response_factor(response_factor)
        self._all_pins = (
            ("_x_pin", Pin(self, 0)),
            ("_y_pin", Pin(self, 1)),
            ("_z_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, elementXYZ, identifier, lock_status, label)

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

    def get_ranges(self) -> num_type:
        return self._ranges

    def set_ranges(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"ranges must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self._ranges = value

    def get_shifting(self) -> num_type:
        return self._shifting

    def set_shifting(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"shifting must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self._shifting = value

    def get_response_factor(self) -> num_type:
        return self._response_factor

    def set_response_factor(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"response_factor must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self._response_factor = value


class _Accelerometer(_MemsBase):
    """加速度计"""

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.2290000021457672,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Accelerometer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self._ranges,
                "输出阻抗": 10000,
                "偏移": self._shifting,
                "响应系数": self._response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "加速度计"


class Accelerometer(_Accelerometer):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        position: coordinate_system.Position,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # build fields first, then call base init
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
        super().__init__(position, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Analog Joystick",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"额定电阻": 10000, "锁定": int(self.lock_status)},
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

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


class Analog_Joystick(_AnalogJoystick):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            elementXYZ,
            identifier,
            lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _AttitudeSensor(_MemsBase):
    """姿态传感器"""

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type = 180,
        shifting: num_type = 2.5,
        response_factor: num_type = 0.0125,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Attitude Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self._ranges,
                "输出阻抗": 10000,
                "偏移": self._shifting,
                "响应系数": self._response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "姿态传感器"


class Attitude_Sensor(_AttitudeSensor):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _GravitySensor(_MemsBase):
    """重力加速计"""

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.229,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Gravity Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self._ranges,
                "输出阻抗": 10000,
                "偏移": self._shifting,
                "响应系数": self._response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "重力加速计"


class Gravity_Sensor(_GravitySensor):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _Gyroscope(_MemsBase):
    """陀螺仪传感器"""

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type = 150,
        shifting: num_type = 2.5,
        response_factor: num_type = 0.0125,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Gyroscope",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self._ranges,
                "输出阻抗": 10000,
                "偏移": self._shifting,
                "响应系数": self._response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "陀螺仪传感器"


class Gyroscope(_Gyroscope):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _LinearAccelerometer(_MemsBase):
    """线性加速度计"""

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.229,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Linear Accelerometer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self._ranges,
                "输出阻抗": 10000,
                "偏移": self._shifting,
                "响应系数": self._response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "线性加速度计"


class Linear_Accelerometer(_LinearAccelerometer):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _MagneticFieldSensor(_MemsBase):
    """磁场传感器"""

    def __init__(
        self,
        position: coordinate_system.Position,
        ranges: num_type = 0.04,
        shifting: num_type = 3.2,
        response_factor: num_type = 80,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Magnetic Field Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self._ranges,
                "输出阻抗": 10000,
                "偏移": self._shifting,
                "响应系数": self._response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @final
    @staticmethod
    def zh_name() -> str:
        return "磁场传感器"


class Magnetic_Field_Sensor(_MagneticFieldSensor):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            elementXYZ=elementXYZ,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _Photodiode(CircuitBase):
    """光电二极管"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Photodiode",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "前向压降": 0.6,
                "击穿电压": 0,
                "额定电流": 1,
                "响应系数": 0.1,
                "响应时间": 0.03,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
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


class Photodiode(_Photodiode):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            elementXYZ,
            identifier,
            lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _Photoresistor(CircuitBase):
    """光敏电阻"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Photoresistor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "亮电阻": 10000,
                "暗电阻": 1000000,
                "响应时间": 0.03,
                "最大电压": 150,
                "响应系数": 0.6,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
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


class Photoresistor(_Photoresistor):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            elementXYZ,
            identifier,
            lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _ProximitySensor(CircuitBase):
    """临近传感器"""

    _all_pins: Tuple[Tuple[Literal["_o_pin"], Pin]]
    _o_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (("_o_pin", Pin(self, 0)),)
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(position, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Proximity Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "高电平": 3,
                "低电平": 0,
                "输出阻抗": 10000,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
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


class Proximity_Sensor(_ProximitySensor):
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
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            coordinate_system.Position(x, y, z),
            elementXYZ,
            identifier,
            lock_status,
            label=label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()
