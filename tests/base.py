import os
from unittest import TestCase, IsolatedAsyncioTestCase
from physicsLab import *

class TestFail(Exception):
    def __init__(self, err_msg: str = "Test fail", no_pop: bool=False) -> None:
        self.err_msg: str = err_msg
        self.no_pop = no_pop

    def __str__(self) -> str:
        if not self.no_pop:
            get_current_experiment().close()
        return self.err_msg

# this is a temp user without any binding
user = web.token_login(
    token="tGTf8gbQBR9P0ZnWhSILjJ5oF6UOkVdm",
    auth_code="xJwcHC7oOnlSdzUTh9NDZ0t1Q32MjPyB",
)
