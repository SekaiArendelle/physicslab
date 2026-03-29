"""Print colored text in the terminal.

This module is one of the lowest-level utilities in ``physicsLab`` and should
not depend on other project modules (including ``errors.py``).

Usage:
    >>> from physicsLab._colorUtils import *
    >>> cprint(Red("test"))  # Prints red text
    # Supports variadic arguments and mixed colored/plain objects.
    # Unlike ``print``, ``sep`` is intentionally not supported.
    >>> cprint(Green("test"), "test", Yellow("test"), 1111, 3.14)
    >>> cprint(Blue("test"))  # Other supported colors:
    >>> cprint(Magenta("test"))
    >>> cprint(Cyan("test"))
    >>> cprint(White("test"))
    >>> cprint(Black("test"))
    >>> cprint(Red("test"), file=sys.stderr)  # Print to stderr
    >>> cprint(Red("test"), end='')  # Supports custom ``end`` like ``print``
    # Use built-in ``print`` if you want plain text output only.
    >>> print(Green("test"), "test", Yellow("test"))  # No color in output
"""

import platform
from physicsLab._typing import final

# Set terminal encoding to UTF-8.
import io
import sys

if platform.system() in ("Windows", "Linux"):
    # Fuck ANSI, fuck Windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Windows 11 supports ANSI escape sequences by default; use Win32 API only on older versions.
_USE_WIN32_COLOR_API = platform.system() == "Windows" and (
    sys.getwindowsversion().major,
    sys.getwindowsversion().minor,
    sys.getwindowsversion().build,
) < (10, 0, 22000)

if _USE_WIN32_COLOR_API:
    import ctypes
    from ctypes import wintypes

    class _CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes._COORD),
            ("dwCursorPosition", wintypes._COORD),
            ("wAttributes", wintypes.WORD),
            ("srWindow", wintypes.SMALL_RECT),
            ("dwMaximumWindowSize", wintypes._COORD),
        ]

    kernel32 = ctypes.windll.kernel32

    _GetStdHandle = ctypes.windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [
        wintypes.DWORD,
    ]
    _GetStdHandle.restype = wintypes.HANDLE

    _GetConsoleScreenBufferInfo = ctypes.windll.kernel32.GetConsoleScreenBufferInfo
    _GetConsoleScreenBufferInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_CONSOLE_SCREEN_BUFFER_INFO),
    ]
    _GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    _SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
    _SetConsoleTextAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD,
    ]
    _SetConsoleTextAttribute.restype = wintypes.BOOL

    _stdout_handle = _GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    _stderr_handle = _GetStdHandle(-12)  # STD_ERROR_HANDLE


class _Color:
    fore: int

    def __init__(self, msg: str) -> None:
        if type(self) is _Color:
            raise NotImplementedError("_Color class can't be instantiated directly")
        if not isinstance(msg, str):
            raise TypeError(
                f"Parameter msg must be of type `str`, but got value `{msg}` of type {type(msg).__name__}"
            )

        self.msg = msg

    def __repr__(self) -> str:
        return self.msg

    @final
    def cprint(self, file):
        if _USE_WIN32_COLOR_API:
            import ctypes

            # Temporarily change terminal text attributes.
            csbi = _CONSOLE_SCREEN_BUFFER_INFO()
            if file is sys.stdout:
                _GetConsoleScreenBufferInfo(_stdout_handle, ctypes.byref(csbi))
                _SetConsoleTextAttribute(_stdout_handle, self.fore)
            elif file is sys.stderr:
                _GetConsoleScreenBufferInfo(_stderr_handle, ctypes.byref(csbi))
                _SetConsoleTextAttribute(_stderr_handle, self.fore)
            else:
                assert False
            print(self.msg, flush=True, end="", file=file)
            # Restore terminal text attributes.
            if file is sys.stdout:
                _SetConsoleTextAttribute(_stdout_handle, csbi.wAttributes)
            elif file is sys.stderr:
                _SetConsoleTextAttribute(_stderr_handle, csbi.wAttributes)
            else:
                assert False
        else:
            print(f"\033[{self.fore}m{self.msg}\033[0m", end="", file=file)


class Black(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 0
    else:
        fore = 30


class Red(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 4
    else:
        fore = 31


class Green(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 2
    else:
        fore = 32


class Yellow(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 6
    else:
        fore = 33


class Blue(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 1
    else:
        fore = 34


class Magenta(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 5
    else:
        fore = 35


class Cyan(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 3
    else:
        fore = 36


class White(_Color):
    if _USE_WIN32_COLOR_API:
        fore = 7
    else:
        fore = 37


def cprint(*args, end="\n", file=sys.stdout) -> None:
    # Flush before printing so buffered content is not affected by color changes on Windows.
    # e.g.
    # print("test")
    # _colorUtils.cprint("test")
    if file == sys.stdout:
        sys.stdout.flush()
    elif file == sys.stderr:
        sys.stderr.flush()
    else:
        assert False, "unreachable touched"

    for arg in args:
        if isinstance(arg, _Color):
            arg.cprint(file=file)
        else:
            print(arg, end="", file=file)
    print(end, end="", file=file)
    # Flush again to ensure all terminal output is written.
    # e.g.
    # cprint(Green("test"), file=sys.stderr)
    # cprint(Red("ttt"), file=sys.stdout)
    if file == sys.stdout:
        sys.stdout.flush()
    elif file == sys.stderr:
        sys.stderr.flush()
    else:
        assert False, "unreachable touched"
