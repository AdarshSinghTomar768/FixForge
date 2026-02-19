import re


def parse_failures(pytest_output: str):
    """
    Parse pytest output to extract file and line numbers
    """

    failures = []

    # improved pattern for pytest errors
    pattern = r"([\w./-]+\.py):(\d+):"

    matches = re.findall(pattern, pytest_output)

    seen = set()

    for file_path, line_number in matches:
        key = (file_path, line_number)

        # avoid duplicates
        if key in seen:
            continue
        seen.add(key)

        failures.append({
            "file": file_path,
            "line": int(line_number),
            "bug_type": "TEST_FAILURE",
            "error": "Assertion/Test failure"
        })

    return failures
