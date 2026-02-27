import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from feature_extractor import extract_features

st.set_page_config(page_title="Phishing URL Detector")

st.title("🔐 AI Powered Phishing URL Detector")
st.markdown("Detect whether a website URL is Phishing or Legitimate")

# ---------------------------
# Train Model Using Extracted Features
# ---------------------------
@st.cache_resource
def train_model():
    data = pd.read_csv("phishing.csv")

    # If dataset contains URL column
    if "url" in data.columns:
        feature_list = []

        for url in data["url"]:
            feature_list.append(extract_features(url))

        X = pd.DataFrame(feature_list)
        y = data.iloc[:, -1]   # last column as label
    else:
        # If dataset already numeric
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

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
