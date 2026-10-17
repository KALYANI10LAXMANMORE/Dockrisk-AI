import re


def check_required_documents(text, required_documents):
    """
    Check whether required documents are mentioned in the document text.
    """

    text_lower = text.lower()

    results = []

    for document in required_documents:

        if document.lower() in text_lower:
            status = "FOUND"
        else:
            status = "MISSING"

        results.append({
            "document": document,
            "status": status
        })

    return results


def check_required_fields(text, required_fields):
    """
    Check whether required information/fields are present.
    """

    text_lower = text.lower()

    results = []

    for field in required_fields:

        # Convert field name into a flexible search pattern
        words = field.lower().split()

        found = all(
            re.search(r"\b" + re.escape(word) + r"\b", text_lower)
            for word in words
        )

        status = "FOUND" if found else "MISSING"

        results.append({
            "field": field,
            "status": status
        })

    return results


def run_compliance_check(
    text,
    required_documents,
    required_fields
):
    """
    Run complete compliance analysis.
    """

    document_results = check_required_documents(
        text,
        required_documents
    )

    field_results = check_required_fields(
        text,
        required_fields
    )

    missing_documents = [
        item["document"]
        for item in document_results
        if item["status"] == "MISSING"
    ]

    missing_fields = [
        item["field"]
        for item in field_results
        if item["status"] == "MISSING"
    ]

    return {
        "documents": document_results,
        "fields": field_results,
        "missing_documents": missing_documents,
        "missing_fields": missing_fields
    }