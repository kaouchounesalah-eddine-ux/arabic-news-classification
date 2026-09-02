
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from src.preprocess import preprocess
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from build_dataset import df


X = df["Body"]
y = df["Category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# preprocessing
X_train = X_train.apply(preprocess)
X_test = X_test.apply(preprocess)

# TF-IDF
vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# multiclass Logistic Regression
lr_model = LogisticRegression(
    max_iter=100000
)

lr_model.fit(X_train_tfidf, y_train)

# predictions
y_pred = lr_model.predict(X_test_tfidf)



print("Actual:")
print(list(y_test))

print("Predicted:")
print(y_pred.tolist())

print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification report:")
print(classification_report(y_test, y_pred))

print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClasses:")
print(lr_model.classes_)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    xticks_rotation=45
)