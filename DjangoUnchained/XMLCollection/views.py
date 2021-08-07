import json
import os
import re
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from lxml import etree
from XMLCollection.models import Article


#       Метод на получение всех статей
@csrf_exempt
def getArticles(request):
    articleList = Article.objects.get_queryset().order_by('id')  # Самое верное решение
    paginator = Paginator(articleList, 10)
    categories = ["В России", "В мире", "Экономика", "Спорт", "Культура", "Инопресса",
                  "Мнения", "Недвижимость", "Технологии", "Автоновости", "Медицина"]
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
    categories = ["В России", "В мире", "Экономика", "Спорт", "Культура", "Инопресса",
                  "Мнения", "Недвижимость", "Технологии", "Автоновости", "Медицина"]
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
        categories = ["В России", "В мире", "Экономика", "Спорт", "Культура", "Инопресса",
                      "Мнения", "Недвижимость", "Технологии", "Автоновости", "Медицина"]
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
@csrf_exempt
def search(request):
    categories = ["В России", "В мире", "Экономика", "Спорт", "Культура", "Инопресса",
                  "Мнения", "Недвижимость", "Технологии", "Автоновости", "Медицина"]
    if request.method == 'POST':
        # Я бился над этой проблемой пару дней, а проблема оказалась тривиальна (нахуй __iexact в SQLite).
        # Этот костыль создан для поиска по категориям. На вопрос почему - ответ:
        # A bug: SQLite only understands upper/lower case for ASCII characters by default.
        # The LIKE operator is case sensitive by default for unicode characters that are beyond
        # the ASCII range. For example, the expression 'a' LIKE 'A' is TRUE but 'æ' LIKE 'Æ' is FALSE.)
        # Ну и ясное дело, я родился в России, а не в великой и объятной Британской колонии
        # if category == "В России":
        #     category = "" + category[0:3] + category[3:].lower()
        # else:
        #     category = "" + category[0:1] + category[1:].lower()
        # Здесь костыль заканчивается
        # category = request.POST.get('category')
        # tag = request.POST.get('tag')
        keyWord = request.POST.get('keyWord')
        # title = request.POST.get('title')
        # print(category + "s" + tag + "f" + keyWord + "c" + title)
        # print(tag)
        # articleList = Article.objects.filter(Q(category=category) | Q(tags=tag))
        # https://qna.habr.com/q/938809 # Доделать поиск
        articleList = Q()  # создаем первый объект Q, что бы складывать с ним другие
        for key in ['category', 'tag', 'keyWord', 'title']:
            value = request.GET.get(key)
            if value and keyWord != "":
                articleList |= Q(**{f'{key}__icontains': keyWord})
        paginator = Paginator(articleList, 10)
        try:
            PList = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            PList = paginator.page(1)
        except EmptyPage:
            PList = paginator.page(paginator.num_pages)
        return render(request, "home.html", locals())
    # Переход по страницам
    if request.method == "GET":
        paginator = Paginator(request.session['data'], 10)
        articleList = request.GET.get('page')
        try:
            PList = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            PList = paginator.page(1)
        except EmptyPage:
            PList = paginator.page(paginator.num_pages)
        return render(request, "home.html", locals())


#       Метод на добавление статей в БД оффлайново
@csrf_exempt
def addArticleFromFile(request):
    pathBy = r".\XMLCollection\articles"
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
            article.save()  # TODO: Надо придумать множественное сохранение записей в БД
            print(file + "\tis readed and added to DataBase")
        else:
            print(file + "\tis already added to DataBase")
            flag = True
    return HttpResponse(200)
