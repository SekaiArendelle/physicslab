
"""
Undirected Graph Implementation

This module provides an implementation of an undirected graph data structure
using an adjacency list representation. It includes classes for representing
nodes and edges, as well as exceptions for handling graph operations.

The UndirectedGraph class supports operations such as adding/removing nodes
and edges, checking for existence of nodes and edges, and iterating over
graph elements. It also provides utility methods for getting node degrees,
counting nodes and edges, and creating copies of the graph.

Url: https://github.com/SekaiArendelle/undirected_graph_py.git
"""

import copy
from typing import Generic, TypeVar, Dict, Iterator, Tuple, Set


class InvalidEdgeError(Exception):
    """Exception raised when trying to add an edge that already exists in the graph."""

    __err_msg: str

    def __init__(self, err_msg: str) -> None:
        self.__err_msg = err_msg

    def __str__(self) -> str:
        return self.__err_msg


class NodeExistsError(Exception):
    """Exception raised when trying to add a node that already exists in the graph."""

    __err_msg: str

    def __init__(self, err_msg: str) -> None:
        self.__err_msg = err_msg

    def __str__(self) -> str:
        return self.__err_msg


class NodeNotExistsError(Exception):
    """Exception raised when trying to access a node that doesn't exist in the graph."""

    __err_msg: str

    def __init__(self, err_msg: str) -> None:
        self.__err_msg = err_msg

    def __str__(self) -> str:
        return self.__err_msg


class EdgeExistsError(Exception):
    """Exception raised when trying to add an edge that already exists in the graph."""

    __err_msg: str

    def __init__(self, err_msg: str) -> None:
        self.__err_msg = err_msg

    def __str__(self) -> str:
        return self.__err_msg


class EdgeNotExistsError(Exception):
    """Exception raised when trying to access an edge that doesn't exist in the graph."""

    __err_msg: str

    def __init__(self, err_msg: str) -> None:
        self.__err_msg = err_msg

    def __str__(self) -> str:
        return self.__err_msg


_Node = TypeVar("_Node")
_Edge = TypeVar("_Edge")


