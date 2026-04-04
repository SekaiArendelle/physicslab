"""High-level electromagnetism experiment API."""

import json
import time
import pathlib
from physicslab import errors
from physicslab import enums
from physicslab.utils import find_path_of_sav_name
from physicslab import coordinate_system
from physicslab.enums import Category
from physicslab.web import User, anonymous_login
from physicslab._summary import Summary, construct_summary_from_plsav_dict
from physicslab._experiment import (
    TYPE_TAG_ELECTROMAGNETISM,
)
from . import elements
from physicslab._camera_save import CameraMode, CameraSave
from ._status_save import ElectromagnetismStatusSave
from ._base import ElectromagnetismBase
from physicslab._typing import Self, Optional, Tuple, Set


class ElectromagnetismExperiment:
    """Represents a complete electromagnetism experiment with elements and camera state."""

    __status_save: ElectromagnetismStatusSave
    __camera_save: CameraSave
    __summary: Summary

    def __init__(
        self,
        name: Optional[str],
        camera_save: CameraSave = CameraSave(
            CameraMode.electromagnetism_mode,
            2,
            coordinate_system.Position(0, 0, 0.88),
            coordinate_system.Rotation(90, 0, 0),
        ),
        introduction: Optional[str] = None,
        tags: Optional[Set[enums.Tag]] = None,
    ) -> None:
        self.status_save = ElectromagnetismStatusSave()
        self.camera_save = camera_save
        self.summary = Summary(
            experiment_type=4,
            subject=name,
            description=introduction,
            tags=set() if tags is None else tags,
            type_tag=TYPE_TAG_ELECTROMAGNETISM,
            parent_id=None,
            parent_name=None,
            parent_category=None,
            content_id=None,
            editor=None,
            coauthors=[],
            localized_description=None,
            model_id=None,
            model_name=None,
            model_tags=[],
            version=0,
            language=None,
            visits=0,
            stars=0,
            supports=0,
            remixes=0,
            comments=0,
            price=0,
            popularity=0,
            creation_date=int(time.time() * 1000),
            update_date=0,
            sorting_date=0,
            summary_id=None,
            category=None,
            localized_subject=None,
            image=0,
            image_region=0,
            user={
                "ID": None,
                "Nickname": None,
                "Signature": None,
                "Avatar": 0,
                "AvatarRegion": 0,
                "Decoration": 0,
                "Verification": None,
            },
            visibility=0,
            settings={},
            multilingual=False,
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @property
    def name(self) -> Optional[str]:
        """Display name of this experiment (may be ``None``)."""
        return self.summary.subject

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self.summary.subject = name

    @property
    def status_save(self) -> ElectromagnetismStatusSave:
        """Runtime state (elements) of this experiment."""
        return self.__status_save

    @status_save.setter
    def status_save(self, status_save: ElectromagnetismStatusSave) -> None:
        if not isinstance(status_save, ElectromagnetismStatusSave):
            raise TypeError(
                f"status_save must be of type `StatusSave`, but got value {status_save} of type {type(status_save).__name__}"
            )

        self.__status_save = status_save

    @property
    def camera_save(self) -> CameraSave:
        """Camera state saved with this experiment."""
        return self.__camera_save

    @camera_save.setter
    def camera_save(self, camera_save: CameraSave) -> None:
        if not isinstance(camera_save, CameraSave):
            raise TypeError(
                f"camera_save must be of type `CameraSave`, but got value {camera_save} of type {type(camera_save).__name__}"
            )

        self.__camera_save = camera_save

    @property
    def introduction(self) -> Optional[str]:
        """Introduction of this experiment (may be ``None``)."""
        return self.summary.description

    @introduction.setter
    def introduction(self, introduction: Optional[str]) -> None:
        self.summary.description = introduction

    @property
    def tags(self) -> Set[enums.Tag]:
        """Community tags of this experiment."""
        return self.summary.tags

    @tags.setter
    def tags(self, tags: Set[enums.Tag]) -> None:
        self.summary.tags = tags

    @property
    def summary(self) -> Summary:
        """Summary metadata of this experiment."""
        return self.__summary

    @summary.setter
    def summary(self, summary: Summary) -> None:
        if not isinstance(summary, Summary):
            raise TypeError(
                f"summary must be of type `Summary`, but got value {summary} of type {type(summary).__name__}"
            )
        self.__summary = summary

    def crt_a_element(self, element: ElectromagnetismBase) -> Self:
        """Add a single element to this experiment and return ``self``."""
        self.status_save.append_element(element)

        return self

    def crt_elements(self, *elements: ElectromagnetismBase) -> Self:
        """Add multiple elements to this experiment and return ``self``."""
        for element in elements:
            self.crt_a_element(element)

        return self

    def del_a_element(self, element: ElectromagnetismBase) -> Self:
        """Remove a single element from this experiment and return ``self``."""
        self.status_save.remove_element(element)

        return self

    def get_elements_count(self) -> int:
        """Return the total number of elements in this experiment."""
        return len(self.status_save.elements)

    def get_element_by_index(self, index: int) -> ElectromagnetismBase:
        """Return the element at position *index* in insertion order."""
        return self.status_save.get_element_by_index(index)

    def get_element_by_id(self, identifier: str) -> ElectromagnetismBase:
        """Return the element with the given *identifier*."""
        return self.status_save.get_element_by_id(identifier)

    def get_element_by_position(
        self,
        position: coordinate_system.Position,
    ) -> ElectromagnetismBase:
        """Return the element located at *position*."""
        return self.status_save.get_element_by_position(position)

    def as_plsav_dict(self) -> dict:
        """Serialise this experiment to a ``plsav`` dictionary."""
        return {
            "Type": 4,
            "Experiment": {
                "ID": None,
                "Type": 4,
                "Components": self.get_elements_count(),
                # duplicate with ["Summary"]["Subject"], seems this mekes no sense
                # "Subject": None,
                "StatusSave": self.status_save.as_str_in_plsav(),
                "CameraSave": self.camera_save.as_str_in_plsav(),
                "Version": 2405,
                "CreationDate": int(time.time() * 1000),
                "Paused": False,
                "Summary": None,
                "Plots": None,
            },
            "ID": None,
            "Summary": self.summary.as_dict(),
            "CreationDate": 0,
            "InternalName": self.name,
            "Speed": 1.0,
            "SpeedMinimum": 0.01,
            "SpeedMaximum": 2.0,
            "SpeedReal": 0.0,
            "Paused": False,
            "Version": 0,
            "CameraSnapshot": None,
            "Plots": [],
            "Widgets": [],
            "WidgetGroups": [],
            "Bookmarks": {},
            "Interfaces": {"Play-Expanded": False, "Chart-Expanded": False},
        }

    def save_to(self, path: pathlib.Path) -> None:
        """Write this experiment to *path* as a ``.plsav`` JSON file."""
        if not isinstance(path, pathlib.Path):
            raise TypeError(
                f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
            )

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.as_plsav_dict(), f, ensure_ascii=True)

    def merge(self, other: "ElectromagnetismExperiment") -> Self:
        """Merge all elements from *other* into this experiment and return ``self``."""
        if not isinstance(other, ElectromagnetismExperiment):
            raise TypeError(
                f"parameter other must be of type `ElectromagnetismExperiment`, but got value {other} of type {type(other).__name__}"
            )

        self.status_save.append_range(other.status_save)

        return self


