import json
import pathlib
import tempfile
import threading
import unittest
from unittest.mock import mock_open, patch

from physicslab import constant, quantum_physics, utils
from physicslab.version import _Version
from physicslab.web._threadpool import CanceledError, ThreadPool


class TestUtils(unittest.TestCase):
    def test_threadpool_cancel_pending_tasks_marks_task_as_cancelled(self):
        gate = threading.Event()

        def block():
            gate.wait(timeout=5)
            return "done"

        with ThreadPool(max_workers=1) as pool:
            running_task = pool.submit(block)
            pending_task = pool.submit(lambda: "pending")
            pool.cancel_all_pending_tasks()
            gate.set()

            self.assertEqual(running_task.result(), "done")
            with self.assertRaises(CanceledError):
                pending_task.result()

    def test_version_ne_uses_version_tuple(self):
        self.assertFalse(_Version(1, 2, 3) != _Version(1, 2, 3))
        self.assertTrue(_Version(1, 2, 3) != _Version(1, 2, 4))
        self.assertTrue(_Version(1, 2, 3) != object())

    @unittest.skipUnless(
        hasattr(constant, "WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR"),
        "Windows-only constant is unavailable",
    )
    def test_get_quantum_physics_version_parses_numeric_segments(self):
        with patch("physicslab.quantum_physics.os.listdir", return_value=["a"]), patch(
            "builtins.open",
            mock_open(read_data=json.dumps({"app_ver": "1.2.3"})),
        ):
            self.assertEqual(
                quantum_physics.get_quantum_physics_version(),
                (1, 2, 3),
            )

    def test_find_path_of_sav_name_skips_invalid_json_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)
            bad_file = tmp_path / "bad.sav"
            good_file = tmp_path / "good.sav"
            bad_file.write_text("{this is invalid", encoding="utf-8")
            good_file.write_text(
                json.dumps({"Summary": {"Subject": "target-name"}}),
                encoding="utf-8",
            )

            with patch.object(constant, "QUANTAM_PHYSICS_EXPERIMENT_DIR", tmp_path):
                found = utils.find_path_of_sav_name("target-name")

            self.assertEqual(found, good_file)

