"""Sensor and MEMS-based circuit element classes."""

import uuid
from physicslab import coordinate_system
from .._base import CircuitBase, Pin
from physicslab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    final,
    Iterator,
    Generator,
    Tuple,
    cast,
)


class _MemsBase(CircuitBase):
    """Base class for MEMS sensor elements with X, Y and Z output pins."""

    _x_pin: Pin
    _y_pin: Pin
    _z_pin: Pin
    __ranges: num_type
    __shifting: num_type
    __response_factor: num_type

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        ranges: num_type,
        shifting: num_type,
        response_factor: num_type,
        identifier: str,
        lock_status: bool,
        label: Optional[str],
    ) -> None:
        self.ranges = ranges
        self.shifting = shifting
        self.response_factor = response_factor
        self._x_pin = Pin(self, 0, "x")
        self._y_pin = Pin(self, 1, "y")
        self._z_pin = Pin(self, 2, "z")
        super().__init__(position, rotation, identifier, lock_status, label)

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"_MemsBase("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def count_all_pins() -> int:
        """Return the total number of pins this element type has."""
        return 3

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "x", cast(property, cls.x)
        yield "y", cast(property, cls.y)
        yield "z", cast(property, cls.z)

    @property
    def x(self) -> Pin:
        """Output pin for the X-axis measurement."""
        return self._x_pin

    @property
    def y(self) -> Pin:
        """Output pin for the Y-axis measurement."""
        return self._y_pin

    @property
    def z(self) -> Pin:
        """Output pin for the Z-axis measurement."""
        return self._z_pin

    @property
    def ranges(self) -> num_type:
        """Measurement range setting for the sensor."""
        return self.__ranges

    @ranges.setter
    def ranges(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"ranges must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__ranges = value

    @property
    def shifting(self) -> num_type:
        """Output voltage offset (bias) of the sensor."""
        return self.__shifting

    @shifting.setter
    def shifting(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"shifting must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__shifting = value

    @property
    def response_factor(self) -> num_type:
        """Sensitivity coefficient mapping physical input to output voltage."""
        return self.__response_factor

    @response_factor.setter
    def response_factor(self, value: num_type) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"response_factor must be of type `int | float`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__response_factor = value


class Accelerometer(_MemsBase):
    """Three-axis accelerometer sensor element."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.2290000021457672,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            rotation=rotation,
        )

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Accelerometer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self.ranges,
                "输出阻抗": 10000,
                "偏移": self.shifting,
                "响应系数": self.response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"Accelerometer("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "加速度计"


class AnalogJoystick(CircuitBase):
    """Dual-axis analog joystick with three pins per axis."""

    _x1_pin: Pin
    _x2_pin: Pin
    _x3_pin: Pin
    _y1_pin: Pin
    _y2_pin: Pin
    _y3_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # build fields first, then call base init
        self._x1_pin = Pin(self, 0, "x1")
        self._x2_pin = Pin(self, 1, "x2")
        self._x3_pin = Pin(self, 2, "x3")
        self._y1_pin = Pin(self, 3, "y1")
        self._y2_pin = Pin(self, 4, "y2")
        self._y3_pin = Pin(self, 5, "y3")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Analog Joystick",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"额定电阻": 10000, "锁定": int(self.lock_status)},
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @staticmethod
    def count_all_pins() -> int:
        """Return the total number of pins this element type has."""
        return 6

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"AnalogJoystick("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "模拟摇杆"

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "x1", cast(property, cls.x1)
        yield "x2", cast(property, cls.x2)
        yield "x3", cast(property, cls.x3)
        yield "y1", cast(property, cls.y1)
        yield "y2", cast(property, cls.y2)
        yield "y3", cast(property, cls.y3)

    @property
    def x1(self) -> Pin:
        """First output pin for the X-axis potentiometer."""
        return self._x1_pin

    @property
    def x2(self) -> Pin:
        """Wiper pin for the X-axis potentiometer."""
        return self._x2_pin

    @property
    def x3(self) -> Pin:
        """Second output pin for the X-axis potentiometer."""
        return self._x3_pin

    @property
    def y1(self) -> Pin:
        """First output pin for the Y-axis potentiometer."""
        return self._y1_pin

    @property
    def y2(self) -> Pin:
        """Wiper pin for the Y-axis potentiometer."""
        return self._y2_pin

    @property
    def y3(self) -> Pin:
        """Second output pin for the Y-axis potentiometer."""
        return self._y3_pin


class AttitudeSensor(_MemsBase):
    """Three-axis attitude (orientation) sensor element."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        ranges: num_type = 180,
        shifting: num_type = 2.5,
        response_factor: num_type = 0.0125,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            rotation=rotation,
        )

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Attitude Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self.ranges,
                "输出阻抗": 10000,
                "偏移": self.shifting,
                "响应系数": self.response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"AttitudeSensor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "姿态传感器"


class GravitySensor(_MemsBase):
    """Three-axis gravity sensor element."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.229,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            rotation=rotation,
        )

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Gravity Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self.ranges,
                "输出阻抗": 10000,
                "偏移": self.shifting,
                "响应系数": self.response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"GravitySensor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "重力加速计"


class Gyroscope(_MemsBase):
    """Three-axis gyroscope sensor element."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        ranges: num_type = 150,
        shifting: num_type = 2.5,
        response_factor: num_type = 0.0125,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            rotation=rotation,
        )

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Gyroscope",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self.ranges,
                "输出阻抗": 10000,
                "偏移": self.shifting,
                "响应系数": self.response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"Gyroscope("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "陀螺仪传感器"


