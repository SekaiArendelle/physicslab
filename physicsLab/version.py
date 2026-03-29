from typing import Tuple


class _Version:
    __major: int
    __minor: int
    __patch: int

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

        if major < 0 or minor < 0 or patch < 0:
            raise ValueError

    @property
    def major(self) -> int:
        return self.__major

    @major.setter
    def major(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"major version must be of type `int`, but got value {value} of type {type(value).__name__}"
            )
        self.__major = value

    @property
    def minor(self) -> int:
        return self.__minor

    @minor.setter
    def minor(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"minor version must be of type `int`, but got value {value} of type {type(value).__name__}"
            )
        self.__minor = value

    @property
    def patch(self) -> int:
        return self.__patch

    @patch.setter
    def patch(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"patch version must be of type `int`, but got value {value} of type {type(value).__name__}"
            )
        self.__patch = value

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def to_tuple(self) -> Tuple[int, int, int]:
        return self.major, self.minor, self.patch

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, _Version):
            return False

        return self.to_tuple() == value.to_tuple()

    def __ne__(self, value: object) -> bool:
        return self.to_tuple() != value

    def __gt__(self, value: object) -> bool:
        if not isinstance(value, _Version):
            return False

        return self.to_tuple() > value.to_tuple()

    def __ge__(self, value: object) -> bool:
        if not isinstance(value, _Version):
            return False

        return self.to_tuple() >= value.to_tuple()

    def __lt__(self, value: object) -> bool:
        if not isinstance(value, _Version):
            return False

        return self.to_tuple() < value.to_tuple()

    def __le__(self, value: object) -> bool:
        if not isinstance(value, _Version):
            return False

        return self.to_tuple() <= value.to_tuple()


__version__ = _Version(3, 0, 0)
