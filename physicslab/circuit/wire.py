"""Wire metadata types for circuit connections."""

from physicslab.enums import ColorOfWire


class WireInfo:
    """Metadata associated with a single wire between two circuit pins."""

    __color: ColorOfWire

    def __init__(self, color: ColorOfWire = ColorOfWire.blue) -> None:
        self.color = color

    @property
    def color(self) -> ColorOfWire:
        """Color of this wire."""
        return self.__color

    @color.setter
    def color(self, value: ColorOfWire) -> None:
        if not isinstance(value, ColorOfWire):
            raise TypeError(
                f"Parameter color must be of type `WireColor`, but got value {value} of type `{type(value).__name__}`"
            )

        self.__color = value