class LinearAccelerometer(_MemsBase):
    """Three-axis linear accelerometer sensor element."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        ranges: num_type = 2,
        shifting: num_type = 0.75,
        response_factor: num_type = 0.229,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            rotation=rotation,
        )

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Linear Accelerometer",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self.ranges,
                "输出阻抗": 10000,
                "偏移": self.shifting,
                "响应系数": self.response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"LinearAccelerometer("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "线性加速度计"


class MagneticFieldSensor(_MemsBase):
    """Three-axis magnetic field sensor element."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        ranges: num_type = 0.04,
        shifting: num_type = 3.2,
        response_factor: num_type = 80,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position,
            ranges=ranges,
            shifting=shifting,
            response_factor=response_factor,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            rotation=rotation,
        )

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
        return {
            "ModelID": "Magnetic Field Sensor",
            "Identifier": self.identifier,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "量程": self.ranges,
                "输出阻抗": 10000,
                "偏移": self.shifting,
                "响应系数": self.response_factor,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"MagneticFieldSensor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"ranges={self.ranges}, "
            f"shifting={self.shifting}, "
            f"response_factor={self.response_factor}, "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "磁场传感器"


class Photodiode(CircuitBase):
    """Light-sensitive photodiode sensor element."""

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
        """Serialise this element to a dict for inclusion in a .plsav file."""
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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @staticmethod
    def count_all_pins() -> int:
        """Return the total number of pins this element type has."""
        return 2

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cast(property, cls.red)
        yield "black", cast(property, cls.black)

    @property
    def red(self) -> Pin:
        """Anode (positive) pin of the photodiode."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Cathode (negative) pin of the photodiode."""
        return self._black_pin

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"Photodiode("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "光电二极管"


class Photoresistor(CircuitBase):
    """Light-dependent resistor (LDR) sensor element."""

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
        """Serialise this element to a dict for inclusion in a .plsav file."""
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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @staticmethod
    def count_all_pins() -> int:
        """Return the total number of pins this element type has."""
        return 2

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "red", cast(property, cls.red)
        yield "black", cast(property, cls.black)

    @property
    def red(self) -> Pin:
        """High-resistance terminal pin of the photoresistor."""
        return self._red_pin

    @property
    def black(self) -> Pin:
        """Low-resistance terminal pin of the photoresistor."""
        return self._black_pin

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"Photoresistor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "光敏电阻"


class ProximitySensor(CircuitBase):
    """Proximity sensor element with a single digital output pin."""

    _o_pin: Pin

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 180),
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._o_pin = Pin(self, 0, "o")
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(position, rotation, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        """Serialise this element to a dict for inclusion in a .plsav file."""
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
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0},
            "DiagramRotation": 0,
            "Label": self.label,
        }

    @staticmethod
    def count_all_pins() -> int:
        """Return the total number of pins this element type has."""
        return 1

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"ProximitySensor("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"label={self.label!r}, "
            f"lock_status={self.lock_status})"
        )

    @final
    @staticmethod
    def zh_name() -> str:
        """Return the Chinese display name for this element."""
        return "临近传感器"

    @classmethod
    def all_pins_property_iter(cls) -> Generator[tuple[str, property], None, None]:
        yield "o", cast(property, cls.o)

    @property
    def o(self) -> Pin:
        """Digital output pin of the proximity sensor."""
        return self._o_pin
