import pandas as pd
import pickle
import numpy as np
from django.http import HttpResponse
from XMLCollection.models import Article
from sklearn.svm import SVC
from . import metodsNLP as nlp

# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import StratifiedKFold, cross_val_score
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier

# TODO: Дополнить большим количеством входных данных (1к по каждому варианту)
def learnNLP(request):
    categoryList = ["религия", "коронавирус"]#, "криминал"]
    articleList = [[262, 688, 698], [454, 420, 654, 754, 770, 226, 250, 281, 305, 318, 393]]#, []]
    articleTexts = []
    for index, categoryName in enumerate(categoryList):
        for j in articleList[index]:
            articleTexts.append([categoryName, Article.objects.all().get(pk=j).text])
    papich = pd.DataFrame(articleTexts, columns=("category", "text"))
    nlp.bagsOfWords_check(papich['text'], papich['category'])
    nlp.NGrams_check(papich['text'], papich['category'])
    nlp.TFIDF_check(papich['text'], papich['category'])
    return HttpResponse(200)


# TODO: в тело запроса требовать модель
# TODO: в ответ выводить лучший результат после обучения
def studyMLFromNLP(request):
    model ="TFIDF.csv"
    path = ".\DjangoUnchained\XMLCollection\ML\\"
    raw = pd.read_csv(path + model)
    X = np.asarray(raw.values[:, 0:-1], dtype=np.float32)
    Y = np.empty(0, dtype=np.int8)
    for catName in raw['CATEGORY']:
        if catName == 'коронавирус':
            Y = np.append(Y, 0)
        elif catName == 'религия':
            Y = np.append(Y, 1)
        elif catName == 'криминал':
            Y = np.append(Y, 2)
    svmClassifier = SVC() # можно применить любой классификатор, НО НАДО ДОРАБОТАТЬ ШТУКУ НИЖЕ
    svmClassifier.fit(X, Y)
    model = "".join(model.split('.')[:-1])
    pickle.dump(svmClassifier, open(path + model + ".dat", 'wb'))

    # models = []
    # models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
    # models.append(('LDA', LinearDiscriminantAnalysis()))
    # models.append(('KNN', KNeighborsClassifier()))
    # models.append(('CART', DecisionTreeClassifier()))
    # models.append(('NB', GaussianNB()))
    # models.append(('SVM', SVC(gamma='auto')))
    # Требуются ДОРАБТКА
    # results = []
    # names = []
    # ТЕСТ ЛУЧШЕГО КЛАССИФИКАТОРА
    # for name, model in models:
    #     kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    #     cv_results = cross_val_score(model, X, Y, cv=kfold, scoring='accuracy')
    #     results.append(cv_results)
    #     names.append(name)
    #     print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    return HttpResponse("Успех!")

# TODO: Ветвление для тестирования разными классификаторами
# TODO: попробовать w2v
def MLclassif(request):
    path = ".\DjangoUnchained\XMLCollection\ML\\"
    model = "TFIDF.dat"
    loadClassifier = pickle.load(open(path + model, 'rb'))
    articleText = Article.objects.all().get(pk=454).text # указываем лбой текст на тест
    # Вообще, стоит написать к хрени сверху ещё и тестер
    text = nlp.text_cleaner(articleText)
    vector = np.array(text)
    vector = nlp.TFIDF_check(vector, 1)
    predict = loadClassifier.predict(vector)
    return HttpResponse("Успех!" + predict)
