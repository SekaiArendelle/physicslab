"""Runtime state storage for an electromagnetism experiment."""

import json
from physicsLab import coordinate_system
from physicsLab import errors
from physicsLab._typing import List, Dict
from . import _base


class ElectromagnetismStatusSave:
    """Stores the runtime state of an electromagnetism experiment (elements, look-ups)."""

    __elements: List[_base.ElectromagnetismBase]
    __id2element: Dict[str, _base.ElectromagnetismBase]
    __position2element: Dict[coordinate_system.Position, _base.ElectromagnetismBase]

    def __init__(self) -> None:
        self.__elements = []
        self.__id2element = {}
        self.__position2element = {}

    @property
    def elements(self) -> List[_base.ElectromagnetismBase]:
        """Ordered list of all elements in the experiment."""
        return self.__elements

    @property
    def id2element(self) -> Dict[str, _base.ElectromagnetismBase]:
        """Mapping from element identifier to element instance."""
        return self.__id2element

    @property
    def position2element(
        self,
    ) -> Dict[coordinate_system.Position, _base.ElectromagnetismBase]:
        """Mapping from position to element instance."""
        return self.__position2element

    def append_element(self, element: _base.ElectromagnetismBase) -> None:
        """Add a new element to the experiment state.

        Args:
            element: The element to add.

        Raises:
            TypeError: If *element* is not an ``ElectromagnetismBase`` instance.
            ElementExistError: If an element with the same identifier already exists.
        """
        if not isinstance(element, _base.ElectromagnetismBase):
            raise TypeError(
                f"parameter element must be of type `ElectromagnetismBase`, but got value {element} of type {type(element).__name__}"
            )
        if element.identifier in self.id2element:
            raise errors.ElementExistError(
                f"An element with identifier {element.identifier} already exists"
            )
        self.elements.append(element)
        self.id2element[element.identifier] = element
        self.position2element[element.position] = element

    def append_range(self, other: "ElectromagnetismStatusSave") -> None:
        """Merge all elements from *other* into this status save."""
        if not isinstance(other, ElectromagnetismStatusSave):
            raise TypeError(
                f"parameter other must be of type `ElectromagnetismStatusSave`, but got value {other} of type {type(other).__name__}"
            )
        for element in other.elements:
            self.append_element(element)

    def remove_element(self, element: _base.ElectromagnetismBase) -> None:
        """Remove an element from the experiment state."""
        if not isinstance(element, _base.ElectromagnetismBase):
            raise TypeError(
                f"parameter element must be of type `ElectromagnetismBase`, but got value {element} of type {type(element).__name__}"
            )
        self.elements.remove(element)
        del self.id2element[element.identifier]
        del self.position2element[element.position]

    def get_element_by_index(self, index: int) -> _base.ElectromagnetismBase:
        """Return the element at position *index* in the ordered element list."""
        if not isinstance(index, int):
            raise TypeError(
                f"parameter index must be of type `int`, but got value {index} of type {type(index).__name__}"
            )
        if index >= len(self.elements) or index < -len(self.elements):
            raise errors.ElementNotExistError(
                f"parameter index out of range, index: {index}, but elements count is {len(self.elements)}"
            )

        return self.elements[index]

    def get_element_by_id(self, identifier: str) -> _base.ElectromagnetismBase:
        """Return the element with the given *identifier*."""
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
    ) -> _base.ElectromagnetismBase:
        """Return the element located at *position*."""
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
        """Serialise the full experiment status to a plain dictionary."""
        return {
            "SimulationSpeed": 1.0,
            "Elements": [element.as_dict() for element in self.elements],
        }

    def as_str_in_plsav(self) -> str:
        """Serialise the experiment status to a JSON string for a ``.plsav`` file."""
        return json.dumps(self.as_dict())
