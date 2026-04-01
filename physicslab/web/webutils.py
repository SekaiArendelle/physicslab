"""Convenient iterators for traversing Physics-Lab-AR community data."""

import time
import urllib3
import requests

from .api import User, get_avatar
from ._threadpool import ThreadPool, _Task
from physicslab import errors
from physicslab.enums import Category, Tag, GetUserMode
from physicslab._typing import Optional, num_type, Callable, List

_DEFAULT_MAX_WORKERS: int = 4


def _run_task(max_retry: Optional[int], func: Callable, *args, **kwargs):
    """Run ``func`` until success or until retry policy is exhausted.

    Args:
        max_retry: Maximum retry count (>= 0). ``None`` means unlimited retries.
    """
    assert (max_retry is None or max_retry >= 0) and callable(func)

    if max_retry is None:
        while True:
            try:
                return func(*args, **kwargs)
            except (
                TimeoutError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
            ):
                continue
    else:
        if max_retry == 0:
            return func(*args, **kwargs)
        for _ in range(max_retry + 1):
            try:
                return func(*args, **kwargs)
            except (
                TimeoutError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
            ):
                continue
        raise errors.MaxRetryError("max retry reached")


class NotificationsIter:
    """Iterate messages from the notifications page."""

    TAKE_AMOUNT: int = -101

    def __init__(
        self,
        user: User,
        category_id: int,
        start_skip: int = 0,
        max_retry: Optional[int] = 0,
        max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        """Initialize a notifications iterator.

        Args:
            user: Authenticated user used to fetch data.
            category_id: Message category:
                0: all, 1: system mail, 2: follows/fans, 3: comments/replies,
                4: content notifications, 5: moderation records.
            start_skip: Initial message offset. Defaults to 0.
            max_retry: Maximum retries per request. Defaults to 0 (no retry).
                ``None`` means unlimited retries (not recommended).
            max_workers: Maximum worker thread count.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(category_id, int):
            raise TypeError(
                f"Parameter `category_id` must be of type `int`, but got value `{category_id}` of type `{type(category_id).__name__}`"
            )
        if not isinstance(start_skip, int):
            raise TypeError(
                f"Parameter `start_skip` must be of type `int`, but got value `{start_skip}` of type `{type(start_skip).__name__}`"
            )
        if not isinstance(max_retry, (int, type(None))):
            raise TypeError(
                f"Parameter `max_retry` must be of type `int` or `None`, but got value `{max_retry}` of type `{type(max_retry).__name__}`"
            )
        if not isinstance(max_workers, int):
            raise TypeError(
                f"Parameter `max_workers` must be of type `int`, but got value `{max_workers}` of type `{type(max_workers).__name__}`"
            )
        if (
            category_id not in range(6)
            or not isinstance(max_retry, type(None))
            and max_retry < 0
            or start_skip < 0
            or max_workers <= 0
        ):
            raise ValueError

        self.user = user
        self.category_id = category_id
        self.start_skip = start_skip
        self.max_retry = max_retry
        self.max_workers = max_workers

    def __iter__(self):
        tasks: List[_Task] = []
        with ThreadPool(max_workers=self.max_workers) as executor:
            while True:
                # Avoid too many queued tasks so shutdown can complete quickly.
                if len(tasks) < 2500:
                    tasks.append(
                        executor.submit(
                            _run_task,
                            self.max_retry,
                            self.user.get_messages,
                            category_id=self.category_id,
                            skip=self.start_skip,
                            take=self.TAKE_AMOUNT,
                            no_templates=True,
                        )
                    )
                    self.start_skip += abs(self.TAKE_AMOUNT)

                if tasks[0].has_result():
                    msgs = tasks.pop(0).result()["Data"]["Messages"]
                    yield from msgs
                    if len(msgs) < abs(self.TAKE_AMOUNT):
                        executor.cancel_all_pending_tasks()
                        break


class ExperimentsIter:
    """Iterate experiments from the community feed."""

    # Uses current backend behavior to request more items per page.
    TAKE_AMOUNT: int = -101

    def __init__(
        self,
        user: User,
        category: Category,
        start_skip: int = 0,
        from_skip: Optional[str] = None,
        tags: Optional[List[Tag]] = None,
        exclude_tags: Optional[List[Tag]] = None,
        languages: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        max_retry: Optional[int] = 0,
        max_workers: int = _DEFAULT_MAX_WORKERS,
        exclude_languages: Optional[List[str]] = None,
    ) -> None:
        """Initialize an experiments iterator.

        Args:
            user: Authenticated user used to fetch data.
            tags: Tags to include.
            exclude_tags: Tags to exclude.
            category: Experiment category.
            languages: Languages to include.
            user_id: Filter by creator user ID.
            max_retry: Maximum retries per request.
            max_workers: Maximum worker thread count.
        """
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be of type `Category`, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(tags, (list, type(None))):
            raise TypeError(
                f"Parameter `tags` must be of type `Optional[list[Tag]]`, but got value `{tags}` of type `{type(tags).__name__}`"
            )
        if tags is not None and not all(isinstance(tag, Tag) for tag in tags):
            raise TypeError(
                f"Parameter `tags` must be of type `Optional[list[Tag]]`, but got value `{tags}` of type `{type(tags).__name__}`"
            )
        if not isinstance(exclude_tags, (list, type(None))):
            raise TypeError(
                f"Parameter `exclude_tags` must be of type `Optional[list[Tag]]`, but got value `{exclude_tags}` of type `{type(exclude_tags).__name__}`"
            )
        if exclude_tags is not None and not all(
            isinstance(tag, Tag) for tag in exclude_tags
        ):
            raise TypeError(
                f"Parameter `exclude_tags` must be of type `Optional[list[Tag]]`, but got value `{exclude_tags}` of type `{type(exclude_tags).__name__}`"
            )
        if not isinstance(languages, (list, type(None))):
            raise TypeError(
                f"Parameter `languages` must be of type `Optional[list[str]]`, but got value `{languages}` of type `{type(languages).__name__}`"
            )
        if languages is not None and not all(
            isinstance(language, str) for language in languages
        ):
            raise TypeError(
                f"Parameter `languages` must be of type `Optional[list[str]]`, but got value `{languages}` of type `{type(languages).__name__}`"
            )
        if not isinstance(user_id, (str, type(None))):
            raise TypeError(
                f"Parameter `user_id` must be of type `Optional[str]`, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        if not isinstance(max_retry, (int, type(None))):
            raise TypeError(
                f"Parameter `max_retry` must be of type `Optional[int]`, but got value `{max_retry}` of type `{type(max_retry).__name__}`"
            )
        if not isinstance(start_skip, int):
            raise TypeError(
                f"Parameter `start_skip` must be of type `int`, but got value `{start_skip}` of type `{type(start_skip).__name__}`"
            )
        if not isinstance(from_skip, (str, type(None))):
            raise TypeError(
                f"Parameter `from_skip` must be of type `Optional[str]`, but got value `{from_skip}` of type `{type(from_skip).__name__}`"
            )
        if not isinstance(max_workers, int):
            raise TypeError(
                f"Parameter `max_workers` must be of type `int`, but got value `{max_workers}` of type `{type(max_workers).__name__}`"
            )
        if not isinstance(exclude_languages, type(None)) and (
            not isinstance(exclude_languages, list)
            or not all(isinstance(tag, str) for tag in exclude_languages)
        ):
            raise TypeError(
                f"Parameter `exclude_languages` must be of type `Optional[List[str]]`, but got value `{exclude_languages}` of type `{type(exclude_languages).__name__}`"
            )
        if start_skip < 0 or max_workers <= 0:
            raise ValueError

        self.user = user
        self.tags = tags
        self.exclude_tags = exclude_tags
        self.category = category
        self.languages = languages
        self.user_id = user_id
        self.max_retry = max_retry
        self.start_skip = start_skip
        self.from_skip = from_skip
        self.max_workers = max_workers
        self.exclude_languages = exclude_languages

    def __iter__(self):
        while True:
            msgs = _run_task(
                self.max_retry,
                self.user.query_experiments,
                category=self.category,
                tags=self.tags,
                exclude_tags=self.exclude_tags,
                languages=self.languages,
                exclude_languages=self.exclude_languages,
                user_id=self.user_id,
                take=self.TAKE_AMOUNT,
                skip=self.start_skip,
                from_skip=self.from_skip,
            )["Data"]["$values"]
            self.start_skip += abs(self.TAKE_AMOUNT)
            self.from_skip = msgs[-1]["ID"]
            yield from msgs
            if len(msgs) < abs(self.TAKE_AMOUNT):
                break


class BannedMsgIter:
    """Iterate ban records in a time range, optionally for one user."""

    banned_template = {
        "ID": "5d57f3c139523f0f640c2211",
        "Identifier": "User-Banned-Record",
    }

    def __init__(
        self,
        user: User,
        start_skip: int = 0,
        start_time: Optional[num_type] = None,
        end_time: Optional[num_type] = None,
        user_id: Optional[str] = None,
        max_retry: Optional[int] = 0,
        get_banned_template: bool = False,
        max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        """Initialize a ban-record iterator.

        Args:
            user: Authenticated user used to query data.
            user_id: Target user ID. ``None`` means all users.
            start_time: Start timestamp in seconds. ``None`` means no lower bound.
            end_time: End timestamp in seconds. ``None`` means now.
            max_retry: Maximum retries per request (>= 0). ``None`` means unlimited.
            get_banned_template: Whether to fetch the latest ban template from server.
                If ``False``, use the built-in template.
            max_workers: Maximum worker thread count.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(start_skip, int):
            raise TypeError(
                f"Parameter `start_skip` must be of type `int`, but got value `{start_skip}` of type `{type(start_skip).__name__}`"
            )
        if not isinstance(start_time, (int, float, type(None))):
            raise TypeError(
                f"Parameter `start_time` must be of type `Optional[num_type]`, but got value `{start_time}` of type `{type(start_time).__name__}`"
            )
        if not isinstance(end_time, (int, float, type(None))):
            raise TypeError(
                f"Parameter `end_time` must be of type `Optional[num_type]`, but got value `{end_time}` of type `{type(end_time).__name__}`"
            )
        if not isinstance(user_id, (str, type(None))):
            raise TypeError(
                f"Parameter `user_id` must be of type `Optional[str]`, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        if not isinstance(max_retry, (int, type(None))):
            raise TypeError(
                f"Parameter `max_retry` must be of type `Optional[int]`, but got value `{max_retry}` of type `{type(max_retry).__name__}`"
            )
        if not isinstance(get_banned_template, bool):
            raise TypeError(
                f"Parameter `get_banned_template` must be of type `bool`, but got value `{get_banned_template}` of type `{type(get_banned_template).__name__}`"
            )
        if not isinstance(max_workers, int):
            raise TypeError(
                f"Parameter `max_workers` must be of type `int`, but got value `{max_workers}` of type `{type(max_workers).__name__}`"
            )
        if max_workers <= 0:
            raise ValueError("Parameter `max_workers` must be greater than 0")

        if get_banned_template:
            response = user.get_messages(5, take=1, no_templates=False)["Data"]
            for template in response["Templates"]:
                if template["Identifier"] == self.banned_template["Identifier"]:
                    self.banned_template = template
                    break

        if end_time is None:
            self.end_time = time.time()
        else:
            self.end_time = end_time

        if (
            start_time is not None
            and start_time < self.end_time
            and start_time < 0
            or start_skip < 0
        ):
            raise ValueError

        self.user = user
        self.start_skip = start_skip
        self.start_time = start_time
        self.user_id = user_id
        self.max_retry = max_retry
        self.max_workers = max_workers

    def __iter__(self):
        for msg in NotificationsIter(
            self.user,
            category_id=5,
            start_skip=self.start_skip,
            max_retry=self.max_retry,
            max_workers=self.max_workers,
        ):
            if (
                msg["TemplateID"] == self.banned_template["ID"]
                and (
                    self.start_time is None
                    or self.start_time * 1000 <= msg["Timestamp"]
                )
                and msg["Timestamp"] < self.end_time * 1000
                and (self.user_id is None or self.user_id in msg["Users"])
            ):
                yield msg
            if (
                self.start_time is not None
                and msg["Timestamp"] < self.start_time * 1000
            ):
                return


class CommentsIter:
    """Iterate comments for a user, experiment, or discussion."""

    def __init__(
        self,
        user: User,
        content_id: str,
        category: str = "User",
        start_time: int = 0,
        max_retry: Optional[int] = 0,
    ) -> None:
        """Initialize a comments iterator.

        Args:
            user: Authenticated user used to fetch data.
            content_id: Target user ID or experiment/discussion ID.
            category: One of ``"User"``, ``"Experiment"``, or ``"Discussion"``.
            start_time: Start timestamp in seconds. Iteration proceeds from newer to older.
            max_retry: Retry count for transient request failures.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(content_id, str):
            raise TypeError(
                f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        if not isinstance(category, str):
            raise TypeError(
                f"Parameter `category` must be of type `str`, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(start_time, (int, float)):
            raise TypeError(
                f"Parameter `start_time` must be of type `int | float`, but got value `{start_time}` of type `{type(start_time).__name__}`"
            )
        if not isinstance(max_retry, (int, type(None))):
            raise TypeError(
                f"Parameter `max_retry` must be of type `Optional[int]`, but got value `{max_retry}` of type `{type(max_retry).__name__}`"
            )
        if category not in ("User", "Experiment", "Discussion"):
            raise ValueError(
                "Parameter `category` must be one of 'User', 'Experiment' or 'Discussion'"
            )
        if category == "User" and not user.is_binded:
            raise PermissionError("user must be binded")

        self.user = user
        self.content_id = content_id
        self.category = category
        self.start_time = int(start_time * 1000)
        self.max_retry = max_retry

    def __iter__(self):
        TAKE_AMOUNT: int = 20
        while True:
            comments = _run_task(
                self.max_retry,
                self.user.get_comments,
                self.content_id,
                self.category,
                skip=self.start_time,
                take=TAKE_AMOUNT,
            )["Data"]["Comments"]

            if len(comments) == 0:
                return
            self.start_time = comments[-1]["Timestamp"]

            yield from comments


class WarnedMsgIter:
    """Iterate warning messages for a user within a time range."""

    def __init__(
        self,
        user: User,
        user_id: str,
        start_time: num_type,
        end_time: Optional[num_type] = None,
        maybe_warned_message_callback: Optional[Callable] = None,
    ) -> None:
        """Initialize a warning-message iterator.

        Args:
            user: Authenticated user used to fetch data.
            user_id: Target user ID. Querying all users is not supported.
            start_time: Start timestamp in seconds.
            end_time: End timestamp in seconds. ``None`` means now.
            maybe_warned_message_callback: Callback for possible warning messages.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(user_id, str):
            raise TypeError(
                f"Parameter `user_id` must be of type `str`, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        if not isinstance(start_time, (int, float)):
            raise TypeError(
                f"Parameter `start_time` must be of type `float`, but got value `{start_time}` of type `{type(start_time).__name__}`"
            )
        if not isinstance(end_time, (int, float, type(None))):
            raise TypeError(
                f"Parameter `end_time` must be of type `Optional[int | float]`, but got value `{end_time}` of type `{type(end_time).__name__}`"
            )
        if maybe_warned_message_callback is not None and not callable(
            maybe_warned_message_callback
        ):
            raise TypeError(
                f"Parameter `maybe_warned_message_callback` must be of type `Optional[Callable]`, but got value `{maybe_warned_message_callback}` of type `{type(maybe_warned_message_callback).__name__}`"
            )
        if not user.is_binded:
            raise PermissionError("anonymous user cannot use this iter")

        if end_time is None:
            end_time = time.time()

        self.user = user
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.maybe_warned_message_callback = maybe_warned_message_callback

    def __iter__(self):
        for comment in CommentsIter(
            self.user, content_id=self.user_id, category="User"
        ):
            if comment["Timestamp"] < self.start_time * 1000:
                return

            if self.start_time * 1000 <= comment["Timestamp"] <= self.end_time * 1000:
                if (
                    comment["Flags"] is not None
                    and "Locked" in comment["Flags"]
                    and "Reminder" in comment["Flags"]
                ):
                    yield comment
                elif (
                    "警告" in comment["Content"]
                    and comment["Verification"]
                    in ("Volunteer", "Editor", "Emeritus", "Administrator")
                    and self.maybe_warned_message_callback is not None
                ):
                    self.maybe_warned_message_callback(comment)


class RelationsIter:
    """Iterate followers or followings for a user."""

    # Uses current backend behavior to request more items per page.
    TAKE_AMOUNT = -101

    def __init__(
        self,
        user: User,
        user_id: str,
        display_type: str = "Follower",
        max_retry: Optional[int] = 0,
        amount: Optional[int] = None,
        query: str = "",
        max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        """Initialize a relations iterator.

        Args:
            user: Authenticated user used to fetch data.
            user_id: Target user ID.
            display_type: ``"Follower"`` or ``"Following"``.
            max_retry: Maximum retries (>= 0). ``None`` means unlimited.
            amount: Number of relations to fetch. ``None`` queries automatically.
            max_workers: Maximum worker thread count.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(user_id, str):
            raise TypeError(
                f"Parameter `user_id` must be of type `str`, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        if not isinstance(display_type, str):
            raise TypeError(
                f"Parameter `display_type` must be of type `str`, but got value `{display_type}` of type `{type(display_type).__name__}`"
            )
        if not isinstance(max_retry, (int, type(None))):
            raise TypeError(
                f"Parameter `max_retry` must be of type `Optional[int]`, but got value `{max_retry}` of type `{type(max_retry).__name__}`"
            )
        if not isinstance(amount, (int, type(None))):
            raise TypeError(
                f"Parameter `amount` must be of type `Optional[int]`, but got value `{amount}` of type `{type(amount).__name__}`"
            )
        if display_type not in ("Follower", "Following"):
            raise ValueError(
                f"Parameter `display_type` must be one of ['Follower', 'Following'], but got value `{display_type} of type '{display_type}'"
            )
        if not isinstance(max_workers, int):
            raise TypeError(
                f"Parameter `max_workers` must be of type `int`, but got value `{max_workers}` of type `{type(max_workers).__name__}`"
            )
        if max_retry is not None and max_retry < 0 or max_workers <= 0:
            raise ValueError

        self.user = user
        self.user_id = user_id
        self.display_type = display_type
        self.max_retry = max_retry
        self.query = query
        if amount is None:
            if self.display_type == "Follower":
                self.amount = self.user.get_user(self.user_id, GetUserMode.by_id)[
                    "Data"
                ]["Statistic"]["FollowerCount"]
            elif self.display_type == "Following":
                self.amount = self.user.get_user(self.user_id, GetUserMode.by_id)[
                    "Data"
                ]["Statistic"]["FollowingCount"]
            else:
                errors.unreachable()
        else:
            self.amount = amount
        self.max_workers = max_workers

    def __iter__(self):
        with ThreadPool(max_workers=self.max_workers) as executor:
            tasks: List[_Task] = [
                executor.submit(
                    _run_task,
                    self.max_retry,
                    self.user.get_relations,
                    user_id=self.user_id,
                    display_type=self.display_type,
                    skip=_skip,
                    take=self.TAKE_AMOUNT,
                    query=self.query,
                )
                for _skip in range(0, self.amount + 1, abs(self.TAKE_AMOUNT))
            ]
            executor.submit_end()

            for task in tasks:
                yield from task.result()["Data"]["$values"]


class AvatarsIter:
    """Iterate avatar images for a user/content target."""

    def __init__(
        self,
        user: User,
        /,
        *,
        target_id: str,
        category: str,
        size_category: str = "full",
        max_retry: Optional[int] = 0,
        max_img_index: Optional[int] = None,
        max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        """Initialize an avatar iterator.

        Args:
            user: Authenticated user used to fetch data.
            target_id: Target user/content ID.
            category: One of ``"Experiment"``, ``"Discussion"``, or ``"User"``.
            size_category: One of ``"small.round"``, ``"thumbnail"``, or ``"full"``.
            max_retry: Maximum retries (>= 0). ``None`` means unlimited.
            max_img_index: Upper bound for image index. ``None`` queries automatically.
            max_workers: Maximum worker thread count.
        """
        if not isinstance(target_id, str):
            raise TypeError(
                f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
            )
        if not isinstance(category, str):
            raise TypeError(
                f"Parameter `category` must be of type `str`, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(size_category, str):
            raise TypeError(
                f"Parameter `size_category` must be of type `str`, but got value `{size_category}` of type `{type(size_category).__name__}`"
            )
        if not isinstance(user, User):
            raise TypeError(
                f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
            )
        if not isinstance(max_retry, (int, type(None))):
            raise TypeError(
                f"Parameter `max_retry` must be of type `Optional[int]`, but got value `{max_retry}` of type `{type(max_retry).__name__}`"
            )
        if not isinstance(max_img_index, (int, type(None))):
            raise TypeError(
                f"Parameter `max_img_index` must be of type `Optional[int]`, but got value `{max_img_index}` of type `{type(max_img_index).__name__}`"
            )
        if not isinstance(max_workers, int):
            raise TypeError(
                f"Parameter `max_workers` must be of type `int`, but got value `{max_workers}` of type `{type(max_workers).__name__}`"
            )
        if (
            category not in ("User", "Experiment", "Discussion")
            or size_category not in ("small.round", "thumbnail", "full")
            or max_img_index is not None
            and max_img_index < 0
            or max_workers <= 0
        ):
            raise ValueError

        if max_img_index is None:
            if category == "User":
                self.max_img_index = user.get_user(target_id, GetUserMode.by_id)[
                    "Data"
                ]["User"]["Avatar"]
                category = "users"
            elif category == "Experiment":
                self.max_img_index = user.get_summary(target_id, Category.Experiment)[
                    "Data"
                ]["Image"]
                category = "experiments"
            elif category == "Discussion":
                self.max_img_index = user.get_summary(target_id, Category.Discussion)[
                    "Data"
                ]["Image"]
                category = "experiments"
            else:
                errors.unreachable()
        else:
            self.max_img_index = max_img_index

        self.target_id = target_id
        self.category = category
        self.size_category = size_category
        self.user = user
        self.max_retry = max_retry
        self.max_workers = max_workers

    def __iter__(self):
        with ThreadPool(max_workers=self.max_workers) as executor:
            tasks: List[_Task] = [
                executor.submit(
                    _run_task,
                    self.max_retry,
                    get_avatar,
                    self.target_id,
                    index,
                    self.category,
                    self.size_category,
                )
                for index in range(self.max_img_index + 1)
            ]
            executor.submit_end()
            for task in tasks:
                try:
                    img = task.result()
                except IndexError:
                    continue
                else:
                    yield img
