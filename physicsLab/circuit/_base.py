import abc
from physicsLab import coordinate_system
from physicsLab._typing import Optional, CircuitElementData


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
