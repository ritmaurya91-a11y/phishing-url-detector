# Phishing URL Detection Using Machine Learning (Mini SOC Tool)

A machine learning-based web application that detects phishing websites in real time by analyzing URL characteristics using feature engineering and a trained classification model.

This project simulates a Security Operations Center (SOC) style URL investigation workflow and helps automate the identification of malicious links.

---

## Features

- Real-time phishing URL detection  
- Automatic URL feature extraction  
- Machine learning-based classification  
- Streamlit web interface  
- SOC-style analysis workflow  
- Lightweight and fast prediction  

---

## Technology Stack

- Python  
- Scikit-learn  
- Pandas  
- Streamlit  

---

## Project Structure

phishing-url-detector/
│
├── app.py # Streamlit web application
├── feature_extractor.py # URL feature extraction logic
├── model.pkl # Trained ML model
├── report.pdf # Project documentation
├── requirements.txt # Python dependencies
└── README.md # Project description

yaml
Copy code

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/your-username/phishing-url-detector.git
cd phishing-url-detector
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Run the application
bash
Copy code
streamlit run app.py
How It Works
User enters a website URL

The system extracts security-related features from the URL

The trained machine learning model classifies the URL as:

Phishing

Legitimate

Result and confidence score are displayed instantly

Dataset
The model is trained on a public phishing dataset containing URL-based features labeled as phishing or legitimate.

Features include:

Presence of IP address

URL length

Special characters

HTTPS usage

Subdomain count

Domain age

Redirection behavior

And more

Use Cases
SOC analyst URL triage

Cybersecurity education and training

Security automation demonstrations

Academic machine learning projects

Author
Aman
Domain: Cybersecurity & Machine Learning

License
This project is intended for educational and research purposes.

Resume Line
Built a machine learning-based phishing URL detection system with real-time web deployment using Streamlit and automated feature extraction.

yaml
Copy code

---

If you want, I can also provide:

✅ `requirements.txt` file  
✅ `.gitignore` file  
✅ Streamlit Cloud deployment steps  
✅ GitHub banner image  
✅ Project architecture diagram  
✅ Report sections (Methodology, Results, Conclusion)  

Just tell me what you need next.