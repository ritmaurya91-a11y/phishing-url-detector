import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extractor import extract_features

st.set_page_config(page_title="Phishing URL Detector", layout="centered")

st.title("🔐 AI Powered Phishing URL Detector")
st.markdown("Detect whether a website URL is **Phishing or Legitimate**")

# ---------------------------
# Train Model
# ---------------------------
@st.cache_resource
def train_model():
    data = pd.read_csv("phishing.csv")

    # If dataset contains raw URLs
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

        st.info(f"🔎 Website Confidence: {confidence:.2f}%")

        # Optional Confidence Bar
        st.progress(int(confidence))

    else:
        st.warning("Please enter a URL")
