import re


def normalize_text(value):
    """
    Normalize text for comparison.
    """

    if not value:
        return ""

    value = value.lower().strip()

    # Remove extra spaces
    value = re.sub(r"\s+", " ", value)

    return value


def compare_values(expected, actual):
    """
    Compare expected and actual values.
    """

    expected = normalize_text(expected)
    actual = normalize_text(actual)

    if not expected or not actual:
        return "UNKNOWN"

    # Exact match
    if expected == actual:
        return "MATCH"

    # One value contains the other
    if expected in actual or actual in expected:
        return "VERIFY"

    return "MISMATCH"


def check_mismatch(expected_data, actual_data):
    """
    Compare expected information with information
    found in the uploaded document.
    """

    results = []

    for field, expected_value in expected_data.items():

        actual_value = actual_data.get(field)

        status = compare_values(
            expected_value,
            actual_value
        )

        results.append({
            "field": field,
            "expected": expected_value,
            "actual": actual_value,
            "status": status
        })

    return results