from flask import Flask, render_template, request
import joblib
import sqlite3

app = Flask(__name__)

# Load ML model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Database connection
connection = sqlite3.connect(
    'phishing.db',
    check_same_thread=False
)

cursor = connection.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    message TEXT,

    result TEXT
)
''')

connection.commit()


@app.route('/', methods=['GET', 'POST'])
def home():

    prediction = ""

    if request.method == 'POST':

        # Get user message
        user_message = request.form['message']

        # Convert text into vector
        message_vector = vectorizer.transform([user_message])

        # Predict
        result = model.predict(message_vector)

        # Check result
        if result[0] == 1:
            prediction = "⚠️ Phishing Message Detected!"

        else:
            prediction = "✅ Safe Message"

        # Save into database
        cursor.execute(
            '''
            INSERT INTO predictions
            (message, result)

            VALUES (?, ?)
            ''',
            (user_message, prediction)
        )

        connection.commit()

    return render_template(
        'index.html',
        prediction=prediction
    )


if __name__ == '__main__':
    app.run(debug=True)