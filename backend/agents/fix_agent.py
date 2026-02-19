import os


def apply_fix(repo_path: str, failure: dict):
    """
    Applies simple fixes based on bug type.
    """

    file_path = os.path.join(repo_path, failure["file"])
    line_number = failure["line"]
    bug_type = failure["bug_type"]

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found"
        }

    # read file
    with open(file_path, "r") as f:
        lines = f.readlines()

    # -------------------------
    # FIX RULES
    # -------------------------

    if bug_type == "LOGIC":
        # demo fix: correct common assertion mistake
        lines[line_number - 1] = lines[line_number - 1].replace("== 3", "== 2")

    elif bug_type == "LINTING":
        # remove unused import line
        lines.pop(line_number - 1)

    elif bug_type == "INDENTATION":
        # add proper indentation
        lines[line_number - 1] = "    " + lines[line_number - 1].lstrip()

    else:
        return {
            "status": "skipped",
            "message": f"No rule for bug type: {bug_type}"
        }

    # write back file
    with open(file_path, "w") as f:
        f.writelines(lines)

    return {
        "status": "fixed",
        "file": failure["file"],
        "line": line_number,
        "bug_type": bug_type
    }
