"""Base class definition for celestial body elements."""

import abc
from physicslab import coordinate_system


class CelestialBase:
    """Base class for celestial elements"""

    __position: coordinate_system.Position
    __velocity: coordinate_system.Velocity
    __acceleration: coordinate_system.Acceleration
    __identifier: str

    def __init__(
        self,
        position: coordinate_system.Position,
        velocity: coordinate_system.Velocity,
        acceleration: coordinate_system.Acceleration,
        identifier: str,
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.identifier = identifier

    @property
    def identifier(self) -> str:
        """Returns the unique string identifier of this celestial element."""
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
        """Returns the position of this celestial element."""
        return self.__position

    @position.setter
    def position(self, position: coordinate_system.Position) -> None:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )

        self.__position = position

    @property
    def velocity(self) -> coordinate_system.Velocity:
        """Returns the velocity of this celestial element."""
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: coordinate_system.Velocity) -> None:
        if not isinstance(velocity, coordinate_system.Velocity):
            raise TypeError(
                f"velocity must be of type `Velocity`, but got value {velocity} of type {type(velocity).__name__}"
            )

        self.__velocity = velocity

    @property
    def acceleration(self) -> coordinate_system.Acceleration:
        """Returns the acceleration of this celestial element."""
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration: coordinate_system.Acceleration) -> None:
        if not isinstance(acceleration, coordinate_system.Acceleration):
            raise TypeError(
                f"acceleration must be of type `Acceleration`, but got value {acceleration} of type {type(acceleration).__name__}"
            )

        self.__acceleration = acceleration

    @abc.abstractmethod
    def as_dict(self) -> dict:
        """Subclasses must return a dict representation of this element for saving to a .plsav file."""
        raise NotImplementedError(
            "The method `as_dict` must be implemented in the subclass"
        )

    @abc.abstractmethod
    def to_constructor_str(self) -> str:
        """Subclasses must return a Python constructor call string that recreates this element."""
        raise NotImplementedError(
            "The method `to_constructor_str` must be implemented in the subclass"
        )
