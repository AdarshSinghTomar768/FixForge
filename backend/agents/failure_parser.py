import re
from agents.bug_classifier import classify_bug


def parse_failures(pytest_output: str):
    """
    Parse pytest output to extract file, line number,
    and classify bug type.
    """

    failures = []

    # pattern: file.py:line:
    pattern = r"([\w./-]+\.py):(\d+):"

    matches = re.findall(pattern, pytest_output)

    seen = set()

    for file_path, line_number in matches:

        key = (file_path, line_number)

        # avoid duplicates
        if key in seen:
            continue
        seen.add(key)

        # 🔥 classify bug type using error output
        bug_type = classify_bug(pytest_output)

        failures.append({
            "file": file_path,
            "line": int(line_number),
            "bug_type": bug_type,
            "error": "Test failure detected"
        })

    return failures
