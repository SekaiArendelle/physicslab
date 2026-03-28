from ._base import CircuitBase
from .wire import WireInfo
from .pin import Pin
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
        return self.__elements[index]

    def get_element_by_id(self, identifier: str) -> CircuitBase:
        if not isinstance(identifier, str):
            raise TypeError(
                f"parameter identifier must be of type `str`, but got value {identifier} of type {type(identifier).__name__}"
            )
        return self.__id2element[identifier]

    def get_element_by_position(
        self, position: coordinate_system.Position
    ) -> CircuitBase:
        if not isinstance(position, coordinate_system.Position):
            raise TypeError(
                f"parameter position must be of type `Position`, but got value {position} of type {type(position).__name__}"
            )
        return self.__position2element[position]

    def as_dict(self) -> dict:
        return {
            "SimulationSpeed": 1.0,
            "Elements": [],
            "Wires": [],
        }
