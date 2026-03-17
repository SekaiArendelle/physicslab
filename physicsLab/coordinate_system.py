from ._typing import num_type

class Position:
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
        if isinstance(value, Position):
            return self.x == value.x and self.y == value.y and self.z == value.z
        elif isinstance(value, tuple) and len(value) == 3:
            return self.x == value[0] and self.y == value[1] and self.z == value[2]
        else:
            return False

    def as_postion_str_in_plsav(self) -> str:
        return f"{self.x},{self.z},{self.y}"
