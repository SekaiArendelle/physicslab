import uuid
from physicsLab import coordinate_system
from ._base import ElectromagnetismBase


class NegativeCharge(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Negative Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0, "强度": -1e-07, "质量": 0.1},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "负电荷"


class PositiveCharge(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Positive Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0, "强度": 1e-07, "质量": 0.1},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "正电荷"


class NegativeTestCharge(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Negative Test Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 0.0, "强度": -1e-10, "质量": 5e-06},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "正试验电荷"


class PositiveTestCharge(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Positive Test Charge",
            "Identifier": self.identifier,
            "Properties": {"锁定": 0.0, "强度": -1e-10, "质量": 5e-06},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "负试验电荷"


class BarMagnet(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Bar Magnet",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0, "强度": 1.0, "质量": 10.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "条形磁铁"


class Compass(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Compass",
            "Identifier": self.identifier,
            "Properties": {"锁定": 1.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "指南针"


class UniformMagneticField(ElectromagnetismBase):
    def __init__(
        self,
        position: coordinate_system.Position,
        rotation: coordinate_system.Rotation = coordinate_system.Rotation(0, 0, 0),
        identifier: str = str(uuid.uuid4()),
        velocity: coordinate_system.Velocity = coordinate_system.Velocity(0, 0, 0),
    ) -> None:
        super().__init__(position, rotation, identifier, velocity)

    def as_dict(self) -> dict:
        return {
            "ModelID": "Uniform Magnetic Field",
            "Identifier": self.identifier,
            "Properties": {"锁定": 0.0, "强度": 1000.0, "方向": 1.0},
            "Position": self.position.as_postion_str_in_plsav(),
            "Rotation": self.rotation.as_rotation_str_in_plsav(),
            "Velocity": self.velocity.as_velocity_str_in_plsav(),
            "AngularVelocity": "0,0,0",
        }

    @staticmethod
    def zh_name() -> str:
        return "匀强磁场"
