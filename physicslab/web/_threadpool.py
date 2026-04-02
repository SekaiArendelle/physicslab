"""Before Python 3.14, ``Thread.join`` on Windows may block exception propagation.
    https://www.bilibili.com/video/BV1au411q7LN/?spm_id_from=333.999.0.0

Because of that behavior, this module provides a lightweight custom thread pool
instead of using ``ThreadPoolExecutor`` directly.
"""

import queue
import platform
from threading import Thread, Condition
from enum import Enum, unique
from physicslab import errors
from physicslab._typing import List, Callable, Self, Any, Optional, Union, Type


class CanceledError(Exception):
    """Task have been canceled"""

    def __repr__(self) -> str:
        return "Task have been canceled"


class _EndOfQueue:
    def __new__(cls):
        return _EndOfQueue


@unique
class _Status(Enum):
    """task's status"""

    wait = 0
    running = 1
    done = 2
    cancelled = 3


class _StatusEvent:
    if platform.system() == "Windows":  # and sys.version_info < (3, 14):

        def __init__(self) -> None:
            self._status: _Status = _Status.wait

        def wait(self) -> None:
            """Execute the wait routine."""
            while self._status != _Status.done:
                pass

        def set_as_done(self) -> None:
            """Set as done."""
            self._status = _Status.done

    else:

        def __init__(self) -> None:
            self._condition = Condition()
            self._status: _Status = _Status.wait

        def wait(self) -> None:
            """Execute the wait routine."""
            with self._condition:
                if self._status != _Status.done:
                    self._condition.wait()

        def set_as_done(self) -> None:
            """Set as done."""
            with self._condition:
                self._status = _Status.done
                self._condition.notify_all()

    def set_as_running(self) -> None:
        """Set as running."""
        self._status = _Status.running

    def set_as_cancelled(self) -> None:
        """Set as cancelled."""
        self._status = _Status.cancelled

    def get_status(self) -> _Status:
        """Get status."""
        return self._status


class _Task:
    def __init__(self, func: Callable, args: tuple, kwargs: dict) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.res: Any = None
        self.exception: Optional[Exception] = None
        self.status_event: _StatusEvent = _StatusEvent()

    def has_result(self) -> bool:
        """Check whether the instance has result."""
        return self.status_event.get_status() == _Status.done

    def result(self):
        """Execute the result routine."""
        if self.status_event.get_status() == _Status.cancelled:
            raise CanceledError
        self.status_event.wait()

        if self.exception is not None:
            raise self.exception
        else:
            return self.res


class ThreadPool:
    """Represent a thread pool component."""

    def __init__(self, *, max_workers: int) -> None:
        """Initialize the thread pool.

        Args:
            max_workers: Maximum number of worker threads.
        """
        if not isinstance(max_workers, int):
            raise TypeError(
                f"Parameter `max_workers` must be of type `int`, but got value `{max_workers}` of type `{type(max_workers).__name__}`"
            )
        if max_workers <= 0:
            raise ValueError

        self.max_workers = max_workers
        self.task_queue: queue.SimpleQueue[Union[_Task, Type[_EndOfQueue]]] = (
            queue.SimpleQueue()
        )
        self.threads: List[Thread] = []

    def _office(self) -> None:
        """workers work here"""
        while True:
            try:
                _task = self.task_queue.get_nowait()
            except queue.Empty:
                continue
            if _task is _EndOfQueue:
                self.submit_end()
                return
            assert isinstance(_task, _Task)
            _task.status_event.set_as_running()
            try:
                _task.res = _task.func(*_task.args, **_task.kwargs)
            except Exception as e:
                _task.exception = e
            finally:
                _task.status_event.set_as_done()

    def submit(self, func, *args, **kwargs) -> _Task:
        """submit a task
        @param func: function to be submitted
        """
        if not callable(func):
            raise TypeError(
                f"Parameter func must be of `callable`, but got value {func} of type `{type(func)}`"
            )

        task = _Task(func, args, kwargs)
        self.task_queue.put_nowait(task)
        if len(self.threads) < self.max_workers:
            worker = Thread(target=self._office, daemon=True)
            self.threads.append(worker)
            worker.start()

        return task

    def submit_end(self) -> None:
        """users should call this method after all tasks are submitted"""
        self.task_queue.put_nowait(_EndOfQueue)

    def cancel_all_pending_tasks(self) -> None:
        """cancel all pending tasks"""
        while True:
            try:
                task = self.task_queue.get_nowait()
            except queue.Empty:
                break
            if task is _EndOfQueue:
                break

            assert isinstance(task, _Task)

            task.status_event.set_as_cancelled()

        self.submit_end()

    def wait(self) -> None:
        """blocking until all tasks are done"""
        for thread in self.threads:
            if platform.system() == "Windows":  # and sys.version_info < (3, 14):
                while thread.is_alive():
                    thread.join(timeout=2)
            else:
                thread.join()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.wait()
