import json
import os
import re
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree


# TODO: Дописать сюда сортировку, фильтр, жизнь


# Получаем текущее положение.
def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


@csrf_exempt
def getMoreArticles(request):
    if request.method == "GET":
        articleList = []
        for root, dirs, files in os.walk("XMLCollection/articles"):
            for filename in files:
                articleList.append(filename)
        paginator = Paginator(articleList, 15)
        try:
            articlesFragments = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            articlesFragments = paginator.page(1)
        except EmptyPage:
            articlesFragments = paginator.page(paginator.num_pages)
        return render(request, "startPage.html", {"articlesFragments": articlesFragments})


@csrf_exempt
def getArticle(request, any):
    try:
        XMLFile = etree.parse("XMLCollection/articles/" + str(any) + ".xml")
        dataURL = XMLFile.find("./URL").text
        dataTitle = XMLFile.find("./title").text
        dataText = XMLFile.find("./text").text
        dataDate = XMLFile.find("./date").text
        dataCategory = XMLFile.find("./category").text
        # dataTags = XMLFile.find("./tags").text
        return render(request, "news.html",
                      {"nameFile": any,
                       "URL": dataURL,
                       "title": dataTitle,
                       "text": dataText,
                       "date": dataDate,
                       "category": dataCategory
                       # "tags": tags
                       })
    except (FileNotFoundError, OSError):
        return HttpResponseRedirect(reverse('XMLCollection:_start_'))


# Изменение файла асинхронно. Возможности изменения подвергаются все атрибуты, доступные на странице.
@csrf_exempt
def save(request):
    if request.method == 'POST' and request.is_ajax():
        data = request.body.decode('utf-8')
        dataJSON = json.loads(data)
        XMLFile = etree.parse("XMLCollection/articles/" + str(dataJSON['nameFile']) + ".xml")
        XMLFile.find('./URL').text = dataJSON['URL']
        XMLFile.find("./title").text = dataJSON['title']
        XMLFile.find("./text").text = dataJSON['text']
        XMLFile.find("./date").text = dataJSON['date']
        XMLFile.find("./category").text = dataJSON['category']
        # XMLFile.find("./tags").text = dataJSON["tags"]
        XMLFile.write("XMLCollection/articles/" + str(dataJSON['nameFile']) + ".xml", encoding="utf-8")
        messages.success(request, 'Изменения сохранены')
        return HttpResponse(200)


# Удаление файла из директории асинхронно.
def delete(request):
    if request.method == 'DELETE' and request.is_ajax():
        data = request.body.decode('utf-8')
        dataJSON = json.loads(data)
        os.remove(os.path.join("./XMLCollection/articles/", str(dataJSON["nameFile"]) + ".xml"))
        return HttpResponse(200)


def addArticle(request):
    if request.method == 'POST':
        xmlData = etree.Element("doc")
        originalURLData = etree.SubElement(xmlData, "URL")
        originalURLData.attrib['verify'] = "true"
        originalURLData.attrib['type'] = "str"
        originalURLData.attrib['auto'] = "true"

        titleXmlData = etree.SubElement(xmlData, "title")
        titleXmlData.attrib['verify'] = "true"
        titleXmlData.attrib['type'] = "str"
        titleXmlData.attrib['auto'] = "true"

        textXmlData = etree.SubElement(xmlData, "text")
        textXmlData.attrib['verify'] = "true"
        textXmlData.attrib['type'] = "str"
        textXmlData.attrib['auto'] = "true"

        dateXmlData = etree.SubElement(xmlData, "date")
        dateXmlData.attrib['verify'] = "true"
        dateXmlData.attrib['type'] = "str"
        dateXmlData.attrib['auto'] = "true"

        categoryXmlData = etree.SubElement(xmlData, "category")
        categoryXmlData.attrib['verify'] = "true"
        categoryXmlData.attrib['type'] = "str"
        categoryXmlData.attrib['auto'] = "true"

        originalURLData.text = str(request.POST.get("URL"))
        titleXmlData.text = str(request.POST.get("title"))
        textXmlData.text = str(request.POST.get("text"))
        dateXmlData.text = str(request.POST.get("date"))
        categoryXmlData.text = str(request.POST.get("category"))

        xmlTree = etree.ElementTree(xmlData)
        xmlTree.write(r"./XMLCollection/articles/" + str(request.POST.get("nameFile")) + ".xml"
                      , encoding="utf-8", xml_declaration=True, pretty_print=True)
        return render(request, "newXMLPage.html")
    if request.method == 'GET':
        return render(request, "newXMLPage.html")


def finder(request):
    if request.method == 'POST':
        listSearchFiles = []
        category = request.POST.get("category")

        if category != "":
            for root, dirs, files in os.walk("./XMLCollection/articles/"):
                for filename in files:
                    xmlData = etree.parse("./XMLCollection/articles/" + str(filename))
                    if str(xmlData.find("./category").text.lower()) == str(category).lower():
                        listSearchFiles.append(str(filename))
        else:
            pass
        listSearchFiles = list(set(listSearchFiles))
        request.session['data'] = listSearchFiles
        paginator = Paginator(listSearchFiles, 15)
        page = request.GET.get('page')
        try:
            articlesFragments = paginator.page(page)
        except PageNotAnInteger:
            articlesFragments = paginator.page(1)
        except EmptyPage:
            articlesFragments = paginator.page(paginator.num_pages)
        return render(request, "startPage.html", {"articlesFragments": articlesFragments})
    if request.method == "GET":
        paginator = Paginator(request.session['data'], 15)
        articlesFragments = request.GET.get('page')
        try:
            articlesFragments = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            articlesFragments = paginator.page(1)
        except EmptyPage:
            articlesFragments = paginator.page(paginator.num_pages)
        return render(request, "startPage.html", {"articlesFragments": articlesFragments})
