import streamlit as st
import pickle
import re
from urllib.parse import urlparse

# =========================
# Load Trained Model
# =========================
model = pickle.load(open("phishing_model.pkl", "rb"))

st.set_page_config(page_title="AI Phishing Detector", page_icon="🔐")

st.title("🔐 AI Powered Phishing URL Detector")
st.write("Enter a website URL to check whether it is Legitimate or Phishing.")

# =========================
# Feature Extraction
# =========================
def extract_features(url):
    parsed = urlparse(url)
    
    return [
        len(url),                         # URL Length
        url.count("."),                   # Dot count
        1 if parsed.scheme == "https" else 0,  # HTTPS
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,  # IP Address
        url.count("-")                    # Hyphen count
    ]

# =========================
# AI Description Generator
# =========================
def generate_ai_description(url, prediction, confidence):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "account", "bank", "paypal", "confirm"
    ]

    popular_brands = [
        "google.com", "facebook.com", "amazon.com",
        "paypal.com", "bankofamerica.com", "microsoft.com"
    ]

    description = ""

    # Brand impersonation detection
    for brand in popular_brands:
        brand_name = brand.split(".")[0]
        if brand_name in domain and brand not in domain:
            description += f"⚠️ The domain appears to imitate the popular brand '{brand_name}', which is a common phishing technique. "

    # Suspicious keyword detection
    for word in suspicious_keywords:
        if word in url.lower():
            description += f"⚠️ The URL contains the keyword '{word}', often used in phishing attacks. "

    # Long URL warning
    if len(url) > 120:
        description += "⚠️ The URL is unusually long, which can indicate obfuscation techniques. "

    # HTTPS check
    if parsed.scheme != "https":
        description += "⚠️ The website does not use HTTPS encryption. "

    # Final result explanation
    if prediction == 1:
        description += f"\n\n🔎 The AI system classified this website as **Phishing** with {confidence:.2f}% confidence."
    else:
        description += f"\n\n🔎 The AI system classified this website as **Legitimate** with {confidence:.2f}% confidence. However, always verify domain spelling carefully."

    return description

# =========================
# User Input
# =========================
url = st.text_input("Enter Website URL")

if st.button("Check URL"):

    if url:

        features = extract_features(url)
        prediction = model.predict([features])[0]
        confidence = max(model.predict_proba([features])[0]) * 100

        if prediction == 1:
            st.error("🚨 Phishing Website Detected")
        else:
            st.success("✅ Legitimate Website")

        # Confidence display
        st.info(f"Confidence Level: {confidence:.2f}%")

        # Low confidence warning
        if confidence < 70:
            st.warning("⚠️ Low confidence prediction. Manual verification recommended.")

        # AI Explanation
        st.subheader("🧠 AI Analysis Report")
        explanation = generate_ai_description(url, prediction, confidence)
        st.write(explanation)

    else:
        st.warning("Please enter a URL.")
