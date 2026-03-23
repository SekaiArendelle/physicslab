import json
from enum import Enum, unique
from physicsLab._typing import num_type
from physicsLab import coordinate_system

@unique
class CameraMode(Enum):
    three_dimensional = 0
    two_dimensional = 1


class CameraSave:
    __camera_mode: CameraMode
    __distance: num_type
    __vision_center: coordinate_system.Position
    __target_rotation: coordinate_system.Rotation

    def __init__(
        self,
        camera_mode: CameraMode,
        distance: num_type,
        vision_center: coordinate_system.Position,
        target_rotation: coordinate_system.Rotation,
    ) -> None:
        self.camera_mode = camera_mode
        self.distance = distance
        self.vision_center = vision_center
        self.target_rotation = target_rotation

    @property
    def camera_mode(self) -> CameraMode:
        return self.__camera_mode

    @camera_mode.setter
    def camera_mode(self, camera_mode: CameraMode) -> None:
        if not isinstance(camera_mode, CameraMode):
            raise TypeError(
                f"camera_mode must be of type `CameraMode`, but got value {camera_mode} of type {type(camera_mode).__name__}"
            )

        self.__camera_mode = camera_mode

    @property
    def distance(self) -> num_type:
        return self.__distance

    @distance.setter
    def distance(self, distance: num_type) -> None:
        if not isinstance(distance, (int, float)):
            raise TypeError(
                f"distance must be of type `int | float`, but got value {distance} of type {type(distance).__name__}"
            )

        self.__distance = distance

    @property
    def vision_center(self) -> coordinate_system.Position:
        return self.__vision_center

    @vision_center.setter
    def vision_center(self, vision_center: coordinate_system.Position) -> None:
        if not isinstance(vision_center, coordinate_system.Position):
            raise TypeError(
                f"vision_center must be of type `Position`, but got value {vision_center} of type {type(vision_center).__name__}"
            )

        self.__vision_center = vision_center

    @property
    def target_rotation(self) -> coordinate_system.Rotation:
        return self.__target_rotation

    @target_rotation.setter
    def target_rotation(self, target_rotation: coordinate_system.Rotation) -> None:
        if not isinstance(target_rotation, coordinate_system.Rotation):
            raise TypeError(
                f"target_rotation must be of type `Rotation`, but got value {target_rotation} of type {type(target_rotation).__name__}"
            )

        self.__target_rotation = target_rotation

    def as_dict(self) -> dict:
        return {
            "Mode": self.camera_mode.value,
            "Distance": self.distance,
            "VisionCenter": self.vision_center.as_postion_str_in_plsav(),
            "TargetRotation": self.target_rotation.as_rotation_str_in_plsav(),
        }

    def as_str_in_plsav(self) -> str:
        return json.dumps(self.as_dict())
