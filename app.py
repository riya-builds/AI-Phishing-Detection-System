from flask import Flask, render_template, request
import joblib
import os
import re
import sqlite3

# ---------------- CREATE APP ----------------
app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ---------------- HOME PAGE ----------------
@app.route('/')
def home():

    return render_template('index.html')

# ---------------- PREDICTION ----------------
@app.route('/predict', methods=['POST'])
def predict():

    # Get user message
    user_message = request.form['message']

    # ---------------- ADVANCED PHISHING PATTERNS ----------------

    suspicious_patterns = [

        r"bit\.ly",
        r"tinyurl",
        r"verify",
        r"login",
        r"bank",
        r"account",
        r"secure",
        r"update",
        r"click",
        r"password",
        r"paypal",
        r"free",
        r"urgent",

        # Suspicious TLDs
        r"\.xyz",
        r"\.top",
        r"\.club",
        r"\.online",
        r"\.site",

        # IP-based URLs
        r"http[s]?://\d+\.\d+\.\d+\.\d+",

    ]

    # ---------------- URL FLAG ----------------

    url_flag = False

    for pattern in suspicious_patterns:

        if re.search(pattern, user_message.lower()):

            url_flag = True
            break

    # ---------------- SUBDOMAIN DETECTION ----------------

    subdomain_flag = False

    dots = user_message.count('.')

    if dots >= 4:

        subdomain_flag = True

    # ---------------- ML PREDICTION ----------------

    message_vector = vectorizer.transform([user_message])

    result = model.predict(message_vector)[0]

    probabilities = model.predict_proba(message_vector)[0]

    spam_confidence = probabilities[1] * 100
    ham_confidence = probabilities[0] * 100

    # ---------------- FINAL DECISION ----------------

    if result == 1 or url_flag or subdomain_flag:

        prediction = (
            f"⚠️ Phishing Detected "
            f"({spam_confidence:.2f}% confidence)"
        )

    else:

        prediction = (
            f"✅ Safe Message "
            f"({ham_confidence:.2f}% confidence)"
        )

    # ---------------- SAVE TO DATABASE ----------------

    connection = sqlite3.connect("predictions.db")

    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO predictions
        (message, result)

        VALUES (?, ?)
        ''',

        (user_message, prediction)
    )

    connection.commit()

    connection.close()

    # ---------------- RETURN RESULT ----------------

    return render_template(
        'index.html',
        prediction_text=prediction
    )

# ---------------- HISTORY PAGE ----------------

@app.route('/history')
def history():

    connection = sqlite3.connect("predictions.db")

    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM predictions
        ORDER BY id DESC
        '''
    )

    rows = cursor.fetchall()

    # ---------------- ANALYTICS ----------------

    total_predictions = len(rows)

    phishing_count = 0
    safe_count = 0

    for row in rows:

        result = row[2]

        if "Phishing" in result:

            phishing_count += 1

        else:

            safe_count += 1

    connection.close()

    return render_template(

        'history.html',

        rows=rows,

        total_predictions=total_predictions,

        phishing_count=phishing_count,

        safe_count=safe_count
    )

# ---------------- RUN APP ----------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )