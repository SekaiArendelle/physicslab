"""Save-state container for celestial experiment elements and simulation settings."""

import uuid
import json
from physicslab import coordinate_system
from physicslab import errors
from physicslab._typing import List, Dict, num_type
from . import _base


class CelestialStatusSave:
    """Manages a collection of celestial elements and their simulation settings."""

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
        """Returns the list of all celestial elements."""
        return self.__elements

    @property
    def id2element(self) -> Dict[str, _base.CelestialBase]:
        """Returns the dict mapping element identifiers to elements."""
        return self.__id2element

    @property
    def position2element(self) -> Dict[coordinate_system.Position, _base.CelestialBase]:
        """Returns the dict mapping element positions to elements."""
        return self.__position2element

    @property
    def main_identifier(self) -> str:
        """Returns the main identifier string of this status save."""
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
        """Returns the simulated world time."""
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
        """Returns the scaling name used for display."""
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
        """Returns the length scale factor."""
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
        """Returns the linear size scale factor."""
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
        """Returns the non-linear size scale factor."""
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
        """Returns whether a star is present in the simulation."""
        return self.__star_present

    @star_present.setter
    def star_present(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(
                f"star_present must be of type `bool`, but got value {value} of type {type(value).__name__}"
            )

        self.__star_present = value

    def append_element(self, element: _base.CelestialBase) -> None:
        """Appends a celestial element to the collection.

        Args:
            element: The celestial element to add.

        Raises:
            TypeError: If element is not a CelestialBase instance.
            ElementExistError: If an element with the same identifier already exists.
        """
        if not isinstance(element, _base.CelestialBase):
            raise TypeError(
                f"parameter element must be of type `CelestialBase`, but got value {element} of type {type(element).__name__}"
            )
        if element.identifier in self.id2element:
            raise errors.ElementExistError(
                f"An element with the same identifier already exists, identifier: {element.identifier}"
            )
        self.elements.append(element)
        self.id2element[element.identifier] = element
        self.position2element[element.position] = element

    def append_range(self, other: "CelestialStatusSave") -> None:
        """Appends all elements from another CelestialStatusSave instance.

        Args:
            other: The CelestialStatusSave whose elements to merge in.

        Raises:
            TypeError: If other is not a CelestialStatusSave instance.
        """
        if not isinstance(other, CelestialStatusSave):
            raise TypeError(
                f"parameter other must be of type `CelestialStatusSave`, but got value {other} of type {type(other).__name__}"
            )
        for element in other.elements:
            self.append_element(element)

    def remove_element(self, element: _base.CelestialBase) -> None:
        """Removes a celestial element from the collection.

        Args:
            element: The celestial element to remove.

        Raises:
            TypeError: If element is not a CelestialBase instance.
        """
        if not isinstance(element, _base.CelestialBase):
            raise TypeError(
                f"parameter element must be of type `CelestialBase`, but got value {element} of type {type(element).__name__}"
            )
        self.elements.remove(element)
        del self.id2element[element.identifier]
        del self.position2element[element.position]

    def get_element_by_index(self, index: int) -> _base.CelestialBase:
        """Returns the celestial element at the given index.

        Args:
            index: Zero-based index into the elements list.

        Returns:
            The CelestialBase element at the specified index.

        Raises:
            TypeError: If index is not an int.
            ElementNotExistError: If index is out of range.
        """
        if not isinstance(index, int):
            raise TypeError(
                f"parameter index must be of type `int`, but got value {index} of type {type(index).__name__}"
            )
        if index >= len(self.elements) or index < -len(self.elements):
            raise errors.ElementNotExistError(
                f"parameter index out of range, index: {index}, but elements count is {len(self.elements)}"
            )

        return self.elements[index]

    def get_element_by_id(self, identifier: str) -> _base.CelestialBase:
        """Returns the celestial element with the given identifier.

        Args:
            identifier: The string identifier to look up.

        Returns:
            The CelestialBase element with the specified identifier.

        Raises:
            TypeError: If identifier is not a str.
            ElementNotExistError: If no element has the given identifier.
        """
        if not isinstance(identifier, str):
            raise TypeError(
                f"parameter identifier must be of type `str`, but got value {identifier} of type {type(identifier).__name__}"
            )
        if identifier not in self.id2element:
            raise errors.ElementNotExistError(
                f"Can't find element with identifier {identifier}"
            )

        return self.id2element[identifier]

    def get_element_by_position(
        self, position: coordinate_system.Position
    ) -> _base.CelestialBase:
        """Returns the celestial element at the given position.

        Args:
            position: The Position to look up.

        Returns:
            The CelestialBase element at the specified position.

        Raises:
            TypeError: If position is not a Position instance.
            ElementNotExistError: If no element is at the given position.
        """
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"parameter position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )
        if position not in self.position2element:
            raise errors.ElementNotExistError(
                f"Can't find element with position {position}"
            )

        return self.position2element[position]

    def as_dict(self) -> dict:
        """Returns a dict representation of this status save for use in a .plsav file."""
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
        """Returns the JSON string representation for embedding in a .plsav file."""
        return json.dumps(self.as_dict())
