
import os
import sys
import pathlib
import warnings
import threading
from .base import *
from ._constant import *
from physicsLab.coordinate_system import Position
from physicsLab._core import _ExperimentStack
from physicsLab._typing import Callable

def my_test_dec(method: Callable):
    def result(*args, **kwarg):
        method(*args, **kwarg)

        if len(_ExperimentStack.data) != 0:
            print(f"File {os.path.abspath(__file__)}, line {method.__code__.co_firstlineno} : "
                  f"test fail due to len(stack_Experiment) != 0")
            _ExperimentStack.clear()
            raise TestFail
    return result

class BasicTest(TestCase):
    @my_test_dec
    def test_experiment_stack(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe1:
            self.assertTrue(_ExperimentStack.inside(expe1))
            with Experiment(OpenMode.crt, "_Test", ExperimentType.Circuit, force_crt=True) as expe2:
                self.assertTrue(_ExperimentStack.inside(expe2))
                expe1.close(delete=True)
                self.assertFalse(_ExperimentStack.inside(expe1))
                expe2.close(delete=True)
                self.assertFalse(_ExperimentStack.inside(expe2))

    @my_test_dec
    def test_load_all_elements(self):
        # 物实导出存档与保存到本地的格式不一样, 因此每种类型的实验都有两种格式的测试数据
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.save(target_path=os.devnull)
            expe.close()

        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Circuit-Elements.sav")) as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.save(target_path=os.devnull)
            expe.close()

    @my_test_dec
    def test_load_from_app(self):
        with Experiment(OpenMode.load_by_plar_app, "6774ffb4c45f930f41ccedf8", Category.Discussion) as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.save(target_path=os.devnull)
            expe.close()

    @my_test_dec
    def test_double_load_error(self):
        expe = Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav"))
        try:
            Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "All-Circuit-Elements.sav"))
        except ExperimentOpenedError:
            pass
        else:
            raise TestFail
        finally:
            expe.close()

    @my_test_dec
    def test_load_invalid_sav(self):
        try:
            Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "invalid.sav"))
        except InvalidSavError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_float32_t_sav(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "float32_t.sav")) as expe:
            self.assertEqual(expe.get_elements_count(), 652)
            self.assertEqual(expe.get_wires_count(), 1385)
            expe.close()

    @my_test_dec
    def test_normal_circuit_usage(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Yes_Gate(0, 0, 0)
            self.assertEqual(expe.get_elements_count(), 1)
            self.assertEqual(a.get_position(), Position(0, 0, 0))
            crt_wire(a.o, a.i)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.clear_wires()
            self.assertEqual(expe.get_wires_count(), 0)
            self.assertEqual(expe.get_elements_count(), 1)
            crt_wire(a.o, a.i)
            expe.crt_element("Logic Input", 0, 0, 0)
            self.assertEqual(expe.get_elements_count(), 2)
            expe.get_element_from_position(0, 0, 0)
            expe.close(delete=True)

    @my_test_dec
    def test_read_experiment(self):
        with Experiment(OpenMode.crt, "__test___read_experiment__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(expe.get_elements_count(), 0)
            self.assertEqual(expe.get_wires_count(), 0)
            Logic_Input(0, 0, 0)
            expe.save()
            expe.close(delete=False)

        with Experiment(OpenMode.load_by_sav_name, "__test___read_experiment__") as exp2:
            self.assertEqual(exp2.get_elements_count(), 1)
            exp2.close(delete=True)

    @my_test_dec
    def test_crt_experiment(self):
        expe: Experiment = Experiment(OpenMode.crt, "__test___crt_experiment__", ExperimentType.Circuit, force_crt=True)
        expe.save()
        try:
            Experiment(OpenMode.crt, "__test___crt_experiment__", ExperimentType.Circuit) # will fail
        except ExperimentExistError:
            pass
        else:
            raise TestFail
        finally:
            expe.close(delete=True)

    @my_test_dec
    def test_crt_wire(self):
        with Experiment(OpenMode.crt, "__test___crt_wire__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, a.i_low, color=WireColor.red)
            self.assertEqual(expe.get_wires_count(), 2)

            del_wire(a.o, a.i_up)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.close(delete=True)

    def test_same_crt_wire(self):
        with Experiment(OpenMode.crt, "__test___same_crt_wire__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Or_Gate(0, 0, 0)
            crt_wire(a.o, a.i_up, color=WireColor.red)
            crt_wire(a.i_up, a.o)
            self.assertEqual(expe.get_wires_count(), 1)
            expe.close(delete=True)

    @my_test_dec
    def test_get_Element(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Or_Gate(0, 0, 0)
            crt_wire(
                expe.get_element_from_position(0, 0, 0)[0].o,
                expe.get_element_from_index(1).i_up
            )
            crt_wire(
                expe.get_element_from_position(0, 0, 0)[0].i_low,
                expe.get_element_from_index(1).o
            )
            self.assertEqual(expe.get_wires_count(), 2)
            expe.close(delete=True)

    @my_test_dec
    def test_errors(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            # 确保__test__实验不存在
            expe.close(delete=True)
        try:
            Experiment(OpenMode.load_by_sav_name, '__test__') # do not exist
        except ExperimentNotExistError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_elementXYZ_2(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            expe.is_elementXYZ = True
            for x in range(10):
                for y in range(10):
                    Yes_Gate(x, y, 0)
            for x in range(10):
                for y in [y * 2 + 10 for y in range(5)]:
                    Multiplier(x, y, 0)

            crt_wire(expe.get_element_from_index(1).o, expe.get_element_from_position(0, 1, 0)[0].i)
            crt_wire(
                expe.get_element_from_index(2).i,
                expe.get_element_from_index(3).o,
                expe.get_element_from_index(4).i
            )
            self.assertEqual(expe.get_wires_count(), 3)
            self.assertEqual(expe.get_elements_count(), 150)
            expe.close(delete=True)

    @my_test_dec
    def test_open_a_lot_of_experiments(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Input(0, 0, 0)
                self.assertEqual(1, exp2.get_elements_count())
                exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_with_and_coverPosition(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            Or_Gate(0, 0, 0)
            self.assertEqual(len(expe.get_element_from_position(0, 0, 0)), 2)
            expe.close(delete=True)

    @my_test_dec
    def test_del_element(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            crt_wire(Logic_Input(0, 0, 0).o, Or_Gate(0, 0, 0).o)
            expe.del_element(expe.get_element_from_index(2))
            self.assertEqual(expe.get_elements_count(), 1)
            self.assertEqual(expe.get_wires_count(), 0)
            expe.close(delete=True)

        with Experiment(OpenMode.load_by_filepath, pathlib.Path(TEST_DATA_DIR) / "All-Circuit-Elements.sav") as expe:
            expe.del_element(expe.get_element_from_index(1))
            self.assertEqual(expe.get_elements_count(), 90)
            expe.close()

    @my_test_dec
    def test_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Simple_Instrument(0, 0, 0, pitches=(48,))
            a = Simple_Instrument(0, 0, 0, pitches=(Simple_Instrument.str2num_pitch("C3"),))
            expe.close(delete=True)

    @my_test_dec
    def test_get_element_error(self):
        with Experiment(OpenMode.crt, "__test___get_element_error__", ExperimentType.Circuit, force_crt=True) as expe:
            Logic_Input(0, 0, 0)
            try:
                expe.get_element_from_index(2)
            except ElementNotFound:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

    @my_test_dec
    def test_is_bigElement(self):
        with Experiment(OpenMode.crt, "__test___is_bigElement__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(Logic_Output.is_bigElement, False)
            self.assertEqual(Multiplier.is_bigElement, True)
            self.assertEqual(Or_Gate.is_bigElement, False)
            self.assertEqual(Logic_Input(0, 0, 0).is_bigElement, False)
            self.assertEqual(Full_Adder(0, 0, 0).is_bigElement, True)
            self.assertEqual(Xor_Gate(0, 0, 0).is_bigElement, False)
            expe.close(delete=True)

    @my_test_dec
    def test_mutiple_notes_in_Simple_Instrument(self):
        with Experiment(OpenMode.crt, "__test__", ExperimentType.Circuit, force_crt=True) as expe:
            Simple_Instrument(0, 0, 0, pitches=(67,))
            expe.close(delete=True)

    @my_test_dec
    def test_merge_experiment(self):
        with Experiment(OpenMode.crt, "__test___merge_experiment__", ExperimentType.Circuit, force_crt=True) as expe:
            crt_wire(Logic_Input(0, 0, 0).o, Logic_Output(1, 0, 0, elementXYZ=True).i)

            with Experiment(OpenMode.crt, "__test___merge_experiment_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)

                self.assertEqual(exp2.get_elements_count(), 3)
                exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_link_wire_in_two_experiment(self):
        with Experiment(OpenMode.crt, "__test___link_wire_in_two_experiment__", ExperimentType.Circuit, force_crt=True) as expe:
            a = Logic_Input(0, 0, 0)
            with Experiment(OpenMode.crt, "__test___link_wire_in_two_experiment_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                b = Logic_Output(0, 0, 0)
                try:
                    crt_wire(a.o, b.i)
                except InvalidWireError:
                    pass
                else:
                    raise TestFail
                finally:
                    exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_merge_experiment2(self):
        with Experiment(OpenMode.crt, "__test___merge_experiment2__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Yes_Gate(0, 0, 0)
            crt_wire(e.i, e.o)

            with Experiment(OpenMode.crt, "__test___merge_experiment2_sub__", ExperimentType.Circuit, force_crt=True) as exp2:
                Logic_Output(0, 0, 0.1)
                exp2.merge(expe, 1, 0, 0, elementXYZ=True)
                a = exp2.get_element_from_position(1, 0, 0)[0]
                crt_wire(a.i, a.o)

                self.assertEqual(exp2.get_elements_count(), 2)
                self.assertEqual(expe.get_wires_count(), 1)
                exp2.close(delete=True)
            expe.close(delete=True)

    @my_test_dec
    def test_crt_self_wire(self):
        with Experiment(OpenMode.crt, "__test___crt_self_wire__", ExperimentType.Circuit, force_crt=True) as expe:
            e = Logic_Output(0, 0, 0)
            try:
                crt_wire(e.i, e.i)
            except InvalidWireError:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

    @my_test_dec
    def test_export(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "float32_t.sav")) as expe:
            expe.export("temp.pl.py", "__test___export__")
            expe.close()

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "__test___export__") as expe:
            self.assertEqual(expe.get_elements_count(), 652)
            self.assertEqual(expe.get_wires_count(), 1385)
            expe.close(delete=True)

    @my_test_dec
    def test_export2(self):
        with Experiment(OpenMode.load_by_filepath, os.path.join(TEST_DATA_DIR, "Export-All-Circuit-Elements.sav")) as expe:
            expe.export("temp.pl.py", "__test__")
            expe.close()

        os.system(f"{sys.executable} temp.pl.py")
        with Experiment(OpenMode.load_by_sav_name, "__test__") as expe:
            self.assertTrue(expe.get_elements_count() == 91)
            expe.close(delete=True)

    @my_test_dec
    def test_type_error(self):
        with Experiment(OpenMode.crt, "__test___type_error__", ExperimentType.Circuit, force_crt=True) as expe:
            try:
                Logic_Input(0, 0, 0, True) # type: ignore
            except TypeError:
                pass
            else:
                raise TestFail
            finally:
                expe.close(delete=True)

    @my_test_dec
    def test_wire_is_too_less(self):
        try:
            with Experiment(OpenMode.crt, "__test___wire_is_too_less__", ExperimentType.Circuit, force_crt=True) as expe:
                crt_wire(Logic_Input(0, 0, 0).o)
        except ValueError:
            pass
        else:
            raise TestFail

    @my_test_dec
    def test_count_all_pins(self):
        self.assertEqual(Multiplier.count_all_pins(), 8)

    @my_test_dec
    def test_get_pin_name(self):
        with Experiment(OpenMode.crt, "__test___get_pin_name__", ExperimentType.Circuit, force_crt=True) as expe:
            self.assertEqual(Multiplier(0, 0, 0).i_low.get_pin_name(), "i_low")
            expe.close(delete=True)

    @my_test_dec
    def test_type_pin(self):
        self.assertTrue(isinstance(InputPin, type(Pin)))
        self.assertTrue(isinstance(OutputPin, type(Pin)))
        self.assertFalse(isinstance(ElementBase, type(Pin)))

    @my_test_dec
    def test_translate_elementXYZ(self):
        o = Position(1, 2, -1)
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    x_, y_, z_ = elementXYZ_to_native(*native_to_elementXYZ(x, y, z, o), o)
                    assert x == x_
                    assert y == y_
                    assert z == z_
