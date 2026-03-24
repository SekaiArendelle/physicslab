import uuid
import json
from physicsLab import coordinate_system
from physicsLab._typing import List, Dict, num_type
from . import _base


class CelestialStatusSave:
    __elements: List[_base.CelestialBase]
    __id2element: Dict[str, _base.CelestialBase]
    __position2element: Dict[coordinate_system.Position, _base.CelestialBase]

    __main_identifier: str
    __world_time: num_type
    __scaling_name: str
    __length_scale: num_type
    __size_linear: num_type
    __size_nonlinear: num_type
    __star_present: bool

    def __init__(self, main_identifier: str = str(uuid.uuid4())) -> None:
        self.__elements = []
        self.__id2element = {}
        self.__position2element = {}

        self.main_identifier = main_identifier
        self.world_time = 0.0
        self.scaling_name = "内太阳系"
        self.length_scale = 1.0
        self.size_linear = 0.0001
        self.size_nonlinear = 0.5
        self.star_present = True

    @property
    def elements(self) -> List[_base.CelestialBase]:
        return self.__elements

    @property
    def id2element(self) -> Dict[str, _base.CelestialBase]:
        return self.__id2element

    @property
    def position2element(self) -> Dict[coordinate_system.Position, _base.CelestialBase]:
        return self.__position2element

    @property
    def main_identifier(self) -> str:
        return self.__main_identifier

    @main_identifier.setter
    def main_identifier(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"main_identifier must be of type `str`, but got value {value} of type {type(value).__name__}"
            )
        self.__main_identifier = value

    @property
    def world_time(self) -> float:
        return self.__world_time

    @world_time.setter
    def world_time(self, value: num_type) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"world_time must be of type `float | int`, but got value {value} of type {type(value).__name__}"
            )

        self.__world_time = value

    @property
    def scaling_name(self) -> str:
        return self.__scaling_name

    @scaling_name.setter
    def scaling_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"scaling_name must be of type `str`, but got value {value} of type {type(value).__name__}"
            )

        self.__scaling_name = value

    @property
    def length_scale(self) -> float:
        return self.__length_scale

    @length_scale.setter
    def length_scale(self, value: num_type) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"length_scale must be of type `float | int`, but got value {value} of type {type(value).__name__}"
            )

        self.__length_scale = value

    @property
    def size_linear(self) -> float:
        return self.__size_linear

    @size_linear.setter
    def size_linear(self, value: num_type) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"size_linear must be of type `float | int`, but got value {value} of type {type(value).__name__}"
            )

        self.__size_linear = value

    @property
    def size_nonlinear(self) -> float:
        return self.__size_nonlinear

    @size_nonlinear.setter
    def size_nonlinear(self, value: num_type) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"size_nonlinear must be of type `float | int`, but got value {value} of type {type(value).__name__}"
            )

        self.__size_nonlinear = value

    @property
    def star_present(self) -> bool:
        return self.__star_present

    @star_present.setter
    def star_present(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"star_present must be of type `bool`, but got value {value} of type {type(value).__name__}"
            )

        self.__star_present = value

    def append_element(self, element: _base.CelestialBase) -> None:
        if not isinstance(element, _base.CelestialBase):
            raise TypeError(
                f"parameter element must be of type `CelestialBase`, but got value {element} of type {type(element).__name__}"
            )
        self.__elements.append(element)
        self.__id2element[element.identifier] = element
        self.__position2element[element.position] = element

    def append_range(self, other: "CelestialStatusSave") -> None:
        if not isinstance(other, CelestialStatusSave):
            raise TypeError(
                f"parameter other must be of type `CelestialStatusSave`, but got value {other} of type {type(other).__name__}"
            )
        for element in other.elements:
            self.append_element(element)

    def remove_element(self, element: _base.CelestialBase) -> None:
        if not isinstance(element, _base.CelestialBase):
            raise TypeError(
                f"parameter element must be of type `CelestialBase`, but got value {element} of type {type(element).__name__}"
            )
        self.__elements.remove(element)
        del self.__id2element[element.identifier]
        del self.__position2element[element.position]

    def get_element_by_index(self, index: int) -> _base.CelestialBase:
        if not isinstance(index, int):
            raise TypeError(
                f"parameter index must be of type `int`, but got value {index} of type {type(index).__name__}"
            )
        return self.__elements[index]

    def get_element_by_id(self, identifier: str) -> _base.CelestialBase:
        if not isinstance(identifier, str):
            raise TypeError(
                f"parameter identifier must be of type `str`, but got value {identifier} of type {type(identifier).__name__}"
            )
        return self.__id2element[identifier]

    def get_element_by_position(
        self, position: coordinate_system.Position
    ) -> _base.CelestialBase:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"parameter position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )
        return self.__position2element[position]

    def as_dict(self) -> dict:
        return {
            "MainIdentifier": self.main_identifier,
            "Elements": {
                element.identifier: element.as_dict() for element in self.elements
            },
            "WorldTime": self.world_time,
            "ScalingName": self.scaling_name,
            "LengthScale": self.length_scale,
            "SizeLinear": self.size_linear,
            "SizeNonlinear": self.size_nonlinear,
            "StarPresent": self.star_present,
            "Setting": None,
        }

    def as_str_in_plsav(self) -> str:
        return json.dumps(self.as_dict())
