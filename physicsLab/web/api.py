# -*- coding: utf-8 -*-
"""Wrapper for Physics-Lab-AR web API
Except for experiment upload API which is encapsulated in class Experiment's __upload
This file provides support for multi-threaded style API calls
"""

import os
import sys
import asyncio
import functools
import contextvars
import requests

from . import _request

from physicsLab import plAR
from physicsLab import enums
from physicsLab import errors
from physicsLab.enums import Tag, Category
from physicsLab._typing import Optional, List, TypedDict, Callable, Awaitable


async def _async_wrapper(func: Callable, *args, **kwargs):
    if sys.version_info < (3, 9):
        # copied from asyncio.to_thread
        loop = asyncio.get_running_loop()
        ctx = contextvars.copy_context()
        func_call = functools.partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(None, func_call)
    else:
        return await asyncio.to_thread(func, *args, **kwargs)


class _api_result(TypedDict):
    """Structure of Physics-Lab-AR API response

    Attributes:
        Token: Access token
        AuthCode: Authorization code
        Data: Actual returned data
    """

    Token: str
    AuthCode: Optional[str]
    Data: dict


def _check_response(
    response: requests.Response, err_callback: Optional[Callable] = None
) -> _api_result:
    """Check the returned response

    Args:
        response: requests response object
        err_callback: Custom error message for Physics-Lab-AR returned status,
                      requires status_code (captures status_code from Physics-Lab-AR response body), no return value

    Returns:
        _api_result: Physics-Lab-AR API response structure
    """
    errors.assert_true(err_callback is None or callable(err_callback))

    response.raise_for_status()

    response_json = response.json()
    status_code = response_json["Status"]

    if status_code == 200:
        return response_json
    if err_callback is not None:
        err_callback(status_code)
    raise errors.ResponseFail(
        response_json()["code"],
        f"Physics-Lab-AR's server returned error code {status_code}: {response_json['Message']}",
    )


def _check_response_json(response: dict) -> _api_result:
    status_code = response["Status"]

    if status_code == 200:
        return response
    raise errors.ResponseFail(
        response["code"],
        f"Physics-Lab-AR's server returned error code {status_code}: {response['Message']}",
    )


def get_start_page() -> _api_result:
    """Get homepage data

    Returns:
        _api_result: Physics-Lab-AR API response structure
    """
    response = requests.get("https://physics-api-cn.turtlesim.com/Users")

    return _check_response(response)


async def async_get_start_page() -> Awaitable[_api_result]:
    return await _async_wrapper(get_start_page)


def get_avatar(
    target_id: str,
    index: int,
    category: str,
    size_category: str,
    usehttps: bool = False,
) -> bytes:
    """Get avatar/experiment cover

    Args:
        target_id: User ID or experiment ID
        index: Index of historical image
        category: Must be "experiments" or "users"
        size_category: Must be "small.round", "thumbnail", or "full"
        usehttps: Whether to use HTTPS protocol, due to certificate and domain mismatch, certificate will not be verified if used

    Returns:
        bytes: Image data
    """
    if not isinstance(target_id, str):
        raise TypeError(
            f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
        )
    if not isinstance(index, int):
        raise TypeError(
            f"Parameter `index` must be of type `int`, but got value `{index}` of type `{type(index).__name__}`"
        )
    if not isinstance(category, str):
        raise TypeError(
            f"Parameter `category` must be of type `str`, but got value `{category}` of type `{type(category).__name__}`"
        )
    if not isinstance(size_category, str):
        raise TypeError(
            f"Parameter `size_category` must be of type `str`, but got value `{size_category}` of type `{type(size_category).__name__}`"
        )
    if not isinstance(usehttps, bool):
        raise TypeError(
            f"Parameter `usehttps` must be of type `bool`, but got value `{usehttps}` of type `{type(usehttps).__name__}`"
        )
    if category not in ("experiments", "users"):
        raise ValueError(
            f"Parameter `category` must be one of ['experiments', 'users'], but got value `{category} of type '{category}'`"
        )
    if size_category not in ("small.round", "thumbnail", "full"):
        raise ValueError(
            f"Parameter `size_category` must be one of ['small.round', 'thumbnail', 'full'], but got value `{size_category} of type '{size_category}'`"
        )

    if category == "users":
        category += "/avatars"
    elif category == "experiments":
        category += "/images"
    else:
        errors.unreachable()

    protocol = "https" if usehttps else "http"
    port = "443" if usehttps else "80"

    url = (
        f"{protocol}://physics-static-cn.turtlesim.com:{port}/{category}"
        f"/{target_id[0:4]}/{target_id[4:6]}/{target_id[6:8]}/{target_id[8:]}/{index}.jpg!{size_category}"
    )

    if usehttps:
        response = requests.get(url, verify=False)
    else:
        response = requests.get(url)

    if b"<Error>" in response.content:
        raise IndexError("avatar not found")
    return response.content


async def async_get_avatar(
    target_id: str, index: int, category: str, size_category: str
) -> Awaitable[_api_result]:
    return await _async_wrapper(get_avatar, target_id, index, category, size_category)


