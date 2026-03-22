import json
import time
import pathlib
from physicsLab import errors
from physicsLab import coordinate_system
from . import elements
from ._camera_save import CameraSave
from ._status_save import ElectromagnetismStatusSave
from ._base import ElectromagnetismBase
from physicsLab._typing import Self, Optional

class ElectromagnetismExperiment:
    __name: Optional[str]
    __status_save: ElectromagnetismStatusSave
    __camera_save: CameraSave

    def __init__(self, name: Optional[str], camera_save: CameraSave = CameraSave()) -> None:
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

    def _crt_a_element(self, element: ElectromagnetismBase) -> None:
        self.status_save.append_element(element)

    def crt_elements(self, *elements: ElectromagnetismBase) -> Self:
        for element in elements:
            self._crt_a_element(element)

        return self

    def del_a_element(self, element: ElectromagnetismBase) -> None:
        self.status_save.remove_element(element)

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
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Positive Charge":
        return elements.PositiveCharge(
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Negative Test Charge":
        return elements.NegativeTestCharge(
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Positive Test Charge":
        return elements.PositiveTestCharge(
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Bar Magnet":
        return elements.BarMagnet(
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Compass":
        return elements.Compass(
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    elif model_id == "Uniform Magnetic Field":
        return elements.UniformMagneticField(
            position=coordinate_system.construct_position_from_plsav_str(element_dict["Position"]),
            rotation=coordinate_system.construct_rotation_from_plsav_str(element_dict["Rotation"]),
            identifier=element_dict["Identifier"],
        )
    else:
        errors.unreachable()

def crt_electromagnetism_experiment(name: Optional[str]) -> ElectromagnetismExperiment:
    return ElectromagnetismExperiment(name)

def load_electromagnetism_experiment_by_file_path(path: pathlib.Path) -> ElectromagnetismExperiment:
    if not isinstance(path, pathlib.Path):
        raise TypeError(
            f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
        )

    plasv_dict = json.loads(path.read_text(encoding="utf-8"))
    if plasv_dict["Type"] != 4:
        raise errors.ExperimentTypeError(f"\"{path}\" does not contain an electromagnetism experiment")

    summary_dict = plasv_dict["Summary"]
    if summary_dict is None:
        subject = None
    else:
        subject = summary_dict["Subject"]
    result = ElectromagnetismExperiment(subject)

    if "Experiment" in plasv_dict.keys():
        # tests/data/All-Electromagnetism-Elements.sav
        status_save_list = json.loads(plasv_dict["Experiment"]["StatusSave"])["Elements"]
        for element_dict in status_save_list:
            result._crt_a_element(_dict_to_element(element_dict))

        return result
    else:
        # tests/data/Export-All-Electromagnetism-Elements.sav
        status_save_list = json.loads(plasv_dict["StatusSave"])["Elements"]
        for element_dict in status_save_list:
            result._crt_a_element(_dict_to_element(element_dict))

        return result
