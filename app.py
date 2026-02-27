import streamlit as st
from joblib import load
from feature_extractor import extract_features

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Phishing URL Detector", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    font-family: 'Segoe UI', sans-serif;
    color: white;
}

/* Glass Container */
.block-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.3);
}

/* Animated Glow Title */
@keyframes glow {
    0% { text-shadow: 0 0 10px #00f2ff; }
    50% { text-shadow: 0 0 25px #00f2ff, 0 0 40px #00f2ff; }
    100% { text-shadow: 0 0 10px #00f2ff; }
}

.glow-text {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    animation: glow 2s infinite alternate;
    color: #ffffff;
}

/* Input Box */
.stTextInput>div>div>input {
    background-color: rgba(255,255,255,0.1);
    color: white;
    border-radius: 10px;
    border: 1px solid #00f2ff;
}

/* Button Style */
.stButton>button {
    background: linear-gradient(90deg, #00f2ff, #4facfe);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00f2ff;
}

/* Clear Visibility Text */
.custom-text {
    font-size: 14px;
    color: #ffffff;
    font-weight: 500;
    text-shadow: 0 0 8px rgba(0,255,255,0.8);
    animation: glow 2s infinite alternate;
    text-align: center;
    margin-top: -10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="glow-text">🔐 AI Powered Phishing URL Detector</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-text">Enter a website URL to analyze security risk</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = load("model.pkl")

# ---------------- INPUT ----------------
url = st.text_input("Enter Website URL")

# ---------------- BUTTON ----------------
if st.button("Analyze"):
    if url:
        features = extract_features(url)

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0].max()

        if prediction == 1:
            st.error("⚠️ Phishing Website Detected")
        else:
            st.success("✅ Legitimate Website")

        st.markdown(
            f"<div class='custom-text'>Confidence: {probability*100:.2f}%</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter a URL")
