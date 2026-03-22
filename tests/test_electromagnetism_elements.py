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


if __name__ == "__main__":
    unittest.main()
