import string
import scipy
import spacy
import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer


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


def bagsOfWords(text, category):
    vec = CountVectorizer(analyzer=text_cleaner)
    fill = vec.fit_transform(text)
    bow = pd.DataFrame(fill.toarray(), columns=vec.get_feature_names())
    return coolWriter(bow, fill, category, 1)


def NGrams(text, category):
    vec = CountVectorizer(ngram_range=(2,2), analyzer=text_cleaner)
    fill = vec.fit_transform(text)
    gram = pd.DataFrame(fill.toarray(), columns=vec.get_feature_names())
    return coolWriter(gram, fill, category, 2)


def TFIDF(text, category):
    vec = TfidfVectorizer(analyzer=text_cleaner)
    fill = vec.fit_transform(text)
    tfidf = pd.DataFrame(fill.toarray(), columns=vec.get_feature_names())
    return coolWriter(tfidf, fill, category, 3)


def coolWriter(dataFrame, count, category, classificatorType):
    if category == "религия":
        dataFrame["category"] = np.full(len(count.getnnz(axis=1)), 1) # 1
    elif category == "коронавирус":
        dataFrame["category"] = np.zeros(len(count.getnnz(axis=1)))  # добавляем категорию
    elif category == "криминал":
        dataFrame["category"] = np.full(len(count.getnnz(axis=1)), 2) # 2
    else:
        print("Err in DRAM module :c")
        return False
    if classificatorType == 1:
        fileName = "BOW_" + category + ".csv"
    elif classificatorType == 2:
        fileName = "NGrams_" + category + ".csv"
    elif classificatorType == 3:
        fileName = "TFIDF_" + category + ".csv"
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

