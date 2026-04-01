"""3-D coordinate system types used throughout physicslab.

Provides typed vector classes (Position, Rotation, Velocity, AngularVelocity,
Acceleration) and helpers for serialising/deserialising them to and from the
``.plsav`` string format used by Physics-Lab-AR.
"""

from ._typing import num_type


class Position:
    """An immutable 3-D position vector (x, y, z)."""

    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Position):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_postion_str_in_plsav(self) -> str:
        """Return the position as a comma-separated string in plsav format (x,z,y)."""
        return f"{self.x},{self.z},{self.y}"


def construct_position_from_plsav_str(position_str: str) -> Position:
    """Construct a Position from a plsav-format string.

    Args:
        position_str: A string of the form ``"x,z,y"`` where each token is a
            number, as produced by Physics-Lab-AR save files.

    Returns:
        The corresponding Position instance.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    try:
        x_str, z_str, y_str = position_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Position(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse position string `{position_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class Rotation:
    """An immutable 3-D rotation vector (x, y, z) in Euler angles."""

    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Rotation):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_rotation_str_in_plsav(self) -> str:
        """Return the rotation as a comma-separated string in plsav format (x,z,y)."""
        return f"{self.x},{self.z},{self.y}"


def construct_rotation_from_plsav_str(rotation_str: str) -> Rotation:
    """Construct a Rotation from a plsav-format string.

    Args:
        rotation_str: A string of the form ``"x,z,y"`` where each token is a
            number, as produced by Physics-Lab-AR save files.

    Returns:
        The corresponding Rotation instance.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    try:
        x_str, z_str, y_str = rotation_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Rotation(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse rotation string `{rotation_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class Velocity:
    """An immutable 3-D velocity vector (x, y, z)."""

    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Velocity):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_velocity_str_in_plsav(self) -> str:
        """Return the velocity as a comma-separated string in plsav format (x,z,y)."""
        return f"{self.x},{self.z},{self.y}"


def construct_velocity_from_plsav_str(velocity_str: str) -> Velocity:
    """Construct a Velocity from a plsav-format string.

    Args:
        velocity_str: A string of the form ``"x,z,y"`` where each token is a
            number, as produced by Physics-Lab-AR save files.

    Returns:
        The corresponding Velocity instance.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    try:
        x_str, z_str, y_str = velocity_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Velocity(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse velocity string `{velocity_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class AngularVelocity:
    """An immutable 3-D angular velocity vector (x, y, z)."""

    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AngularVelocity):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_angular_velocity_str_in_plsav(self) -> str:
        """Return the angular velocity as a comma-separated string in plsav format (x,z,y)."""
        return f"{self.x},{self.z},{self.y}"


def construct_angular_velocity_from_plsav_str(
    angular_velocity_str: str,
) -> AngularVelocity:
    """Construct an AngularVelocity from a plsav-format string.

    Args:
        angular_velocity_str: A string of the form ``"x,z,y"`` where each token
            is a number, as produced by Physics-Lab-AR save files.

    Returns:
        The corresponding AngularVelocity instance.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    try:
        x_str, z_str, y_str = angular_velocity_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return AngularVelocity(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse angular velocity string `{angular_velocity_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )


class Acceleration:
    """An immutable 3-D acceleration vector (x, y, z)."""

    x: num_type
    y: num_type
    z: num_type

    def __init__(self, x: num_type, y: num_type, z: num_type) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Parameter `x` must be of type `int | float`, but got value `{x}` of type `{type(x).__name__}`"
            )
        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Parameter `y` must be of type `int | float`, but got value `{y}` of type `{type(y).__name__}`"
            )
        if not isinstance(z, (int, float)):
            raise TypeError(
                f"Parameter `z` must be of type `int | float`, but got value `{z}` of type `{type(z).__name__}`"
            )

        self.x: num_type = x
        self.y: num_type = y
        self.z: num_type = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Acceleration):
            return False

        return self.x == value.x and self.y == value.y and self.z == value.z

    def as_acceleration_str_in_plsav(self) -> str:
        """Return the acceleration as a comma-separated string in plsav format (x,z,y)."""
        return f"{self.x},{self.z},{self.y}"


def construct_acceleration_from_plsav_str(acceleration_str: str) -> Acceleration:
    """Construct an Acceleration from a plsav-format string.

    Args:
        acceleration_str: A string of the form ``"x,z,y"`` where each token is
            a number, as produced by Physics-Lab-AR save files.

    Returns:
        The corresponding Acceleration instance.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    try:
        x_str, z_str, y_str = acceleration_str.split(",")
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        return Acceleration(x, y, z)
    except Exception as e:
        raise ValueError(
            f"Failed to parse acceleration string `{acceleration_str}` in plsav format. Expected format: `x,z,y` where x, y, z are numbers. Error: {e}"
        )
