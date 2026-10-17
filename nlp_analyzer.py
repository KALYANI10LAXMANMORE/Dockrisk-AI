import re


SUSPICIOUS_PHRASES = {
    "Payment-related phrase": [
        "pay registration fee",
        "processing fee required",
        "pay amount",
        "send money"
    ],

    "Urgency-related phrase": [
        "act now",
        "immediately",
        "limited time",
        "within 24 hours"
    ],

    "Job promise phrase": [
        "guaranteed job",
        "100% placement",
        "guaranteed income"
    ]
}


def preprocess_text(text):
    """
    Clean and normalize document text.
    """

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = text.strip().lower()

    return text


def analyze_text_with_nlp(text):
    """
    Perform basic phrase-based NLP analysis.
    """

    cleaned_text = preprocess_text(text)

    findings = []

    for category, phrases in SUSPICIOUS_PHRASES.items():

        matched_phrases = []

        for phrase in phrases:

            if phrase in cleaned_text:
                matched_phrases.append(phrase)

        if matched_phrases:

            findings.append({
                "category": category,
                "matched_phrases": matched_phrases
            })

    return findings