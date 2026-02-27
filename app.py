import streamlit as st
import re
from urllib.parse import urlparse
from difflib import SequenceMatcher

st.set_page_config(page_title="AI Phishing Detector", page_icon="🔐")

st.title("🔐 AI Powered Phishing URL Detector")
st.write("Enter a website URL to check whether it is Legitimate or Phishing.")

# ======================================
# SMART PHISHING DETECTION ENGINE
# ======================================
def detect_phishing(url):
    score = 0
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    domain_name = domain.split(".")[0]

    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "account", "bank", "paypal", "confirm"
    ]

    popular_brands = [
        "google", "facebook", "amazon",
        "paypal", "microsoft", "bankofamerica"
    ]

    if parsed.scheme != "https":
        score += 20

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 40

    for word in suspicious_keywords:
        if word in url.lower():
            score += 15

    if len(url) > 100:
        score += 10

    if url.count("-") > 2:
        score += 10

    # Strong brand typo detection
    for brand in popular_brands:
        similarity = SequenceMatcher(None, domain_name, brand).ratio()
        if similarity > 0.80 and domain_name != brand:
            return 1, 95.0

    if score >= 50:
        return 1, float(min(score, 100))
    else:
        return 0, float(100 - score)


# ======================================
# DETAILED AI ANALYSIS REPORT
# ======================================
def generate_ai_description(url, prediction, confidence):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    explanation = "🔎 Detailed Security Analysis Report:\n\n"

    explanation += f"• The analyzed URL is: {url}\n"
    explanation += f"• The extracted domain is: {domain}\n"

    if parsed.scheme == "https":
        explanation += "• The website uses HTTPS protocol for encrypted communication.\n"
    else:
        explanation += "• The website does NOT use HTTPS protocol, increasing security risk.\n"

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        explanation += "• The URL contains an IP address instead of a proper domain name.\n"
    else:
        explanation += "• No direct IP address detected in the URL structure.\n"

    explanation += f"• The total URL length is {len(url)} characters.\n"

    hyphen_count = url.count("-")
    explanation += f"• The URL contains {hyphen_count} hyphen(s).\n"

    if prediction == 1:
        explanation += "\n🚨 Final Verdict: The website is classified as PHISHING.\n"
        explanation += f"• Risk Confidence Level: {confidence:.2f}%\n"
        explanation += "• This URL exhibits characteristics commonly associated with phishing campaigns.\n"
        explanation += "• Users are strongly advised NOT to enter sensitive credentials.\n"
        explanation += "• Avoid sharing financial or personal information on this website.\n"
    else:
        explanation += "\n✅ Final Verdict: The website is classified as LEGITIMATE.\n"
        explanation += f"• Safety Confidence Level: {confidence:.2f}%\n"
        explanation += "• No major phishing indicators were detected during analysis.\n"
        explanation += "• Always verify domain authenticity before sharing data.\n"

    explanation += "\n🛡 This assessment is generated using an AI-based phishing detection engine."

    return explanation


# ======================================
# USER INPUT
# ======================================
url = st.text_input("Enter Website URL")

if st.button("Check URL"):

    if url:

        prediction, confidence = detect_phishing(url)

        if prediction == 1:
            st.error("🚨 Phishing Website Detected")

            # 🔴 HIGH RISK DISPLAY
            if confidence >= 90:
                st.markdown("## 🔴 HIGH RISK WEBSITE")
            elif confidence >= 70:
                st.markdown("## 🟠 MEDIUM RISK WEBSITE")
            else:
                st.markdown("## 🟡 LOW RISK WEBSITE")

        else:
            st.success("✅ Legitimate Website")
            st.markdown("## 🟢 LOW RISK WEBSITE")

        st.info(f"Confidence Score: {confidence:.2f}%")

        st.subheader("🧠 AI Analysis Report")
        explanation = generate_ai_description(url, prediction, confidence)
        st.text(explanation)

    else:
        st.warning("Please enter a URL.")
