import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

df = pd.read_csv("data/phishing.csv")

# Keep only URL-based features
features = [
    "having_IP_Address","URL_Length","Shortining_Service","having_At_Symbol",
    "double_slash_redirecting","Prefix_Suffix","having_Sub_Domain","SSLfinal_State"
]

X = df[features]
y = df["Result"].map({-1: 1, 1: 0})  # phishing=1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

dump(model, "model.pkl")

print("URL-only model trained and saved.")
