"""Shared typing aliases and TypedDict definitions used across physicslab."""

from typing import *
from typing_extensions import * # type: ignore

num_type: TypeAlias = Union[int, float]


class CircuitElementData(TypedDict):
    """TypedDict representing the raw JSON structure of a circuit element."""

    ModelID: str
    IsBroken: bool
    IsLocked: bool
    Identifier: str
    Properties: Dict[Any, Any]
    Statistics: Dict[Any, Any]
    Position: str
    Rotation: str
    DiagramCached: bool
    DiagramPosition: Dict[Any, Any]
    DiagramRotation: int
    Label: Optional[str]
