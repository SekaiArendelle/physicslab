"""Concrete electromagnetism element classes (charges, magnets, etc.)."""

import uuid
from physicsLab import coordinate_system
from ._base import ElectromagnetismBase
from physicsLab._typing import Optional


class NegativeCharge(ElectromagnetismBase):
    """A negative point charge element in an electromagnetism experiment."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Negative Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": int(self.lock_status), "强度": -1e-07, "质量": 0.1},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"NegativeCharge("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "负电荷"


class PositiveCharge(ElectromagnetismBase):
    """A positive point charge element in an electromagnetism experiment."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Positive Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": int(self.lock_status), "强度": 1e-07, "质量": 0.1},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"PositiveCharge("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "正电荷"


class NegativeTestCharge(ElectromagnetismBase):
    """A small negative test charge element used to probe electric fields."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = False,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Negative Test Charge",
            "Identifier": self.identifier,
            "Properties": {
                "锁定": int(self.lock_status),
                "强度": -1e-10,
                "质量": 5e-06,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"NegativeTestCharge("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "正试验电荷"


class PositiveTestCharge(ElectromagnetismBase):
    """A small positive test charge element used to probe electric fields."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = False,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Positive Test Charge",
            "Identifier": self.identifier,
            "Properties": {
                "锁定": int(self.lock_status),
                "强度": -1e-10,
                "质量": 5e-06,
            },
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"PositiveTestCharge("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "负试验电荷"


class BarMagnet(ElectromagnetismBase):
    """A bar magnet element in an electromagnetism experiment."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Bar Magnet",
            "Identifier": self.identifier,
            "Properties": {"锁定": int(self.lock_status), "强度": 1.0, "质量": 10.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"BarMagnet("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "条形磁铁"


class Compass(ElectromagnetismBase):
    """A compass element that responds to magnetic fields."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = True,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Compass",
            "Identifier": self.identifier,
            "Properties": {"锁定": int(self.lock_status)},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"Compass("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "指南针"


class UniformMagneticField(ElectromagnetismBase):
    """A uniform magnetic field element in an electromagnetism experiment."""

    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: Optional[str] = None,
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
        angular_velocity: coordinate_system.AngularVelocity = coordinate_system.AngularVelocity(
            0, 0, 0
        ),
        lock_status: bool = False,
    ) -> None:
        if identifier is None:
            identifier = str(uuid.uuid4())
        super().__init__(
            position, rotation, identifier, velocity, angular_velocity, lock_status
        )

    def as_dict(self) -> dict:
        return {
            "ModelID": "Uniform Magnetic Field",
            "Identifier": self.identifier,
            "Properties": {"锁定": int(self.lock_status), "强度": 1000.0, "方向": 1.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": self.angular_velocity.as_angular_velocity_str_in_plsav(),
        }

    def to_constructor_str(self) -> str:
        """Return a Python constructor call string that reproduces this element."""
        return (
            f"UniformMagneticField("
            f"position=Position({self.position.x}, {self.position.y}, {self.position.z}), "
            f"rotation=Rotation({self.rotation.x}, {self.rotation.y}, {self.rotation.z}), "
            f"identifier={self.identifier!r}, "
            f"velocity=Velocity({self.velocity.x}, {self.velocity.y}, {self.velocity.z}), "
            f"angular_velocity=AngularVelocity({self.angular_velocity.x}, {self.angular_velocity.y}, {self.angular_velocity.z}), "
            f"lock_status={self.lock_status})"
        )

    @staticmethod
    def zh_name() -> str:
        return "匀强磁场"
