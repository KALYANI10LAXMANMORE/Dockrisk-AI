import re
def clean_value(value):
    if not value:
        return None

    value = re.sub(r"\s+", " ", value)
    value = value.strip(" :-\t\n")

    return value if value else None


def extract_information(text):
    """
    Extract important information from document text.
    Used for DocRisk AI mismatch and risk analysis.
    """

    information = {}

    # -------------------------------------------------
    # EMAIL
    # -------------------------------------------------
    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    information["email"] = email[0] if email else None

    # -------------------------------------------------
    # PHONE NUMBER
    # -------------------------------------------------
    phone = re.findall(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    information["phone"] = phone[0] if phone else None

    # -------------------------------------------------
    # WEBSITE
    # -------------------------------------------------
    website = re.findall(
        r"(?:https?://|www\.)[^\s]+",
        text
    )

    information["website"] = website[0] if website else None

    # -------------------------------------------------
    # DATE
    # -------------------------------------------------
    dates = re.findall(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|\d{1,2}\s+[A-Za-z]+\s+\d{4})\b",
        text
    )

    information["dates"] = dates

    # -------------------------------------------------
    # DURATION
    # -------------------------------------------------
    duration = re.findall(
        r"\b\d+\s*(?:months?|weeks?|days?)\b",
        text,
        re.IGNORECASE
    )

    information["duration"] = duration

    # -------------------------------------------------
    # STIPEND / SALARY
    # -------------------------------------------------
    stipend = re.findall(
        r"(?:₹|Rs\.?|INR)\s?[\d,]+",
        text,
        re.IGNORECASE
    )

    information["salary_or_stipend"] = stipend

    # -------------------------------------------------
    # STUDENT / CANDIDATE NAME
    # -------------------------------------------------
    name_patterns = [
        r"(?:student\s*name|candidate\s*name|name)\s*[:\-]\s*([A-Za-z ]{3,50})",
    ]

    name = None

    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            name = clean_value(match.group(1))
            break

    information["student_name"] = name
    information["candidate_name"] = name

    # -------------------------------------------------
    # COLLEGE NAME
    # -------------------------------------------------
    college_patterns = [
        r"(?:college\s*name|college|institute\s*name|institution\s*name)"
        r"\s*[:\-]\s*([A-Za-z0-9&.,() \-]{5,100})"
    ]

    college = None

    for pattern in college_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            college = clean_value(match.group(1))
            break

    information["college_name"] = college
    information["college"] = college

    # -------------------------------------------------
    # BRANCH
    # -------------------------------------------------
    branch_patterns = [
        r"(?:branch|department|course)\s*[:\-]\s*([A-Za-z0-9&/(). \-]{2,50})"
    ]

    branch = None

    for pattern in branch_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            branch = clean_value(match.group(1))
            break

    information["branch"] = branch

    # -------------------------------------------------
    # YEAR
    # -------------------------------------------------
    year_patterns = [
        r"(?:year|academic\s*year)\s*[:\-]\s*([A-Za-z0-9\- ]{2,30})"
    ]

    year = None

    for pattern in year_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            year = clean_value(match.group(1))
            break

    information["year"] = year

    # -------------------------------------------------
    # ANNUAL INCOME
    # -------------------------------------------------
    income_patterns = [
        r"(?:annual\s*income|family\s*income|income)"
        r"\s*[:\-]\s*(?:₹|Rs\.?|INR)?\s*([\d,]+)"
    ]

    annual_income = None

    for pattern in income_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            annual_income = clean_value(match.group(1))
            break

    information["annual_income"] = annual_income

    # -------------------------------------------------
    # RETURN ALL INFORMATION
    # -------------------------------------------------

    return information