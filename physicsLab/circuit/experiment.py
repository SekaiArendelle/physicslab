import json
import pathlib
import time
import uuid
from physicsLab import coordinate_system
from physicsLab import errors
from physicsLab.utils import find_path_of_sav_name
from physicsLab.enums import Category, ColorOfWire, SwitchState, PDTSwitchState
from physicsLab.web import User, anonymous_login
from physicsLab._camera_save import CameraMode, CameraSave
from physicsLab._typing import Optional, Self, Tuple
from . import elements
from ._base import CircuitBase, Pin
from ._status_save import CircuitStatusSave
from .wire import WireInfo


class CircuitExperiment:
    __name: Optional[str]
    __status_save: CircuitStatusSave
    __camera_save: CameraSave

    def __init__(
        self,
        name: Optional[str],
        camera_save: CameraSave = CameraSave(
            CameraMode.circuit_mode,
            2.7,
            coordinate_system.Position(-0.1715205, -0.7228146, 1.08),
            coordinate_system.Rotation(50, 0, 0),
        ),
    ) -> None:
        self.name = name
        self.status_save = CircuitStatusSave()
        self.camera_save = camera_save

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        if not isinstance(name, (str, type(None))):
            raise TypeError(
                f"name must be of type `str | None`, but got value {name} of type {type(name).__name__}"
            )

        self.__name = name

    @property
    def status_save(self) -> CircuitStatusSave:
        return self.__status_save

    @status_save.setter
    def status_save(self, status_save: CircuitStatusSave) -> None:
        if not isinstance(status_save, CircuitStatusSave):
            raise TypeError(
                f"status_save must be of type `CircuitStatusSave`, but got value {status_save} of type {type(status_save).__name__}"
            )

        self.__status_save = status_save

    @property
    def camera_save(self) -> CameraSave:
        return self.__camera_save

    @camera_save.setter
    def camera_save(self, camera_save: CameraSave) -> None:
        if not isinstance(camera_save, CameraSave):
            raise TypeError(
                f"camera_save must be of type `CameraSave`, but got value {camera_save} of type {type(camera_save).__name__}"
            )

        self.__camera_save = camera_save

    def crt_a_element(self, element: CircuitBase) -> Self:
        self.status_save.append_element(element)
        return self

    def crt_elements(self, *elements: CircuitBase) -> Self:
        for element in elements:
            self.crt_a_element(element)
        return self

    def del_a_element(self, element: CircuitBase) -> Self:
        self.status_save.remove_element(element)
        return self

    def get_elements_count(self) -> int:
        return len(self.status_save.elements)

    def get_element_by_index(self, index: int) -> CircuitBase:
        return self.status_save.get_element_by_index(index)

    def get_element_by_id(self, identifier: str) -> CircuitBase:
        return self.status_save.get_element_by_id(identifier)

    def get_element_by_position(
        self, position: coordinate_system.Position
    ) -> CircuitBase:
        return self.status_save.get_element_by_position(position)

    def crt_a_wire(
        self,
        source_pin: Pin,
        target_pin: Pin,
        color: ColorOfWire = ColorOfWire.blue,
    ) -> Self:
        if not isinstance(source_pin, Pin):
            raise TypeError(
                f"parameter source_pin must be of type `Pin`, but got value {source_pin} of type {type(source_pin).__name__}"
            )
        if not isinstance(target_pin, Pin):
            raise TypeError(
                f"parameter target_pin must be of type `Pin`, but got value {target_pin} of type {type(target_pin).__name__}"
            )
        if not isinstance(color, ColorOfWire):
            raise TypeError(
                f"parameter color must be of type `ColorOfWire`, but got value {color} of type {type(color).__name__}"
            )
        if source_pin == target_pin:
            raise errors.InvalidWireError("Cannot create a wire between the same pin")

        if (
            source_pin.element not in self.status_save.elements
            or target_pin.element not in self.status_save.elements
        ):
            raise errors.InvalidWireError(
                "Cannot create a wire between pins from another experiment"
            )

        wire_info = WireInfo(color=color)
        if self.status_save.circuit_graph.has_edge(source_pin, target_pin):
            self.status_save.circuit_graph.assign_edge(
                source_pin, target_pin, wire_info
            )
        else:
            self.status_save.append_wire(source_pin, target_pin, wire_info)

        return self

    def crt_wires(
        self,
        source_pin: Pin,
        *target_pins: Pin,
        color: ColorOfWire = ColorOfWire.blue,
    ) -> Self:
        if len(target_pins) == 0:
            raise ValueError("At least one target pin is required")

        for target_pin in target_pins:
            self.crt_a_wire(source_pin, target_pin, color=color)
        return self

    def del_a_wire(self, source_pin: Pin, target_pin: Pin) -> Self:
        try:
            self.status_save.remove_wire(source_pin, target_pin)
        except ValueError as e:
            raise errors.InvalidWireError(str(e))
        return self

    def clear_wires(self) -> Self:
        self.status_save.circuit_graph.clear()
        return self

    def get_wires_count(self) -> int:
        return self.status_save.circuit_graph.count_edges()

    def as_plsav_dict(self) -> dict:
        return {
            "Type": 0,
            "Experiment": {
                "ID": None,
                "Type": 0,
                "Components": self.get_elements_count(),
                "Subject": self.name,
                "StatusSave": self.status_save.as_str_in_plsav(),
                "CameraSave": self.camera_save.as_str_in_plsav(),
                "Version": 2405,
                "CreationDate": int(time.time() * 1000),
                "Paused": False,
                "Summary": None,
                "Plots": None,
            },
            "ID": None,
            "Summary": {
                "Type": 0,
                "ParentID": None,
                "ParentName": None,
                "ParentCategory": None,
                "ContentID": None,
                "Editor": None,
                "Coauthors": [],
                "Description": None,
                "LocalizedDescription": None,
                "Tags": ["Type-0"],
                "ModelID": None,
                "ModelName": None,
                "ModelTags": [],
                "Version": 0,
                "Language": None,
                "Visits": 0,
                "Stars": 0,
                "Supports": 0,
                "Remixes": 0,
                "Comments": 0,
                "Price": 0,
                "Popularity": 0,
                "CreationDate": int(time.time() * 1000),
                "UpdateDate": 0,
                "SortingDate": 0,
                "ID": None,
                "Category": None,
                "Subject": self.name,
                "LocalizedSubject": None,
                "Image": 0,
                "ImageRegion": 0,
                "User": {
                    "ID": None,
                    "Nickname": None,
                    "Signature": None,
                    "Avatar": 0,
                    "AvatarRegion": 0,
                    "Decoration": 0,
                    "Verification": None,
                },
                "Visibility": 0,
                "Settings": {},
                "Multilingual": False,
            },
            "CreationDate": 0,
            "InternalName": str(uuid.uuid4()),
            "Speed": 1.0,
            "SpeedMinimum": 0.1,
            "SpeedMaximum": 2.0,
            "SpeedReal": 0.0,
            "Paused": False,
            "Version": 0,
            "CameraSnapshot": None,
            "Plots": [],
            "Widgets": [],
            "WidgetGroups": [],
            "Bookmarks": {},
            "Interfaces": {"Play-Expanded": False, "Chart-Expanded": False},
        }

    def save_to(self, path: pathlib.Path) -> None:
        if not isinstance(path, pathlib.Path):
            raise TypeError(
                f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
            )
        path.write_text(json.dumps(self.as_plsav_dict()), encoding="utf-8")

    def merge(self, other: "CircuitExperiment") -> Self:
        if not isinstance(other, CircuitExperiment):
            raise TypeError(
                f"parameter other must be of type `CircuitExperiment`, but got value {other} of type {type(other).__name__}"
            )

        self.status_save.append_range(other.status_save)
        return self


