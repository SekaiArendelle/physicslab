import abc
from physicsLab import coordinate_system


class ElectromagnetismBase:
    """Base class for electromagnetism elements"""

    __position: coordinate_system.Position
    __rotation: coordinate_system.Rotation
    __velocity: coordinate_system.Velocity
    __identifier: str

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        identifier: str,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        self.position = position
        self.rotation = rotation
        self.identifier = identifier
        self.velocity = velocity

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        if not isinstance(identifier, str):
            raise TypeError(
                f"identifier must be of type `str`, but got value {identifier} of type {type(identifier).__name__}"
            )

        self.__identifier = identifier

    @property
    def position(self) -> coordinate_system.Position:
        return self.__position

    @position.setter
    def position(self, position: coordinate_system.Position) -> None:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )

        self.__position = position

    @property
    def rotation(self) -> coordinate_system.Rotation:
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation: coordinate_system.Rotation) -> None:
        if not isinstance(rotation, coordinate_system.Rotation):
            raise TypeError(
                f"rotation must be of type `Rotation`, but got value {rotation} of type {type(rotation).__name__}"
            )

        self.__rotation = rotation

    @property
    def velocity(self) -> coordinate_system.Velocity:
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: coordinate_system.Velocity) -> None:
        if not isinstance(velocity, coordinate_system.Velocity):
            raise TypeError(
                f"velocity must be of type `Velocity`, but got value {velocity} of type {type(velocity).__name__}"
            )

        self.__velocity = velocity

    @abc.abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError(
            "The method `as_dict` must be implemented in the subclass"
        )
