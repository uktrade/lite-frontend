FIREARM_LABELS = {
    "firearm-type": "Select the type of firearm product",
    "firearm-category": "Firearm category",
    "name": "Give the product a descriptive name",
    "calibre": "What is the calibre of the product?",
    "is-registered-firearms-dealer": "Are you a registered firearms dealer?",
    "is-good-controlled": "Do you know the product's control list entry?",
    "control-list-entries": "Enter the control list entry",
    "is-pv-graded": "Does the product have a government security grading or classification?",
    "pv-grading-prefix": "Enter a prefix (optional)",
    "pv-grading-grading": "What is the security grading or classification?",
    "pv-grading-suffix": "Enter a suffix (optional)",
    "pv-grading-issuing-authority": "Name and address of the issuing authority",
    "pv-grading-details-reference": "Reference",
    "pv-grading-details-date-of-issue": "Date of issue",
    "is-replica": "Is the product a replica firearm?",
    "is-replica-description": "Describe the firearm the product is a replica of",
    "firearms-act-1968-section": "Which section of the Firearms Act 1968 is the product covered by?",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation": "Explain",
    "has-product-document": "Do you have a document that shows what your product is and what it’s designed to do?",
    "is-document-sensitive": "Is the document rated above Official-sensitive?",
    "product-document": "Upload a document that shows what your product is designed to do",
    "product-document-description": "Description (optional)",
    "is-covered-by-firearm-act-section-five": "Is the product covered by section 5 of the Firearms Act 1968?",
    "section-5-certificate-document": "Upload your section 5 letter of authority",
    "section-5-certificate-reference-number": "Certificate reference number",
    "section-5-certificate-date-of-expiry": "Certificate date of expiry",
}


def add_labels(summary, labels):
    labelled_summary = ()
    for key, *rest in summary:
        labelled_summary += ((key, *rest, labels.get(key, key)),)

    return labelled_summary
