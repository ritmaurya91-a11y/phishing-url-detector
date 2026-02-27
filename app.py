import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extractor import extract_features
from urllib.parse import urlparse

st.set_page_config(page_title="AI Phishing Detector", layout="centered")

st.title("🔐 AI Powered Phishing URL Detector")
st.markdown("Detect whether a website URL is **Phishing or Legitimate**")

# ---------------------------
# Train Model
# ---------------------------
@st.cache_resource
def train_model():
    data = pd.read_csv("phishing.csv")

    if "url" in data.columns:
        feature_list = []
        for url in data["url"]:
            feature_list.append(extract_features(str(url)))

        X = pd.DataFrame(feature_list)
        y = data.iloc[:, -1]
    else:
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)
    y = pd.to_numeric(y, errors="coerce").fillna(0)

    X = X.astype(float)
    y = y.astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model

model = train_model()

# ---------------------------
# AI Explanation Generator
# ---------------------------
def generate_ai_explanation(url, prediction, confidence):
    parsed = urlparse(url)

    reasons = []

    if len(url) > 100:
        reasons.append("The URL is unusually long, which is common in phishing attacks.")

    if url.count("-") > 2:
        reasons.append("Multiple hyphens detected in the domain, often used in fake websites.")

    if "@" in url:
        reasons.append("The '@' symbol can redirect users and is suspicious.")

    if parsed.scheme != "https":
        reasons.append("The website is not using HTTPS, which reduces security.")

    if any(char.isdigit() for char in parsed.netloc):
        reasons.append("Numbers detected in the domain, sometimes used to mimic real brands.")

    if not reasons:
        reasons.append("The URL structure appears normal with no major suspicious patterns.")

    result_type = "Phishing" if prediction == 1 else "Legitimate"

    explanation = f"""
### 🤖 AI Security Analysis

**Prediction:** {result_type}  
**Confidence Level:** {confidence:.2f}%

**Why?**

"""
    for r in reasons:
        explanation += f"- {r}\n"

    explanation += "\nThis analysis is generated using AI-based pattern detection and URL feature evaluation."

    return explanation


# ---------------------------
# User Input
# ---------------------------
url = st.text_input("Enter Website URL")

if st.button("Analyze"):
    if url:
        features = extract_features(url)

        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]
        confidence = np.max(probabilities) * 100

        if prediction == 1:
            st.error("⚠️ Phishing Website Detected")
        else:
            st.success("✅ Legitimate Website")

        st.info(f"🔎 Confidence: {confidence:.2f}%")
        st.progress(int(confidence))

        # AI Explanation
        explanation = generate_ai_explanation(url, prediction, confidence)
        st.markdown(explanation)

    else:
        st.warning("Please enter a URL")
