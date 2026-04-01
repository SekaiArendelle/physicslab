import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys

sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import pathlib
import inspect
import re
import unittest

import _user
import _constant

from physicslab import (
    Position,
    Rotation,
    ColorOfWire,
    generate_a_new_sav_path,
    Category,
    crt_circuit_experiment,
    load_circuit_experiment_by_file_path,
    load_circuit_experiment_by_sav_name,
    load_circuit_experiment_from_app,
    find_path_of_sav_name,
    ElementExistError,
    ElementNotExistError,
    ExperimentNotExistError,
)
from physicslab.circuit import elements
from physicslab.circuit._base import CircuitBase
from physicslab.enums import SwitchState, PDTSwitchState


class TestCircuitExperiment(unittest.TestCase):
    def test_crt_and_remove_element(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            b = elements.LogicOutput(Position(1, 0, 0), Rotation(0, 0, 180))
            expe.crt_elements(a, b)
            self.assertEqual(expe.get_elements_count(), 2)

            expe.del_a_element(b)
            self.assertEqual(expe.get_elements_count(), 1)

    def test_wire_apis(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            b = elements.LogicOutput(Position(1, 0, 0), Rotation(0, 0, 180))
            c = elements.LogicOutput(Position(2, 0, 0), Rotation(0, 0, 180))
            expe.crt_elements(a, b, c)

            expe.crt_a_wire(a.o, b.i, color=ColorOfWire.red)
            self.assertEqual(expe.get_wires_count(), 1)

            expe.del_a_wire(a.o, b.i)
            self.assertEqual(expe.get_wires_count(), 0)

            expe.crt_wires(a.o, b.i, c.i, color=ColorOfWire.blue)
            self.assertEqual(expe.get_wires_count(), 2)

            expe.clear_wires()
            self.assertEqual(expe.get_wires_count(), 0)

            d = elements.LogicInput(Position(3, 0, 0), Rotation(0, 0, 180))
            e = elements.LogicInput(Position(4, 0, 0), Rotation(0, 0, 180))
            with self.assertRaises(ElementNotExistError):
                expe.crt_a_wire(d.o, e.o)

    def test_load_all_element(self):
        with load_circuit_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "All-Circuit-Elements.sav"
        ) as expe:
            self.assertEqual(expe.get_elements_count(), 91)
            self.assertEqual(expe.get_wires_count(), 0)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_all_element_from_exported_sav(self):
        with load_circuit_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "Export-All-Circuit-Elements.sav"
        ) as expe:
            self.assertEqual(expe.get_elements_count(), 91)
            self.assertEqual(expe.get_wires_count(), 0)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_float32(self):
        with load_circuit_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "float32_t.sav"
        ) as expe:
            self.assertEqual(expe.get_elements_count(), 652)
            self.assertEqual(expe.get_wires_count(), 1385)

    def test_load_circuit_experiment_by_sav_name(self):
        name = "__test_load_circuit_experiment_by_sav_name__"
        path = find_path_of_sav_name(name)
        if path is None:
            with crt_circuit_experiment(name) as expe:
                a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
                expe.crt_a_element(a)
                new_sav_path = generate_a_new_sav_path()
                if not new_sav_path.parent.exists():
                    new_sav_path.parent.mkdir(parents=True)
                expe.save_to(new_sav_path)

        expe, filepath = load_circuit_experiment_by_sav_name(name)
        self.assertGreaterEqual(expe.get_elements_count(), 1)
        filepath.unlink()

    def test_merge(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            b = elements.LogicOutput(Position(1, 0, 0), Rotation(0, 0, 180))
            expe.crt_elements(a, b)
            expe.crt_a_wire(a.o, b.i)

            with crt_circuit_experiment(None) as expe2:
                c = elements.LogicOutput(Position(2, 0, 0), Rotation(0, 0, 180))
                expe2.crt_a_element(c)
                expe2.merge(expe)

                self.assertEqual(expe2.get_elements_count(), 3)
                self.assertEqual(expe2.get_wires_count(), 1)

    def test_load_from_app(self):
        with load_circuit_experiment_from_app(
            "6774ffb4c45f930f41ccedf8", Category.Discussion, user=_user.user
        ) as expe:
            self.assertEqual(expe.get_elements_count(), 91)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_element_twice(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            expe.crt_a_element(a)
            with self.assertRaises(ElementExistError):
                expe.crt_a_element(a)

    def test_get_element_by_index(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            expe.crt_a_element(a)
            self.assertEqual(expe.get_element_by_index(0), a)
            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_index(1)

    def test_get_element_by_id(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            expe.crt_a_element(a)
            self.assertEqual(expe.get_element_by_id(a.identifier), a)
            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_id("nonexistent_id")

    def test_get_element_by_position(self):
        with crt_circuit_experiment(None) as expe:
            a = elements.LogicInput(Position(0, 0, 0), Rotation(0, 0, 180))
            expe.crt_a_element(a)
            self.assertEqual(expe.get_element_by_position(a.position), a)
            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_position(Position(1, 1, 1))

    def test_load_nonexistent_file_path(self):
        with self.assertRaises(ExperimentNotExistError):
            load_circuit_experiment_by_file_path(
                pathlib.Path(_constant.TEST_DATA_DIR) / "nonexistent_file.sav"
            )


class TestCircuitElements(unittest.TestCase):
    def _assert_element_common(self, _instance: CircuitBase, model_id: str):
        self.assertEqual(_instance.as_dict()["ModelID"], model_id)
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")
        self.assertEqual(_instance.count_all_pins(), len(list(_instance.all_pins())))

        self.assertIsNone(_instance.label)
        self.assertIsNone(_instance.as_dict()["Label"])
        _instance.label = "Test label"
        self.assertEqual(_instance.label, "Test label")
        self.assertEqual(_instance.as_dict()["Label"], "Test label")

        self.assertTrue(_instance.lock_status)
        _instance.lock_status = False
        self.assertFalse(_instance.lock_status)
        if "锁定" in _instance.as_dict()["Properties"]:
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 0)

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"elements.{constructor_str}")

    def test_accelerometer(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Accelerometer(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Accelerometer")

    def test_air_switch(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.AirSwitch(
                Position(1, 2, 3), Rotation(0, 0, 180), switch_state=SwitchState.ON
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Air Switch")
            self.assertEqual(_instance.as_dict()["Properties"]["开关"], 1)

    def test_analog_joystick(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.AnalogJoystick(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Analog Joystick")

    def test_and_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.AndGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "And Gate")

    def test_attitude_sensor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.AttitudeSensor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Attitude Sensor")

    def test_basic_capacitor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.BasicCapacitor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Basic Capacitor")

    def test_basic_diode(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.BasicDiode(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Basic Diode")

    def test_basic_inductor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.BasicInductor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Basic Inductor")

    def test_battery_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.BatterySource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Battery Source")

    def test_buzzer(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Buzzer(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Buzzer")

    def test_color_light_emitting_diode(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ColorLightEmittingDiode(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Color Light-Emitting Diode")

    def test_comparator(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Comparator(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Comparator")

    def test_counter(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Counter(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Counter")

    def test_current_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.CurrentSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Current Source")

    def test_d_flipflop(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.DFlipflop(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "D Flipflop")

    def test_d_p_d_t_switch(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.DPDTSwitch(
                Position(1, 2, 3),
                Rotation(0, 0, 180),
                switch_state=PDTSwitchState.RIGHT,
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "DPDT Switch")
            self.assertEqual(_instance.as_dict()["Properties"]["开关"], 2)

    def test_dual_light_emitting_diode(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.DualLightEmittingDiode(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Dual Light-Emitting Diode")

    def test_eight_bit_display(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.EightBitDisplay(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Eight Bit Display")

    def test_eight_bit_input(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.EightBitInput(
                Position(1, 2, 3), Rotation(0, 0, 180), 1
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "8bit Input")
            self.assertEqual(_instance.as_dict()["Properties"]["十进制"], 1)

    def test_electric_bell(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ElectricBell(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Electric Bell")

    def test_electric_fan(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ElectricFan(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Electric Fan")

    def test_electricity_meter(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ElectricityMeter(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Electricity Meter")

    def test_full_adder(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.FullAdder(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Full Adder")

    def test_full_subtractor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.FullSubtractor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Full Subtractor")

    def test_fuse_component(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.FuseComponent(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Fuse Component")

    def test_galvanometer(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Galvanometer(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Galvanometer")

    def test_gravity_sensor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.GravitySensor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Gravity Sensor")

    def test_ground_component(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.GroundComponent(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Ground Component")

    def test_gyroscope(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Gyroscope(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Gyroscope")

    def test_half_adder(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.HalfAdder(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Half Adder")

    def test_half_subtractor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.HalfSubtractor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Half Subtractor")

    def test_imp_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ImpGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Imp Gate")

    def test_incandescent_lamp(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.IncandescentLamp(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Incandescent Lamp")

    def test_j_k_flipflop(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.JKFlipflop(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "JK Flipflop")

    def test_light_emitting_diode(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.LightEmittingDiode(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Light-Emitting Diode")

    def test_linear_accelerometer(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.LinearAccelerometer(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Linear Accelerometer")

    def test_logic_input(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.LogicInput(
                Position(1, 2, 3), Rotation(0, 0, 180), output_status=True
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Logic Input")
            self.assertEqual(_instance.as_dict()["Properties"]["开关"], 1)

    def test_logic_output(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.LogicOutput(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Logic Output")

    def test_magnetic_field_sensor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.MagneticFieldSensor(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Magnetic Field Sensor")

    def test_microammeter(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Microammeter(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Microammeter")

    def test_multimeter(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Multimeter(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Multimeter")

    def test_multiplier(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Multiplier(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Multiplier")

    def test_musical_box(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.MusicalBox(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Musical Box")

    def test_mutual_inductor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.MutualInductor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Mutual Inductor")

    def test_n_e555(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.NE555(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "555 Timer")

    def test_n_m_o_s_f_e_t(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.N_MOSFET(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "N-MOSFET")

    def test_nand_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.NandGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Nand Gate")

    def test_nimp_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.NimpGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Nimp Gate")

    def test_no_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.NoGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "No Gate")

    def test_nor_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.NorGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Nor Gate")

    def test_operational_amplifier(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.OperationalAmplifier(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Operational Amplifier")

    def test_or_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.OrGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Or Gate")

    def test_p_m_o_s_f_e_t(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.P_MOSFET(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "P-MOSFET")

    def test_photodiode(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Photodiode(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Photodiode")

    def test_photoresistor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Photoresistor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Photoresistor")

    def test_proximity_sensor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ProximitySensor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Proximity Sensor")

    def test_pulse_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.PulseSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Pulse Source")

    def test_push_switch(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.PushSwitch(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Push Switch")

    def test_random_generator(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.RandomGenerator(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Random Generator")

    def test_real_t_flipflop(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.RealTFlipflop(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Real-T Flipflop")

    def test_rectifier(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Rectifier(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Rectifier")

    def test_relay_component(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.RelayComponent(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Relay Component")

    def test_resistance_box(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ResistanceBox(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Resistance Box")

    def test_resistance_law(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.ResistanceLaw(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Resistance Law")

    def test_resistor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Resistor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Resistor")

    def test_s_p_d_t_switch(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SPDTSwitch(
                Position(1, 2, 3),
                Rotation(0, 0, 180),
                switch_state=PDTSwitchState.RIGHT,
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "SPDT Switch")
            self.assertEqual(_instance.as_dict()["Properties"]["开关"], 2)

    def test_sawtooth_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SawtoothSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Sawtooth Source")

    def test_schmitt_trigger(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SchmittTrigger(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Schmitt Trigger")

    def test_simple_ammeter(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SimpleAmmeter(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Simple Ammeter")

    def test_simple_instrument(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SimpleInstrument(
                Position(1, 2, 3), Rotation(0, 0, 180), pitches=[60, 64, 67]
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Simple Instrument")
            props = _instance.as_dict()["Properties"]
            self.assertEqual(props["和弦"], 3)
            self.assertEqual(props["音高"], 60)
            self.assertEqual(props["音高1"], 64)
            self.assertEqual(props["音高2"], 67)

    def test_simple_switch(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SimpleSwitch(
                Position(1, 2, 3), Rotation(0, 0, 180), switch_state=SwitchState.ON
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Simple Switch")
            self.assertEqual(_instance.as_dict()["Properties"]["开关"], 1)

    def test_simple_voltmeter(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SimpleVoltmeter(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Simple Voltmeter")

    def test_sinewave_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SinewaveSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Sinewave Source")

    def test_slide_rheostat(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SlideRheostat(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Slide Rheostat")

    def test_solenoid(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Solenoid(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Solenoid")

    def test_spark_gap(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SparkGap(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Spark Gap")

    def test_square_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.SquareSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Square Source")

    def test_student_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.StudentSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Student Source")

    def test_t_flipflop(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.TFlipflop(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "T Flipflop")

    def test_tapped_transformer(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.TappedTransformer(
                Position(1, 2, 3), Rotation(0, 0, 180)
            )
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Tapped Transformer")

    def test_tesla_coil(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.TeslaCoil(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Tesla Coil")

    def test_transformer(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Transformer(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Transformer")

    def test_transistor(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.Transistor(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Transistor")

    def test_triangle_source(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.TriangleSource(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Triangle Source")

    def test_xnor_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.XnorGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Xnor Gate")

    def test_xor_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.XorGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Xor Gate")

    def test_yes_gate(self):
        with crt_circuit_experiment(None) as expe:
            _instance = elements.YesGate(Position(1, 2, 3), Rotation(0, 0, 180))
            expe.crt_a_element(_instance)
            self._assert_element_common(_instance, "Yes Gate")

    def test_all_circuit_element_subclasses_are_covered(self):
        all_element_subclasses = {
            name
            for name, obj in inspect.getmembers(elements, inspect.isclass)
            if issubclass(obj, CircuitBase)
            and obj is not CircuitBase
            and obj.__module__.startswith("physicslab.circuit.elements.")
            and not name.startswith("_")
        }

        covered_classes = set()
        for method_name, method in inspect.getmembers(
            self.__class__, inspect.isfunction
        ):
            if not method_name.startswith("test_"):
                continue
            if method_name == "test_all_circuit_element_subclasses_are_covered":
                continue

            source = inspect.getsource(method)
            covered_classes.update(re.findall(r"elements\.(\w+)\(", source))

        missing = sorted(all_element_subclasses - covered_classes)
        self.assertEqual(
            missing,
            [],
            msg=f"Missing TestCircuitElements coverage for: {', '.join(missing)}",
        )


if __name__ == "__main__":
    unittest.main()
