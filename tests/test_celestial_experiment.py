import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys

sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import _user
import pathlib
import inspect
import re
import unittest
import _constant
from physicslab import (
    Position,
    Velocity,
    Acceleration,
    generate_a_new_sav_path,
    Category,
    find_path_of_sav_name,
    crt_celestial_experiment,
    load_celestial_experiment_by_file_path,
    load_celestial_experiment_from_app,
    load_celestial_experiment_by_sav_name,
    ElementNotExistError,
    ExperimentNotExistError,
)
from physicslab.celestial import planets
from physicslab.celestial._base import CelestialBase


class TestCelestialExperiment(unittest.TestCase):
    def test_introduction_round_trip_in_summary(self):
        intro = "line1\nline2"
        with crt_celestial_experiment("intro-test") as expe:
            expe.introduction = intro
            self.assertEqual(expe.as_plsav_dict()["Summary"]["Description"], ["line1", "line2"])

        with load_celestial_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "All-Celestial-Elements.sav"
        ) as expe:
            self.assertTrue(expe.introduction is None)

    def test_remove_element(self):
        with crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            earth = planets.Earth(Position(10, 0, 0))
            expe.crt_elements(sun, earth)
            self.assertTrue(expe.get_elements_count() == 2)
            expe.del_a_element(earth)
            self.assertTrue(expe.get_elements_count() == 1)

    def test_load_celestial_experiment_by_sav_name(self):
        name = "__test_load_celestial_experiment_by_sav_name__"
        path = find_path_of_sav_name(name)
        if path is None:
            with crt_celestial_experiment(name) as expe:
                expe.crt_elements(planets.Sun(Position(0, 0, 0)))
                new_sav_path = generate_a_new_sav_path()
                if not new_sav_path.parent.exists():
                    new_sav_path.parent.mkdir(parents=True)
                expe.save_to(new_sav_path)

        expe, filepath = load_celestial_experiment_by_sav_name(name)
        self.assertGreaterEqual(expe.get_elements_count(), 1)
        filepath.unlink()

    def test_merge(self):
        with crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            expe.crt_elements(sun)
            self.assertEqual(expe.get_elements_count(), 1)

            with crt_celestial_experiment(None) as expe2:
                earth = planets.Earth(Position(10, 0, 0))
                moon = planets.Moon(Position(10.1, 0, 0))
                expe2.crt_elements(earth, moon)
                self.assertEqual(expe2.get_elements_count(), 2)
                expe.merge(expe2)
                self.assertEqual(expe.get_elements_count(), 3)

    def test_load_all_element(self):
        with load_celestial_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "All-Celestial-Elements.sav"
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_all_element_from_exported_sav(self):
        with load_celestial_experiment_by_file_path(
            pathlib.Path(_constant.TEST_DATA_DIR) / "Export-All-Celestial-Elements.sav"
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save_to(pathlib.Path(os.devnull))

    def test_load_from_app(self):
        with load_celestial_experiment_from_app(
            "677500138c54132a83289f9c", Category.Discussion, user=_user.user
        ) as expe:
            self.assertTrue(expe.get_elements_count() == 27)
            expe.save_to(pathlib.Path(os.devnull))

    def test_get_element_by_index(self):
        with crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            earth = planets.Earth(Position(10, 0, 0))
            expe.crt_elements(sun, earth)
            self.assertEqual(expe.get_element_by_index(0), sun)
            self.assertEqual(expe.get_element_by_index(1), earth)

            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_index(2)

    def test_get_element_by_id(self):
        with crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            earth = planets.Earth(Position(10, 0, 0))
            expe.crt_elements(sun, earth)
            self.assertEqual(expe.get_element_by_id(sun.identifier), sun)
            self.assertEqual(expe.get_element_by_id(earth.identifier), earth)

            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_id("nonexistent_id")

    def test_get_element_by_position(self):
        with crt_celestial_experiment(None) as expe:
            sun = planets.Sun(Position(0, 0, 0))
            earth = planets.Earth(Position(10, 0, 0))
            expe.crt_elements(sun, earth)
            self.assertEqual(expe.get_element_by_position(sun.position), sun)
            self.assertEqual(expe.get_element_by_position(earth.position), earth)

            with self.assertRaises(ElementNotExistError):
                expe.get_element_by_position(Position(1, 1, 1))

    def test_load_nonexistent_file_path(self):
        with self.assertRaises(ExperimentNotExistError):
            load_celestial_experiment_by_file_path(
                pathlib.Path(_constant.TEST_DATA_DIR) / "nonexistent_file.sav"
            )


class TestCelestialElements(unittest.TestCase):
    def test_mercury(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Mercury(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Mercury")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_venus(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Venus(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Venus")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_sun(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Sun(Position(1, 2, 3), velocity=Velocity(0.1, 0.2, 0.3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.velocity, Velocity(0.1, 0.2, 0.3))
        # Check specific fields for Sun
        self.assertEqual(_instance.as_dict()["Model"], "Sun")
        self.assertEqual(_instance.as_dict()["Mass"], 1989100.0)
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_earth(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Earth(Position(1, 2, 3), velocity=Velocity(0, 1, 0))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Model"], "Earth")
        self.assertEqual(_instance.as_dict()["Name"], "地球")
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_mars(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Mars(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Mars")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_jupiter(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Jupiter(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Jupiter")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_saturn(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Saturn(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Saturn")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_uranus(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Uranus(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Uranus")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_neptune(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Neptune(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Neptune")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_pluto(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Pluto(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Pluto")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_blue_giant(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.BlueGiant(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Blue Giant")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_red_giant(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.RedGiant(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Red Giant")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_red_dwarf(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.RedDwarf(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Red Dwarf")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_white_dwarf(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.WhiteDwarf(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "White Dwarf")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_blackhole(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Blackhole(Position(1, 2, 3), velocity=Velocity(0, 0, 0))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Blackhole")
        self.assertEqual(_instance.as_dict()["Type"], -1)  # Check type identifier
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_fantasy_star(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.FantasyStar(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Fantasy Star")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_moon(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Moon(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Moon")
        self.assertEqual(_instance.as_dict()["Type"], 2)
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_chocolate_ball(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.ChocolateBall(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Chocolate Ball")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_continential(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Continential(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Continential")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_arctic(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Arctic(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Arctic")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_arid(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Arid(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Arid")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_barren(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Barren(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Barren")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_desert(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Desert(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Desert")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_jungle(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Jungle(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Jungle")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_toxic(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Toxic(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Toxic")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_lava(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Lava(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Lava")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_ocean(self):
        expe = crt_celestial_experiment(None)
        _instance = planets.Ocean(Position(1, 2, 3))
        expe.crt_elements(_instance)

        self.assertEqual(_instance.as_dict()["Model"], "Ocean")
        self.assertEqual(_instance.position, Position(1, 2, 3))
        self.assertEqual(_instance.as_dict()["Position"], "1,3,2")

        constructor_str = _instance.to_constructor_str()
        self.assertIsInstance(constructor_str, str)
        eval(f"planets.{constructor_str}")

    def test_all_celestial_classes_are_covered(self):
        all_celestial_classes = {
            name
            for name, obj in inspect.getmembers(planets, inspect.isclass)
            if issubclass(obj, CelestialBase)
            and obj is not CelestialBase
            and obj.__module__.startswith("physicslab.celestial.")
            and not name.startswith("_")
        }

        covered_classes = set()
        for method_name, method in inspect.getmembers(
            self.__class__, inspect.isfunction
        ):
            if not method_name.startswith("test_"):
                continue
            if method_name == "test_all_celestial_classes_are_covered":
                continue

            source = inspect.getsource(method)
            covered_classes.update(re.findall(r"planets\.(\w+)\(", source))

        missing = sorted(all_celestial_classes - covered_classes)
        self.assertEqual(
            missing,
            [],
            msg=f"Missing TestCelestialElements coverage for: {', '.join(missing)}",
        )


if __name__ == "__main__":
    unittest.main()