def _construct_camera_save(camera_save: str) -> CameraSave:
    camera_save_dict = json.loads(camera_save)
    return CameraSave(
        camera_mode=CameraMode(camera_save_dict["Mode"]),
        distance=camera_save_dict["Distance"],
        vision_center=coordinate_system.construct_position_from_plsav_str(
            camera_save_dict["VisionCenter"]
        ),
        target_rotation=coordinate_system.construct_rotation_from_plsav_str(
            camera_save_dict["TargetRotation"]
        ),
    )


def _construct_pin_by_label(element: CircuitBase, pin_label: int) -> Pin:
    for _, pin in element.all_pins():
        if pin.pin_label == pin_label:
            return pin
    raise ValueError(
        f"element {element.identifier} does not have pin with label {pin_label}"
    )


def _construct_color_of_wire(color_name: str) -> ColorOfWire:
    if not isinstance(color_name, str):
        raise TypeError(
            f"color_name must be of type `str`, but got value {color_name} of type {type(color_name).__name__}"
        )

    for color in ColorOfWire:
        if color_name.startswith(color.value):
            return color

    raise ValueError(f"unknown wire color: {color_name}")


def _dict_to_element(element_dict: dict) -> CircuitBase:
    model_id = element_dict["ModelID"]
    position = coordinate_system.construct_position_from_plsav_str(
        element_dict["Position"]
    )
    rotation = coordinate_system.construct_rotation_from_plsav_str(
        element_dict["Rotation"]
    )
    identifier = element_dict["Identifier"]
    lock_status = bool(element_dict["IsLocked"])
    label = element_dict.get("Label")
    props = element_dict["Properties"]

    if model_id == "555 Timer":
        return elements.NE555(position, rotation, identifier, label, lock_status)
    elif model_id == "8bit Input":
        return elements.EightBitInput(
            position,
            rotation,
            int(props["十进制"]),
            props["高电平"],
            props["低电平"],
            identifier,
            label,
            lock_status,
        )
    elif model_id in ("8bit Display", "Eight Bit Display"):
        return elements.EightBitDisplay(
            position,
            rotation,
            props["高电平"],
            props["低电平"],
            identifier,
            label,
            lock_status,
        )
    elif model_id == "Accelerometer":
        return elements.Accelerometer(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Air Switch":
        return elements.AirSwitch(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
            switch_state=SwitchState(int(props["开关"])),
        )
    elif model_id == "Analog Joystick":
        return elements.AnalogJoystick(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "And Gate":
        return elements.AndGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Attitude Sensor":
        return elements.AttitudeSensor(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Basic Capacitor":
        return elements.BasicCapacitor(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Basic Diode":
        return elements.BasicDiode(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Basic Inductor":
        return elements.BasicInductor(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Battery Source":
        return elements.BatterySource(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Buzzer":
        return elements.Buzzer(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Color Light-Emitting Diode":
        return elements.ColorLightEmittingDiode(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Comparator":
        return elements.Comparator(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Counter":
        return elements.Counter(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Current Source":
        return elements.CurrentSource(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "D Flipflop":
        return elements.DFlipflop(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "DPDT Switch":
        return elements.DPDTSwitch(
            position,
            rotation,
            identifier=identifier,
            switch_state=PDTSwitchState(int(props["开关"])),
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Dual Light-Emitting Diode":
        return elements.DualLightEmittingDiode(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Electric Bell":
        return elements.ElectricBell(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Electric Fan":
        return elements.ElectricFan(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Electricity Meter":
        return elements.ElectricityMeter(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Full Adder":
        return elements.FullAdder(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Full Subtractor":
        return elements.FullSubtractor(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Fuse Component":
        return elements.FuseComponent(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Galvanometer":
        return elements.Galvanometer(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Gravity Sensor":
        return elements.GravitySensor(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Ground Component":
        return elements.GroundComponent(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Gyroscope":
        return elements.Gyroscope(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Half Adder":
        return elements.HalfAdder(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Half Subtractor":
        return elements.HalfSubtractor(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Imp Gate":
        return elements.ImpGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Incandescent Lamp":
        return elements.IncandescentLamp(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "JK Flipflop":
        return elements.JKFlipflop(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Light-Emitting Diode":
        return elements.LightEmittingDiode(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Linear Accelerometer":
        return elements.LinearAccelerometer(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Logic Input":
        return elements.LogicInput(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Logic Output":
        return elements.LogicOutput(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Magnetic Field Sensor":
        return elements.MagneticFieldSensor(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Microammeter":
        return elements.Microammeter(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Multimeter":
        return elements.Multimeter(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Multiplier":
        return elements.Multiplier(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Musical Box":
        return elements.MusicalBox(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Mutual Inductor":
        return elements.MutualInductor(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "N-MOSFET":
        return elements.N_MOSFET(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Nand Gate":
        return elements.NandGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Nimp Gate":
        return elements.NimpGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "No Gate":
        return elements.NoGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Nor Gate":
        return elements.NorGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Operational Amplifier":
        return elements.OperationalAmplifier(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Or Gate":
        return elements.OrGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "P-MOSFET":
        return elements.P_MOSFET(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Photodiode":
        return elements.Photodiode(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Photoresistor":
        return elements.Photoresistor(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Proximity Sensor":
        return elements.ProximitySensor(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Pulse Source":
        return elements.PulseSource(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Push Switch":
        return elements.PushSwitch(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Random Generator":
        return elements.RandomGenerator(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Real-T Flipflop":
        return elements.RealTFlipflop(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Rectifier":
        return elements.Rectifier(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Relay Component":
        return elements.RelayComponent(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Resistance Box":
        return elements.ResistanceBox(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Resistance Law":
        return elements.ResistanceLaw(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Resistor":
        return elements.Resistor(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "SPDT Switch":
        return elements.SPDTSwitch(
            position,
            rotation,
            identifier=identifier,
            switch_state=PDTSwitchState(int(props["开关"])),
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Sawtooth Source":
        return elements.SawtoothSource(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Schmitt Trigger":
        return elements.SchmittTrigger(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Simple Ammeter":
        return elements.SimpleAmmeter(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Simple Instrument":
        pitches = []
        for i in range(int(props["和弦"])):
            if i == 0:
                pitches.append(int(props["音高"]))
            else:
                pitches.append(int(props[f"音高{i}"]))
        return elements.SimpleInstrument(
            position=position,
            rotation=rotation,
            pitches=pitches,
            rated_oltage=props["额定电压"],
            volume=props["音量"],
            instrument=int(props.get("乐器", 0)),
            bpm=int(props["节拍"]),
            is_ideal=bool(props["理想模式"]),
            is_pulse=bool(props["脉冲"]),
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Simple Switch":
        return elements.SimpleSwitch(
            position,
            rotation,
            identifier=identifier,
            switch_state=SwitchState(int(props["开关"])),
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Simple Voltmeter":
        return elements.SimpleVoltmeter(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Sinewave Source":
        return elements.SinewaveSource(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Slide Rheostat":
        return elements.SlideRheostat(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "Solenoid":
        return elements.Solenoid(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Spark Gap":
        return elements.SparkGap(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Square Source":
        return elements.SquareSource(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Student Source":
        return elements.StudentSource(
            position,
            rotation,
            identifier=identifier,
            lock_status=lock_status,
            label=label,
        )
    elif model_id == "T Flipflop":
        return elements.TFlipflop(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Tapped Transformer":
        return elements.TappedTransformer(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Tesla Coil":
        return elements.TeslaCoil(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Transformer":
        return elements.Transformer(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Transistor":
        return elements.Transistor(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Triangle Source":
        return elements.TriangleSource(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Xnor Gate":
        return elements.XnorGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Xor Gate":
        return elements.XorGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    elif model_id == "Yes Gate":
        return elements.YesGate(
            position,
            rotation,
            identifier=identifier,
            label=label,
            lock_status=lock_status,
        )
    else:
        errors.unreachable()


def crt_circuit_experiment(name: Optional[str]) -> CircuitExperiment:
    return CircuitExperiment(name)


def load_circuit_experiment_by_file_path(path: pathlib.Path) -> CircuitExperiment:
    if not isinstance(path, pathlib.Path):
        raise TypeError(
            f"path must be of type `Path`, but got value {path} of type {type(path).__name__}"
        )
    if not path.exists() or not path.is_file():
        raise errors.ExperimentNotExistError(f'File "{path}" does not exist')

    with open(path, "r", encoding="utf-8") as f:
        plasv_dict = json.load(f)
    if plasv_dict["Type"] != 0:
        raise errors.ExperimentTypeError(
            f'"{path}" does not contain a circuit experiment'
        )

    if isinstance(plasv_dict["Summary"], dict):
        subject = plasv_dict["Summary"]["Subject"]
    elif "Experiment" in plasv_dict and "Subject" in plasv_dict["Experiment"]:
        subject = plasv_dict["Experiment"]["Subject"]
    else:
        subject = plasv_dict.get("Subject", None)

    if "Experiment" in plasv_dict.keys():
        status_save_dict = json.loads(plasv_dict["Experiment"]["StatusSave"])
        camera_save = _construct_camera_save(plasv_dict["Experiment"]["CameraSave"])
    else:
        status_save_dict = json.loads(plasv_dict["StatusSave"])
        camera_save = _construct_camera_save(plasv_dict["CameraSave"])

    result = CircuitExperiment(subject, camera_save)

    for element_dict in status_save_dict["Elements"]:
        result.crt_a_element(_dict_to_element(element_dict))

    for wire_dict in status_save_dict["Wires"]:
        source_element = result.get_element_by_id(wire_dict["Source"])
        target_element = result.get_element_by_id(wire_dict["Target"])
        source_pin = _construct_pin_by_label(source_element, wire_dict["SourcePin"])
        target_pin = _construct_pin_by_label(target_element, wire_dict["TargetPin"])
        result.crt_a_wire(
            source_pin=source_pin,
            target_pin=target_pin,
            color=_construct_color_of_wire(wire_dict["ColorName"]),
        )

    return result


def load_circuit_experiment_by_sav_name(
    sav_name: str,
) -> Tuple[CircuitExperiment, pathlib.Path]:
    file = find_path_of_sav_name(sav_name)
    if file is None:
        raise errors.ExperimentNotExistError(
            f'Experiment with name "{sav_name}" does not exist'
        )

    return load_circuit_experiment_by_file_path(file), file


def load_circuit_experiment_from_app(
    content_id: str,
    category: Category,
    user: User = anonymous_login(),
) -> CircuitExperiment:
    if not isinstance(content_id, str):
        raise TypeError(
            f"content_id must be of type `str`, but got value {content_id} of type {type(content_id).__name__}`"
        )
    if not isinstance(category, Category):
        raise TypeError(
            f"category must be of type `Category`, but got value {category} of type {type(category).__name__}`"
        )
    if not isinstance(user, User):
        raise TypeError(
            f"user must be of type `User`, but got value {user} of type {type(user).__name__}`"
        )

    _summary = user.get_summary(content_id, category)["Data"]
    _experiment = user.get_experiment(_summary["ContentID"])["Data"]

    if _experiment["Type"] != 0:
        raise errors.ExperimentTypeError(
            f'Content ID "{content_id}" does not correspond to a circuit experiment'
        )

    result = CircuitExperiment(_summary["Subject"])
    status_save_dict = json.loads(_experiment["StatusSave"])
    for element_dict in status_save_dict["Elements"]:
        result.crt_a_element(_dict_to_element(element_dict))
    for wire_dict in status_save_dict["Wires"]:
        source_element = result.get_element_by_id(wire_dict["Source"])
        target_element = result.get_element_by_id(wire_dict["Target"])
        source_pin = _construct_pin_by_label(source_element, wire_dict["SourcePin"])
        target_pin = _construct_pin_by_label(target_element, wire_dict["TargetPin"])
        result.crt_a_wire(
            source_pin=source_pin,
            target_pin=target_pin,
            color=_construct_color_of_wire(wire_dict["ColorName"]),
        )

    return result
