
from typing import *
from typing_extensions import *

num_type: TypeAlias = Union[int, float]


class CircuitElementData(TypedDict):
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
