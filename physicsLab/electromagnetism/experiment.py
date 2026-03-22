import uuid
import json
import time
import pathlib
from physicsLab import constant
from physicsLab import errors
from physicsLab import coordinate_system
from physicsLab.enums import Category
from physicsLab.web import User, anonymous_login
from . import elements
from ._camera_save import CameraSave
from ._status_save import ElectromagnetismStatusSave
from ._base import ElectromagnetismBase
from physicsLab._typing import Self, Optional, Tuple


class ElectromagnetismExperiment:
    __name: Optional[str]
    __status_save: ElectromagnetismStatusSave
    __camera_save: CameraSave

    def __init__(
        self, name: Optional[str], camera_save: CameraSave = CameraSave()
    ) -> None:
        self.name = name
        self.status_save = ElectromagnetismStatusSave()
        self.camera_save = camera_save

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        if not isinstance(name, (str, type(None))):
            raise TypeError(
                f"name must be of type `str | None`, but got value {name} of type {type(name).__name__}"
            )

        self.__name = name

    @property
    def status_save(self) -> ElectromagnetismStatusSave:
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
        return self.__camera_save

    @camera_save.setter
    def camera_save(self, camera_save: CameraSave) -> None:
        if not isinstance(camera_save, CameraSave):
            raise TypeError(
                f"camera_save must be of type `CameraSave`, but got value {camera_save} of type {type(camera_save).__name__}"
            )

        self.__camera_save = camera_save

    def crt_a_element(self, element: ElectromagnetismBase) -> Self:
        self.status_save.append_element(element)

        return self

    def crt_elements(self, *elements: ElectromagnetismBase) -> Self:
        for element in elements:
            self.crt_a_element(element)

        return self

    def del_a_element(self, element: ElectromagnetismBase) -> Self:
        self.status_save.remove_element(element)

        return self

    def get_elements_count(self) -> int:
        return len(self.status_save.elements)

    def as_plsav_dict(self) -> dict:
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
            "Summary": {
                "Type": 4,
                "ParentID": None,
                "ParentName": None,
                "ParentCategory": None,
                "ContentID": None,
                "Editor": None,
                "Coauthors": [],
                "Description": None,
                "LocalizedDescription": None,
                "Tags": ["Type-4"],
                "ModelID": None,
                "ModelName": None,
                "ModelTags": [],
                "Version": 0,
                "Language": None,
                "Visits": 0,
                "Stars": 0,
                "Supports": 0,
                "Remixes": 0,
                "Comments": 0,
                "Price": 0,
                "Popularity": 0,
                "CreationDate": int(time.time() * 1000),
                "UpdateDate": 0,
                "SortingDate": 0,
                "ID": None,
                "Category": None,
                "Subject": self.name,
                "LocalizedSubject": None,
                "Image": 0,
                "ImageRegion": 0,
                "User": {
                    "ID": None,
                    "Nickname": None,
                    "Signature": None,
                    "Avatar": 0,
                    "AvatarRegion": 0,
                    "Decoration": 0,
                    "Verification": None,
                },
                "Visibility": 0,
                "Settings": {},
                "Multilingual": False,
            },
            "CreationDate": 0,
            "Speed": 1.0,
            "SpeedMinimum": 0.1,
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
        if not isinstance(path, pathlib.Path):
            raise TypeError(
                f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
            )

        path.write_text(json.dumps(self.as_plsav_dict()), encoding="utf-8")


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


def generate_a_new_sav_path() -> pathlib.Path:
    return pathlib.Path(
        constant.QUANTAM_PHYSICS_EXPERIMENT_DIR / str(uuid.uuid4())
    ).with_suffix(".sav")


def crt_electromagnetism_experiment(name: Optional[str]) -> ElectromagnetismExperiment:
    return ElectromagnetismExperiment(name)


def load_electromagnetism_experiment_by_file_path(
    path: pathlib.Path,
) -> ElectromagnetismExperiment:
    if not isinstance(path, pathlib.Path):
        raise TypeError(
            f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
        )

    plasv_dict = json.loads(path.read_text(encoding="utf-8"))
    if plasv_dict["Type"] != 4:
        raise errors.ExperimentTypeError(
            f'"{path}" does not contain an electromagnetism experiment'
        )

    summary_dict = plasv_dict["Summary"]
    if summary_dict is None:
        subject = None
    else:
        subject = summary_dict["Subject"]
    result = ElectromagnetismExperiment(subject)

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


def find_path_of_sav_name(sav_name: str) -> Optional[pathlib.Path]:
    if not isinstance(sav_name, str):
        raise TypeError(
            f"sav_name must be of type `str`, but got value {sav_name} of type {type(sav_name).__name__}"
        )

    for file in constant.QUANTAM_PHYSICS_EXPERIMENT_DIR.glob("*.sav"):
        if not file.is_file():
            continue

        plsav_dict: dict = json.loads(file.read_text(encoding="utf-8"))
        if "Summary" not in plsav_dict.keys():
            continue
        summary_dict: Optional[dict] = plsav_dict["Summary"]
        if summary_dict is None:
            continue
        if "Subject" in summary_dict.keys():
            if summary_dict["Subject"] == sav_name:
                return file
        elif "Subject" in plsav_dict.keys():
            if plsav_dict["Subject"] == sav_name:
                return file

    return None


def load_electromagnetism_experiment_by_sav_name(
    sav_name: str,
) -> Tuple[ElectromagnetismExperiment, pathlib.Path]:
    file = find_path_of_sav_name(sav_name)
    if file is None:
        raise errors.ExperimentNotExistError(
            f'Experiment with name "{sav_name}" does not exist'
        )

    return load_electromagnetism_experiment_by_file_path(file), file


def load_electromagnetism_experiment_from_app(
    content_id: str, category: Category, user: User = anonymous_login()
) -> ElectromagnetismExperiment:
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

    result = ElectromagnetismExperiment(_summary["Subject"])

    status_save_dict = json.loads(_experiment["StatusSave"])
    elements_list = status_save_dict["Elements"]
    for element_dict in elements_list:
        result.crt_a_element(_dict_to_element(element_dict))

    return result
