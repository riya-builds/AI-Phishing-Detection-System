import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# ---------------- LOAD ORIGINAL DATASET ----------------
data = pd.read_csv(
    'dataset/sms.tsv',
    sep='\t',
    names=['label', 'message']
)

# ---------------- ADD CUSTOM PHISHING DATA ----------------
custom_data = pd.DataFrame({
    'label': [
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'ham',
        'ham',
        'ham'
    ],

    'message': [
        'your bank account will be suspended click now',
        'verify your account immediately',
        'click here to reset your password',
        'urgent login attempt detected',
        'your paypal account has been locked',
        'confirm your debit card details now',
        'security alert verify your banking information',
        'hello how are you',
        'lets meet tomorrow',
        'call me when you reach home'
    ]
})

# Merge original + custom data
data = pd.concat([data, custom_data], ignore_index=True)

# ---------------- CHECK DATA ----------------
print("\nFirst 5 rows:")
print(data.head())

print("\nLABEL DISTRIBUTION (BEFORE MAPPING):")
print(data['label'].value_counts())

# ---------------- CLEAN DATA ----------------
data = data.dropna()

# ---------------- LABEL MAPPING ----------------
data['label'] = data['label'].map({
    'ham': 0,
    'spam': 1
})

# Remove failed rows
data = data.dropna()

print("\nLABEL DISTRIBUTION (AFTER MAPPING):")
print(data['label'].value_counts())

# ---------------- FEATURE EXTRACTION ----------------
vectorizer = CountVectorizer()

X = vectorizer.fit_transform(data['message'])

y = data['label']

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nDataset Shape:")
print("Train:", X_train.shape)
print("Test:", X_test.shape)

# ---------------- MODEL TRAINING ----------------
model = MultinomialNB()

model.fit(X_train, y_train)

print("\nModel Training Completed")

# ---------------- PREDICTION ----------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n====================")
print("Accuracy:", accuracy)
print("====================\n")

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ model.pkl saved")
print("✅ vectorizer.pkl saved")