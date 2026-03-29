"""Python API for Physics-Lab-AR"""

from .version import __version__

from .coordinate_system import *

from .enums import ExperimentType, Category, Tag, OpenMode, ColorOfWire, GetUserMode

from .circuit import *
from .celestial import *
from .electromagnetism import *

from .errors import *

from physicsLab.quantum_physics import *
from physicsLab.utils import *

from physicsLab import web
