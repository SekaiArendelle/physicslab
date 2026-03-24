import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys

sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import base
import pathlib
import unittest
import _constant
from physicsLab import Position, Velocity, generate_a_new_sav_path, Category
from physicsLab.celestial import planets
from physicsLab.celestial import experiment


class TestCelestialExperiment(unittest.TestCase):
    def test_remove_element(self):
        with experiment.crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            earth = planets.Earth(Position(10, 0, 0))
            expe.crt_elements(sun, earth)
            self.assertTrue(expe.get_elements_count() == 2)
            expe.del_a_element(earth)
            self.assertTrue(expe.get_elements_count() == 1)

    def test_load_celestial_experiment_by_sav_name(self):
        name = "__test_load_celestial_experiment_by_sav_name__"
        path = experiment.find_path_of_sav_name(name)
        if path is None:
            with experiment.crt_celestial_experiment(name) as expe:
                expe.crt_elements(planets.Sun(Position(0, 0, 0)))
                expe.save_to(generate_a_new_sav_path())

        expe, filepath = experiment.load_celestial_experiment_by_sav_name(name)
        self.assertGreaterEqual(expe.get_elements_count(), 1)
        filepath.unlink()

    def test_merge(self):
        with experiment.crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            expe.crt_elements(sun)
            self.assertEqual(expe.get_elements_count(), 1)

            with experiment.crt_celestial_experiment(None) as expe2:
                earth = planets.Earth(Position(10, 0, 0))
                moon = planets.Moon(Position(10.1, 0, 0))
                expe2.crt_elements(earth, moon)
                self.assertEqual(expe2.get_elements_count(), 2)
                expe.merge(expe2)
                self.assertEqual(expe.get_elements_count(), 3)

    def test_load_all_element(self):
        with experiment.load_celestial_experiment_by_file_path(pathlib.Path(_constant.TEST_DATA_DIR) / "All-Celestial-Elements.sav") as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save_to(pathlib.Path(os.devnull))


    def test_load_all_element_from_exported_sav(self):
        with experiment.load_celestial_experiment_by_file_path(pathlib.Path(_constant.TEST_DATA_DIR) / "Export-All-Celestial-Elements.sav") as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_from_app(self):
        with experiment.load_celestial_experiment_from_app("677500138c54132a83289f9c", Category.Discussion, user=base.user) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save_to(pathlib.Path(os.devnull))


class TestCelestialElement(unittest.TestCase):
    def test_mercury(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Mercury(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Mercury")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_venus(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Venus(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Venus")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_sun(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Sun(Position(1, 2, 3), velocity=Velocity(0.1, 0.2, 0.3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
        # Check specific fields for Sun
        self.assertEqual(_instance.as_dict()["Model"], "Sun")
        self.assertEqual(_instance.as_dict()["Mass"], 1989100.0)
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_earth(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Earth(Position(1, 2, 3), velocity=Velocity(0, 1, 0))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Model"], "Earth")
        self.assertEqual(_instance.as_dict()["Name"], "地球")
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_mars(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Mars(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Mars")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_jupiter(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Jupiter(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Jupiter")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_saturn(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Saturn(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Saturn")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_uranus(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Uranus(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Uranus")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_neptune(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Neptune(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Neptune")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_pluto(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Pluto(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Pluto")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_blue_giant(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.BlueGiant(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Blue Giant")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_red_giant(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.RedGiant(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Red Giant")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_red_dwarf(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.RedDwarf(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Red Dwarf")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_white_dwarf(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.WhiteDwarf(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "White Dwarf")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_blackhole(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Blackhole(Position(1, 2, 3), velocity=Velocity(0, 0, 0))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Blackhole")
        self.assertEqual(_instance.as_dict()["Type"], -1)  # Check type identifier
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_fantasy_star(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.FantasyStar(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Fantasy Star")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_moon(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Moon(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Moon")
        self.assertEqual(_instance.as_dict()["Type"], 2)
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_chocolate_ball(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.ChocolateBall(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Chocolate Ball")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_continential(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Continential(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Continential")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_arctic(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Arctic(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Arctic")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_arid(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Arid(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Arid")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_barren(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Barren(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Barren")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_desert(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Desert(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Desert")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_jungle(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Jungle(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Jungle")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_toxic(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Toxic(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Toxic")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_lava(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Lava(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Lava")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

    def test_ocean(self):
        expe = experiment.crt_celestial_experiment(None)
        _instance = planets.Ocean(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Ocean")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")


if __name__ == "__main__":
    unittest.main()
