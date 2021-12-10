import string
import spacy
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from XMLCollection.models import Article
from .apps import load as Classification


#   РМ. Метод, верно удаляющий знаки
def punctuation(text):
    for char in text:
        if char == "-":
            text = text.replace(char, " ")
        if char in string.punctuation:
            text = text.replace(char, "")
    return text


#   РМ. Токенизация
def tokenizer(text):
    text = str(text).lower()  # Единый регистр
    text = punctuation(text)  # удаляем знаки
    text = nltk.re.sub(r'[\d]+', '', text)
    textToken = RegexpTokenizer(r'\w+').tokenize(text)  # Токенизация!
    tokens = [word for word in textToken if word not in stopwords.words('russian')]  # Удаляем стоп
    finalTokens = [word for word in tokens if word not in stopwords.words('english')]
    return finalTokens


#   РМ. Стеммизация
def stemming(text):
    stem = SnowballStemmer("russian")
    text = [stem.stem(word) for word in text]
    stem = SnowballStemmer("english")
    text = [stem.stem(word) for word in text]
    return text


#   РМ. Леммизация
def lemmatizing(text):
    # python -m spacy download ru_core_news_sm
    SpObj = spacy.load('ru_core_news_sm', disable=['parser', 'ner'])
    doc = SpObj(" ".join(text))
    lemma = [token.lemma_ for token in doc]
    return lemma


#   РМ. Все ступени NLP
def allSteps(text):
    return lemmatizing(stemming(tokenizer(text)))


#   РМ. Лексическое представление ответов классификатора с %
def stringResultOfSlassification(arr):
    if arr[1] == 0:
        return "\'Автоновости\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 1:
        return "\'В мире\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 2:
        return "\'В России\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 3:
        return "\'Инопресса\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 4:
        return "\'Культура\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 5:
        return "\'Медицина\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 6:
        return "\'Недвижимость\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 7:
        return "\'Спорт\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 8:
        return "\'Технологии\' с вероятностью " + str(arr[0]) + "%\r\n"
    elif arr[1] == 9:
        return "\'Экономика\' с вероятностью " + str(arr[0]) + "%\r\n"


#   РМ. Обучение! Ну и ещё метрика для умных
def studyClassificator(X, Y):
    model = Pipeline([('vect', CountVectorizer()), # создаём модель (analyzer=allSteps)
                      ('tfidf', TfidfTransformer()),
                      ('clf', LogisticRegression())]) #
    # делаем выборку
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=0.20, random_state=1)
    model.fit(X_train, Y_train) # Обучаем
    # Проверяем! И далее оцениваем прогноз.     Расскомментировать на случай тестов
    # predictions = model.predict(X_validation)
    # print(accuracy_score(Y_validation, predictions))
    # print(confusion_matrix(Y_validation, predictions))
    # print(classification_report(Y_validation, predictions))
    return model


#   РМ. Выдаёт результат по работе
def resultClassification(id):
    articleText = Article.objects.all().get(pk=id).text # текст берём в соответствии с отправленным id
    vectorText = allSteps(articleText)
    predict = Classification.predict(vectorText)
    return resultCounter(predict)


#   РМ. Получаем результат в процентах по трём самым вероятным категориям.
def resultCounter(predict):
    arrPredict, result = list(predict), []
    percent, stringResult = len(arrPredict), "Классификатор предсказывает, что статья относится к категории:\r\n"
    for i in range(10):
        result.append([float('{:.2f}'.format((100 / percent) * arrPredict.count(i), '.2f')), i])
    result.sort(reverse=True)
    for i in range(3):
        stringResult = stringResult + stringResultOfSlassification(result[i])
    return stringResult


#   РМ. Получение статей из БД с ограничением 50шт для создания обучающей и тестовой выборки
def getArticlesToNLP(categories, lim):
    raf = [[], [], [], [], [], [], [], [], [], []]
    for index, category in enumerate(categories):
        articles = Article.objects.filter(category=category)[:lim].values_list("id", flat=True)
        size = len(articles)
        for i in range(size):
            raf[index].append(Article.objects.get(id=articles[i]).id)
    return raf


#   НРМ.Если вдруг не установлен
def init():
    nltk.download()
    return True
