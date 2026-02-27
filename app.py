import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from feature_extractor import extract_features

st.set_page_config(page_title="Phishing URL Detector", layout="centered")

st.title("🔐 AI Powered Phishing URL Detector")
st.markdown("Detect whether a website URL is **Phishing or Legitimate**")

# ---------------------------
# Train Model Automatically
# ---------------------------
@st.cache_resource
def train_model():
    data = pd.read_csv("phishing.csv")

    X = data.drop("label", axis=1)
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    return model, accuracy

model, accuracy = train_model()

st.success(f"Model Accuracy: {accuracy*100:.2f}%")

# ---------------------------
# User Input
# ---------------------------
url = st.text_input("Enter Website URL")

if st.button("Analyze"):
    if url:
        features = extract_features(url)
        prediction = model.predict([features])[0]

        if prediction == 1:
            st.error("⚠️ Phishing Website Detected")
        else:
            st.success("✅ Legitimate Website")
    else:
        st.warning("Please enter a URL")
