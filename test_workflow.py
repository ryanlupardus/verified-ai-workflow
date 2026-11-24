import unittest

from candidate_v2 import Cart
from verify import check, report


class WorkflowTest(unittest.TestCase):
    def test_both_candidates_face_identical_inputs_and_checker(self):
        before, after = report("v1"), report("v2")
        self.assertEqual((before["status"], before["failures"], before["cases"]), ("FAIL", 8, 18))
        self.assertEqual((after["status"], after["failures"], after["cases"]), ("PASS", 0, 18))
        self.assertEqual(next(row["case"] for row in before["findings"] if not row["passed"]), "outer_discard")
        for name in ("orders.csv", "expected.json", "requirements.md", "verify.py"):
            self.assertEqual(before["sha256"][name], after["sha256"][name])
        self.assertNotEqual(before["sha256"]["candidate_v1.py"], after["sha256"]["candidate_v2.py"])

    def test_detached_export_and_separate_carts(self):
        left, right = Cart(), Cart()
        left.put("x", 0)
        left.export()["x"] = 9
        self.assertEqual(left.read("x"), 0)
        self.assertIsNone(right.read("x"))

    def test_missing_or_duplicate_expectations_cannot_pass(self):
        row = {"case_id": "one"}
        for rows, expected in (([], {}), ([row], {}), ([row, row], {"one": {}})):
            with self.assertRaisesRegex(ValueError, "IDs must match"):
                check(Cart, rows, expected)

    def test_invalid_save_leaves_session_open_and_inner_discard_works(self):
        cart = Cart()
        cart.put("x", 2)
        cart.begin()
        cart.put("x", 3)
        cart.begin()
        cart.put("x", 4)
        with self.assertRaises(TypeError):
            cart.finish(1)
        cart.finish(False)
        self.assertEqual(cart.read("x"), 3)
        cart.finish(True)
        self.assertEqual(cart.read("x"), 3)
