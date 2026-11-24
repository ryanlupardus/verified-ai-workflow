import json
from pathlib import Path
import subprocess
import sys
import unittest


class WorkflowCLITest(unittest.TestCase):
    def test_cli_reproduces_retained_reports_and_exit_codes(self):
        root = Path(__file__).resolve().parent
        for version, exit_code in (("v1", 1), ("v2", 0)):
            with self.subTest(version=version):
                run = subprocess.run(
                    [sys.executable, "-B", "verify.py", version],
                    cwd=root,
                    capture_output=True,
                    encoding="utf-8",
                    timeout=30,
                )
                self.assertEqual(run.returncode, exit_code, run.stderr)
                archived = (root / f"result-{version}.json").read_text(encoding="utf-8")
                self.assertEqual(json.loads(run.stdout), json.loads(archived))
