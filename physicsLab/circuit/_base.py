import abc
from physicsLab import coordinate_system
from physicsLab._typing import Optional, CircuitElementData, Iterator, Tuple


class CircuitBase:
    __position: coordinate_system.Position
    __rotation: coordinate_system.Rotation
    __identifier: str
    __lock_status: bool
    __label: Optional[str]

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        identifier: str,
        lock_status: bool,
        label: Optional[str],
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

    @abc.abstractmethod
    def all_pins(self) -> Iterator[Tuple[str, "Pin"]]:
        raise NotImplementedError(
            "Subclasses of CircuitBase must implement the all_pins method"
        )

    @staticmethod
    @abc.abstractmethod
    def count_all_pins() -> int:
        raise NotImplementedError(
            "Subclasses of CircuitBase must implement the count_all_pins method"
        )

    @abc.abstractmethod
    def to_constructor_str(self) -> str:
        raise NotImplementedError(
            "Subclasses of CircuitBase must implement the to_constructor_str method"
        )


class Pin:
    __element: CircuitBase
    __pin_label: int
    __pin_name: str

    def __init__(self, element: CircuitBase, pin_label: int, pin_name: str) -> None:
        self.element = element
        self.pin_label = pin_label
        self.pin_name = pin_name

    @property
    def element(self) -> CircuitBase:
        return self.__element

    @element.setter
    def element(self, value: CircuitBase) -> None:
        if not isinstance(value, CircuitBase):
            raise TypeError(
                f"element must be of type `CircuitBase`, but got value {value} of type `{type(value).__name__}`"
            )

        self.__element = value

    @property
    def pin_label(self) -> int:
        return self.__pin_label

    @pin_label.setter
    def pin_label(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"pin_label must be of type `int`, but got value {value} of type `{type(value).__name__}`"
            )

        self.__pin_label = value

    @property
    def pin_name(self) -> str:
        return self.__pin_name

    @pin_name.setter
    def pin_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"pin_name must be of type `str`, but got value {value} of type `{type(value).__name__}`"
            )

        self.__pin_name = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return False

        return self.element == other.element and self.pin_label == other.pin_label

    def __hash__(self) -> int:
        return hash((self.element, self.pin_label))


class InputPin(Pin):
    """Input pin, only for logic circuit"""

    def __init__(self, element: CircuitBase, pinLabel: int, pin_name: str) -> None:
        super().__init__(element, pinLabel, pin_name)


class OutputPin(Pin):
    """Output pin, only for logic circuit"""

    def __init__(self, element, pinLabel: int, pin_name: str) -> None:
        super().__init__(element, pinLabel, pin_name)
