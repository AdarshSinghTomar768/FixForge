import subprocess
import os
from agents.failure_parser import parse_failures


def run_tests(repo_path: str):
    """
    Runs pytest inside the cloned repository
    and parses failures.
    """

    if not os.path.exists(repo_path):
        return {
            "status": "error",
            "message": "Repo path does not exist"
        }

    try:
        result = subprocess.run(
            ["pytest"],
            cwd=repo_path,       # run inside repo
            capture_output=True,
            text=True
        )

        # 🔥 Parse failures from pytest output
        failures = parse_failures(result.stdout)

        return {
            "status": "success",
            "return_code": result.returncode,
            "failures": failures,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
