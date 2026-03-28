from ._base import CircuitBase


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


class InputPin(Pin):
    """Input pin, only for logic circuit"""

    def __init__(self, element: CircuitBase, pinLabel: int, pin_name: str) -> None:
        super().__init__(element, pinLabel, pin_name)


class OutputPin(Pin):
    """Output pin, only for logic circuit"""

    def __init__(self, element, pinLabel: int, pin_name: str) -> None:
        super().__init__(element, pinLabel, pin_name)
