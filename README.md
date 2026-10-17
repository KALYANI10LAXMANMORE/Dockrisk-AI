# Dockrisk-AI
# DocRisk AI – Intelligent Document Risk Detection System

## 📌 Project Overview

**DocRisk AI** is a Python-based web application developed using Streamlit to analyze uploaded documents and identify potentially suspicious language or risk-related content.

The system extracts text from documents, checks for suspicious keywords and phrases, and generates a risk score to help users identify content that may require further verification.

DocRisk AI is designed to assist users in reviewing documents more efficiently. It provides alerts based on detected patterns and does not independently determine whether a document is fraudulent.

## 🎯 Objectives

- To automate the initial analysis of uploaded documents.
- To extract text from PDF documents.
- To identify suspicious words, phrases, and potentially risky statements.
- To calculate a risk score based on predefined rules.
- To display analysis results through a user-friendly web interface.
- To help users identify documents that may need manual verification.

## ✨ Key Features

- **Document Upload:** Upload supported documents for analysis.
- **Text Extraction:** Extract text from PDF files using PyMuPDF.
- **OCR Support:** Enable text extraction from scanned documents when OCR is configured.
- **Suspicious Language Detection:** Identify predefined suspicious keywords and phrases using rule-based detection.
- **Risk Score Generation:** Calculate a risk score based on detected patterns.
- **Risk Alerts:** Highlight potentially suspicious content for further review.
- **Interactive Dashboard:** Display document analysis results using Streamlit.
- **Document Review Assistance:** Help users decide which documents may require additional verification.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend and web application interface |
| PyMuPDF | Extracting text from PDF documents |
| OCR | Extracting text from scanned documents, when configured |
| Regular Expressions (Regex) | Matching text patterns, when implemented |
| Rule-Based Detection | Identifying suspicious keywords and phrases |

## ⚙️ How It Works

1. The user uploads a supported document.
2. The application extracts text from the document.
3. If the document is scanned, OCR can be used to extract readable text.
4. The extracted text is analyzed using predefined rules and suspicious keywords.
5. The system calculates a risk score based on the implemented detection logic.
6. The application displays the analysis results and relevant alerts.
7. The user reviews the results and decides whether further verification is necessary.

## 🏗️ System Architecture

**User → Streamlit Interface → Document Processing → Text Extraction / OCR → Rule-Based Risk Analysis → Risk Score and Alerts**

## 💻 Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- pip package manager
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/KALYANI10LAXMANMORE/AIDOC.git
```

### Step 2: Navigate to the Project Folder

```bash
cd AIDOC
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```
