from flask import Flask, render_template, request
import joblib
import sqlite3
import os

app = Flask(__name__)

# Load ML model + vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# ---------------- DATABASE SETUP ----------------

connection = sqlite3.connect('phishing.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    result TEXT
)
''')

connection.commit()

# ---------------- HOME ROUTE ----------------

@app.route('/', methods=['GET', 'POST'])
def home():

    prediction = ""

    if request.method == 'POST':

        user_message = request.form['message']

        # Convert text to vector
        message_vector = vectorizer.transform([user_message])

        # Predict
        result = model.predict(message_vector)

        # Interpret result
        if result[0] == 1:
            prediction = "⚠️ Phishing Message Detected!"
        else:
            prediction = "✅ Safe Message"

        # Save to database
        cursor.execute('''
            INSERT INTO predictions (message, result)
            VALUES (?, ?)
        ''', (user_message, prediction))

        connection.commit()

    return render_template('index.html', prediction=prediction)

# ---------------- RUN SERVER ----------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)