import json
import os
import re
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
from XMLCollection.models import Article


categories = ["В РОССИИ", "В МИРЕ", "ЭКОНОМИКА", "СПОРТ", "КУЛЬТУРА", "ИНОПРЕССА",
                "МНЕНИЯ", "НЕДВИЖИМОСТЬ", "ТЕХНОЛОГИИ", "АВТОНОВОСТИ", "МЕДИЦИНА"]

#       Метод на получение всех статей
@csrf_exempt
def getArticles(request):
    articleList = Article.objects.get_queryset().order_by('id')  # Самое верное решение
    paginator = Paginator(articleList, 10)
    categories = ["В РОССИИ", "В МИРЕ", "ЭКОНОМИКА", "СПОРТ", "КУЛЬТУРА", "ИНОПРЕССА",
                  "МНЕНИЯ", "НЕДВИЖИМОСТЬ", "ТЕХНОЛОГИИ", "АВТОНОВОСТИ", "МЕДИЦИНА"]
    try:
        PList = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        PList = paginator.page(1)
    except EmptyPage:
        PList = paginator.page(paginator.num_pages)
    return render(request, "home.html", locals())


#       Метод на получение конкретной статьи
@csrf_exempt
def getArticle(request, any):
    article = Article.objects.all().get(pk=any)
    # TODO: Штуку ниже надо как то упростить, но пока оставлю так
    categories = ["В РОССИИ", "В МИРЕ", "ЭКОНОМИКА", "СПОРТ", "КУЛЬТУРА", "ИНОПРЕССА",
                  "МНЕНИЯ", "НЕДВИЖИМОСТЬ", "ТЕХНОЛОГИИ", "АВТОНОВОСТИ", "МЕДИЦИНА"]
    return render(request, "news.html", locals())


#       Метод на внесение статей в форме
@csrf_exempt
def addArticle(request):
    if request.method == 'POST':
        article = Article()
        article.title = str(request.POST.get("title"))
        article.category = str(request.POST.get("category"))
        article.date = str(request.POST.get("date"))
        article.text = str(request.POST.get("text"))
        article.tags = str(request.POST.get("tags"))
        article.keyWords = str(request.POST.get("keyWords"))
        article.url = str(request.POST.get("url"))
        article.save()
        # messages.info("Статья успешно создана!") TODO: доработать
        return redirect('/')
    if request.method == 'GET':
        categories = ["В РОССИИ", "В МИРЕ", "ЭКОНОМИКА", "СПОРТ", "КУЛЬТУРА", "ИНОПРЕССА",
                      "МНЕНИЯ", "НЕДВИЖИМОСТЬ", "ТЕХНОЛОГИИ", "АВТОНОВОСТИ", "МЕДИЦИНА"]
        return render(request, "add.html", locals())

#       Метод на сохранение изменений
@csrf_exempt
def saveArticle(request):
    # Получение данных
    data = request.body.decode('utf-8')
    dataJSON = json.loads(data)
    # Обработка ID
    id, updateArticle = dataJSON['id'], Article()
    if str(id) != "":
        updateArticle = Article.objects.get(id=id)
    # Обновление данных
    updateArticle.title = dataJSON['title']
    updateArticle.category = dataJSON['category']
    updateArticle.date = dataJSON['date']
    updateArticle.text = dataJSON['text']
    updateArticle.tags = dataJSON['tags']
    updateArticle.keyWords = dataJSON['keyWords']
    updateArticle.url = dataJSON['url']
    updateArticle.save()
    return HttpResponse(200)


#       Метод на удаление статьи
@csrf_exempt
def delArticle(request):
    articleToDelete = request.POST.get('articleID')
    if str(articleToDelete) != "":
        Article.objects.filter(id=articleToDelete).delete()
    # Возможно стоит добавить отправку сообщения о невозможности удаления
    return redirect('/')


# TODO: Метод на поиск по словам и фильтру

