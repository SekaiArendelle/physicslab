from physicsLab import errors
from physicsLab._tools import round_data
from physicsLab._core import _Experiment
from .._circuit_core import (
    CircuitBase,
    Pin,
    _deprecated_init_attr_experiment,
    _deprecated_assign_element_to_experiment,
)
from physicsLab.enums import SwitchState, PDTSwitchState
from physicsLab._typing import (
    Optional,
    num_type,
    CircuitElementData,
    Self,
    override,
    final,
    Iterator,
    Tuple,
    Literal,
)


class _SwitchBase(CircuitBase):
    """开关基类"""

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)


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
        identifier: Optional[str] = None,
        switch_state: SwitchState = SwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        super().__init__(
            x,
            y,
            z,
            elementXYZ=None,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
        self.switch_state = switch_state
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def switch_state(self) -> SwitchState:
        return self._switch_state

    @switch_state.setter
    def switch_state(self, value: SwitchState) -> None:
        if not isinstance(value, SwitchState):
            raise TypeError(
                f"switch_state must be of type `SwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self._switch_state = value

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

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Simple Switch",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {
                "开关": self.switch_state.value,
                "锁定": int(self.lock_status),
            },
            "Statistics": {},
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def __repr__(self) -> str:
        res = (
            f"Simple_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ},"
            f"switch_state={self.switch_state})"
        )

        return res


class Simple_Switch(_SimpleSwitch):
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
        switch_state: SwitchState = SwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            identifier=identifier,
            switch_state=switch_state,
            label=label,
            lock_status=lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        switch_state: PDTSwitchState = PDTSwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        self.switch_state = switch_state
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def switch_state(self) -> PDTSwitchState:
        return self._switch_state

    @switch_state.setter
    def switch_state(self, value: PDTSwitchState) -> None:
        if not isinstance(value, PDTSwitchState):
            raise TypeError(
                f"switch_state must be of type `PDTSwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self._switch_state = value

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def __repr__(self) -> str:
        res = (
            f"SPDT_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ},"
            f"switch_state={self.switch_state})"
        )

        return res

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


class SPDT_Switch(_SPDTSwitch):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        switch_state: PDTSwitchState = PDTSwitchState.OFF,
        experiment: Optional[_Experiment] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            elementXYZ,
            identifier,
            switch_state,
            lock_status,
            label,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        switch_state: PDTSwitchState = PDTSwitchState.OFF,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_low_pin", Pin(self, 0)),
            ("_mid_low_pin", Pin(self, 1)),
            ("_r_low_pin", Pin(self, 2)),
            ("_l_up_pin", Pin(self, 3)),
            ("_mid_up_pin", Pin(self, 4)),
            ("_r_up_pin", Pin(self, 5)),
        )
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        self.switch_state = switch_state
        for name, pin in self._all_pins:
            setattr(self, name, pin)

    @property
    def switch_state(self) -> PDTSwitchState:
        return self._switch_state

    @switch_state.setter
    def switch_state(self, value: PDTSwitchState) -> None:
        if not isinstance(value, PDTSwitchState):
            raise TypeError(
                f"switch_state must be of type `PDTSwitchState`, but got value `{value}` of type `{type(value).__name__}`"
            )
        self._switch_state = value

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @final
    @staticmethod
    def zh_name() -> str:
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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Z": 0, "Magnitude": 0},
            "DiagramRotation": 0,
        }

    def __repr__(self) -> str:
        res = (
            f"DPDT_Switch({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ},"
            f"switch_state={self.switch_state})"
        )

        return res

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


