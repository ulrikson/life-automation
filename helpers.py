import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)


class TextHelper:
    def __init__(self, text) -> None:
        self.text = text
        self.language = "swedish"

    def clean_and_lemmatize_text(self):
        stop_words = set(stopwords.words(self.language))
        word_tokens = word_tokenize(self.text)
        lemmatizer = WordNetLemmatizer()
        filtered_text = [
            lemmatizer.lemmatize(word) for word in word_tokens if not word in stop_words
        ]
        clean_text = self.remove_punctuation_and_empty_strings(filtered_text)

        return " ".join(clean_text)

    def remove_punctuation_and_empty_strings(self, filtered_text):
        filtered_text = [
            "".join(c for c in w if c not in string.punctuation) for w in filtered_text
        ]
        return [word for word in filtered_text if word]


if __name__ == "__main__":
    text = "Hej! Jag heter Adam och jag gillar att programmera. Jag har en hund som heter Sixten."
    text_helper = TextHelper(text)
    print(text_helper.clean_and_lemmatize_text())
