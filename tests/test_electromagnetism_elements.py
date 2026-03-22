import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys
sys.path.append(LIBRARY_DIR)

import pathlib
import unittest
from ._constant import *
from physicsLab.electromagnetism import experiment

class TestElectromagnetismExperiment(unittest.TestCase):
    def test_load_from_filepath(self):
        with experiment.load_electromagnetism_experiment_by_file_path(pathlib.Path(TEST_DATA_DIR) / "All-Electromagnetism-Elements.sav") as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_from_exported_filepath(self):
        with experiment.load_electromagnetism_experiment_by_file_path(pathlib.Path(TEST_DATA_DIR) / "Export-All-Electromagnetism-Elements.sav") as expe:
            self.assertTrue(expe.get_elements_count() == 7)
            expe.save_to(pathlib.Path(os.devnull))

if __name__ == "__main__":
    unittest.main()