class DPDT_Switch(_DPDTSwitch):
    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        /,
        *,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        switch_state: PDTSwitchState = PDTSwitchState.OFF,
        experiment: Optional[_Experiment] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x, y, z, elementXYZ, identifier, switch_state, lock_status, label
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Push Switch",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"开关": 0.0, "默认开关": 0.0, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0},
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
        return "按钮开关"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class Push_Switch(_PushSwitch):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _AirSwitch(CircuitBase):
    """空气开关"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin
    __switch_state: SwitchState

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
        switch_state: SwitchState = SwitchState.OFF,
    ) -> None:
        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.switch_state = switch_state
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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
            "Position": self._position.as_postion_str_in_plsav(),
            "Rotation": self._rotation.as_rotation_str_in_plsav(),
            "DiagramCached": False,
            "DiagramPosition": {"X": 0, "Y": 0, "Magnitude": 0.0},
            "DiagramRotation": 0,
        }

    def all_pins(self) -> Iterator[Tuple[str, Pin]]:
        return iter(self._all_pins)

    @property
    def switch_state(self) -> SwitchState:
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
            f"elementXYZ={self.is_elementXYZ}, "
            f"switch_state={self.switch_state})"
        )

        return res


class Air_Switch(_AirSwitch):
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
        switch_state: SwitchState = SwitchState.OFF,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x, y, z, elementXYZ, identifier, lock_status, label, switch_state
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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
        return "白炽灯泡"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class Incandescent_Lamp(_IncandescentLamp):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _BatterySource(CircuitBase):
    """一节电池"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin
    voltage: num_type
    internal_resistance: num_type

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        voltage: num_type = 1.5,
        internal_resistance: num_type = 0,
        elementXYZ: Optional[bool] = None,
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

        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)

        self.voltage = voltage
        self.internal_resistance = internal_resistance
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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
        return "一节电池"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class Battery_Source(_BatterySource):
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
        voltage: num_type = 1.5,
        internal_resistance: num_type = 0,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            voltage=voltage,
            internal_resistance=internal_resistance,
            elementXYZ=elementXYZ,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _StudentSource(CircuitBase):
    """学生电源"""

    _all_pins: Tuple[
        Tuple[Literal["_l_pin"], Pin],
        Tuple[Literal["_l_mid_pin"], Pin],
        Tuple[Literal["_r_mid_pin"], Pin],
        Tuple[
            Literal["_r_pin"],
            Pin,
        ],
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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_l_mid_pin", Pin(self, 1)),
            ("_r_mid_pin", Pin(self, 2)),
            ("_r_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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


class Student_Source(_StudentSource):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _Resistor(CircuitBase):
    """电阻"""

    _all_pins: Tuple[Tuple[Literal["_red_pin"], Pin], Tuple[Literal["_black_pin"], Pin]]
    _red_pin: Pin
    _black_pin: Pin
    resistance: num_type

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        resistance: num_type = 10,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if not isinstance(resistance, (int, float)):
            raise TypeError(
                f"resistance must be of type `int | float`, but got value `{resistance}` of type `{type(resistance).__name__}`"
            )

        self._all_pins = (
            ("_red_pin", Pin(self, 0)),
            ("_black_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.resistance = resistance
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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
        return "电阻"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2

    def fix_resistance(self) -> Self:
        """修正电阻值的浮点误差"""
        self.resistance = round_data(self.resistance)
        return self

    def __repr__(self) -> str:
        return (
            f"Resistor({self._position.x}, {self._position.y}, {self._position.z}, "
            f"elementXYZ={self.is_elementXYZ}, "
            f"resistance={self.resistance})"
        )


class Resistor(_Resistor):
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
        resistance: num_type = 10,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x,
            y,
            z,
            resistance=resistance,
            elementXYZ=elementXYZ,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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
        return "保险丝"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class Fuse_Component(_FuseComponent):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_low_pin", Pin(self, 0)),
            ("_r_low_pin", Pin(self, 1)),
            ("_l_up_pin", Pin(self, 2)),
            ("_r_up_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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


class Slide_Rheostat(_SlideRheostat):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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
        return "多用电表"

    @final
    @staticmethod
    def count_all_pins() -> int:
        return 2


class Multimeter(_Multimeter):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Galvanometer",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 3.0, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
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


class Galvanometer(_Galvanometer):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Microammeter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"量程": 0.1, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0, "功率": 0.0, "电压": 0.0, "刻度": 0.0},
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


class Microammeter(_Microammeter):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_l_mid_pin", Pin(self, 2)),
            ("_r_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 3)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

    def as_dict(self) -> CircuitElementData:
        return {
            "ModelID": "Electricity Meter",
            "Identifier": self.identifier,
            "Label": self.label,
            "IsBroken": False,
            "IsLocked": False,
            "Properties": {"示数": 0.0, "额定电流": 6.0, "锁定": int(self.lock_status)},
            "Statistics": {"电流": 0.0, "电压": 0.0, "功率": 0.0},
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


class Electricity_Meter(_ElectricityMeter):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


class _ResistanceBox(CircuitBase):
    """电阻箱"""

    _all_pins: Tuple[Tuple[Literal["_l_pin"], Pin], Tuple[Literal["_r_pin"], Pin]]
    _l_pin: Pin
    _r_pin: Pin
    resistance: num_type

    def __init__(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
        resistance: num_type = 10,
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        if not isinstance(resistance, (int, float)):
            raise TypeError(
                f"resistance must be of type `int | float`, but got value {resistance} of type {type(resistance).__name__}"
            )

        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_r_pin", Pin(self, 1)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        self.resistance = resistance
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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


class Resistance_Box(_ResistanceBox):
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
        resistance: num_type = 10,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        # this class is deprecated
        _deprecated_init_attr_experiment(self, experiment=experiment)
        super().__init__(
            x, y, z, resistance, elementXYZ, identifier, lock_status, label
        )
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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


class Simple_Ammeter(_SimpleAmmeter):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()


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
        elementXYZ: Optional[bool] = None,
        identifier: Optional[str] = None,
        lock_status: bool = True,
        label: Optional[str] = None,
    ) -> None:
        self._all_pins = (
            ("_l_pin", Pin(self, 0)),
            ("_mid_pin", Pin(self, 1)),
            ("_r_pin", Pin(self, 2)),
        )
        for name, pin in self._all_pins:
            setattr(self, name, pin)
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)

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


class Simple_Voltmeter(_SimpleVoltmeter):
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
        super().__init__(x, y, z, elementXYZ, identifier, lock_status, label)
        _deprecated_assign_element_to_experiment(self)

    @property
    def data(self) -> CircuitElementData:
        return self.as_dict()
