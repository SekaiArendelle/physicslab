
from typing import *
from typing_extensions import *

from physicsLab.savTemplate import Generate

num_type: TypeAlias = Union[int, float]


class CircuitElementData(TypedDict):
    ModelID: Union[str, Type[Generate]]
    IsBroken: bool
    IsLocked: bool
    Identifier: Union[str, Type[Generate]]
    Properties: Dict[Any, Any]
    Statistics: Dict[Any, Any]
    Position: Union[str, Type[Generate]]
    Rotation: Union[str, Type[Generate]]
    DiagramCached: bool
    DiagramPosition: Dict[Any, Any]
    DiagramRotation: int
    Label: Optional[str]
