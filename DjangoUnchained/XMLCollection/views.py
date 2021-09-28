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


def category():
    return ["В России", "В мире", "Экономика", "Спорт", "Культура", "Инопресса",
            "Мнения", "Недвижимость", "Технологии", "Автоновости", "Медицина"]


#       Метод на получение всех статей
@csrf_exempt
def getArticles(request):
    articleList = Article.objects.get_queryset().order_by('id')  # Самое верное решение
    paginator = Paginator(articleList, 10)
    categories = category()
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
    categories = category()
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
        categories = category()
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


@csrf_exempt
def search(request):
    categories = category()
    if request.method == 'POST':
        # Я бился над этой проблемой пару дней, а проблема оказалась тривиальна (нахуй __iexact в SQLite).
        # Этот костыль создан для поиска по категориям. На вопрос почему - ответ:
        # A bug: SQLite only understands upper/lower case for ASCII characters by default.
        # The LIKE operator is case sensitive by default for unicode characters that are beyond
        # the ASCII range. For example, the expression 'a' LIKE 'A' is TRUE but 'æ' LIKE 'Æ' is FALSE.)
        # Ну и ясное дело, я родился в России, а не в великой и объятной Британской колонии

        # Крутой способ, но почему то не хочет работать(
        # conditions = {'category': request.POST.get('category'),
        #               'tag': request.POST.get('tag'),
        #               'keyWord': request.POST.get('keyWord'),
        #               'title': request.POST.get('title')}
        # request = Q()
        # for key, value in conditions.items():
        #     if value != "":
        #         request &= Q(**{f'{key}__icontains': value})
        # articleList = Article.objects.filter(request)

        filters = Q()
        if request.POST.get('category'):
            filters &= Q(category__icontains=request.POST.get('category'))
        if request.POST.get('tag'):
            filters &= Q(tags__icontains=request.POST.get('tag'))
        if request.POST.get('keyWord'):
            filters &= Q(keyWord__icontains=request.POST.get('keyWord'))
        if request.POST.get('title'):
            filters &= Q(title__icontains=request.POST.get('title'))
        articleList = Article.objects.filter(filters)
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
        paginator = Paginator(request.session['data'], 10) #TODO: Пофиксить переход
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
    flag = True
    for file in files:
        # Чтение файла
        with open(pathBy + "\\" + file, encoding='utf-8') as fobj:
            xml = fobj.read()
        XMLWorker = etree.fromstring(bytes(xml, encoding='utf8'))
        article = Article()
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
            article.save()
            print(file + "\tis readed and added to DataBase")
        else:
            print(file + "\tis already added to DataBase")
            flag = True
    return HttpResponse(200)
