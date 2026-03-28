
"""physicsLab的异常系统
有2个主要的组成部分: 可恢复的异常, 不可恢复的错误

* 可恢复的异常: 基于Python的Exception自定义的一系列错误类

* 不可恢复的错误:
    当某些错误发生的时候, physicsLab认为程序抽象机已经崩溃, 无法继续运行
    也就是说, 当该错误发生时, 仅表明程序出现了bug, 因此坚决不给用户捕获异常的可能
    因此一旦这些错误发生, physicsLab会调用os.abort来终止程序, 而不是抛出一个异常
    被视为 不可恢复的错误 的有:
    * assertion_error: 断言错误, physicsLab认为其为不可恢复的错误, 因此请不要使用 AssertionError
"""

import os
import sys
import threading

from ._typing import NoReturn
from physicsLab import _unwind
from physicsLab import _colorUtils
from physicsLab._typing import Optional

BUG_REPORT: str = (
    "please send a bug-report at "
    "https://github.com/SekaiArendelle/physicsLab/issues "
    "with your code, *.sav and traceback / coredump for Python"
)


def _unrecoverable_error(err_type: str, msg: Optional[str]) -> NoReturn:
    """不可恢复的错误, 表明程序抽象机已崩溃
    会打印的错误信息并退出程序
    """
    _colorUtils.cprint(_colorUtils.Red(err_type), end="", file=sys.stderr)
    if msg is None:
        print("\n", file=sys.stderr)
    else:
        _colorUtils.cprint(": ", _colorUtils.Red(msg), file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()
    os.abort()


_unrecoverable_error_lock = threading.Lock()


def assertion_error(msg: str) -> NoReturn:
    """断言错误, physicsLab认为其为不可恢复的错误"""
    _unrecoverable_error_lock.acquire()
    _unwind.print_stack(full=True)
    _unrecoverable_error("AssertionError", msg)


def assert_true(
    condition: bool,
    msg: str = BUG_REPORT,
) -> None:
    if not condition:
        assertion_error(msg)


def unreachable() -> NoReturn:
    assertion_error(f"Unreachable touched, {BUG_REPORT}")


class InvalidWireError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidSavError(Exception):
    """存档文件错误"""

    def __str__(self):
        return "The archive file is incorrect"


class ExperimentOpenedError(Exception):
    """已打开实验"""

    def __str__(self):
        return "The experiment has been opened"


class ExperimentClosedError(Exception):
    """未打开实验"""

    def __str__(self):
        return "The experiment has been closed"


# TODO 强化报错信息：将实验的具体信息也打印出来
class ExperimentExistError(Exception):
    """实验已存在"""

    def __str__(self):
        return "Duplicate name archives are forbidden"


class ExperimentNotExistError(Exception):
    """实验不存在"""

    def __init__(self, err_msg: str = "The experiment does not exist") -> None:
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg


class ExperimentHasCrtError(Exception):
    """实验已创建"""

    def __str__(self):
        return "The experiment has been created"


class ExperimentHasNotCrtError(Exception):
    """实验未创建"""

    def __str__(self):
        return "The experiment has not been created"


class ExperimentTypeError(Exception):
    """打开的实验与调用的元件不符"""

    def __init__(
        self,
        err_msg: str = "The type of experiment does not match the element",
    ) -> None:
        self.err_msg = err_msg

    def __str__(self) -> str:
        return self.err_msg


# 用于get_Element 获取元件引用失败
class ElementNotFound(Exception):
    def __init__(self, err_msg: str = "Can't find element") -> None:
        self.err_msg = err_msg

    def __str__(self) -> str:
        return self.err_msg


class ExperimentError(Exception):
    def __init__(self, string: str = "") -> None:
        self.err_msg: str = string

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
    """重试次数过多"""

    def __init__(self, err_msg: str):
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg
