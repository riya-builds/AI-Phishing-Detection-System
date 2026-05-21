import pandas as pd

data = pd.read_csv(
    'dataset/sms.tsv',
    sep='\t',
    names=['label', 'message']
)

print(data.head())

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(data['message'])

print(X)

data['label'] = data['label'].map({
    'ham': 0,
    'spam': 1
})

y = data['label']

print(y.head())

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(X_train.shape)
print(X_test.shape)

from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()

model.fit(X_train, y_train)

print("Model Training Completed")

from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)