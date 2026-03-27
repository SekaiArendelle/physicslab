import abc
from physicsLab import errors
from physicsLab import coordinate_system

from physicsLab._core import get_current_experiment
from physicsLab._typing import Optional, List, CircuitElementData


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


class CircuitBase:
    __position: coordinate_system.Position
    __rotation: coordinate_system.Rotation
    __identifier: str
    __lock_status: bool
    __label: Optional[str]

    def __init__(
        self,
        position: coordinate_system.Position,
        identifier: str,
        lock_status: bool,
        label: Optional[str],
        rotation: coordinate_system.Rotation,
    ) -> None:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"position must be an instance of coordinate_system.Position, "
                f"got {type(position).__name__}"
            )
        self.position = position
        self.rotation = rotation
        self.identifier = identifier
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

    @property
    def rotation(self) -> coordinate_system.Rotation:
        return self.__rotation

    @rotation.setter
    def rotation(self, value: coordinate_system.Rotation) -> None:
        if not isinstance(value, coordinate_system.Rotation):
            raise TypeError(
                f"rotation must be an instance of coordinate_system.Rotation, got {type(value).__name__}"
            )

        self.__rotation = value

    @property
    def position(self) -> coordinate_system.Position:
        return self.__position

    @position.setter
    def position(
        self,
        value: coordinate_system.Position,
    ) -> None:
        if not isinstance(value, coordinate_system.Position):
            raise TypeError(
                f"position must be an instance of coordinate_system.Position, got {type(value).__name__}"
            )

        self.__position = value

    @property
    def lock_status(self) -> bool:
        return self.__lock_status

    @lock_status.setter
    def lock_status(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"lock_status must be of type `bool`, but got value {value} of type {type(value).__name__}"
            )

        self.__lock_status = value

    @property
    def label(self) -> Optional[str]:
        return self.__label

    @label.setter
    def label(self, value: Optional[str]) -> None:
        if not isinstance(value, (str, type(None))):
            raise TypeError(
                f"label must be of type `Optional[str]`, but got value {value} of type `{type(value).__name__}`"
            )

        self.__label = value

    @abc.abstractmethod
    def as_dict(self) -> CircuitElementData:
        raise NotImplementedError(
            "Subclasses of CircuitBase must implement the as_dict method"
        )
