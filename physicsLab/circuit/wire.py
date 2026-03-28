from physicsLab.enums import ColorOfWire


class WireInfo:
    __color: ColorOfWire

    def __init__(self, color: ColorOfWire = ColorOfWire.blue) -> None:
        self.color = color

    @property
    def color(self) -> ColorOfWire:
        return self.__color

    @color.setter
    def color(self, value: ColorOfWire) -> None:
        if not isinstance(value, ColorOfWire):
            raise TypeError(
                f"Parameter color must be of type `WireColor`, but got value {value} of type `{type(value).__name__}`"
            )

        self.__color = value
