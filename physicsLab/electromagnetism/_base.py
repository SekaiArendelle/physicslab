"""Base class for electromagnetism experiment elements."""

import abc
from physicsLab import coordinate_system


class ElectromagnetismBase:
    """Base class for electromagnetism elements"""

    __position: coordinate_system.Position
    __rotation: coordinate_system.Rotation
    __velocity: coordinate_system.Velocity
    __angular_velocity: coordinate_system.AngularVelocity
    __identifier: str
    __lock_status: bool

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation,
        identifier: str,
        velocity: coordinate_system.Velocity,
        angular_velocity: coordinate_system.AngularVelocity,
        lock_status: bool,
    ) -> None:
        self.position = position
        self.rotation = rotation
        self.identifier = identifier
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.lock_status = lock_status

    @property
    def lock_status(self) -> bool:
        """Whether this element is locked in place."""
        return self.__lock_status

    @lock_status.setter
    def lock_status(self, lock_status: bool) -> None:
        if not isinstance(lock_status, bool):
            raise TypeError(
                f"lock_status must be of type `bool`, but got value {lock_status} of type {type(lock_status).__name__}"
            )

        self.__lock_status = lock_status

    @property
    def identifier(self) -> str:
        """Unique string identifier for this element."""
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
        """World-space position of this element."""
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
        """Euler-angle rotation of this element."""
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
        """Initial linear velocity of this element."""
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: coordinate_system.Velocity) -> None:
        if not isinstance(velocity, coordinate_system.Velocity):
            raise TypeError(
                f"velocity must be of type `Velocity`, but got value {velocity} of type {type(velocity).__name__}"
            )

        self.__velocity = velocity

    @property
    def angular_velocity(self) -> coordinate_system.AngularVelocity:
        """Initial angular velocity of this element."""
        return self.__angular_velocity

    @angular_velocity.setter
    def angular_velocity(
        self, angular_velocity: coordinate_system.AngularVelocity
    ) -> None:
        if not isinstance(angular_velocity, coordinate_system.AngularVelocity):
            raise TypeError(
                f"angular_velocity must be of type `AngularVelocity`, but got value {angular_velocity} of type {type(angular_velocity).__name__}"
            )

        self.__angular_velocity = angular_velocity

    @staticmethod
    @abc.abstractmethod
    def zh_name() -> str:
        """Return the Chinese name of this element type as used in Physics-Lab-AR."""
        raise NotImplementedError(
            "The method `zh_name` must be implemented in the subclass"
        )

    @abc.abstractmethod
    def as_dict(self) -> dict:
        """Serialise this element to a dictionary for inclusion in a ``.plsav`` file."""
        raise NotImplementedError(
            "The method `as_dict` must be implemented in the subclass"
        )
