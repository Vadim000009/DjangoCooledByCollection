import pandas as pd
import pickle
import os
import time
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from XMLCollection.models import Article
from . import metodsNLP as nlp


dataFile = "Data.csv"
path = ".\DjangoUnchained\XMLCollection\ML\\"
if os.path.exists(path):
    pass
else:
    path = ".\XMLCollection\ML\\"


# Метод подготовки данных
def preparedLearnNLP(request, any):
    categoryList, articleTexts = ["Автоновости", "В мире", "В России", "Инопресса", "Культура", "Медицина",
                    "Недвижимость", "Спорт", "Технологии", "Экономика"], []
    articleList = nlp.getArticlesToNLP(categoryList, any)
    start_time = time.time()
    for index, categoryName in enumerate(categoryList):
        for j in articleList[index]:
            articleTexts.append([index, nlp.allSteps(Article.objects.all().get(pk=j).text)])
    print("--- %s seconds ---" % (time.time() - start_time))
    dataFileRAW = pd.DataFrame(articleTexts, columns=("category", "text"))
    dataFileRAW.to_csv(path + dataFile, index=False)
    return HttpResponse(200)


# Метод обучения по подготовленным данным
def studyMLFromNLP(request):
    raw = pd.read_csv(path + dataFile)
    X, Y = raw['text'], raw['category']
    resultCorvus = nlp.studyClassificator(X, Y)
    pickle.dump(resultCorvus, open(path + dataFile[:-3] + "dat", 'wb')) # Применяем соления для лучшей консервации
    return HttpResponse("Успех!")


@csrf_exempt
def MLclassif(request, any):
    result = nlp.resultClassification(any, 0)
    return JsonResponse(result, safe=False)


@csrf_exempt
def MLclassifText(request):
    data = request.body.decode('utf-8')
    dataJSON = json.loads(data)
    result = nlp.resultClassification(dataJSON['text'], 1)
    return JsonResponse(result, safe=False)
