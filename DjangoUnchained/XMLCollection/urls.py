from django.urls import path
from django.views.generic import RedirectView

from . import views, viewsNLP


urlpatterns = [
    path("", views.getArticles, name="_article_list_"),             # Получить все статьи
    path('id=<int:any>', views.getArticle, name="_article_"),       # Получить определённую статью
    path('add', views.addArticle, name="_add_"),                    # Создать статью
    path('save', views.saveArticle, name="_save_"),                 # Сохранить статью
    path('delete', views.delArticle, name="_delete_"),              # Удалить статью
    path('search', views.search, name='_search_'),                  # Поиск статьи
    path('check', views.addArticleFromFile, name="_check_"),        # Сбор статей с диска
    path('learn', viewsNLP.learnNLP, name="_learn_"),               # Подготовка обучения
    path('study', viewsNLP.studyMLFromNLP, name="_study_"),         # Обучалочка
    path('exam=<int:any>', viewsNLP.MLclassif, name="_exam_"),      # Экзамен
    path('./static/images/favicon.ico', views.okay),
]