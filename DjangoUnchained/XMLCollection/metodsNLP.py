import string
import spacy
import nltk
import multiprocessing as cpu
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer


cores = cpu.cpu_count() - 2


# Метод, верно удаляющий знаки
def punctuation(text):
    for char in text:
        if char == "-":
            text = text.replace(char, " ")
        if char in string.punctuation:
            text = text.replace(char, "")
    return text


def tokenizer(text):
    text = str(text).lower()  # Единый регистр
    text = punctuation(text)  # удаляем знаки
    text = nltk.re.sub(r'[\d]+', '', text)
    textToken = RegexpTokenizer(r'\w+').tokenize(text)  # Токенизация!
    tokens = [word for word in textToken if word not in stopwords.words('russian')]  # Удаляем стоп
    finalTokens = [word for word in tokens if word not in stopwords.words('english')]
    return finalTokens


def stemming(text):
    stem = SnowballStemmer("russian")
    text = [stem.stem(word) for word in text]
    stem = SnowballStemmer("english")
    text = [stem.stem(word) for word in text]
    return text


def lemmatizing(text):
    # python -m spacy download ru_core_news_sm
    SpObj = spacy.load('ru_core_news_sm', disable=['parser', 'ner'])
    doc = SpObj(" ".join(text))
    lemma = [token.lemma_ for token in doc]
    return lemma


def text_cleaner(text):
    return lemmatizing(stemming(tokenizer(text)))


def bagsOfWords_check(text, category):
    vec = CountVectorizer(analyzer=text_cleaner)
    fill = vec.fit_transform(text)
    bow = pd.DataFrame(fill.toarray(), columns=vec.get_feature_names())
    return coolWriter(bow, category, 1)


def NGrams_check(text, category):
    vec = CountVectorizer(ngram_range=(2, 2), analyzer=text_cleaner)
    fill = vec.fit_transform(text)
    gram = pd.DataFrame(fill.toarray(), columns=vec.get_feature_names())
    return coolWriter(gram, category, 2)


def TFIDF_check(text, category):
    vec = TfidfVectorizer(analyzer=text_cleaner)
    fill = vec.fit_transform(text)
    tfidf = pd.DataFrame(fill.toarray(), columns=vec.get_feature_names())
    if category == 1:
        return fill.toarray()   # Костыль, подправить
    return coolWriter(tfidf, category, 3)


def coolWriter(dataFrame, category,  classificatorType):
    path = ".\DjangoUnchained\XMLCollection\ML\\"
    dataFrame['CATEGORY'] = category
    if classificatorType == 1:
        fileName = path + "BOW.csv"
    elif classificatorType == 2:
        fileName = path + "NGrams.csv"
    elif classificatorType == 3:
        fileName = path + "TFIDF.csv"
    else:
        print("Err in DRAM module :c")
        return False
    print(fileName)
    dataFrame.to_csv(fileName, index=False) # и сохраняем эту сборную солянку
    return True


# Если вдруг не установлен
def init():
    nltk.download()
    return True

