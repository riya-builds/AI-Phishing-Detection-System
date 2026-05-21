# AI Phishing Detection System

An AI-powered phishing message detection web application built using Flask, Machine Learning, and SQLite.

---

## Features

- Detects phishing/spam messages using Machine Learning
- TF-IDF vectorization for text processing
- Naive Bayes classification model
- Modern responsive UI
- Stores prediction history using SQLite database
- Real-time message analysis

---

## Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- SQLite
- HTML
- CSS

---

## Machine Learning Workflow

1. Dataset Collection
2. Text Preprocessing
3. TF-IDF Vectorization
4. Naive Bayes Model Training
5. Prediction Generation

---

## Project Structure

```bash
AI-Phishing-Detector/
│
├── dataset/
├── static/
├── templates/
├── venv/
├── app.py
├── train_model.py
├── model.pkl
├── vectorizer.pkl
├── phishing.db
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-link>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

---

## Future Improvements

- Deep Learning integration
- URL-based phishing detection
- Email header analysis
- User authentication system
- Cloud deployment

---

## Author

Riya Kumari