import pandas as pd


df = pd.read_csv("donnees/Le360.com.csv")


category_mapping = {
    "Business": "اقتصاد",
    "Culture": "ثقافة",
    "International": "دولي",
    "Sport": "رياضة",
    "Policy": "سياسة",
    "Society": "مجتمع",
}


# Keep only the six PFA categories
df = df[df["Category"].isin(category_mapping)]


# Translate categories into the PFA labels
df["Category"] = df["Category"].map(category_mapping)







# Select 1000 articles from each category
samples = []

for category in category_mapping.values():

    category_articles = df[df["Category"] == category]

    sample = category_articles.sample(
        n=1000,
        random_state=42
    )

    samples.append(sample)


df = pd.concat(samples, ignore_index=True)


