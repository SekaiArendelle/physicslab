import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys

sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import pathlib
import unittest
import _constant
import base
from physicsLab import Position, Category
from physicsLab.electromagnetism import elements
from physicsLab.electromagnetism import experiment


class TestElectromagnetismExperiment(unittest.TestCase):
    def test_load_from_filepath(self):
        with experiment.load_electromagnetism_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "All-Electromagnetism-Elements.sav"
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_from_exported_filepath(self):
        with experiment.load_electromagnetism_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR)
            / "Export-All-Electromagnetism-Elements.sav"
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_remove_element(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            negative_charge = elements.NegativeCharge(Position(0, 0, 0))
            positive_charge = elements.PositiveCharge(Position(1, 0, 0))
            expe.crt_elements(positive_charge, negative_charge)
            self.assertTrue(expe.get_elements_count() == 2)
            expe.del_a_element(negative_charge)
            self.assertTrue(expe.get_elements_count() == 1)

    def test_load_electromagnetism_experiment_by_sav_name(self):
        path = experiment.find_path_of_sav_name(
            "__test_load_electromagnetism_experiment_by_sav_name__"
        )
        if path is None:
            experiment.crt_electromagnetism_experiment(
                "__test_load_electromagnetism_experiment_by_sav_name__"
            ).save_to(experiment.generate_a_new_sav_path())
        expe, filepath = experiment.load_electromagnetism_experiment_by_sav_name(
            "__test_load_electromagnetism_experiment_by_sav_name__"
        )
        filepath.unlink()

    def test_load_electromagnetism_experiment_from_app(self):
        with experiment.load_electromagnetism_experiment_from_app(
            "67750037c45f930f41ccee02", Category.Discussion, base.user
        ) as expe:
            self.assertEqual(expe.get_elements_count(), 7)

    def test_negative_charge(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeCharge(Position(0, 0, 0))
            expe.crt_elements(charge)
            self.assertIsInstance(charge.as_dict(), dict)
            self.assertEqual(charge.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(charge.as_dict()["Properties"]["锁定"], 1.0)

    def test_positive_charge(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            charge = elements.PositiveCharge(Position(0, 0, 0))
            expe.crt_elements(charge)
            self.assertIsInstance(charge.as_dict(), dict)
            self.assertEqual(charge.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(charge.as_dict()["Properties"]["锁定"], 1.0)

    def test_negative_test_charge(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeTestCharge(Position(0, 0, 0))
            expe.crt_elements(charge)
            self.assertIsInstance(charge.as_dict(), dict)
            self.assertEqual(charge.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(charge.as_dict()["Properties"]["锁定"], 0.0)

    def test_positive_test_charge(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            charge = elements.PositiveTestCharge(Position(0, 0, 0))
            expe.crt_elements(charge)
            self.assertIsInstance(charge.as_dict(), dict)
            self.assertEqual(charge.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(charge.as_dict()["Properties"]["锁定"], 0.0)

    def test_bar_magnet(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            magnet = elements.BarMagnet(Position(0, 0, 0))
            expe.crt_elements(magnet)
            self.assertIsInstance(magnet.as_dict(), dict)
            self.assertEqual(magnet.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(magnet.as_dict()["Properties"]["锁定"], 1.0)

    def test_compass(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            compass = elements.Compass(Position(0, 0, 0))
            expe.crt_elements(compass)
            self.assertIsInstance(compass.as_dict(), dict)
            self.assertEqual(compass.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(compass.as_dict()["Properties"]["锁定"], 1.0)

    def test_uniform_magnetic_field(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            field = elements.UniformMagneticField(Position(0, 0, 0))
            expe.crt_elements(field)
            self.assertIsInstance(field.as_dict(), dict)
            self.assertEqual(field.position, Position(0, 0, 0))
            # check lock status via as_dict
            self.assertEqual(field.as_dict()["Properties"]["锁定"], 0.0)

    def test_merge(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            charge = elements.NegativeCharge(Position(0, 0, 0))
            magnet = elements.BarMagnet(Position(1, 0, 0))
            expe.crt_elements(charge, magnet)
            self.assertEqual(expe.get_elements_count(), 2)
            with experiment.crt_electromagnetism_experiment(None) as expe2:
                compass = elements.Compass(Position(0, 1, 0))
                field = elements.UniformMagneticField(Position(1, 1, 0))
                expe2.crt_elements(compass, field)
                self.assertEqual(expe2.get_elements_count(), 2)
                expe.merge(expe2)
                self.assertEqual(expe.get_elements_count(), 4)


if __name__ == "__main__":
    unittest.main()
