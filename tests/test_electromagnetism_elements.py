import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys
sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import pathlib
import unittest
import _constant
from physicsLab import Position
from physicsLab.electromagnetism import elements
from physicsLab.electromagnetism import experiment

class TestElectromagnetismExperiment(unittest.TestCase):
    def test_load_from_filepath(self):
        with experiment.load_electromagnetism_experiment_by_file_path(pathlib.Path(_constant.TEST_DATA_DIR) / "All-Electromagnetism-Elements.sav") as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_from_exported_filepath(self):
        with experiment.load_electromagnetism_experiment_by_file_path(pathlib.Path(_constant.TEST_DATA_DIR) / "Export-All-Electromagnetism-Elements.sav") as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_remove_element(self):
        with experiment.crt_electromagnetism_experiment(None) as expe:
            negative_charge = elements.NegativeCharge(Position(0, 0, 0))
            positive_charge = elements.PositiveCharge(Position(1, 0, 0))
            expe.crt_elements(
                positive_charge, negative_charge
            )
            self.assertTrue(expe.get_elements_count() == 2)
            expe.del_a_element(negative_charge)
            self.assertTrue(expe.get_elements_count() == 1)

if __name__ == "__main__":
    unittest.main()
