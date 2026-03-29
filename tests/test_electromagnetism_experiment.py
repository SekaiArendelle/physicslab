import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys

sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import pathlib
import unittest
import _constant
import _user
from physicsLab import (
    Position,
    Velocity,
    Category,
    generate_a_new_sav_path,
    find_path_of_sav_name,
    load_electromagnetism_experiment_by_file_path,
    load_electromagnetism_experiment_from_app,
    load_electromagnetism_experiment_by_sav_name,
    crt_electromagnetism_experiment,
    ElementNotExistError,
)
from physicsLab.electromagnetism import elements


class TestElectromagnetismExperiment(unittest.TestCase):
    def test_load_from_filepath(self):
        with load_electromagnetism_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "All-Electromagnetism-Elements.sav"
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_from_exported_filepath(self):
        with load_electromagnetism_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR)
            / "Export-All-Electromagnetism-Elements.sav"
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_remove_element(self):
        with crt_electromagnetism_experiment(None) as expe:
            negative_charge = elements.NegativeCharge(Position(0, 0, 0))
            positive_charge = elements.PositiveCharge(Position(1, 0, 0))
            expe.crt_elements(positive_charge, negative_charge)
            self.assertTrue(expe.get_elements_count() == 2)
            expe.del_a_element(negative_charge)
            self.assertTrue(expe.get_elements_count() == 1)

    def test_load_electromagnetism_experiment_by_sav_name(self):
        path = find_path_of_sav_name(
            "__test_load_electromagnetism_experiment_by_sav_name__"
        )
        if path is None:
            new_sav_path = generate_a_new_sav_path()
            if not new_sav_path.parent.exists():
                new_sav_path.parent.mkdir(parents=True)
            crt_electromagnetism_experiment(
                "__test_load_electromagnetism_experiment_by_sav_name__"
            ).save_to(new_sav_path)
        expe, filepath = load_electromagnetism_experiment_by_sav_name(
            "__test_load_electromagnetism_experiment_by_sav_name__"
        )
        filepath.unlink()

    def test_load_electromagnetism_experiment_from_app(self):
        with load_electromagnetism_experiment_from_app(
            "67750037c45f930f41ccee02", Category.Discussion, _user.user
        ) as expe:
            self.assertEqual(expe.get_elements_count(), 7)

    def test_merge(self):
        with crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeCharge(Position(0, 0, 0))
            magnet = elements.BarMagnet(Position(1, 0, 0))
            expe.crt_elements(charge, magnet)
            self.assertEqual(expe.get_elements_count(), 2)
            with crt_electromagnetism_experiment(None) as expe2:
                compass = elements.Compass(Position(0, 1, 0))
                field = elements.UniformMagneticField(Position(1, 1, 0))
                expe2.crt_elements(compass, field)
                self.assertEqual(expe2.get_elements_count(), 2)
                expe.merge(expe2)
                self.assertEqual(expe.get_elements_count(), 4)

    def test_get_element_by_index(self):
        with crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeCharge(Position(0, 0, 0))
            magnet = elements.BarMagnet(Position(1, 0, 0))
            expe.crt_elements(charge, magnet)
            self.assertEqual(expe.get_element_by_index(0), charge)
            self.assertEqual(expe.get_element_by_index(1), magnet)
            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_index(2)

    def test_get_element_by_id(self):
        with crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeCharge(Position(0, 0, 0))
            magnet = elements.BarMagnet(Position(1, 0, 0))
            expe.crt_elements(charge, magnet)
            self.assertEqual(expe.get_element_by_id(charge.identifier), charge)
            self.assertEqual(expe.get_element_by_id(magnet.identifier), magnet)
            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_id("nonexistent_id")

    def test_get_element_by_position(self):
        with crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeCharge(Position(0, 0, 0))
            magnet = elements.BarMagnet(Position(1, 0, 0))
            expe.crt_elements(charge, magnet)
            self.assertEqual(expe.get_element_by_position(Position(0, 0, 0)), charge)
            self.assertEqual(expe.get_element_by_position(Position(1, 0, 0)), magnet)
            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_position(Position(2, 0, 0))


class TestElectromagnetismElements(unittest.TestCase):
    def test_negative_charge(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.NegativeCharge(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 1.0)

    def test_positive_charge(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.PositiveCharge(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 1.0)

    def test_negative_test_charge(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.NegativeTestCharge(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 0.0)

    def test_positive_test_charge(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.PositiveTestCharge(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 0.0)

    def test_bar_magnet(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.BarMagnet(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 1.0)

    def test_compass(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.Compass(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 1.0)

    def test_uniform_magnetic_field(self):
        with crt_electromagnetism_experiment(None) as expe:
            _instance = elements.UniformMagneticField(
                Position(0, 0, 0), velocity=Velocity(0.1, 0.2, 0.3)
            )
            expe.crt_elements(_instance)
            self.assertIsInstance(_instance.as_dict(), dict)
            self.assertEqual(_instance.position, Position(0, 0, 0))
            self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
            # check lock status via as_dict
            self.assertEqual(_instance.as_dict()["Properties"]["锁定"], 0.0)


if __name__ == "__main__":
    unittest.main()
