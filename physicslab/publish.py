"""Helpers for publishing experiment objects to Physics-Lab-AR."""

import os
import copy
import json
import gzip

from physicslab import errors, quantum_physics
from physicslab.enums import Category
from physicslab.circuit import CircuitExperiment
from physicslab.celestial import CelestialExperiment
from physicslab.electromagnetism import ElectromagnetismExperiment
from physicslab._typing import Union, Optional, Tuple, TypeAlias
from physicslab.web import _request, User

_Experiment: TypeAlias = Union[
    CircuitExperiment, CelestialExperiment, ElectromagnetismExperiment
]


def _check_type(expe: _Experiment, user: User) -> None:
    if not isinstance(
        expe, (CircuitExperiment, CelestialExperiment, ElectromagnetismExperiment)
    ):
        raise TypeError(
            "Parameter `expe` must be of type `CircuitExperiment`, "
            "`CelestialExperiment` or `ElectromagnetismExperiment`, "
            f"but got value `{expe}` of type `{type(expe).__name__}`"
        )
    if not isinstance(user, User):
        raise TypeError(
            f"Parameter `user` must be of type `User`, but got value `{user}` of type `{type(user).__name__}`"
        )


def _get_plar_version() -> int:
    version = quantum_physics.get_quantum_physics_version()
    if version is None:
        return 2411
    return int(f"{version[0]}{version[1]}{version[2]}")


def _submit_experiment(
    expe: _Experiment,
    user: User,
    category: Optional[Category],
    image_path: Optional[str],
) -> Tuple[dict, dict]:
    _check_type(expe, user)
    if not isinstance(category, (Category, type(None))):
        raise TypeError(
            f"Parameter `category` must be of type `Category` or `None`, but got value `{category}` of type `{type(category).__name__}`"
        )
    if not isinstance(image_path, (str, type(None))):
        raise TypeError(
            f"Parameter `image_path` must be of type `str` or `None`, but got value `{image_path}` of type `{type(image_path).__name__}`"
        )
    if image_path is not None and (not os.path.exists(image_path) or not os.path.isfile(image_path)):
        raise FileNotFoundError(f"`{image_path}` not found")
    if not user.is_binded:
        raise PermissionError("you must register first")

    plsav = expe.as_plsav_dict()
    workspace = copy.deepcopy(plsav)
    workspace["Summary"] = None
    summary = plsav["Summary"]

    if summary["Language"] is None:
        summary["Language"] = "Chinese"
    summary["User"]["ID"] = user.user_id
    summary["User"]["Nickname"] = user.nickname
    summary["User"]["Signature"] = user.signature
    summary["User"]["Avatar"] = user.avatar
    summary["User"]["AvatarRegion"] = user.avatar_region
    summary["User"]["Decoration"] = user.decoration
    summary["User"]["Verification"] = user.verification
    summary["Version"] = _get_plar_version()

    if category is not None:
        summary["Category"] = category.value

    submit_data = {
        "Summary": summary,
        "Workspace": workspace,
    }
    if image_path is not None:
        image_size = os.path.getsize(image_path)
        if image_size >= 1048576:
            # Use bug of Quantum-Physics to upload image
            image_size = -image_size
        submit_data["Request"] = {
            "FileSize": image_size,
            "Extension": ".jpg",
        }

    response = _request.post_https(
        domain=user.domain,
        port=443,
        path="Contents/SubmitExperiment",
        header={
            "x-API-Token": "null" if user.token is None else user.token,
            "x-API-AuthCode": user.auth_code,
            "x-API-Version": str(summary["Version"]),
            "Accept-Encoding": "gzip",
            "Content-Type": "gzipped/json",
        },
        body=gzip.compress(json.dumps(submit_data).encode("utf-8")),
    )

    if response["Status"] == 403:
        raise PermissionError(
            "you can't submit experiment because you are not the author "
            "or experiment status(elements, tags...) is invalid"
        )
    if response["Status"] != 200:
        raise errors.ResponseFail(
            response["Status"],
            f"Physics-Lab-AR's server returned error code {response['Status']}: {response['Message']}",
        )

    return response, submit_data


def upload_experiment(
    expe: _Experiment,
    user: User,
    category: Category,
    image_path: Optional[str],
) -> dict:
    """Publish a new experiment."""
    if not isinstance(category, Category):
        raise TypeError(
            f"Parameter `category` must be of type `Category`, but got value `{category}` of type `{type(category).__name__}`"
        )

    summary_id = expe.as_plsav_dict()["Summary"]["ID"]
    if summary_id is not None:
        # TODO This branch is always false
        raise RuntimeError(
            "upload can only be used to upload a brand new experiment, "
            "try using `.update_experiment` instead"
        )

    submit_response, submit_data = _submit_experiment(expe, user, category, image_path)

    if image_path is not None:
        submit_data["Summary"]["Image"] += 1

    user.confirm_experiment(
        submit_response["Data"]["Summary"]["ID"],
        category,
        submit_data["Summary"]["Image"],
    )

    if image_path is not None:
        user.upload_image(
            submit_response["Data"]["Token"]["Policy"],
            submit_response["Data"]["Token"]["Authorization"],
            image_path,
        )

    return submit_response


def update_experiment(
    expe: _Experiment,
    user: User,
    image_path: Optional[str] = None,
) -> dict:
    """Update an existing experiment."""
    summary_id = expe.as_plsav_dict()["Summary"]["ID"]
    if summary_id is None:
        raise RuntimeError(
            "update can only be used to upload an exist experiment, "
            "try using `.upload_experiment` instead"
        )

    submit_response, submit_data = _submit_experiment(expe, user, None, image_path)

    if image_path is not None:
        submit_data["Summary"]["Image"] += 1
        user.upload_image(
            submit_response["Data"]["Token"]["Policy"],
            submit_response["Data"]["Token"]["Authorization"],
            image_path,
        )

    return submit_response
