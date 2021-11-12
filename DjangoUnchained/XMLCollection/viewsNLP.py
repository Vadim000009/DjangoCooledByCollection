import pandas as pd
import pickle
import numpy as np
from django.http import HttpResponse
from XMLCollection.models import Article
from . import metodsNLP as nlp

# Часть тестов для крутых ответов
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


# TODO: Дополнить большим количеством входных данных (1к по каждому варианту)
def learnNLP(request):
    # Вообще, запрос вида "SELECT id FROM XMLCollection_article where category='category' limit 50;"
    # БЫЛ БЫ ЛУЧШЕ, но.. мы ищем лёгкие пути?
    categoryList = ["Технологии", "Автоновости", "В России", "Инопресса", "Медицина",
                    "Спорт", "Недвижимость", "Культура", "Экономика"]
    articleList = [
        [2, 30, 34, 35, 62, 71, 87, 95, 104, 112, 117, 138, 154, 159, 162, 188, 196, 200, 207, 212, 217, 223, 229, 256,
         257, 268, 270, 287, 290, 303, 313, 316, 341, 372, 379, 388, 390, 402, 408, 409, 413, 417, 425, 440, 467, 503,
         509, 513, 529, 533],
        [41, 81, 99, 100, 105, 176, 192, 263, 293, 300, 333, 350, 374, 383, 411, 433, 456, 494, 518, 536, 615, 636, 662,
         682, 692, 714, 739, 753, 817, 829, 835, 933, 937, 947, 968, 1042, 1070, 1080, 1096, 1105],
        [9, 13, 15, 19, 23, 24, 25, 33, 38, 45, 47, 51, 55, 56, 63, 66, 72, 78, 85, 89, 94, 97, 102, 109, 111, 115, 119,
         125, 126, 130, 136, 137, 144, 145, 147, 150, 153, 156, 161, 165, 170, 180, 181, 186, 191, 197, 201, 202, 204,
         210],
        [22, 28, 50, 52, 53, 54, 59, 74, 77, 80, 86, 106, 121, 127, 128, 129, 131, 139, 142, 149, 157, 164, 167, 169,
         171, 172, 173, 177, 178, 184, 187, 211, 226, 231, 237, 240, 244, 245, 248, 258, 262, 265, 269, 273, 277, 296,
         302, 309, 312, 314],
        [8, 10, 21, 31, 37, 43, 49, 60, 64, 73, 82, 92, 96, 110, 113, 123, 190, 193, 206, 208, 209, 216, 220, 228, 234,
         259, 266, 274, 279, 284, 288, 295, 297, 306, 320, 328, 331, 348, 355, 360, 368, 377, 381, 384, 394, 416, 430,
         431, 437, 442],
        [11, 16, 26, 32, 39, 67, 69, 79, 83, 91, 101, 107, 116, 122, 140, 146, 151, 160, 189, 194, 198, 203, 214, 222,
         230, 232, 243, 253, 254, 260, 264, 272, 280, 283, 291, 299, 325, 334, 340, 344, 352, 363, 373, 421, 427, 434,
         441, 448, 455, 463],
        [14, 20, 29, 36, 40, 42, 46, 65, 76, 90, 98, 103, 108, 114, 118, 120, 132, 134, 141, 148, 152, 158, 163, 185,
         199, 218, 224, 233, 235, 261, 271, 278, 282, 301, 304, 308, 324, 327, 336, 343, 346, 366, 376, 380, 385, 389,
         392, 419, 424, 432],
        [12, 18, 27, 58, 75, 84, 143, 155, 183, 227, 252, 338, 345, 353, 357, 406, 451, 489, 504, 524, 651, 666, 724,
         743, 745, 758, 783, 853, 896, 911, 993, 997, 1003, 1032, 1049, 1091, 1123, 1148, 1163, 1175, 1265, 1320, 1329,
         1353, 1383, 1399, 1486, 1508, 1587, 1590],
        [166, 292, 310, 349, 487, 550, 577, 583, 669, 710, 731, 857, 893, 945, 1051, 1276, 1413, 1472, 1574, 1628],
        [44, 88, 175, 195, 219, 239, 275, 330, 367, 640, 659, 712, 823, 862, 881, 902, 930, 948, 966, 970, 1024, 1076,
         1097, 1099, 1157, 1261, 1302, 1361, 1427, 1490, 1537, 1548, 1558, 1569, 1636]
    ]
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
    model = "TFIDF.csv"
    path = ".\DjangoUnchained\XMLCollection\ML\\"
    raw = pd.read_csv(path + model)
    X = np.asarray(raw.values[:, 0:-1], dtype=np.float32)
    Y = np.empty(0, dtype=np.int8)
    for catName in raw['CATEGORY']:
        if catName == 'Технологии':
            Y = np.append(Y, 0)
        elif catName == 'Автоновости':
            Y = np.append(Y, 1)
        elif catName == 'В России':
            Y = np.append(Y, 2)
        elif catName == 'Инопресса':
            Y = np.append(Y, 3)
        elif catName == 'Медицина':
            Y = np.append(Y, 4)
        elif catName == 'Спорт':
            Y = np.append(Y, 5)
        elif catName == 'Недвижимость':
            Y = np.append(Y, 6)
        elif catName == 'Культура':
            Y = np.append(Y, 7)
        elif catName == 'Экономика':
            Y = np.append(Y, 8)
    svmClassifier = GaussianNB()  # можно применить любой классификатор, НО НАДО ДОРАБОТАТЬ ШТУКУ НИЖЕ
    svmClassifier.fit(X, Y)
    model = "".join(model.split('.')[:-1])
    pickle.dump(svmClassifier, open(path + model + ".dat", 'wb'))
    # ### Процесс поиск ЛУЧШЕГО классификатора ###
    # models = []
    # models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
    # models.append(('LDA', LinearDiscriminantAnalysis()))
    # models.append(('KNN', KNeighborsClassifier()))
    # models.append(('CART', DecisionTreeClassifier()))
    # models.append(('NB', GaussianNB()))
    # models.append(('SVM', SVC(gamma='auto')))
    # # Требуются ДОРАБОТКИ
    # results = []
    # names = []
    # # ТЕСТ ЛУЧШЕГО КЛАССИФИКАТОРА
    # for name, model in models:
    #     kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    #     cv_results = cross_val_score(model, X, Y, cv=kfold, scoring='accuracy')
    #     results.append(cv_results)
    #     names.append(name)
    #     print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

    # ### Создаем прогноз на контрольной выборке, тем самым показываем, что может наш классификатор ###
    # X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=0.20, random_state=1)
    # model = GaussianNB()
    # model.fit(X_train, Y_train)
    # predictions = model.predict(X_validation)
    # # Оцениваем прогноз
    # print(accuracy_score(Y_validation, predictions))
    # print(confusion_matrix(Y_validation, predictions))
    # print(classification_report(Y_validation, predictions))
    return HttpResponse("Успех!")


# TODO: Ветвление для тестирования разными классификаторами
# TODO: попробовать w2v
def MLclassif(request):
    path = ".\DjangoUnchained\XMLCollection\ML\\"
    model = "TFIDF.dat"
    loadClassifier = pickle.load(open(path + model, 'rb'))
    articleText = Article.objects.all().get(pk=454).text  # указываем лбой текст на тест
    # Вообще, стоит написать к хрени сверху ещё и тестер
    #text = nlp.text_cleaner(articleText)
    #vector = np.array(text)
    vector = nlp.TFIDF_check([articleText], 1)
    vector = nlp.zeros(vector, 15698)
    predict = loadClassifier.predict(np.asarray(vector.reshape(-1, 1)))
    return HttpResponse(predict)
