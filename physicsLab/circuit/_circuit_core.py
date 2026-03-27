from physicsLab import errors
from physicsLab import coordinate_system

from physicsLab.enums import ExperimentType, WireColor
from physicsLab._tools import randString
from physicsLab._core import (
    _Experiment,
    get_current_experiment,
)
from physicsLab._typing import (
    Optional,
    Self,
    num_type,
    override,
    final,
    List,
    Tuple,
    Iterator,
)


class _PinMeta(type):
    """该类仅仅用来实现以下效果:
    通过 isinstance(cls, type(Pin)) 判断cls是否是引脚的class
    """


# 对于逻辑电路，应该使用`InputPin` 和 `OutputPin`
class Pin(metaclass=_PinMeta):
    """电学元件引脚"""

    __slots__ = ("element_self", "_pin_label")

    def __init__(self, input_self: "CircuitBase", _pin_label: int) -> None:
        self.element_self: "CircuitBase" = input_self
        self._pin_label: int = _pin_label

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return False

        return (
            self.element_self == other.element_self
            and self._pin_label == other._pin_label
        )

    def __hash__(self) -> int:
        return hash(self.element_self) + hash(self._pin_label)

    def export_str(self) -> str:
        """将引脚转换为 a_element.a_pin 的形式"""
        pin_name = self.get_pin_name()
        return f"e{self.element_self.get_index()}.{pin_name}"

    def get_pin_name(self) -> str:
        """获取该引脚在该元件中的名字
        @return: (e.g. i_up)
        """
        for name, a_pin in self.element_self.all_pins():
            if a_pin == self:
                return name[1:-4]
        errors.unreachable()

    def get_wires(self) -> List["Wire"]:
        """获取该引脚上连接的所有导线"""
        res = []
        for a_wire in self.element_self.experiment.Wires:
            if a_wire.Source == self or a_wire.Target == self:
                res.append(a_wire)
        return res


class InputPin(Pin):
    """仅用于逻辑电路的输入引脚"""

    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)


class OutputPin(Pin):
    """仅用于逻辑电路的输出引脚"""

    def __init__(self, input_self, pinLabel: int) -> None:
        super().__init__(input_self, pinLabel)


class Wire:
    """导线"""

    __slots__ = ("Source", "Target", "color")

    def __init__(
        self, source_pin: Pin, target_pin: Pin, color: WireColor = WireColor.blue
    ) -> None:
        if not isinstance(source_pin, Pin):
            raise TypeError(
                f"Parameter source_pin must be of type `Pin`, but got value {source_pin} of type `{type(source_pin).__name__}`"
            )
        if not isinstance(target_pin, Pin):
            raise TypeError(
                f"Parameter target_pin must be of type `Pin`, but got value {target_pin} of type `{type(target_pin).__name__}`"
            )
        if not isinstance(color, WireColor):
            raise TypeError(
                f"Parameter color must be of type `WireColor`, but got value {color} of type `{type(color).__name__}`"
            )

        if source_pin.element_self.experiment is not target_pin.element_self.experiment:
            raise errors.InvalidWireError("can't link wire in two experiment")

        if source_pin == target_pin:
            raise errors.InvalidWireError("can't link wire to itself")

        self.Source: Pin = source_pin
        self.Target: Pin = target_pin
        self.color: WireColor = color

    def __hash__(self) -> int:
        return hash(self.Source) + hash(self.Target)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Wire):
            return False

        # 判断两个导线是否相等与导线的颜色无关
        if (
            self.Source == other.Source
            and self.Target == other.Target
            or self.Source == other.Target
            and self.Target == other.Source
        ):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"crt_wire({self.Source.export_str()}, {self.Target.export_str()}, color={self.color})"

    def release(self) -> dict:
        return {
            "Source": self.Source.element_self.identifier,
            "SourcePin": self.Source._pin_label,
            "Target": self.Target.element_self.identifier,
            "TargetPin": self.Target._pin_label,
            "ColorName": f"{self.color.value}色导线",
        }


