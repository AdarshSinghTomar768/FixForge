def classify_bug(error_text: str):
    """
    Classify bug type based on pytest error output.
    """

    text = error_text.lower()

    if "syntaxerror" in text:
        return "SYNTAX"

    elif "importerror" in text or "modulenotfounderror" in text:
        return "IMPORT"

    elif "typeerror" in text:
        return "TYPE_ERROR"

    elif "indentationerror" in text:
        return "INDENTATION"

    elif "assertionerror" in text:
        return "LOGIC"

    elif "unused import" in text or "flake8" in text:
        return "LINTING"

    return "UNKNOWN"
