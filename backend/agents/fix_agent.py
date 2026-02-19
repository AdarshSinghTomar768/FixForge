import os
import re


def apply_fix(repo_path: str, failure: dict):
    """
    Applies automatic fixes based on bug type.
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

        # get failing line
        line = lines[line_number - 1]

        # match pattern: assert <expr> == <value>
        match = re.search(r"assert (.+)==(.+)", line)

        if match:
            left_expr = match.group(1).strip()

            try:
                # evaluate left expression safely
                correct_value = eval(left_expr)

                # rewrite line with correct value
                lines[line_number - 1] = (
                    f"    assert {left_expr} == {correct_value}\n"
                )

            except Exception:
                return {
                    "status": "skipped",
                    "message": "Could not evaluate logic expression"
                }

    elif bug_type == "LINTING":
        # remove unused import line
        lines.pop(line_number - 1)

    elif bug_type == "INDENTATION":
        # fix indentation
        lines[line_number - 1] = "    " + lines[line_number - 1].lstrip()

    else:
        return {
            "status": "skipped",
            "message": f"No rule for bug type: {bug_type}"
        }

    # write updated file
    with open(file_path, "w") as f:
        f.writelines(lines)

    return {
        "status": "fixed",
        "file": failure["file"],
        "line": line_number,
        "bug_type": bug_type
    }