class UndirectedGraph(Generic[_Node, _Edge]):
    """An undirected graph implementation using an adjacency list representation."""

    _adjacency_list: Dict[_Node, Dict[_Node, _Edge]]
    # to speed up calculating counting edges
    _count_edges: int

    def __init__(self) -> None:
        """Initialize an empty undirected graph."""
        self._adjacency_list = {}
        self._count_edges = 0

    def __contains__(self, node: _Node) -> bool:
        """Check if a node exists in the graph.

        Args:
            node: The node to check for existence

        Returns:
            True if the node exists in the graph, False otherwise
        """
        return node in self._adjacency_list

    def __len__(self) -> int:
        """Get the number of nodes in the graph.

        Returns:
            The number of nodes in the graph
        """
        return len(self._adjacency_list)

    def __repr__(self) -> str:
        """Return a string representation of the graph.

        Returns:
            A string representation showing the graph's edges
        """
        cls = self.__class__.__name__
        return f"{cls}({list(self.edges())})"

    def __deepcopy__(self, memo) -> "UndirectedGraph":
        """Create a deep copy of the graph.

        Args:
            memo: A dictionary to track already copied objects

        Returns:
            A deep copy of the graph
        """
        if id(self) in memo:
            return memo[id(self)]
        return self.copy()

    def copy(self) -> "UndirectedGraph":
        """Create a shallow copy of the graph.

        Returns:
            A shallow copy of the graph
        """
        result = UndirectedGraph()
        result._adjacency_list = copy.deepcopy(self._adjacency_list)
        result._count_edges = self._count_edges
        return result

    def swap(self, other: "UndirectedGraph") -> None:
        """Swap the contents of this graph with another graph.

        Args:
            other: Another UndirectedGraph instance to swap with
        """
        self._adjacency_list, other._adjacency_list = (
            other._adjacency_list,
            self._adjacency_list,
        )
        self._count_edges, other._count_edges = other._count_edges, self._count_edges

    def empty(self) -> bool:
        """Check if the graph is empty.

        Returns:
            True if the graph has no nodes, False otherwise
        """
        return self._adjacency_list == {}

    def add_node(self, node: _Node) -> None:
        """Add a node to the graph.

        Args:
            node: The node to add to the graph

        Raises:
            NodeExistsError: If the node already exists in the graph
        """
        if node in self._adjacency_list:
            raise NodeExistsError(f"Node {node} already exists")
        self._adjacency_list[node] = {}

    def remove_node(self, node: _Node) -> None:
        """Remove a node and all its edges from the graph.

        Args:
            node: The node to remove from the graph

        Raises:
            NodeNotExistsError: If the node doesn't exist in the graph
        """
        if node not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node} does not exist")

        for neighbor in self._adjacency_list[node]:
            self._adjacency_list[neighbor].pop(node)
        self._count_edges -= len(self._adjacency_list[node])
        self._adjacency_list.pop(node)

    def construct_edge(self, node1: _Node, node2: _Node, edge: _Edge) -> None:
        """Add a new edge between two nodes in the graph.

        Args:
            node1: The first node
            node2: The second node
            edge: The edge data to associate with the connection

        Raises:
            NodeNotExistsError: If either node doesn't exist in the graph
            EdgeExistsError: If an edge already exists between these nodes
            InvalidEdgeError: If the node1 and node2 are the same node
        """
        if node1 not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node1} does not exist")
        if node2 not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node2} does not exist")
        if node2 in self._adjacency_list[node1]:
            raise EdgeExistsError(f"Edge {node1} <-> {node2} already exists")
        assert node1 not in self._adjacency_list[node2]
        if node1 == node2:
            raise InvalidEdgeError("Cannot add self-loop edge")

        self._adjacency_list[node1][node2] = edge
        self._adjacency_list[node2][node1] = edge

        self._count_edges += 1

    def assign_edge(self, node1: _Node, node2: _Node, edge: _Edge) -> None:
        """Update the edge data between two existing nodes.

        Args:
            node1: The first node
            node2: The second node
            edge: The new edge data to associate with the connection

        Raises:
            NodeNotExistsError: If either node doesn't exist in the graph
            EdgeNotExistsError: If no edge exists between these nodes
            InvalidEdgeError: If the node1 and node2 are the same node
        """
        if node1 not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node1} does not exist")
        if node2 not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node2} does not exist")
        if node1 not in self._adjacency_list[node2]:
            raise EdgeNotExistsError(f"Edge {node1} <-> {node2} does not exist")
        assert node2 in self._adjacency_list[node1]
        if node1 == node2:
            raise InvalidEdgeError(f"Edge {node1} <-> {node2} already exists")

        self._adjacency_list[node1][node2] = edge
        self._adjacency_list[node2][node1] = edge

    def remove_edge(self, node1: _Node, node2: _Node) -> None:
        """Remove an edge between two nodes.

        Args:
            node1: The first node
            node2: The second node

        Raises:
            NodeNotExistsError: If either node doesn't exist in the graph
            EdgeNotExistsError: If no edge exists between these nodes
        """
        if node1 not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node1} does not exist")
        if node2 not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node2} does not exist")
        if node1 not in self._adjacency_list[node2]:
            raise EdgeNotExistsError(f"Edge {node1} <-> {node2} does not exist")
        assert node2 in self._adjacency_list[node1]
        assert node1 != node2

        self._adjacency_list[node1].pop(node2)
        self._adjacency_list[node2].pop(node1)

        self._count_edges -= 1

    def has_edge(self, node1: _Node, node2: _Node) -> bool:
        """Check if edge exists between two nodes.

        Args:
            node1: The first node
            node2: The second node

        Returns:
            True if edge exists between node1 and node2, False otherwise
        """
        return node1 in self._adjacency_list and node2 in self._adjacency_list[node1]

    def clear(self) -> None:
        """Remove all nodes and edges from the graph."""
        self._adjacency_list.clear()
        self._count_edges = 0

    def count_nodes(self) -> int:
        """Count the number of nodes in the graph.

        Returns:
            The number of nodes in the graph
        """
        return len(self._adjacency_list)

    def count_edges(self) -> int:
        """Count the number of edges in the graph.

        Returns:
            The number of edges in the graph
        """
        assert self._count_edges >= 0
        return self._count_edges

    def degree(self, node: _Node) -> int:
        """Get the degree of a node (number of edges connected to it).

        Args:
            node: The node to get the degree for

        Returns:
            The degree of the node

        Raises:
            NodeNotExistsError: If the node doesn't exist in the graph
        """
        if node not in self._adjacency_list:
            raise NodeNotExistsError(f"Node {node} not in graph")

        return len(self._adjacency_list[node])

    def nodes(self) -> Iterator[_Node]:
        """Get an iterator over all nodes in the graph.

        Returns:
            An iterator over all nodes
        """
        return iter(self._adjacency_list.keys())

    def edges(self) -> Iterator[Tuple[_Node, _Node, _Edge]]:
        """Get an iterator over all edges in the graph.

        Returns:
            An iterator over tuples of (node1, node2, edge_data)
        """
        _seen: Set[Tuple[_Node, _Node]] = set()
        for _node in self._adjacency_list.keys():
            for _neighbor in self._adjacency_list[_node]:
                if (_node, _neighbor) not in _seen and (_neighbor, _node) not in _seen:
                    _seen.add((_node, _neighbor))
                    yield _node, _neighbor, self._adjacency_list[_node][_neighbor]

    def neighbors(self, node: _Node) -> Iterator[_Node]:
        """Get an iterator over the neighbors of a node.

        Args:
            node: The node to get neighbors for

        Returns:
            An iterator over neighboring nodes
        """
        return iter(self._adjacency_list[node])
