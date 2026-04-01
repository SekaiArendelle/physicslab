"""Custom exception types and error helpers for physicsLab."""

from ._typing import NoReturn

BUG_REPORT: str = (
    "please send a bug-report at "
    "https://github.com/SekaiArendelle/physicsLab/issues "
    "with your code, *.sav and traceback / coredump for Python"
)


class UnreachableError(Exception):
    """Raised when code that should never execute is reached."""

    def __init__(self) -> None: ...

    def __str__(self) -> str:
        """Return a human-readable description including a bug-report link."""
        return f"Unreachable touched, {BUG_REPORT}"


def unreachable() -> NoReturn:
    """Raise ``UnreachableError`` to signal that an unreachable code path was hit."""
    raise UnreachableError()


class InvalidWireError(Exception):
    """Raised when an invalid wire connection is attempted."""

    __msg: str

    def __init__(self, msg: str) -> None:
        self.__msg = msg

    def __str__(self) -> str:
        return self.__msg


class InvalidSavError(Exception):
    """Raised when a save archive file is invalid."""

    def __str__(self):
        return "The archive file is incorrect"


class ExperimentExistError(Exception):
    """Raised when creating an experiment that already exists."""

    def __str__(self):
        return "Duplicate name archives are forbidden"


class ExperimentNotExistError(Exception):
    """Raised when an experiment cannot be found."""

    def __init__(self, err_msg: str = "The experiment does not exist") -> None:
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg


class ExperimentTypeError(Exception):
    """The experiment type is incorrect"""

    __err_msg: str

    def __init__(self, err_msg: str) -> None:
        self.__err_msg = err_msg

    def __str__(self) -> str:
        return self.__err_msg


class ElementNotExistError(Exception):
    """Raised when a requested circuit or experiment element cannot be found."""

    def __init__(self, err_msg: str = "Can't find element") -> None:
        self.err_msg = err_msg

    def __str__(self) -> str:
        return self.err_msg


class ElementExistError(Exception):
    """Raised when a duplicate element is added to an experiment."""

    def __init__(self, err_msg: str) -> None:
        assert isinstance(err_msg, str)
        self.err_msg = err_msg

    def __str__(self) -> str:
        return self.err_msg


class ResponseFail(Exception):
    """The response successfully returned but the returned data from Quantum-Physics is invalid"""

    def __init__(self, err_code: int, err_msg: str):
        self.err_code: int = err_code
        self.err_msg: str = err_msg

    def __str__(self):
        return f"Physics-Lab-AR's server returns error code {self.err_code} : {self.err_msg}"


class MaxRetryError(Exception):
    """Raised when retry attempts exceed the configured limit."""

    def __init__(self, err_msg: str):
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg
