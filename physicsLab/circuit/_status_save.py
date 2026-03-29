import json
from physicsLab import errors
from ._base import CircuitBase, Pin
from .wire import WireInfo
from physicsLab import coordinate_system
from physicsLab._typing import List, Dict
from physicsLab.vendor import undirected_graph


class CircuitStatusSave:
    __elements: List[CircuitBase]
    __id2element: Dict[str, CircuitBase]
    __position2element: Dict[coordinate_system.Position, CircuitBase]
    __circuit_graph: undirected_graph.UndirectedGraph[Pin, WireInfo]

    def __init__(self) -> None:
        self.__elements = []
        self.__id2element = {}
        self.__position2element = {}
        self.__circuit_graph = undirected_graph.UndirectedGraph()

    @property
    def elements(self) -> List[CircuitBase]:
        return self.__elements

    @property
    def id2element(self) -> Dict[str, CircuitBase]:
        return self.__id2element

    @property
    def position2element(self) -> Dict[coordinate_system.Position, CircuitBase]:
        return self.__position2element

    @property
    def circuit_graph(self) -> undirected_graph.UndirectedGraph[Pin, WireInfo]:
        return self.__circuit_graph

    def get_element_by_index(self, index: int) -> CircuitBase:
        if not isinstance(index, int):
            raise TypeError(
                f"parameter index must be of type `int`, but got value {index} of type {type(index).__name__}"
            )
        if index >= len(self.elements) or index < -len(self.elements):
            raise errors.ElementNotExistError(
                f"parameter index out of range, index: {index}, but elements count is {len(self.elements)}"
            )

        return self.elements[index]

    def get_element_by_id(self, identifier: str) -> CircuitBase:
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
    ) -> CircuitBase:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"parameter position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )
        if position not in self.position2element:
            raise errors.ElementNotExistError(
                f"Can't find element with position {position}"
            )

        return self.position2element[position]

    def append_element(self, element: CircuitBase) -> None:
        if not isinstance(element, CircuitBase):
            raise TypeError(
                f"parameter element must be of type `CircuitBase`, but got value {element} of type {type(element).__name__}"
            )
        if element.identifier in self.id2element:
            raise errors.ElementExistError(
                f"element with identifier {element.identifier} already exists"
            )
        self.elements.append(element)
        self.id2element[element.identifier] = element
        self.position2element[element.position] = element

    def append_wire(
        self, source_pin: Pin, target_pin: Pin, wire_info: WireInfo
    ) -> None:
        if not isinstance(source_pin, Pin):
            raise TypeError(
                f"parameter source_pin must be of type `Pin`, but got value {source_pin} of type {type(source_pin).__name__}"
            )
        if not isinstance(target_pin, Pin):
            raise TypeError(
                f"parameter target_pin must be of type `Pin`, but got value {target_pin} of type {type(target_pin).__name__}"
            )
        if not isinstance(wire_info, WireInfo):
            raise TypeError(
                f"parameter wire_info must be of type `WireInfo`, but got value {wire_info} of type {type(wire_info).__name__}"
            )
        if self.circuit_graph.has_edge(source_pin, target_pin):
            raise ValueError(
                f"There is already a wire between source_pin {source_pin} and target_pin {target_pin}"
            )

        if source_pin not in self.circuit_graph:
            self.circuit_graph.add_node(source_pin)
        if target_pin not in self.circuit_graph:
            self.circuit_graph.add_node(target_pin)

        self.circuit_graph.construct_edge(source_pin, target_pin, wire_info)

    def remove_element(self, element: CircuitBase) -> None:
        if not isinstance(element, CircuitBase):
            raise TypeError(
                f"parameter element must be of type `CircuitBase`, but got value {element} of type {type(element).__name__}"
            )
        self.elements.remove(element)
        del self.id2element[element.identifier]
        del self.position2element[element.position]

        need_remove_pins: List[Pin] = [
            pin for pin in self.circuit_graph.nodes() if pin.element == element
        ]
        for pin in need_remove_pins:
            self.circuit_graph.remove_node(pin)

    def remove_wire(self, source_pin: Pin, target_pin: Pin) -> None:
        if not isinstance(source_pin, Pin):
            raise TypeError(
                f"parameter source_pin must be of type `Pin`, but got value {source_pin} of type {type(source_pin).__name__}"
            )
        if not isinstance(target_pin, Pin):
            raise TypeError(
                f"parameter target_pin must be of type `Pin`, but got value {target_pin} of type {type(target_pin).__name__}"
            )
        if not self.circuit_graph.has_edge(source_pin, target_pin):
            raise ValueError(
                f"There is no wire between source_pin {source_pin} and target_pin {target_pin}"
            )

        self.circuit_graph.remove_edge(source_pin, target_pin)

    def append_range(self, other: "CircuitStatusSave") -> None:
        if not isinstance(other, CircuitStatusSave):
            raise TypeError(
                f"parameter other must be of type `CircuitStatusSave`, but got value {other} of type {type(other).__name__}"
            )

        for element in other.elements:
            self.append_element(element)
        for source_pin, target_pin, wire_info in other.circuit_graph.edges():
            self.append_wire(source_pin, target_pin, wire_info)

    def as_dict(self) -> dict:
        return {
            "SimulationSpeed": 1.0,
            "Elements": [element.as_dict() for element in self.elements],
            "Wires": [
                {
                    "Source": source_pin.element.identifier,
                    "SourcePin": source_pin.pin_label,
                    "Target": target_pin.element.identifier,
                    "TargetPin": target_pin.pin_label,
                    "ColorName": f"{wire_info.color.value}色导线",
                }
                for source_pin, target_pin, wire_info in self.circuit_graph.edges()
            ],
        }

    def as_str_in_plsav(self) -> str:
        return json.dumps(self.as_dict())
