import time
import json
import pathlib
from physicsLab import errors
from physicsLab.utils import find_path_of_sav_name
from physicsLab import coordinate_system
from physicsLab.enums import Category
from physicsLab.web import User, anonymous_login
from . import planets
from ._status_save import CelestialStatusSave
from ._base import CelestialBase
from physicsLab._typing import Self, Optional, Tuple
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

    def get_element_by_position(
        self, position: coordinate_system.Position
    ) -> CelestialBase:
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


def _dict_to_element(element_dict: dict) -> CelestialBase:
    model_id = element_dict["Model"]
    identifier = element_dict["Identifier"]
    position = coordinate_system.construct_position_from_plsav_str(
        element_dict["Position"]
    )
    velocity = coordinate_system.construct_velocity_from_plsav_str(
        element_dict["Velocity"]
    )
    acceleration = coordinate_system.construct_acceleration_from_plsav_str(
        element_dict["Acceleration"]
    )

    if model_id == "Mercury":
        return planets.Mercury(position, velocity, acceleration, identifier)
    elif model_id == "Venus":
        return planets.Venus(position, velocity, acceleration, identifier)
    elif model_id == "Earth":
        return planets.Earth(position, velocity, acceleration, identifier)
    elif model_id == "Mars":
        return planets.Mars(position, velocity, acceleration, identifier)
    elif model_id == "Jupiter":
        return planets.Jupiter(position, velocity, acceleration, identifier)
    elif model_id == "Saturn":
        return planets.Saturn(position, velocity, acceleration, identifier)
    elif model_id == "Uranus":
        return planets.Uranus(position, velocity, acceleration, identifier)
    elif model_id == "Neptune":
        return planets.Neptune(position, velocity, acceleration, identifier)
    elif model_id == "Pluto":
        return planets.Pluto(position, velocity, acceleration, identifier)
    elif model_id == "Sun":
        return planets.Sun(position, velocity, acceleration, identifier)
    elif model_id == "Blue Giant":
        return planets.BlueGiant(position, velocity, acceleration, identifier)
    elif model_id == "Red Giant":
        return planets.RedGiant(position, velocity, acceleration, identifier)
    elif model_id == "Red Dwarf":
        return planets.RedDwarf(position, velocity, acceleration, identifier)
    elif model_id == "White Dwarf":
        return planets.WhiteDwarf(position, velocity, acceleration, identifier)
    elif model_id == "Blackhole":
        return planets.Blackhole(position, velocity, acceleration, identifier)
    elif model_id == "Fantasy Star":
        return planets.FantasyStar(position, velocity, acceleration, identifier)
    elif model_id == "Moon":
        return planets.Moon(position, velocity, acceleration, identifier)
    elif model_id == "Chocolate Ball":
        return planets.ChocolateBall(position, velocity, acceleration, identifier)
    elif model_id == "Continential":
        return planets.Continential(position, velocity, acceleration, identifier)
    elif model_id == "Arctic":
        return planets.Arctic(position, velocity, acceleration, identifier)
    elif model_id == "Arid":
        return planets.Arid(position, velocity, acceleration, identifier)
    elif model_id == "Barren":
        return planets.Barren(position, velocity, acceleration, identifier)
    elif model_id == "Desert":
        return planets.Desert(position, velocity, acceleration, identifier)
    elif model_id == "Jungle":
        return planets.Jungle(position, velocity, acceleration, identifier)
    elif model_id == "Toxic":
        return planets.Toxic(position, velocity, acceleration, identifier)
    elif model_id == "Lava":
        return planets.Lava(position, velocity, acceleration, identifier)
    elif model_id == "Ocean":
        return planets.Ocean(position, velocity, acceleration, identifier)
    else:
        errors.unreachable()


def crt_celestial_experiment(name: Optional[str]) -> CelestialExperiment:
    return CelestialExperiment(name)


def load_celestial_experiment_by_file_path(
    path: pathlib.Path,
) -> CelestialExperiment:
    if not isinstance(path, pathlib.Path):
        raise TypeError(
            f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
        )
    if not path.exists() or not path.is_file():
        raise errors.ExperimentNotExistError(f'File "{path}" does not exist')

    with open(path, 'r', encoding='utf-8') as f:
        plasv_dict = json.load(f)
    if plasv_dict["Type"] != 3:
        raise errors.ExperimentTypeError(
            f'"{path}" does not contain a celestial experiment'
        )

    summary_dict = plasv_dict["Summary"]
    if summary_dict is None:
        subject = None
    else:
        subject = summary_dict["Subject"]
    result = CelestialExperiment(subject)

    if "Experiment" in plasv_dict.keys():
        status_save_list = json.loads(plasv_dict["Experiment"]["StatusSave"])[
            "Elements"
        ]
        for element_dict in status_save_list.values():
            result.crt_a_element(_dict_to_element(element_dict))

        return result
    else:
        status_save_list = json.loads(plasv_dict["StatusSave"])["Elements"]
        for element_dict in status_save_list.values():
            result.crt_a_element(_dict_to_element(element_dict))

        return result


def load_celestial_experiment_by_sav_name(
    sav_name: str,
) -> Tuple[CelestialExperiment, pathlib.Path]:
    file = find_path_of_sav_name(sav_name)
    if file is None:
        raise errors.ExperimentNotExistError(
            f'Experiment with name "{sav_name}" does not exist'
        )

    return load_celestial_experiment_by_file_path(file), file


def load_celestial_experiment_from_app(
    content_id: str, category: Category, user: User = anonymous_login()
) -> CelestialExperiment:
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

    if _experiment["Type"] != 3:
        raise errors.ExperimentTypeError(
            f'Content ID "{content_id}" does not correspond to a celestial experiment'
        )

    result = CelestialExperiment(_summary["Subject"])

    status_save_dict = json.loads(_experiment["StatusSave"])
    elements_list = status_save_dict["Elements"]
    for element_dict in elements_list.values():
        result.crt_a_element(_dict_to_element(element_dict))

    return result
