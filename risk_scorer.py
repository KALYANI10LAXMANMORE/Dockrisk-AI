def calculate_risk_score(
    risks,
    missing_documents,
    missing_fields,
    mismatches
):
    """
    Calculate overall document risk score from 0 to 100.
    """

    score = 0

    # Risk detected
    score += len(risks) * 15

    # Missing documents
    score += len(missing_documents) * 10

    # Missing required fields
    score += len(missing_fields) * 5

    # Mismatches
    score += len(mismatches) * 15

    # Maximum score = 100
    score = min(score, 100)

    # Risk level
    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level
    }


def get_risk_message(level):
    """
    Return a simple explanation for the risk level.
    """

    messages = {
        "LOW": "The document appears to have a relatively low risk.",
        "MEDIUM": "The document contains some issues that should be reviewed.",
        "HIGH": "The document contains significant risk indicators and requires careful verification."
    }

    return messages.get(
        level,
        "Risk level could not be determined."
    )