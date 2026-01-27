import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

# Load dataset
df = pd.read_csv("data/phishing.csv")

# Drop ID column
df.drop(columns=["id"], inplace=True)

# Convert target: phishing(-1)=1, legitimate(1)=0
df["Result"] = df["Result"].map({-1: 1, 1: 0})

X = df.drop(columns=["Result"])
y = df["Result"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
dump(model, "model.pkl")

print("Model saved as model.pkl")
