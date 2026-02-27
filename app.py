import streamlit as st
import re
from urllib.parse import urlparse
from difflib import SequenceMatcher

st.set_page_config(page_title="AI Phishing Detector", page_icon="🔐")

st.title("🔐 AI Powered Phishing URL Detector")
st.write("Enter a website URL to check whether it is Legitimate or Phishing.")

# ==============================
# Smart AI Phishing Detection
# ==============================
def detect_phishing(url):
    score = 0
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Remove www
    if domain.startswith("www."):
        domain = domain[4:]

    # Extract main domain name
    domain_name = domain.split(".")[0]

    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "account", "bank", "paypal", "confirm"
    ]

    popular_brands = [
        "google", "facebook", "amazon",
        "paypal", "microsoft", "bankofamerica"
    ]

    # 1️⃣ HTTPS Check
    if parsed.scheme != "https":
        score += 20

    # 2️⃣ IP Address in URL
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 40

    # 3️⃣ Suspicious Keywords
    for word in suspicious_keywords:
        if word in url.lower():
            score += 15

    # 4️⃣ Very Long URL
    if len(url) > 100:
        score += 10

    # 5️⃣ Too Many Hyphens
    if url.count("-") > 2:
        score += 10

    # 6️⃣ 🔥 Strong Brand Typosquatting Detection
    for brand in popular_brands:
        similarity = SequenceMatcher(None, domain_name, brand).ratio()

        # Very similar but not exact match
        if similarity > 0.80 and domain_name != brand:
            score += 60

    # Final Decision
    if score >= 50:
        return 1, min(score, 100)
    else:
        return 0, 100 - score


# ==============================
# AI Explanation Generator
# ==============================
def generate_ai_description(url, prediction, confidence):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    explanation = ""

    if parsed.scheme != "https":
        explanation += "⚠️ The website does not use HTTPS encryption. "

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        explanation += "⚠️ The URL contains an IP address instead of a domain name. "

    if len(url) > 100:
        explanation += "⚠️ The URL is unusually long. "

    if prediction == 1:
        explanation += f"\n\n🚨 The AI system classified this website as **Phishing** with {confidence:.2f}% risk score."
    else:
        explanation += f"\n\n✅ The AI system classified this website as **Legitimate** with {confidence:.2f}% safety score."

    return explanation


# ==============================
# User Input Section
# ==============================
url = st.text_input("Enter Website URL")

if st.button("Check URL"):

    if url:

        prediction, confidence = detect_phishing(url)

        if prediction == 1:
            st.error("🚨 Phishing Website Detected")
        else:
            st.success("✅ Legitimate Website")

        st.info(f"Confidence Score: {confidence:.2f}%")

        if confidence < 70:
            st.warning("⚠️ Low confidence result. Please verify manually.")

        st.subheader("🧠 AI Analysis Report")
        explanation = generate_ai_description(url, prediction, confidence)
        st.write(explanation)

    else:
        st.warning("Please enter a URL.")
