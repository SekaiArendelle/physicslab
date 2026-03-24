import time
import json
import pathlib
from physicsLab import coordinate_system
from ._status_save import CelestialStatusSave
from ._base import CelestialBase
from physicsLab._typing import Self, Optional
from physicsLab._camera_save import CameraMode, CameraSave


class CelestialExperiment:
    __name: Optional[str]
    __status_save: CelestialStatusSave
    __camera_save: CameraSave

    def __init__(
        self,
        name: Optional[str],
        camera_save: CameraSave = CameraSave(
            CameraMode.celestial_mode,
            4.52230835,
            coordinate_system.Position(0, 0, 1.083),
            coordinate_system.Rotation(90, 0, 0),
        ),
    ) -> None:
        self.name = name
        self.status_save = CelestialStatusSave()
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
    def status_save(self) -> CelestialStatusSave:
        return self.__status_save

    @status_save.setter
    def status_save(self, status_save: CelestialStatusSave) -> None:
        if not isinstance(status_save, CelestialStatusSave):
            raise TypeError(
                f"status_save must be of type `CelestialStatusSave`, but got value {status_save} of type {type(status_save).__name__}"
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

    def crt_a_element(self, element: CelestialBase) -> Self:
        self.status_save.append_element(element)

        return self

    def crt_elements(self, *elements: CelestialBase) -> Self:
        for element in elements:
            self.crt_a_element(element)

        return self

    def del_a_element(self, element: CelestialBase) -> Self:
        self.status_save.remove_element(element)

        return self

    def get_elements_count(self) -> int:
        return len(self.status_save.elements)

    def get_element_by_index(self, index: int) -> CelestialBase:
        return self.status_save.get_element_by_index(index)

    def get_element_by_id(self, identifier: str) -> CelestialBase:
        return self.status_save.get_element_by_id(identifier)

    def get_element_by_position(self, position: coordinate_system.Position) -> CelestialBase:
        return self.status_save.get_element_by_position(position)

    def as_plsav_dict(self) -> dict:
        return {
            "Type": 3,
            "Experiment": {
                "ID": None,
                "Type": 3,
                "Components": self.get_elements_count(),
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
                "Type": 3,
                "ParentID": None,
                "ParentName": None,
                "ParentCategory": None,
                "ContentID": None,
                "Editor": None,
                "Coauthors": [],
                "Description": None,
                "LocalizedDescription": None,
                "Tags": ["Type-3"],
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
            "SpeedMaximum": 10.0,
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

    def merge(self, other: "CelestialExperiment") -> Self:
        if not isinstance(other, CelestialExperiment):
            raise TypeError(
                f"parameter other must be of type `CelestialExperiment`, but got value {other} of type {type(other).__name__}"
            )

        self.status_save.append_range(other.status_save)

        return self
