import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression



df = pd.read_json("donnees/articles.sample.json")

X = df["content"]
y = df["categories"].str[0]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
text = X_train.iloc[0]

normalized_text = (
    text.replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
)

print("Original:")
print(text)

print("\nNormalized:")
print(normalized_text)