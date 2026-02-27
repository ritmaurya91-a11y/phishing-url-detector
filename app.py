import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extractor import extract_features
from urllib.parse import urlparse

st.set_page_config(page_title="AI Phishing Detector", layout="centered")

st.title("🔐 AI Powered Phishing URL Detector")

# ---------------------------
# Train Model
# ---------------------------
@st.cache_resource
def train_model():
    data = pd.read_csv("phishing.csv")

    if "url" in data.columns:
        features = []
        for u in data["url"]:
            features.append(extract_features(str(u)))

        X = pd.DataFrame(features)
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
# AI Description Generator
# ---------------------------
def generate_ai_description(url, prediction, confidence):
    parsed = urlparse(url)
    description = ""

    if prediction == 1:
        description += "This website shows multiple suspicious characteristics commonly associated with phishing attacks. "

        if len(url) > 100:
            description += "The URL length is unusually long, which attackers often use to hide malicious intent. "

        if url.count("-") > 2:
            description += "Excessive hyphen usage suggests possible domain impersonation. "

        if parsed.scheme != "https":
            description += "The absence of HTTPS encryption reduces security and increases risk. "

        if any(char.isdigit() for char in parsed.netloc):
            description += "The presence of numbers in the domain may indicate brand mimicry attempts. "

        description += f"Based on feature analysis, the model classified this site as high-risk with {confidence:.2f}% confidence."

    else:
        description += "The website structure appears consistent with legitimate domains. "

        if parsed.scheme == "https":
            description += "It uses secure HTTPS encryption. "

        if len(url) < 100:
            description += "The URL length is within a normal range. "

        if url.count("-") <= 2:
            description += "There are no excessive special characters in the domain. "

        description += f"The model considers this site low-risk with {confidence:.2f}% confidence."

    return description


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

        st.progress(int(confidence))

        # Clean AI Description
        description = generate_ai_description(url, prediction, confidence)
        st.write(description)

    else:
        st.warning("Please enter a URL")
