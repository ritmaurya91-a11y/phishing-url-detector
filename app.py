import streamlit as st
from joblib import load
from feature_extractor import extract_features

model = load("model.pkl")

st.set_page_config(page_title="Phishing URL Detector")

st.title("Phishing URL Detector (Mini SOC Tool)")

url = st.text_input("Enter Website URL")

if st.button("Analyze"):
    if url:
        features = extract_features(url)

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0].max()

        if prediction == 1:
            st.error("⚠️ Phishing Website Detected")
        else:
            st.success("✅ Legitimate Website")

        st.write(f"Confidence: {probability*100:.2f}%")
    else:
        st.warning("Please enter a URL")
