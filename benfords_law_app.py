import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import chisquare

st.set_page_config(page_title="Benford's Law Audit Tool", layout="centered")
st.title("📊 Benford's Law Analysis Tool")

# Upload file
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Preview of Uploaded Data")
    st.write(df.head())

    # Select numeric column
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        st.error("No numeric columns found.")
    else:
        selected_col = st.selectbox("Select the column to test with Benford's Law", numeric_cols)

        # Extract first digits
        values = df[selected_col].dropna()
        first_digits = [int(str(int(abs(x)))[0]) for x in values if x != 0]

        # Calculate actual distribution
        actual_counts = Counter(first_digits)
        total = sum(actual_counts.values())
        actual_dist = {d: actual_counts.get(d, 0) / total for d in range(1, 10)}

        # Benford's expected distribution
        benford_dist = {d: np.log10(1 + 1/d) for d in range(1, 10)}

        # Plot
        digits = list(range(1, 10))
        actual = [actual_dist.get(d, 0) for d in digits]
        expected = [benford_dist[d] for d in digits]

        st.subheader("Digit Distribution Comparison")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(digits, actual, label="Actual", alpha=0.7)
        ax.plot(digits, expected, 'r--', label="Benford Expected", linewidth=2)
        ax.set_xlabel("First Digit")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Benford's Law on '{selected_col}'")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # Chi-squared test
        observed = [actual_counts.get(d, 0) for d in digits]
        expected_counts = [benford_dist[d] * total for d in digits]
        chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected_counts)

        st.subheader("Chi-Squared Test Result")
        st.markdown(f"""
        **Chi-squared statistic**: `{chi2_stat:.2f}`  
        **p-value**: `{p_value:.4f}`  
        """)

        if p_value < 0.01:
            st.error("❌ Strong evidence of deviation from Benford’s Law (possible red flag).")
        elif p_value < 0.05:
            st.warning("⚠️ Moderate deviation from Benford’s Law (review recommended).")
        else:
            st.success("✅ No significant deviation from Benford’s Law (no red flags).")
