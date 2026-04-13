import subprocess
import unittest


class TestTask1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        for target in ("task1", "task1_asan", "corner_case_stress.so"):
            result = subprocess.run(
                ["make", target],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Compilation of {target} failed (exit {result.returncode}):\n"
                    f"stdout: {result.stdout}\n"
                    f"stderr: {result.stderr}"
                )

    def test_output_and_exit_code(self):
        result = subprocess.run(
            ["./task1"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"task1_asan exited with code {result.returncode}")
        self.assertEqual(result.stdout, "Hello World!\n", f"Unexpected stdout: {result.stdout!r}")


    def test_no_asan_report(self):
        result = subprocess.run(
            ["./task1_asan"],
            capture_output=True,
            text=True,
        )
        self.assertNotIn(
            "ERROR: ",
            result.stderr,
            f"ASan report detected:\n{result.stderr}",
        )

    def test_malloc_override(self):
        import os
        env = os.environ.copy()
        env["LD_PRELOAD"] = "./corner_case_stress.so"
        result = subprocess.run(
            ["./task1"],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(result.returncode, 1, f"task1 exited with code {result.returncode}")
        self.assertIn("Malloc fails\n", result.stdout, f"Unexpected stdout: {result.stdout!r}")


if __name__ == "__main__":
    unittest.main()
