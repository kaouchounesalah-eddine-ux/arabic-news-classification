import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from src.preprocess import preprocess



df = pd.read_json("donnees/articles.sample.json")

X = df["content"]
y = df["categories"].str[0]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
X_train = X_train.apply(preprocess)
X_test = X_test.apply(preprocess)

label_set = sorted(y_train.unique())
# Create the vectorizer
vectorizer = TfidfVectorizer()

# Learn the vocabulary and convert the articles into vectors
X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)
print(len(X_test))


predictions={}
predec_prob=[]
for categorie in label_set:
    i=0
    binary_categorie=[] 
    while i < len(y_train):
        if categorie == y_train.iloc[i]:
            binary_categorie.append(1)
        else:
            binary_categorie.append(0)
        i+=1
    lr_model = LogisticRegression()
    lr_model.fit(X_train_tfidf, binary_categorie)


    y_pred = lr_model.predict_proba(X_test_tfidf)[0][1]
    predictions[categorie] = float(y_pred)

    predec_prob.append(float(y_pred))
    


print(predictions)
    
    
    




 


# # Create the vectorizer
# vectorizer = TfidfVectorizer()

# # Learn the vocabulary and convert the articles into vectors
# X = vectorizer.fit_transform(df["content"])

# print(df)
# print(X[0])
# print(X.getnnz())
# print(vectorizer.get_feature_names_out())


# import numpy as np

# X = np.array([[0.5, 1.5], [1,1], [1.5, 0.5], [3, 0.5], [2, 2], [1, 2.5]])
# y = np.array([0, 0, 0, 1, 1, 1])
# from sklearn.linear_model import LogisticRegression

# lr_model = LogisticRegression()
# lr_model.fit(X, y)

# print(lr_model.coef_)









# # -----------------------------------------
# # df["label"] = df["categories"].str[0]
# # print(df[["categories","label"]].head())
# # print("========== First 5 rows ==========")
# # print(df.head())

# # print("\n========== Dataset Information ==========")
# # print(df.info())

# # print("\n========== Columns ==========")
# # print(df.columns)

# # print("\n========== Shape ==========")
# # print(df.shape)
# # print(df.iloc[3])