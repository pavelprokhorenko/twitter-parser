from re import compile

SELECT_ABBREVIATIONS_PATTERN = compile(r"(.)([A-Z][a-z]+)")
SEPARATE_WORD_FORM_ABBREVIATIONS_PATTERN = compile(r"([a-z0-9])([A-Z])")


def to_snake_case_safe(camel_str: str) -> str:
    """
    Convert string from `camelCase` to `snake_case`
    with saving abbreviation (or any string with multiple consecutive capital letters),
    e.g. getHTTPResponse -> get_http_response.

    Warning! Conversion is not reversible anymore.
    You cannot get "getHTTPResponse" from "get_http_response".
    """

    camel_str = SELECT_ABBREVIATIONS_PATTERN.sub(r"\1_\2", camel_str)
    return SEPARATE_WORD_FORM_ABBREVIATIONS_PATTERN.sub(r"\1_\2", camel_str).lower()