def crt_wire(*pins: Pin, color: WireColor = WireColor.blue) -> List[Wire]:
    """连接导线"""
    if not all(isinstance(a_pin, Pin) for a_pin in pins):
        raise TypeError(f"Parameter pins must be of type `tuple[Pin]`")
    if not isinstance(color, WireColor):
        raise TypeError(
            f"Parameter color must be of type `WireColor`, but got value {color} of type `{type(color).__name__}`"
        )
    if len(pins) <= 1:
        raise ValueError("pins must be more than 1")

    _expe = get_current_experiment()
    if _expe.experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    res: List[Wire] = []
    for i in range(len(pins) - 1):
        source_pin, target_pin = pins[i], pins[i + 1]
        a_wire = Wire(source_pin, target_pin, color)
        res.append(a_wire)
        _expe.Wires.add(a_wire)

    return res


def del_wire(source_pin: Pin, target_pin: Pin) -> None:
    """删除导线"""
    if not isinstance(source_pin, Pin):
        raise TypeError(
            f"Parameter source_pin must be of type `Pin`, but got value {source_pin} of type `{type(source_pin).__name__}`"
        )
    if not isinstance(target_pin, Pin):
        raise TypeError(
            f"Parameter target_pin must be of type `Pin`, but got value {target_pin} of type `{type(target_pin).__name__}`"
        )

    _expe = get_current_experiment()
    if _expe.experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    _expe.Wires.remove(Wire(source_pin, target_pin))


class CircuitBase:
    """所有电学元件的父类"""

    _position: coordinate_system.Position
    _rotation: coordinate_system.Rotation
    __identifier: str
    _lock_status: bool
    _label: Optional[str]

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: str,
        lock_status: bool,
        label: Optional[str],
    ) -> None:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"position must be an instance of coordinate_system.Position, "
                f"got {type(position).__name__}"
            )
        self.set_position(position.x, position.y, position.z)
        self.identifier = identifier
        self.set_rotation(0, 0, 180)
        self.lock_status = lock_status
        self.label = label

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"identifier must be of type `str`, but got value {value} of type `{type(value).__name__}`"
            )
        self.__identifier = value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self._position.x}, {self._position.y}, {self._position.z}, "
            f")"
        )

    @final
    def set_rotation(self, x_r: num_type, y_r: num_type, z_r: num_type) -> Self:
        """设置元件的角度"""
        if not isinstance(x_r, (int, float)):
            raise TypeError(
                f"Parameter x_r must be of type `int | float`, but got value {x_r} of type `{type(x_r).__name__}`"
            )
        if not isinstance(y_r, (int, float)):
            raise TypeError(
                f"Parameter y_r must be of type `int | float`, but got value {y_r} of type `{type(y_r).__name__}`"
            )
        if not isinstance(z_r, (int, float)):
            raise TypeError(
                f"Parameter z_r must be of type `int | float`, but got value {z_r} of type `{type(z_r).__name__}`"
            )

        self._rotation = coordinate_system.Rotation(x_r, y_r, z_r)
        return self

    @override
    def set_position(
        self,
        x: num_type,
        y: num_type,
        z: num_type,
    ) -> Self:
        """设置元件的位置"""
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter x must be of type `int | float`, but got value {x} of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter y must be of type `int | float`, but got value {y} of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter z must be of type `int | float`, but got value {z} of type `{type(z).__name__}`"
            )
        self._position = coordinate_system.Position(x, y, z)

        _Expe: _Experiment = self.experiment

        for self_list in _Expe._position2elements.values():
            if self in self_list:
                self_list.remove(self)

        errors.assert_true(hasattr(self, "_position"))
        if self._position in _Expe._position2elements.keys():
            _Expe._position2elements[self._position].append(self)
        else:
            _Expe._position2elements[self._position] = [self]

        return self

    @property
    @final
    def lock_status(self) -> bool:
        return self._lock_status

    @lock_status.setter
    @final
    def lock_status(self, value: bool) -> None:
        """是否锁定元件 (位置不会受元件间碰撞的影响)

        Args:
            status: 是否锁定元件
        """
        if not isinstance(value, bool):
            raise TypeError(
                f"lock_status must be of type `bool`, but got value {value} of type {type(value).__name__}"
            )

        self._lock_status = value

    @property
    @final
    def label(self) -> Optional[str]:
        return self._label

    @label.setter
    @final
    def label(self, value: Optional[str]) -> None:
        if not isinstance(value, (str, type(None))):
            raise TypeError(
                f"label must be of type `Optional[str]`, but got value {value} of type `{type(value).__name__}`"
            )

        self._label = value