class User:
    """This class only provides blocking API"""

    token: Optional[str]
    auth_code: str
    # True: Account bound; False: Account not bound, anonymous login
    is_binded: bool
    # Hardware fingerprint
    device_token: Optional[str]
    # Account ID
    user_id: str
    # Nickname
    nickname: Optional[str]
    # Signature
    signature: Optional[str]
    # Gold coin amount
    gold: int
    # User level
    level: int
    # Avatar index
    avatar: int
    avatar_region: int
    decoration: int
    # Stores all reward information related to daily activities (such as ActivityID)
    statistic: dict

    def __init__(
        self,
        token: Optional[str],
        auth_code: str,
        is_binded: bool,
        device_token: Optional[str],
        user_id: str,
        nickname: Optional[str],
        signature: Optional[str],
        gold: int,
        level: int,
        avatar: int,
        avatar_region: int,
        decoration: int,
        verification,
        statistic: dict,
        domain: str = "physics-api-cn.turtlesim.com",
    ) -> None:
        """Data initialization only"""
        if not isinstance(token, (str, type(None))):
            raise TypeError(
                f"Parameter `token` must be of type `str`, but got value `{token}` of type `{type(token).__name__}`"
            )
        if not isinstance(auth_code, str):
            raise TypeError(
                f"Parameter `auth_code` must be of type `str`, but got value `{auth_code}` of type `{type(auth_code).__name__}`"
            )
        if not isinstance(is_binded, bool):
            raise TypeError(
                f"Parameter `is_binded` must be of type `bool`, but got value `{is_binded}` of type `{type(is_binded).__name__}`"
            )
        if not isinstance(device_token, (str, type(None))):
            raise TypeError(
                f"Parameter `device_token` must be of type `str`, but got value `{device_token}` of type `{type(device_token).__name__}`"
            )
        if not isinstance(user_id, str):
            raise TypeError(
                f"Parameter `user_id` must be of type `str`, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        if not isinstance(nickname, (str, type(None))):
            raise TypeError(
                f"Parameter `nickname` must be of type `str` or None, but got value `{nickname}` of type `{type(nickname).__name__}`"
            )
        if not isinstance(signature, (str, type(None))):
            raise TypeError(
                f"Parameter `signature` must be of type `str` or None, but got value `{signature}` of type `{type(signature).__name__}`"
            )
        if not isinstance(gold, int):
            raise TypeError(
                f"Parameter `gold` must be of type `int`, but got value `{gold}` of type `{type(gold).__name__}`"
            )
        if not isinstance(level, int):
            raise TypeError(
                f"Parameter `level` must be of type `int`, but got value `{level}` of type `{type(level).__name__}`"
            )
        if not isinstance(avatar, int):
            raise TypeError(
                f"Parameter `avatar` must be of type `int`, but got value `{avatar}` of type `{type(avatar).__name__}`"
            )
        if not isinstance(avatar_region, int):
            raise TypeError(
                f"Parameter `avatar_region` must be of type `int`, but got value `{avatar_region}` of type `{type(avatar_region).__name__}`"
            )
        if not isinstance(decoration, int):
            raise TypeError(
                f"Parameter `decoration` must be of type `int`, but got value `{decoration}` of type `{type(decoration).__name__}`"
            )
        if not isinstance(statistic, dict):
            raise TypeError(
                f"Parameter `statistic` must be of type `dict`, but got value `{statistic}` of type `{type(statistic).__name__}`"
            )
        if not isinstance(domain, str):
            raise TypeError(
                f"Parameter `domain` must be of type `str`, but got value `{domain}` of type `{type(domain).__name__}`"
            )

        # TODO Use assert_true to check types
        assert auth_code is not None, errors.BUG_REPORT
        self.token: Optional[str] = token
        self.auth_code: str = auth_code
        # True: Account bound; False: Account not bound, anonymous login
        self.is_binded: bool = is_binded
        self.device_token: Optional[str] = device_token
        self.user_id: str = user_id
        self.nickname: Optional[str] = nickname
        self.signature: Optional[str] = signature
        self.gold: int = gold
        self.level: int = level
        self.avatar: int = avatar
        self.avatar_region: int = avatar_region
        self.decoration: int = decoration
        self.verification = verification
        # Stores all reward information related to daily activities (such as ActivityID)
        self.statistic: dict = statistic
        self.domain: str = domain

    def get_library(self) -> _api_result:
        """Get community works list

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/GetLibrary",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "Identifier": "Discussions",
                "Language": "Chinese",
            },
        )

        return _check_response_json(response)

    async def async_get_library(self) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_library)

    def query_experiments(
        self,
        category: Category,
        tags: Optional[List[Tag]] = None,
        exclude_tags: Optional[List[Tag]] = None,
        languages: Optional[List[str]] = None,
        exclude_languages: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        take: int = 20,
        skip: int = 0,
        from_skip: Optional[str] = None,
    ) -> _api_result:
        """Query experiments

        Args:
            category: Experiment area or black hole area
            tags: Search for experiments with corresponding Physics-Lab-AR experiment tags in the list
            exclude_tags: All experiments except those with tags in the list will be searched
            languages: Search for experiments with corresponding languages in the list
            exclude_languages: All experiments except those with languages in the list will be searched
            user_id: Specify the publisher of the works to search for
            take: Number of searches
            skip: Number of searches to skip
            from_skip: Starting position identifier

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(tags, (list, type(None))):
            raise TypeError(
                f"Parameter `tags` must be of type 'list' or None, but got value `{tags}` of type `{type(tags).__name__}`"
            )
        if tags is not None and not all(isinstance(tag, Tag) for tag in tags):
            raise TypeError(
                f"Parameter `tags` must be a list of Tag enum instances, but got value `{tags} of type list containing non-Tag elements`"
            )
        if not isinstance(exclude_tags, (list, type(None))):
            raise TypeError(
                f"Parameter `exclude_tags` must be of type 'list' or None, but got value `{exclude_tags}` of type `{type(exclude_tags).__name__}`"
            )
        if exclude_tags is not None and not all(
            isinstance(tag, Tag) for tag in exclude_tags
        ):
            raise TypeError(
                f"Parameter `exclude_tags` must be a list of Tag enum instances, but got value `{exclude_tags} of type list containing non-Tag elements`"
            )
        if not isinstance(languages, (list, type(None))):
            raise TypeError(
                f"Parameter `languages` must be of type `Optional[list]`, but got value `{languages}` of type `{type(languages).__name__}`"
            )
        if languages is not None and not all(
            isinstance(language, str) for language in languages
        ):
            raise TypeError(
                f"Parameter `languages` must be type `list | str`, but got value `{languages}` of type `{type(languages).__name__}`"
            )
        if not isinstance(exclude_languages, (list, type(None))):
            raise TypeError(
                f"Parameter `exclude_languages` must be of type `Optional[list]`, but got value `{exclude_languages}` of type `{type(exclude_languages).__name__}`"
            )
        if exclude_languages is not None and not all(
            isinstance(language, str) for language in exclude_languages
        ):
            raise TypeError(
                f"Parameter `exclude_languages` must be a list of str, but got value `{exclude_languages} of type list containing non-str elements`"
            )
        if not isinstance(user_id, (str, type(None))):
            raise TypeError(
                f"Parameter `user_id` must be of type `str` or None, but got value `{user_id}` of type {type(user_id).__name__}`"
            )
        if not isinstance(take, int):
            raise TypeError(
                f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`"
            )
        if not isinstance(skip, int):
            raise TypeError(
                f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`"
            )
        if not isinstance(from_skip, (str, type(None))):
            raise TypeError(
                f"Parameter `from_skip` must be of type `str` or None, but got value `{from_skip}` of type `{type(from_skip).__name__}`"
            )

        if languages is None:
            languages = []
        if exclude_languages is None:
            exclude_languages = []

        if tags is None:
            _tags = None
        else:
            _tags = [tag.value for tag in tags]

        if exclude_tags is None:
            _exclude_tags = exclude_tags
        else:
            _exclude_tags = [tag.value for tag in exclude_tags]

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/QueryExperiments",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "Query": {
                    "Category": category.value,
                    "Languages": languages,
                    "ExcludeLanguages": exclude_languages,
                    "Tags": _tags,
                    "ExcludeTags": _exclude_tags,
                    "ModelTags": None,
                    "ModelID": None,
                    "ParentID": None,
                    "UserID": user_id,
                    "Special": None,
                    "From": from_skip,
                    "Skip": skip,
                    "Take": take,
                    "Days": 0,
                    "Sort": 0,  # TODO 这个也许是那个史上热门之类的?
                    "ShowAnnouncement": False,
                }
            },
        )

        return _check_response_json(response)

    async def async_query_experiments(
        self,
        category: enums.Category,
        tags: Optional[List[enums.Tag]] = None,
        exclude_tags: Optional[List[enums.Tag]] = None,
        languages: Optional[List[str]] = None,
        exclude_languages: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        take: int = 20,
        skip: int = 0,
        from_skip: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.query_experiments,
            category,
            tags,
            exclude_tags,
            languages,
            exclude_languages,
            user_id,
            take,
            skip,
            from_skip,
        )

    def get_experiment(
        self,
        content_id: str,
        category: Optional[Category] = None,
    ) -> _api_result:
        """Get experiment

        Args:
            content_id: When category is not None, content_id is experiment ID,
                       otherwise it will be recognized as get_summary()["Data"]["ContentID"] result
            category: Experiment area or black hole area

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(content_id, str):
            raise TypeError(
                f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        if not isinstance(category, (Category, type(None))):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum or None, but got value `{category}` of type `{type(category).__name__}`"
            )

        if category is not None:
            # If experiment ID is passed, first get summary to obtain ContentID
            content_id = self.get_summary(content_id, category)["Data"]["ContentID"]

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/GetExperiment",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ContentID": content_id,
            },
        )

        return _check_response_json(response)

    async def async_get_experiment(
        self,
        content_id: str,
        category: Optional[enums.Category] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_experiment, content_id, category)

    def confirm_experiment(
        self, summary_id: str, category: Category, image_counter: int
    ) -> _api_result:
        """Confirm experiment publication

        Args:
            summary_id: Summary ID
            category: Experiment area or black hole area
            image_counter: Image counter

        Returns:
            _api_result: Physics-Lab-AR API response structure

        Notes:
            Low-level API, do not use directly
            Use Experiment.update() and Experiment.upload() methods to publish experiments
        """
        if not isinstance(summary_id, str):
            raise TypeError(
                f"Parameter `summary_id` must be of type `str`, but got value `{summary_id}` of type `{type(summary_id).__name__}`"
            )
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(image_counter, int):
            raise TypeError(
                f"Parameter `image_counter` must be of type `int`, but got value `{image_counter}` of type `{type(image_counter).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/ConfirmExperiment",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "SummaryID": summary_id,
                "Category": category.value,
                "Image": image_counter,
                "Extension": ".jpg",
            },
        )

        return _check_response_json(response)

    async def async_confirm_experiment(
        self, summary_id: str, category: enums.Category, image_counter: int
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.confirm_experiment, summary_id, category, image_counter
        )

    def remove_experiment(
        self, summary_id: str, category: Category, reason: Optional[str] = None
    ) -> _api_result:
        """Hide experiment

        Args:
            summary_id: Experiment ID
            category: Experiment area or black hole area
            reason: Reason for hiding

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(summary_id, str):
            raise TypeError(
                f"Parameter `summary_id` must be of type `str`, but got value `{summary_id}` of type `{type(summary_id).__name__}`"
            )
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(reason, (str, type(None))):
            raise TypeError(
                f"Parameter `reason` must be of type `str` or None, but got value `{reason}` of type `{type(reason).__name__}`"
            )

        _plar_ver = plAR.get_plAR_version()
        plar_ver = (
            f"{_plar_ver[0]}{_plar_ver[1]}{_plar_ver[2]}"
            if _plar_ver is not None
            else "2411"
        )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/RemoveExperiment",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
                "x-API-Version": plar_ver,
            },
            body={
                "Category": category.value,
                "SummaryID": summary_id,
                "Hiding": True,
                "Reason": reason,
            },
        )

        return _check_response_json(response)

    async def async_remove_experiment(
        self,
        summary_id: str,
        category: enums.Category,
        reason: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.remove_experiment, summary_id, category, reason
        )

    def post_comment(
        self,
        target_id: str,
        target_type: str,
        content: str,
        reply_id: Optional[str] = None,
        special: Optional[str] = None,
    ) -> _api_result:
        """Post comment

        Args:
            target_id: Target user/experiment ID
            target_type: User, Discussion, Experiment
            content: Comment content
            reply_id: ID of user being replied to (can be automatically derived)
            special: "Reminder" for sending warning, None for normal comment

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(target_id, str):
            raise TypeError(
                f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
            )
        if not isinstance(content, str):
            raise TypeError(
                f"Parameter `content` must be of type `str`, but got value `{content}` of type `{type(content).__name__}`"
            )
        if not isinstance(target_type, str):
            raise TypeError(
                f"Parameter `target_type` must be of type `str`, but got value `{target_type}` of type `{type(target_type).__name__}`"
            )
        if not isinstance(reply_id, (str, type(None))):
            raise TypeError(
                f"Parameter `reply_id` must be of type `str` or None, but got value `{reply_id}` of type `{type(reply_id).__name__}`"
            )
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError(
                f"Parameter `target_type` must be one of ['User', 'Discussion', 'Experiment'], but got value `{target_type}`"
            )
        if special not in (None, "Reminder"):
            raise ValueError(
                f"Parameter `special` must be one of [None, 'Reminder'], but got value `{special}`"
            )

        if reply_id is None:
            reply_id = ""

            # Physics-Lab-AR supports multiple languages: Chinese, English, French, German, Spanish, Japanese, Ukrainian, Polish
            if (
                content.startswith("回复@")
                or content.startswith("Reply@")
                or content.startswith("Répondre@")
                or content.startswith("Antworten@")
                or content.startswith("Respuesta@")
                or content.startswith("応答@")
                or content.startswith("Відповісти@")
                or content.startswith("Odpowiadać@")
            ):
                _nickname = ""
                is_match: bool = False
                for chr in content:
                    if chr in (":", " "):
                        break
                    elif is_match:
                        _nickname += chr
                    elif chr == "@":
                        is_match = True
                        continue

                if _nickname != "":
                    try:
                        reply_id = self.get_user(_nickname, enums.GetUserMode.by_name)[
                            "Data"
                        ]["User"]["ID"]
                    except errors.ResponseFail:
                        pass

        assert isinstance(reply_id, str)

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Messages/PostComment",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "TargetID": target_id,
                "TargetType": target_type,
                "Language": "Chinese",
                "ReplyID": reply_id,
                "Content": content,
                "Special": special,
            },
        )

        return _check_response_json(response)

    async def async_post_comment(
        self,
        target_id: str,
        target_type: str,
        content: str,
        reply_id: Optional[str] = None,
        special: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.post_comment, target_id, target_type, content, reply_id, special
        )

    def remove_comment(self, comment_id: str, target_type: str) -> _api_result:
        """Delete comment

        Args:
            comment_id: Comment ID, can be obtained through `get_comments`
            target_type: User, Discussion, Experiment

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(comment_id, str):
            raise TypeError(
                f"Parameter `comment_id` must be of type `str`, but got value `{comment_id}` of type `{type(comment_id).__name__}`"
            )
        if not isinstance(target_type, str):
            raise TypeError(
                f"Parameter `target_type` must be of type `str`, but got value `{target_type}` of type `{type(target_type).__name__}`"
            )
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError(
                f"Parameter `target_type` must be one of ['User', 'Discussion', 'Experiment'], but got value `{target_type}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Messages/RemoveComment",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "TargetType": target_type,
                "CommentID": comment_id,
            },
        )

        return _check_response_json(response)

    async def async_remove_comment(
        self, comment_id: str, target_type: str
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.remove_comment, comment_id, target_type)

    def get_comments(
        self,
        target_id: str,
        target_type: str,
        take: int = 16,
        skip: int = 0,
        comment_id: Optional[str] = None,
    ) -> _api_result:
        """获取评论板信息

        Args:
            target_id: 物实用户的ID/实验的id
            target_type: User, Discussion, Experiment
            take: 获取留言的数量
            skip: 跳过的留言数量, 为(unix时间戳 * 1000)
            comment_id: 从comment_id开始获取take条消息 (另一种skip的规则)

        Returns:
            _api_result: 物实api返回体结构
        """
        if not isinstance(target_id, str):
            raise TypeError(
                f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
            )
        if not isinstance(target_type, str):
            raise TypeError(
                f"Parameter `target_type` must be of type `str`, but got value `{target_type}` of type `{type(target_type).__name__}`"
            )
        if not isinstance(take, int):
            raise TypeError(
                f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`"
            )
        if not isinstance(skip, int):
            raise TypeError(
                f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`"
            )
        if not isinstance(comment_id, (str, type(None))):
            raise TypeError(
                f"Parameter `comment_id` must be of type `str` or None, but got value `{comment_id}` of type `{type(comment_id).__name__}`"
            )
        if target_type not in ("User", "Discussion", "Experiment"):
            raise ValueError(
                f"Parameter `target_type` must be one of ['User', 'Discussion', 'Experiment'], but got value `{target_type} of type '{target_type}'"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Messages/GetComments",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "TargetID": target_id,
                "TargetType": target_type,
                "CommentID": comment_id,
                "Take": take,
                "Skip": skip,
            },
        )

        return _check_response_json(response)

    async def async_get_comments(
        self,
        target_id: str,
        target_type: str,
        take: int = 16,
        skip: int = 0,
        comment_id: Optional[str] = None,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.get_comments, target_id, target_type, take, skip, comment_id
        )

    def get_summary(self, content_id: str, category: Category) -> _api_result:
        """Get experiment introduction

        Args:
            content_id: Experiment ID
            category: Experiment area or black hole area

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(content_id, str):
            raise TypeError(
                f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/GetSummary",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ContentID": content_id,
                "Category": category.value,
            },
        )

        def callback(status_code):
            if status_code == 403:
                raise PermissionError("login failed")
            if status_code == 404:
                raise errors.ResponseFail(
                    response.json()["code"],
                    "experiment not found(may be you select category wrong)",
                )

        return _check_response_json(response)

    async def async_get_summary(
        self, content_id: str, category: enums.Category
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_summary, content_id, category)

    def get_derivatives(self, content_id: str, category: Category) -> _api_result:
        """Get work details, Physics-Lab-AR uses this interface when reading works for the first time

        Args:
            content_id: Experiment ID
            category: Experiment area or black hole area

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(content_id, str):
            raise TypeError(
                f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/GetDerivatives",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ContentID": content_id,
                "Category": category.value,
            },
        )

        return _check_response_json(response)

    async def async_get_derivatives(
        self, content_id: str, category: enums.Category
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_derivatives, content_id, category)

    def get_user_by_name(self, name: str) -> _api_result:
        """Get user information

        Args:
            name: Username

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(name, str):
            raise TypeError(
                f"Parameter `name` must be of type `str`, but got value `{name}` of type `{type(name).__name__}`"
            )
        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/GetUser",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={"Name": name},
        )

        return _check_response_json(response)

    async def async_get_user_by_name(self, name: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_user_by_name, name)

    def get_user_by_id(self, id: str) -> _api_result:
        """Get user information

        Args:
            id: User ID

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(id, str):
            raise TypeError(
                f"Parameter `id` must be of type `str`, but got value `{id}` of type `{type(id).__name__}`"
            )
        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/GetUser",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={"ID": id},
        )

        return _check_response_json(response)

    async def async_get_user_by_id(self, id: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_user_by_id, id)

    def get_user(
        self,
        msg: str,
        get_user_mode: enums.GetUserMode,
    ) -> _api_result:
        """Get user information

        Args:
            msg: User ID/Username
            get_user_mode: Get user information by ID/Username

        Returns:
            _api_result: Physics-Lab-AR API response structure

        Notes:
            Only for compatibility, use `get_user_by_id` or `get_user_by_name` is recommended
        """
        if not isinstance(msg, str):
            raise TypeError(
                f"Parameter `msg` must be of type `str`, but got value `{msg}` of type {type(msg).__name__}`"
            )
        if not isinstance(get_user_mode, enums.GetUserMode):
            raise TypeError(
                f"Parameter `get_user_mode` must be an instance of type "
                f"`physicsLab.enums.GetUserMode`, but got value `{get_user_mode}` of type {type(get_user_mode).__name__}`"
            )

        if get_user_mode == enums.GetUserMode.by_id:
            return self.get_user_by_id(msg)
        elif get_user_mode == enums.GetUserMode.by_name:
            return self.get_user_by_name(msg)
        else:
            errors.unreachable()

    async def async_get_user(
        self,
        msg: str,
        get_user_mode: enums.GetUserMode,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_user, msg, get_user_mode)

    def get_profile(self) -> _api_result:
        """Get user homepage information

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/GetProfile",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ID": self.user_id,
            },
        )

        return _check_response_json(response)

    async def async_get_profile(self) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_profile)

    def star_content(
        self, content_id: str, category: Category, star_type: int, status: bool = True
    ) -> _api_result:
        """Favorite/Support an experiment

        Args:
            content_id: Experiment ID
            category: Experiment area, Black hole area
            star_type: 0: Favorite, 1: Support experiment with gold coins
            status: True: Favorite, False: Unfavorite (no effect on support)

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(content_id, str):
            raise TypeError(
                f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(status, bool):
            raise TypeError(
                f"Parameter `status` must be of type `bool`, but got value `{status}` of type `{type(status).__name__}`"
            )
        if not isinstance(star_type, int):
            raise TypeError(
                f"Parameter `star_type` must be of type `int`, but got value `{star_type}` of type `{type(star_type).__name__}`"
            )
        if star_type not in (0, 1):
            raise ValueError(
                f"Parameter `star_type` must be one of [0, 1], but got value `{star_type} of type '{star_type}'`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/StarContent",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ContentID": content_id,
                "Status": status,
                "Category": category.value,
                "Type": star_type,
            },
        )

        return _check_response_json(response)

    async def async_star_content(
        self,
        content_id: str,
        category: enums.Category,
        star_type: int,
        status: bool = True,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.star_content, content_id, category, star_type, status
        )

    def upload_image(
        self, policy: str, authorization: str, image_path: str
    ) -> _api_result:
        """Upload experiment image

        Args:
            authorization: Can be obtained through /Contents/SubmitExperiment["Data"]["Token"]["Policy"]
            policy: Can be obtained through /Contents/SubmitExperiment["Data"]["Token"]["Policy"]
            image_path: Local path of image to be uploaded

        Returns:
            _api_result: Physics-Lab-AR API response structure

        Notes:
            This API is a low-level API, it is recommended to use the more complete Experiment.upload() and Experiment.update() methods for uploading images
        """
        if policy is None or authorization is None:
            raise RuntimeError("Sorry, Physics-Lab-AR can't upload this iamge")
        if not isinstance(policy, str):
            raise TypeError(
                f"Parameter `policy` must be of type `str`, but got value `{policy}` of type `{type(policy).__name__}`"
            )
        if not isinstance(authorization, str):
            raise TypeError(
                f"Parameter `authorization` must be of type `str`, but got value `{authorization}` of type `{type(authorization).__name__}`"
            )
        if not isinstance(image_path, str):
            raise TypeError(
                f"Parameter `image_path` must be of type `str`, but got value `{image_path}` of type `{type(image_path).__name__}`"
            )
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            raise FileNotFoundError(f"`{image_path}` not found")

        with open(image_path, "rb") as f:
            data = {
                "policy": (None, policy, None),
                "authorization": (None, authorization, None),
                "file": ("temp.jpg", f, None),
            }
            response = requests.post(
                "http://v0.api.upyun.com/qphysics",
                files=data,
            )
            response.raise_for_status()
            if response.json()["code"] != 200:
                raise errors.ResponseFail(
                    response.json()["code"],
                    f"Physics-Lab-AR returned error code {response.json()['code']} : "
                    f"{response.json()['message']}`",
                )
            return response.json()

    async def async_upload_image(
        self, policy: str, authorization: str, image_path: str
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.upload_image, policy, authorization, image_path
        )

    def get_message(self, message_id: str) -> _api_result:
        """Read system email message

        Args:
            message_id: Message ID

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(message_id, str):
            raise TypeError(
                f"Parameter `message_id` must be of type `str`, but got value `{message_id}` of type `{type(message_id).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Messages/GetMessage",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "MessageID": message_id,
            },
        )

        return _check_response_json(response)

    async def async_get_message(self, message_id: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.get_message, message_id)

    def get_messages(
        self,
        category_id: int,
        skip: int = 0,
        take: int = 16,
        no_templates: bool = True,
    ) -> _api_result:
        """Get messages received by user

        Args:
            category_id: Message type:
                0: All, 1: System email, 2: Followers and fans, 3: Comments and replies, 4: Work notifications, 5: Management records
            skip: Skip skip messages
            take: Take take messages
            no_templates: Whether to not return template messages for message types

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if category_id not in (0, 1, 2, 3, 4, 5):
            raise TypeError(
                f"Parameter `category_id` must be an integer within [0, 5], but got value `{category_id}` of type `{category_id}`"
            )
        if not isinstance(skip, int):
            raise TypeError(
                f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`"
            )
        if not isinstance(take, int):
            raise TypeError(
                f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`"
            )
        if not isinstance(no_templates, bool):
            raise TypeError(
                f"Parameter `no_templates` must be of type `bool`, but got value `{no_templates}` of type `{type(no_templates).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Messages/GetMessages",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "CategoryID": category_id,
                "Skip": skip,
                "Take": take,
                "NoTemplates": no_templates,
            },
        )

        return _check_response_json(response)

    async def async_get_messages(
        self,
        category_id: int,
        skip: int = 0,
        take: int = 16,
        no_templates: bool = True,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.get_messages, category_id, skip, take, no_templates
        )

    def get_supporters(
        self,
        content_id: str,
        category: Category,
        skip: int = 0,
        take: int = 16,
    ) -> _api_result:
        """Get support list

        Args:
            content_id: Content ID
            category: .Experiment or .Discussion
            skip: Pass in a timestamp, skip skip messages
            take: Take take messages

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(content_id, str):
            raise TypeError(
                f"Parameter `content_id` must be of type `str`, but got value `{content_id}` of type `{type(content_id).__name__}`"
            )
        if not isinstance(category, Category):
            raise TypeError(
                f"Parameter `category` must be an instance of Category enum, but got value `{category}` of type `{type(category).__name__}`"
            )
        if not isinstance(skip, int):
            raise TypeError(
                f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`"
            )
        if not isinstance(take, int):
            raise TypeError(
                f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Contents/GetSupporters",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ContentID": content_id,
                "Category": category.value,
                "Skip": skip,
                "Take": take,
            },
        )

        return _check_response_json(response)

    async def async_get_supporters(
        self,
        content_id: str,
        category: enums.Category,
        skip: int = 0,
        take: int = 16,
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.get_supporters, content_id, category, skip, take
        )

    def get_relations(
        self,
        user_id: str,
        display_type: str = "Follower",
        skip: int = 0,
        take: int = 20,
        query: str = "",  # TODO 获取编辑，志愿者列表啊之类的貌似也是这个api
    ) -> _api_result:
        """Get user's followers/following list

        Args:
            user_id: User ID
            display_type: Can only be Follower: followers, Following: following
            skip: Skip skip users
            take: Take take users
            query: User ID or nickname

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if display_type not in ("Follower", "Following"):
            raise ValueError(
                f"Parameter `display_type` must be one of ['Follower', 'Following'], but got value `{display_type}` of type `{display_type}`"
            )
        if not isinstance(user_id, str):
            raise TypeError(
                f"Parameter `user_id` must be of type `str`, but got value `{user_id}` of type `{type(user_id).__name__}`"
            )
        if not isinstance(skip, int):
            raise TypeError(
                f"Parameter `skip` must be of type `int`, but got value `{skip}` of type `{type(skip).__name__}`"
            )
        if not isinstance(take, int):
            raise TypeError(
                f"Parameter `take` must be of type `int`, but got value `{take}` of type `{type(take).__name__}`"
            )

        if display_type == "Follower":
            display_type_ = 0
        elif display_type == "Following":
            display_type_ = 1
        else:
            errors.unreachable()

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/GetRelations",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "UserID": user_id,
                "DisplayType": display_type_,
                "Skip": skip,
                "Take": take,
                "Query": query,
            },
        )

        return _check_response_json(response)

    async def async_get_relations(
        self,
        user_id: str,
        display_type: str = "Follower",
        skip: int = 0,
        take: int = 20,
        query: str = "",
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(
            self.get_relations, user_id, display_type, skip, take, query
        )

    def follow(self, target_id: str, action: bool = True) -> _api_result:
        """Follow user

        Args:
            target_id: ID of user to be followed
            action: true to follow, false to unfollow

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(target_id, str):
            raise TypeError(
                f"Parameter `target_id` must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
            )
        if not isinstance(action, bool):
            raise TypeError(
                f"Parameter `action` must be of type `bool`, but got value `{action}` of type `{type(action).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/Follow",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "TargetID": target_id,
                "Action": int(action),
            },
        )

        return _check_response_json(response)

    async def async_follow(
        self, target_id: str, action: bool = True
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.follow, target_id, action)

    def rename(self, nickname: str) -> _api_result:
        """Change user nickname

        Args:
            nickname: New nickname

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(nickname, str):
            raise TypeError(
                f"Parameter `nickname` must be of type `str`, but got value `{nickname}` of type {type(nickname).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/Rename",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "Target": nickname,
                "UserID": self.user_id,
            },
        )

        return _check_response_json(response)

    async def async_rename(self, nickname: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.rename, nickname)

    def modify_information(self, target: str) -> _api_result:
        """Modify user signature

        Args:
            target: New signature

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(target, str):
            raise TypeError(
                f"Parameter `target` must be of type `str`, but got value `{target}` of type `{type(target).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/ModifyInformation",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "Target": target,
                "Field": "Signature",
            },
        )

        return _check_response_json(response)

    async def async_modify_information(self, target: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.modify_information, target)

    def receive_bonus(self, activity_id: str, index: int) -> _api_result:
        """Claim daily check-in reward

        Args:
            activity_id: Activity ID
            index: Which reward of the activity

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(activity_id, str):
            raise TypeError(
                f"Parameter `activity_id` must be of type `str`, but got value `{activity_id}` of type `{type(activity_id).__name__}`"
            )
        if not isinstance(index, int):
            raise TypeError(
                f"Parameter `index` must be of type `int`, but got value `{index}` of type `{type(index).__name__}`"
            )
        if index < 0:
            raise ValueError(
                f"Parameter `index` must be a non-negative integer, but got value `{index}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/ReceiveBonus",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "ActivityID": activity_id,
                "Index": index,
                "Statistic": self.statistic,
            },
        )

        return _check_response_json(response)

    async def async_receive_bonus(
        self, activity_id: str, index: int
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.receive_bonus, activity_id, index)

    def ban(self, target_id: str, reason: str, length: int) -> _api_result:
        """Ban user

        Args:
            target_id: ID of user to be banned
            reason: Ban reason
            length: Ban duration in days

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(target_id, str):
            raise TypeError(
                f"Parameter target_id must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
            )
        if not isinstance(reason, str):
            raise TypeError(
                f"Parameter reason must be of type `str`, but got value `{reason}` of type `{type(reason).__name__}`"
            )
        if not isinstance(length, int):
            raise TypeError(
                f"Parameter length must be of type `int`, but got value `{length}` of type `{type(length).__name__}`"
            )

        if length <= 0:  # TODO Try negative number someday
            raise ValueError

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/Ban",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "TargetID": target_id,
                "Reason": reason,
                "Length": length,
            },
        )

        return _check_response_json(response)

    async def async_ban(
        self, target_id: str, reason: str, length: int
    ) -> Awaitable[_api_result]:
        return await _async_wrapper(self.ban, target_id, reason, length)

    def unban(self, target_id: str, reason: str) -> _api_result:
        """Unban user

        Args:
            target_id: ID of user to be unbanned
            reason: Unban reason

        Returns:
            _api_result: Physics-Lab-AR API response structure
        """
        if not isinstance(target_id, str):
            raise TypeError(
                f"Parameter target_id must be of type `str`, but got value `{target_id}` of type `{type(target_id).__name__}`"
            )
        if not isinstance(reason, str):
            raise TypeError(
                f"Parameter reason must be of type `str`, but got value `{reason}` of type `{type(reason).__name__}`"
            )

        response = _request.post_https(
            domain=self.domain,
            port=443,
            path="Users/Unban",
            header={
                "Content-Type": "application/json",
                "x-API-Token": self.token,
                "x-API-AuthCode": self.auth_code,
            },
            body={
                "TargetID": target_id,
                "Reason": reason,
            },
        )

        return _check_response_json(response)

    async def async_unban(self, target_id: str, reason: str) -> Awaitable[_api_result]:
        return await _async_wrapper(self.unban, target_id, reason)


def anonymous_login() -> User:
    """Anonymous login to Physics-Lab-AR"""
    plar_version = plAR.get_plAR_version()
    if plar_version is not None:
        plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
    else:
        plar_version = 2411

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        json={
            "Login": None,
            "Password": None,
            "Version": plar_version,
            "Device": {
                "Identifier": "7db01528cf13e2199e141c402d79190e",
                "Language": "Chinese",
            },
        },
        headers={
            "Content-Type": "application/json",
        },
    )

    api_result = _check_response(response)
    assert api_result["AuthCode"] is not None, errors.BUG_REPORT
    return User(
        token=api_result["Token"],
        auth_code=api_result["AuthCode"],
        is_binded=api_result["Data"]["User"]["IsBinded"],
        device_token=api_result["Data"]["DeviceToken"],
        user_id=api_result["Data"]["User"]["ID"],
        nickname=api_result["Data"]["User"]["Nickname"],
        signature=api_result["Data"]["User"]["Signature"],
        gold=api_result["Data"]["User"]["Gold"],
        level=api_result["Data"]["User"]["Level"],
        avatar=api_result["Data"]["User"]["Avatar"],
        avatar_region=api_result["Data"]["User"]["AvatarRegion"],
        decoration=api_result["Data"]["User"]["Decoration"],
        verification=api_result["Data"]["User"]["Verification"],
        statistic=api_result["Data"]["Statistic"],
    )


def email_login(email: str, password: str) -> User:
    """Login to Physics-Lab-AR via email"""
    if not isinstance(email, str):
        raise TypeError(
            f"Parameter email must be of type `str`, but got value {email} of type `{type(email).__name__}`"
        )
    if not isinstance(password, str):
        raise TypeError(
            f"Parameter password must be of type `str`, but got value {password} of type `{type(password).__name__}`"
        )

    plar_version = plAR.get_plAR_version()
    if plar_version is not None:
        plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
    else:
        plar_version = 2411

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        json={
            "Login": email,
            "Password": password,
            "Version": plar_version,
            "Device": {
                "Identifier": "7db01528cf13e2199e141c402d79190e",
                "Language": "Chinese",
            },
        },
        headers={
            "Content-Type": "application/json",
        },
    )

    api_result = _check_response(response)
    assert api_result["AuthCode"] is not None, errors.BUG_REPORT
    return User(
        token=api_result["Token"],
        auth_code=api_result["AuthCode"],
        is_binded=api_result["Data"]["User"]["IsBinded"],
        device_token=api_result["Data"]["DeviceToken"],
        user_id=api_result["Data"]["User"]["ID"],
        nickname=api_result["Data"]["User"]["Nickname"],
        signature=api_result["Data"]["User"]["Signature"],
        gold=api_result["Data"]["User"]["Gold"],
        level=api_result["Data"]["User"]["Level"],
        avatar=api_result["Data"]["User"]["Avatar"],
        avatar_region=api_result["Data"]["User"]["AvatarRegion"],
        decoration=api_result["Data"]["User"]["Decoration"],
        verification=api_result["Data"]["User"]["Verification"],
        statistic=api_result["Data"]["Statistic"],
    )


def token_login(token: str, auth_code: str) -> User:
    """Login to Physics-Lab-AR via token"""
    if not isinstance(token, str):
        raise TypeError(
            f"Parameter email must be of type `str`, but got value {token} of type `{type(token).__name__}`"
        )
    if not isinstance(auth_code, str):
        raise TypeError(
            f"Parameter password must be of type `str`, but got value {auth_code} of type `{type(auth_code).__name__}`"
        )

    plar_version = plAR.get_plAR_version()
    if plar_version is not None:
        plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
    else:
        plar_version = 2411

    response = requests.post(
        "http://physics-api-cn.turtlesim.com/Users/Authenticate",
        json={
            "Login": None,
            "Password": None,
            "Version": plar_version,
            "Device": {
                "Identifier": "7db01528cf13e2199e141c402d79190e",
                "Language": "Chinese",
            },
        },
        headers={
            "Content-Type": "application/json",
            "x-API-Token": token,
            "x-API-AuthCode": auth_code,
        },
    )

    api_result = _check_response(response)
    assert api_result["AuthCode"] is not None, errors.BUG_REPORT
    return User(
        token=api_result["Token"],
        auth_code=api_result["AuthCode"],
        is_binded=api_result["Data"]["User"]["IsBinded"],
        device_token=api_result["Data"]["DeviceToken"],
        user_id=api_result["Data"]["User"]["ID"],
        nickname=api_result["Data"]["User"]["Nickname"],
        signature=api_result["Data"]["User"]["Signature"],
        gold=api_result["Data"]["User"]["Gold"],
        level=api_result["Data"]["User"]["Level"],
        avatar=api_result["Data"]["User"]["Avatar"],
        avatar_region=api_result["Data"]["User"]["AvatarRegion"],
        decoration=api_result["Data"]["User"]["Decoration"],
        verification=api_result["Data"]["User"]["Verification"],
        statistic=api_result["Data"]["Statistic"],
    )


async def async_anonymous_login() -> Awaitable[User]:
    return await _async_wrapper(anonymous_login)


async def async_email_login(email: str, password: str) -> Awaitable[User]:
    return await _async_wrapper(email_login, email, password)


async def async_token_login(token: str) -> Awaitable[User]:
    return await _async_wrapper(token_login, token)