#       Метод на добавление статей в БД оффлайново
@csrf_exempt
def addArticleFromFile(request):
    # TODO: Исправить путь
    pathBy = r"C:\Users\1\PycharmProjects\DjangoCooledByCollection\DjangoUnchained\XMLCollection\articles"
    files = os.listdir(pathBy)
    article, flag = Article(), True
    for file in files:
        # Чтение файла
        with open(pathBy + "\\" + file, encoding='utf-8') as fobj:
            xml = fobj.read()
        XMLWorker = etree.fromstring(bytes(xml, encoding='utf8'))
        for elem in XMLWorker.getchildren():
            if elem.tag == "title":
                article.title = elem.text
                # Поиск наименования статьи в БД. Если нет - уходим
                if Article.objects.filter(title=str(article.title)):
                    flag = False
                    break
            # Логика поиска нужных элементов
            elif elem.tag == "category":
                article.category = elem.text
            elif elem.tag == "date":
                article.date = elem.text
            elif elem.tag == "text":
                article.text = elem.text
            elif elem.tag == "tags":
                article.tags = elem.text
            elif elem.tag == "keyWords":
                article.keyWords = elem.text
            elif elem.tag == "URL":
                article.url = elem.text
        if flag:
            article.save()  # Надо придумать множественное сохранение записей в БД
            print(file + "\tis readed and added to DataBase")
        else:
            print(file + "\tis already added to DataBase")
            flag = True
    return HttpResponse(200)


def finder(request):
    categories = ["", "В РОССИИ", "В МИРЕ", "ЭКОНОМИКА", "СПОРТ", "КУЛЬТУРА", "ИНОПРЕССА",
                  "МНЕНИЯ", "НЕДВИЖИМОСТЬ", "ТЕХНОЛОГИИ", "АВТОНОВОСТИ", "МЕДИЦИНА"]
    if request.method == 'POST':
        listSearchFiles = []
        category = request.POST.get("category")
        tags = request.POST.get("tags")
        if (tags and category) != "":
            for root, dirs, files in os.walk("./XMLCollection/articles/"):
                for filename in files:
                    xmlData = etree.parse("./XMLCollection/articles/" + str(filename))
                    if str(xmlData.find("./category").text.lower()) == str(category).lower():
                        patternTags = re.compile(r"([А-Яа-я]+)|([А-Яа-я]+\s[А-Яа-я]+)")
                        enteredTags = patternTags.findall(str(tags))
                        for tag in enteredTags:
                            for tagTo in patternTags.findall(xmlData.find("./tags").text):
                                if str(tag).lower() == str(tagTo).lower():
                                    listSearchFiles.append(str(filename))

        if category != "" and len(tags) == 0:
            for root, dirs, files in os.walk("./XMLCollection/articles/"):
                for filename in files:
                    xmlData = etree.parse("./XMLCollection/articles/" + str(filename))
                    if str(xmlData.find("./category").text.lower()) == str(category).lower():
                        listSearchFiles.append(str(filename))
        else:
            pass
        # сколько же всего предстоит сделать летом... А у меня ещё полный Титец
        if tags != "" and len(category) == 0:
            for root, dirs, files in os.walk("./XMLCollection/articles/"):
                for filename in files:
                    xmlData = etree.parse("./XMLCollection/articles/" + str(filename))
                    patternTags = re.compile(r"([А-Яа-я]+)|([А-Яа-я]+\s[А-Яа-я]+)")
                    enteredTags = patternTags.findall(str(tags))
                    for tag in enteredTags:
                        for tagTo in patternTags.findall(xmlData.find("./tags").text):
                            if str(tag).lower() == str(tagTo).lower():
                                listSearchFiles.append(str(filename))

        listSearchFiles = list(set(listSearchFiles))
        listSearchFiles.sort()
        request.session['data'] = listSearchFiles
        paginator = Paginator(listSearchFiles, 15)
        page = request.GET.get('page')
        try:
            articlesFragments = paginator.page(page)
        except PageNotAnInteger:
            articlesFragments = paginator.page(1)
        except EmptyPage:
            articlesFragments = paginator.page(paginator.num_pages)
        return render(request, "startPage.html", {"articlesFragments": articlesFragments,
                                                  "categories": categories})

    if request.method == "GET":
        paginator = Paginator(request.session['data'], 15)
        articlesFragments = request.GET.get('page')
        try:
            articlesFragments = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            articlesFragments = paginator.page(1)
        except EmptyPage:
            articlesFragments = paginator.page(paginator.num_pages)
        return render(request, "startPage.html", {"articlesFragments": articlesFragments,
                                                  "categories": categories})
