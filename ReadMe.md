# Generate the contents for README.md and requirements.txt

readme_text = """
# Benford's Law Audit Tool

📊 **Benford's Law Analysis Tool for Auditors and Data Analysts**

This Streamlit app allows internal auditors, compliance analysts, and fraud examiners to upload a dataset, select a numeric column, and analyze whether the data conforms to **Benford's Law**.

Benford's Law is a powerful method to detect anomalies or red flags in financial data — often used in fraud detection, forensic accounting, and audit analytics.

---

## 🔍 Features

- Upload **CSV or Excel** files
- Select a numeric column for analysis
- Compare actual first-digit distribution to Benford's expected distribution
- Visual **bar chart** of actual vs expected
- **Chi-squared test** to evaluate conformity
- Risk flag:
  - ✅ No issues
  - ⚠️ Possible concerns
  - ❌ Likely deviation from natural distribution

---

## 📦 How to Use

### ▶️ Run locally:
```bash
pip install -r requirements.txt
streamlit run benfords_law_app.py
