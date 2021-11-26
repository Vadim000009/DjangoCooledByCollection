import nltk
import string

import spacy
from gensim.utils import simple_preprocess
from gensim.corpora import MmCorpus
from gensim.models.phrases import Phrases
from gensim.models.word2vec import Word2Vec
from gensim.models import LdaModel, LdaMulticore
from gensim.test.utils import get_tmpfile
from gensim import corpora, models
from multiprocessing import cpu_count
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import numpy as np


# Метод, верно удаляющий знаки
def punctuation(text):
    for char in text:
        if char == "-":
            text = text.replace(char, " ")
        if char in string.punctuation:
            text = text.replace(char, "")
    return text


def procLemma(text):
    tokenz = RegexpTokenizer(r'\w+')
    stop_words = stopwords.words('russian')
    stemmer = SnowballStemmer("russian")
    SpObj = spacy.load('ru_core_news_sm', disable=['parser', 'ner'])
    tokens = []
    for article in text:
        proces = str(article).lower()
        proces = punctuation(proces)
        proces = nltk.re.sub(r'[\d]+', '', proces)
        procToken = tokenz.tokenize(proces)
        tokens = [word for word in procToken if word not in stop_words]
        proces = [stemmer.stem(word) for word in tokens]
        doc = SpObj(" ".join(proces))
        lemma = [token.lemma_ for token in doc]
        tokens.append(lemma)
    return tokens



def tokenized(text):
    tokens = []
    for article in text:
        tokens.append(simple_preprocess(article, deacc=True))
    return tokens


def createDictionary(tokens, name):
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(i) for i in tokens]
    dictionary.save("dictionary_" + name + ".dict")
    return dictionary, corpus


def createBagFokenWords(tokens, dictionary):
    BOW = [dictionary.doc2bow(text, allow_update=True) for text in tokens]
    output = get_tmpfile("BOW.mm")
    MmCorpus.serialize(output, BOW)
    return BOW


def TFIDF(BOW, dictionary):
    word_weight, weight_tfidf = [], []
    for doc in BOW:
        for id, freq in doc:
            word_weight.append([dictionary[id], freq])
    tfidf = models.TfidfModel(BOW, smartirs='ntc')
    for doc in tfidf[BOW]:
        for id, freq in doc:
            weight_tfidf.append([dictionary[id], np.around(freq, decimals=3)])


def biGram(tokens):
    bigram = Phrases(tokens, min_count=3, threshold=10)
    trigram = Phrases(bigram[tokens], threshold=10)
    return trigram


def w2v(tokens):
    w2vec = Word2Vec(tokens, min_count=0, workers=cpu_count())
    w2vec.save('Word2Vec')


def learnNLP(corpus, dictionary):
    LDAmodel = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
    LDAmodel.save('LDA.model')
    return
