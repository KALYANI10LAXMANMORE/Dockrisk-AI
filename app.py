import re
from io import BytesIO
from datetime import datetime

import streamlit as st
import pandas as pd

# Optional libraries
try:
    import pymupdf as fitz
except ImportError:
    fitz = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="DocRisk AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    :root { --navy:#14213d; --blue:#2563eb; --pale:#f4f7fc; --line:#e2e8f0; }
    .stApp { background: linear-gradient(180deg, #f4f7fc 0%, #fbfcff 42%, #f7f9fd 100%); color:#172033; }
    .block-container { max-width: 1450px; padding-top: 1.5rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #101c36 0%, #172b50 100%); border-right:1px solid #20365e; }
    [data-testid="stSidebar"] * { color:#eef4ff; }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#b8c7e0 !important; }
    [data-testid="stSidebar"] hr { border-color:#34486b; }
    .hero { background: radial-gradient(circle at 88% 18%, rgba(96,165,250,.35), transparent 30%), linear-gradient(125deg,#101c36 0%,#1d3d76 55%,#2563eb 100%); padding:34px 38px; border-radius:24px; color:white; margin-bottom:28px; box-shadow:0 16px 40px rgba(30,64,175,.18); border:1px solid rgba(255,255,255,.12); }
    .hero-title { font-size:clamp(30px,3.2vw,42px); line-height:1.15; font-weight:850; letter-spacing:-1px; margin-bottom:10px; color:#fff; }
    .hero-subtitle { font-size:clamp(16px,1.7vw,20px); font-weight:650; margin-bottom:12px; color:#e0ecff; }
    .hero div:last-child { max-width:850px; line-height:1.7; color:#eaf1ff; }
    .section-title { color:#14213d; font-size:24px; font-weight:800; letter-spacing:-.35px; margin-top:24px; margin-bottom:14px; }
    .metric-card { background:linear-gradient(145deg,#fff 0%,#f6f9ff 100%); border:1px solid #e0e8f5; border-radius:18px; padding:20px 21px; min-height:125px; box-shadow:0 7px 22px rgba(15,23,42,.045); transition:transform .18s ease, box-shadow .18s ease; }
    .metric-label { color:#65748b; font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:.65px; }
    .metric-value { color:#1d4ed8; font-size:clamp(22px,2.1vw,30px); line-height:1.25; font-weight:850; margin-top:12px; overflow-wrap:anywhere; }
    .risk-high { background:#fff0f0; color:#a51d2d; border:1px solid #fecaca; padding:14px 17px; border-radius:14px; font-weight:750; }
    .risk-medium { background:#fff8e6; color:#945b00; border:1px solid #fde68a; padding:14px 17px; border-radius:14px; font-weight:750; }
    .risk-low { background:#edfff5; color:#137447; border:1px solid #bbf7d0; padding:14px 17px; border-radius:14px; font-weight:750; }
    .small-note { color:#64748b; font-size:13px; }
    div[data-testid="stFileUploader"] { background:#fff; border:1.5px dashed #9bb6e8; border-radius:16px; padding:14px; }
    div[data-testid="stFileUploader"] section { background:transparent; }
    .stButton > button, .stDownloadButton > button { min-height:44px; border-radius:12px; font-weight:750; border:1px solid #d5e1f3; transition:all .15s ease; }
    .stButton > button[kind="primary"] { background:linear-gradient(100deg,#1d4ed8,#3b82f6); border:0; box-shadow:0 6px 15px rgba(37,99,235,.2); }
    .stButton > button[kind="primary"] p { color:white; }
    div[data-testid="stAlert"] { border-radius:13px; }
    div[data-testid="stTabs"] button { font-weight:700; }
    div[data-testid="stDataFrame"], div[data-testid="stTable"] { border:1px solid #e3eaf5; border-radius:13px; overflow:hidden; }
    textarea, input, [data-baseweb="select"] > div { border-radius:10px !important; }
    hr { border-color:#e1e8f2; }
    @media (max-width: 768px) { .block-container { padding:1rem .8rem 2rem; } .hero { padding:24px 22px; border-radius:18px; } .section-title { font-size:21px; } .metric-card { padding:15px; min-height:105px; } }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛡️ DocRisk AI")
    st.markdown("### Intelligent Document Risk Analysis")
    st.divider()

    st.markdown("### 🔍 Analysis Modules")
    st.markdown("📄 Single Document Upload")
    st.markdown("🔤 OCR & Text Extraction")
    st.markdown("🧠 Information Extraction")
    st.markdown("📋 Compliance Analysis")
    st.markdown("🔎 Information Validation")
    st.markdown("⚠️ Risk Detection")
    st.markdown("📊 Risk Scoring")
    st.markdown("💡 Risk Explanation")
    st.markdown("📑 Report Generation")

    st.divider()
    st.caption("Academic Project | DocRisk AI")


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🛡️ DocRisk AI</div>
        <div class="hero-subtitle">
            AI-Powered Intelligent Document Risk Analysis
        </div>
        <div>
            Analyze a document, detect missing information, identify suspicious
            patterns and validate important document details.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DOCUMENT REQUIREMENTS
# ---------------------------------------------------------
REQUIREMENTS = {
     "General Document": {
        "documents": [],
        "fields": ["Email", "Phone", "Date"],
    },
    "Scholarship Document": {
        "documents": [
            "Aadhaar Card",
            "Marksheet",
            "Income Certificate",
            "Bank Passbook",
        ],
        "fields": [
            "Student Name",
            "College Name",
            "Branch",
            "Year",
            "Annual Income",
        ],
    },
    "Admission Document": {
        "documents": [
            "Aadhaar Card",
            "Marksheet",
            "Transfer Certificate",
            "Migration Certificate",
        ],
        "fields": [
            "Student Name",
            "College Name",
            "Branch",
            "Year",
        ],
    },
    "Offer Letter": {
        "documents": [],
        "fields": [
            "Candidate Name",
            "Company Name",
            "Job Role",
            "Date",
            "Email",
            "Duration",
            "Salary / Stipend",
        ],
    },
}


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def clean_text(text):
    """Clean extracted text without destroying important values."""
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_pdf(uploaded_file):
    if fitz is None:
        return "", "PyMuPDF is not installed."

    try:
        pdf_bytes = uploaded_file.read()
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            pages = []
            for page in document:
                pages.append(page.get_text("text"))

            text = clean_text("\n".join(pages))

            # If the PDF is scanned and has no selectable text, try OCR.
            if len(text.strip()) < 30 and pytesseract is not None and Image is not None:
                ocr_pages = []

                for page in document:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    image = Image.open(BytesIO(pix.tobytes("png")))
                    ocr_pages.append(pytesseract.image_to_string(image))

                text = clean_text("\n".join(ocr_pages))

        return text, None

    except Exception as error:
        return "", f"PDF extraction failed: {error}"


def extract_text_from_image(uploaded_file):
    if Image is None:
        return "", "Pillow is not installed."

    if pytesseract is None:
        return "", "pytesseract is not installed."

    try:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
        return clean_text(text), None

    except Exception as error:
        return "", f"Image OCR failed: {error}"


def extract_document_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if file_name.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(uploaded_file)

    return "", "Unsupported file format."


def first_match(patterns, text, flags=re.IGNORECASE):
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            value = match.group(1).strip(" :.-\n\t")
            if value:
                return value
    return "Not Found"


def extract_information(text):
    """Extract common fields from a single document using regex patterns."""

    information = {}

    information["candidate_name"] = first_match(
        [
            r"(?:candidate\s*name|applicant\s*name|student\s*name|name)\s*[:\-]\s*([^\n]+)",
            r"(?:dear|mr\.?|mrs\.?|ms\.?)\s+([A-Za-z][A-Za-z .]{2,40})",
        ],
        text,
    )

    information["student_name"] = information["candidate_name"]

    information["company_name"] = first_match(
        [
            r"(?:company\s*name|company|organization|organisation)\s*[:\-]\s*([^\n]+)",
            r"(?:at|from)\s+([A-Z][A-Za-z0-9&., ]{2,50})",
        ],
        text,
    )

    information["job_role"] = first_match(
        [
            r"(?:job\s*role|role|position|designation|title)\s*[:\-]\s*([^\n]+)",
            r"(?:selected\s+for|appointed\s+as|hired\s+as)\s+([^\n]+)",
        ],
        text,
    )

    information["college_name"] = first_match(
        [
            r"(?:college\s*name|college|institute|institution|university)\s*[:\-]\s*([^\n]+)"
        ],
        text,
    )

    information["branch"] = first_match(
        [
            r"(?:branch|department|stream|course)\s*[:\-]\s*([^\n]+)",
        ],
        text,
    )

    information["year"] = first_match(
        [
            r"(?:year|academic\s*year|study\s*year)\s*[:\-]\s*([^\n]+)",
            r"\b(20[2-3][0-9]\s*[-/]\s*20[2-3][0-9])\b",
        ],
        text,
    )

    information["annual_income"] = first_match(
        [
            r"(?:annual\s*income|family\s*income|income)\s*[:\-]?\s*(?:rs\.?|₹)?\s*([\d,]+)",
        ],
        text,
    )

    information["email"] = first_match(
        [r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b"],
        text,
    )

    information["phone"] = first_match(
        [
            r"(?:phone|mobile|contact|telephone)\s*[:\-]?\s*(\+?\d[\d\s\-]{8,14}\d)",
            r"\b([6-9]\d{9})\b",
        ],
        text,
    )

    information["date"] = first_match(
        [
            r"(?:date|issued\s*on|joining\s*date|start\s*date)\s*[:\-]\s*([^\n]+)",
            r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
            r"\b(\d{1,2}\s+[A-Za-z]+\s+20\d{2})\b",
        ],
        text,
    )

    information["duration"] = first_match(
        [
            r"(?:duration|period|tenure)\s*[:\-]\s*([^\n]+)",
            r"\b(\d+\s*(?:months?|weeks?|days?))\b",
        ],
        text,
    )

    information["salary_or_stipend"] = first_match(
        [
            r"(?:salary|stipend|package|ctc|compensation|pay)\s*[:\-]?\s*((?:rs\.?|₹)?\s*[\d,]+(?:\s*(?:per\s*month|monthly|lpa|per\s*annum|pa))?)",
            r"\b((?:rs\.?|₹)\s*[\d,]+(?:\s*(?:per\s*month|monthly|lpa|per\s*annum|pa))?)\b",
        ],
        text,
    )

    information["website"] = first_match(
        [r"\b((?:https?://|www\.)[^\s]+)\b"],
        text,
    )

    return information


def value_found(value):
    if value is None:
        return False

    value = str(value).strip().lower()
    return value not in {
        "",
        "not found",
        "none",
        "null",
        "n/a",
        "na",
    }


def get_value(info, field):
    mapping = {
        "Candidate Name": ["candidate_name", "student_name"],
        "Student Name": ["student_name", "candidate_name"],
        "Company Name": ["company_name"],
        "Job Role": ["job_role"],
        "College Name": ["college_name"],
        "Branch": ["branch"],
        "Year": ["year"],
        "Annual Income": ["annual_income"],
        "Date": ["date"],
        "Email": ["email"],
        "Phone": ["phone"],
        "Duration": ["duration"],
        "Salary / Stipend": ["salary_or_stipend"],
    }

    for key in mapping.get(field, []):
        value = info.get(key)
        if value_found(value):
            return value

    return "Not Found"


def detect_missing_fields(info, required_fields):
    missing = []

    for field in required_fields:
        if not value_found(get_value(info, field)):
            missing.append(field)

    return missing


def detect_suspicious_patterns(text):
    """Rule-based suspicious pattern detection for academic demonstration."""

    lower_text = text.lower()
    risks = []

    patterns = [
        (
            "Registration fee / payment demand",
            [
                "registration fee",
                "pay rs",
                "pay ₹",
                "payment required",
                "processing fee",
                "security deposit",
                "joining fee",
            ],
            "The document asks the user to pay money before confirmation or joining.",
        ),
        (
            "OTP or sensitive banking information request",
            [
                "otp",
                "one time password",
                "bank account",
                "account number",
                "cvv",
                "pin",
                "aadhaar card",
                "send your documents",
            ],
            "The document requests sensitive personal, banking or authentication information.",
        ),
        (
            "Urgency or pressure language",
            [
                "immediately",
                "within 30 minutes",
                "limited time",
                "act now",
                "urgent",
                "offer valid only",
            ],
            "Urgent language may pressure the user into making a quick decision.",
        ),
        (
            "Unusually attractive salary claim",
            [
                "work-from-home",
                "work from home",
                "earn huge",
                "guaranteed income",
                "selected for a job",
            ],
            "The document contains claims that should be verified independently.",
        ),
        (
            "Missing official verification details",
            [
                "contact us",
                "hr",
                "human resource",
            ],
            "The document may require verification of the sender, official email and company identity.",
        ),
    ]

    for title, keywords, explanation in patterns:
        matched = [word for word in keywords if word in lower_text]

        if matched:
            risks.append(
                {
                    "Risk": title,
                    "Matched Keywords": ", ".join(matched),
                    "Explanation": explanation,
                    "Severity": "High" if title in {
                        "Registration fee / payment demand",
                        "OTP or sensitive banking information request",
                    } else "Medium",
                }
            )

    # Generic warning for missing email or website
    if "email" not in lower_text and "@" not in text:
        risks.append(
            {
                "Risk": "No visible official email address",
                "Matched Keywords": "email not detected",
                "Explanation": "Verify the sender through an official company website or known contact.",
                "Severity": "Medium",
            }
        )

    return risks


def calculate_score(risks, missing_fields):
    score = 0

    for risk in risks:
        if risk["Severity"] == "High":
            score += 25
        else:
            score += 12

    score += len(missing_fields) * 5
    return min(score, 100)


def risk_level(score):
    if score >= 70:
        return "High Risk", "risk-high"
    if score >= 35:
        return "Medium Risk", "risk-medium"
    return "Low Risk", "risk-low"


def create_report(file_name, document_type, score, level, risks, missing_fields, info):
    lines = [
        "DocRisk AI - Document Risk Analysis Report",
        "=" * 50,
        f"File Name: {file_name}",
        f"Document Type: {document_type}",
        f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        "",
        f"Risk Score: {score}/100",
        f"Risk Level: {level}",
        "",
        "Extracted Information",
        "-" * 30,
    ]

    for key, value in info.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")

    lines.extend(["", "Missing Fields", "-" * 30])
    lines.extend(missing_fields if missing_fields else ["No missing required fields detected."])

    lines.extend(["", "Detected Risks", "-" * 30])

    if risks:
        for risk in risks:
            lines.append(f"- {risk['Risk']} ({risk['Severity']})")
            lines.append(f"  {risk['Explanation']}")
    else:
        lines.append("No suspicious pattern detected by the rule-based checks.")

    lines.extend(
        [
            "",
            "Disclaimer",
            "-" * 30,
            "This is an academic rule-based screening tool. It does not prove that a document is genuine or fraudulent.",
        ]
    )

    return "\n".join(lines)


# ---------------------------------------------------------
# USER INTERFACE
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📄 Select Document Type</div>',
    unsafe_allow_html=True,
)

document_type = st.selectbox(
    "Choose the type of document you want to analyze",
    list(REQUIREMENTS.keys()),
)

requirements = REQUIREMENTS[document_type]

st.markdown(
    '<div class="section-title">📤 Upload Document</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload one PDF or image document",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Supported formats: PDF, PNG, JPG and JPEG.",
)

if uploaded_file is not None:
    file_size_kb = uploaded_file.size / 1024
    file_size_mb = file_size_kb / 1024

    st.info(
        f"Selected file: **{uploaded_file.name}** | "
        f"Size: **{file_size_kb:.2f} KB ({file_size_mb:.2f} MB)**"
    )

    if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
        with st.spinner("Analyzing document. Please wait..."):
            extracted_text, extraction_error = extract_document_text(uploaded_file)

        if extraction_error:
            st.error(extraction_error)
            st.stop()

        if not extracted_text.strip():
            st.error(
                "No text could be extracted. For scanned PDFs, install Tesseract OCR "
                "or upload a clearer document image."
            )
            st.stop()

        extracted_info = extract_information(extracted_text)
        missing_fields = detect_missing_fields(
            extracted_info,
            requirements["fields"],
        )
        risks = detect_suspicious_patterns(extracted_text)
        score = calculate_score(risks, missing_fields)
        level, level_class = risk_level(score)

        st.session_state["analysis_result"] = {
            "file_name": uploaded_file.name,
            "document_type": document_type,
            "text": extracted_text,
            "info": extracted_info,
            "missing_fields": missing_fields,
            "risks": risks,
            "score": score,
            "level": level,
            "level_class": level_class,
        }


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------
result = st.session_state.get("analysis_result")

if result:
    st.divider()

    st.markdown(
        '<div class="section-title">📊 Analysis Summary</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Risk Score</div>
                <div class="metric-value">{result["score"]}/100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value">{result["level"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Missing Fields</div>
                <div class="metric-value">{len(result["missing_fields"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Detected Risks</div>
                <div class="metric-value">{len(result["risks"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="{result["level_class"]}">⚠️ {result["level"]}: '
        f'Please verify the document through official sources.</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📝 Extracted Text",
            "🧠 Information",
            "📋 Compliance",
            "🔎 Validation",
            "⚠️ Risk Detection",
            "📑 Report",
        ]
    )

    with tab1:
        st.subheader("Extracted Document Text")
        st.text_area(
            "Text extracted from uploaded document",
            result["text"],
            height=350,
        )

    with tab2:
        st.subheader("Extracted Information")

        display_rows = []
        for key, value in result["info"].items():
            display_rows.append(
                {
                    "Field": key.replace("_", " ").title(),
                    "Value": value,
                }
            )

        st.dataframe(
            pd.DataFrame(display_rows),
            use_container_width=True,
            hide_index=True,
        )

    with tab3:
        st.subheader("Compliance Analysis")

        if requirements["documents"]:
            st.write("Required supporting documents:")
            for item in requirements["documents"]:
                st.write(f"• {item}")
            st.caption(
                "Supporting-document verification requires separate uploads. "
                "This version analyzes only the uploaded document."
            )
        else:
            st.success("No separate supporting documents are configured for this type.")

        if requirements["fields"]:
            st.write("Required information fields:")
            for field in requirements["fields"]:
                status = "✅ Found" if field not in result["missing_fields"] else "❌ Missing"
                st.write(f"{status} — {field}")

    with tab4:
        st.subheader("Information Validation")

        validation_rows = []

        for field in requirements["fields"]:
            value = get_value(result["info"], field)
            validation_rows.append(
                {
                    "Field": field,
                    "Extracted Value": value,
                    "Status": "Valid/Found" if value_found(value) else "Missing",
                }
            )

        if validation_rows:
            st.dataframe(
                pd.DataFrame(validation_rows),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No validation fields configured for this document type.")

    with tab5:
        st.subheader("Suspicious Pattern Detection")

        if result["risks"]:
            risk_rows = [
                {
                    "Risk": risk["Risk"],
                    "Severity": risk["Severity"],
                    "Matched Keywords": risk["Matched Keywords"],
                    "Explanation": risk["Explanation"],
                }
                for risk in result["risks"]
            ]

            st.dataframe(
                pd.DataFrame(risk_rows),
                use_container_width=True,
                hide_index=True,
            )

            st.warning(
                "These are rule-based warning signs. They do not prove that the document is fake."
            )
        else:
            st.success("No suspicious pattern was detected by the current rules.")

    with tab6:
        st.subheader("Download Analysis Report")

        report_text = create_report(
            result["file_name"],
            result["document_type"],
            result["score"],
            result["level"],
            result["risks"],
            result["missing_fields"],
            result["info"],
        )

        st.download_button(
            label="⬇️ Download TXT Report",
            data=report_text,
            file_name="docrisk_ai_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.text_area(
            "Report Preview",
            report_text,
            height=350,
        )

    st.caption(
        "DocRisk AI is an academic screening project. Always verify important documents "
        "with the official organization, institution or authority."
    )
