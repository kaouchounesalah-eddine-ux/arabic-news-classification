import unicodedata


def normalize_arabic(text):
    return (
        text.replace("أ", "ا")
            .replace("إ", "ا")
            .replace("آ", "ا")
    )


def remove_diacritics(text):
    return "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
        
    )


def remove_tatweel(text):
    return text.replace("ـ", "")

def remove_taarif(text):
    return " ".join(
        word.removeprefix("ال")
        for word in text.split()
    )

def remove_numbers(text):
    return "".join(
        char
        for char in text
        if not char.isdigit()
    )

def remove_marks(text):
    return text.replace('\\"', '"').replace('"', '') if isinstance(text, str) else text

arabic_stopwords = {
    "في", "من", "إلى", "على", "عن", "و", "أو",
    "أن", "إن", "كان", "كانت", "هذا", "هذه",
    "ذلك", "التي", "الذي", "هو", "هي", "هم",
    "ما", "لا", "لم", "لن", "مع", "كما"
}

def remove_stopwords(text):
    return " ".join(
        word
        for word in text.split()
        if word not in arabic_stopwords
    )

def preprocess(text):
    text = normalize_arabic(text)
    text = remove_diacritics(text)
    text = remove_tatweel(text)
    text = remove_taarif(text)
    text = remove_numbers(text)
    text = remove_marks(text)
    text = remove_stopwords(text)

    return text