def _dict_to_element(element_dict: dict) -> ElectromagnetismBase:
    model_id = element_dict["ModelID"]

    if model_id == "Negative Charge":
        return elements.NegativeCharge(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Positive Charge":
        return elements.PositiveCharge(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Negative Test Charge":
        return elements.NegativeTestCharge(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Positive Test Charge":
        return elements.PositiveTestCharge(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Bar Magnet":
        return elements.BarMagnet(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Compass":
        return elements.Compass(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Uniform Magnetic Field":
        return elements.UniformMagneticField(
            position=coordinate_system.construct_position_from_plsav_str(
                element_dict["Position"]
            ),
            rotation=coordinate_system.construct_rotation_from_plsav_str(
                element_dict["Rotation"]
            ),
            identifier=element_dict["Identifier"],
        )
    else:
        errors.unreachable()


def crt_electromagnetism_experiment(name: Optional[str]) -> ElectromagnetismExperiment:
    """Create and return a new empty electromagnetism experiment with the given *name*."""
    return ElectromagnetismExperiment(name)


def load_electromagnetism_experiment_by_file_path(
    path: pathlib.Path,
) -> ElectromagnetismExperiment:
    """Load an electromagnetism experiment from a ``.plsav`` file at *path*.

    Args:
        path: Path to the ``.plsav`` file.

    Returns:
        The loaded ``ElectromagnetismExperiment`` instance.

    Raises:
        TypeError: If *path* is not a ``pathlib.Path``.
        ExperimentNotExistError: If the file does not exist.
        ExperimentTypeError: If the file does not contain an electromagnetism experiment.
    """
    if not isinstance(path, pathlib.Path):
        raise TypeError(
            f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
        )
    if not path.exists() or not path.is_file():
        raise errors.ExperimentNotExistError(f'File "{path}" does not exist')

    with open(path, "r", encoding="utf-8") as f:
        plasv_dict = json.load(f)
    if plasv_dict["Type"] != 4:
        raise errors.ExperimentTypeError(
            f'"{path}" does not contain an electromagnetism experiment'
        )

    summary_dict = plasv_dict["Summary"]
    summary = construct_summary_from_plsav_dict(
        summary_dict, experiment_type=4, type_tag=TYPE_TAG_ELECTROMAGNETISM
    )
    result = ElectromagnetismExperiment(
        summary.subject, introduction=summary.description, tags=summary.tags
    )

    if "Experiment" in plasv_dict.keys():
        # tests/data/All-Electromagnetism-Elements.sav
        status_save_list = json.loads(plasv_dict["Experiment"]["StatusSave"])[
            "Elements"
        ]
        for element_dict in status_save_list:
            result.crt_a_element(_dict_to_element(element_dict))

        return result
    else:
        # tests/data/Export-All-Electromagnetism-Elements.sav
        status_save_list = json.loads(plasv_dict["StatusSave"])["Elements"]
        for element_dict in status_save_list:
            result.crt_a_element(_dict_to_element(element_dict))

        return result


def load_electromagnetism_experiment_by_sav_name(
    sav_name: str,
) -> Tuple[ElectromagnetismExperiment, pathlib.Path]:
    """Load an electromagnetism experiment by its save-file display name.

    Args:
        sav_name: The experiment name as displayed in Physics-Lab-AR.

    Returns:
        A ``(experiment, path)`` tuple.

    Raises:
        ExperimentNotExistError: If no matching save file is found.
    """
    file = find_path_of_sav_name(sav_name)
    if file is None:
        raise errors.ExperimentNotExistError(
            f'Experiment with name "{sav_name}" does not exist'
        )

    return load_electromagnetism_experiment_by_file_path(file), file


def load_electromagnetism_experiment_from_app(
    content_id: str, category: Category, user: User = anonymous_login()
) -> ElectromagnetismExperiment:
    """Download and load an electromagnetism experiment from Physics-Lab-AR.

    Args:
        content_id: The community content ID.
        category: The community content category.
        user: Authenticated user session (defaults to anonymous login).

    Returns:
        The loaded ``ElectromagnetismExperiment`` instance.

    Raises:
        TypeError: If any argument has an unexpected type.
        ExperimentTypeError: If the content is not an electromagnetism experiment.
    """
    if not isinstance(content_id, str):
        raise TypeError(
            f"content_id must be of type `str`, but got value {content_id} of type {type(content_id).__name__}`"
        )
    if not isinstance(category, Category):
        raise TypeError(
            f"category must be of type `Category`, but got value {category} of type {type(category).__name__}`"
        )
    if not isinstance(user, User):
        raise TypeError(
            f"user must be of type `User`, but got value {user} of type {type(user).__name__}`"
        )

    _summary = user.get_summary(content_id, category)["Data"]
    _experiment = user.get_experiment(_summary["ContentID"])["Data"]

    if _experiment["Type"] != 4:
        raise errors.ExperimentTypeError(
            f'Content ID "{content_id}" does not correspond to an electromagnetism experiment'
        )

    summary = construct_summary_from_plsav_dict(
        _summary, experiment_type=4, type_tag=TYPE_TAG_ELECTROMAGNETISM
    )
    result = ElectromagnetismExperiment(
        summary.subject, introduction=summary.description, tags=summary.tags
    )

    status_save_dict = json.loads(_experiment["StatusSave"])
    elements_list = status_save_dict["Elements"]
    for element_dict in elements_list:
        result.crt_a_element(_dict_to_element(element_dict))

    return result
