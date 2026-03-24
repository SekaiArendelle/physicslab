import json
from physicsLab._typing import List, Dict, Optional, Any
from . import _base


class CelestialStatusSave:
    __elements: List[_base.CelestialBase]
    __id2element: Dict[str, _base.CelestialBase]

    main_identifier: Optional[str]
    world_time: float
    scaling_name: str
    length_scale: float
    size_linear: float
    size_nonlinear: float
    star_present: bool

    def __init__(self) -> None:
        self.__elements = []
        self.__id2element = {}

        self.main_identifier = None
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

    def append_element(self, element: _base.CelestialBase) -> None:
        if not isinstance(element, _base.CelestialBase):
            raise TypeError(
                f"parameter element must be of type `CelestialBase`, but got value {element} of type {type(element).__name__}"
            )
        self.__elements.append(element)
        self.__id2element[element.identifier] = element

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

    def get_element_by_id(self, identifier: str) -> _base.CelestialBase:
        if not isinstance(identifier, str):
            raise TypeError(
                f"parameter identifier must be of type `str`, but got value {identifier} of type {type(identifier).__name__}"
            )
        return self.__id2element[identifier]

    def as_dict(self) -> dict:
        return {
            "MainIdentifier": self.main_identifier,
            "Elements": {e.identifier: e.as_dict() for e in self.elements},
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