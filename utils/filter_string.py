import re


def filter_string(unfiltered_string: str) -> str:
    """filters a string based on salesforce reserved characters for sosl"""

    sf_query_reserved_characters = str.maketrans({"?": r"\?", "&": r"\&", "|": r"\|", "!": r"\!",
                                                  "{": r"\{", "}": r"\}", "[": r"[?", "(": r"\(",
                                                  ")": r"\)", "~": r"\~", ":": r"\:", "\"": r"\"",
                                                  "\'": r"\'", "+": r"\+", "-": r"\-", "]": r"\]", "\\": r"\\",
                                                  "^": r"\^", "$": r"\$", "*": r"\*"})

    filtered_string = unfiltered_string.translate(sf_query_reserved_characters)
    return filtered_string
