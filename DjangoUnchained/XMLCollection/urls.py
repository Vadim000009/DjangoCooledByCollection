from django.urls import path
from . import views


urlpatterns = [
    path("", views.getArticles, name="_article_list_"),             # Получить все статьи
    path('id=<int:any>', views.getArticle, name="_article_"),       # Получить определённую статью
    path('add', views.addArticle, name="_add_"),                    # Создать статью
    path('save', views.saveArticle, name="_save_"),                 # Сохранить статью
    path('delete', views.delArticle, name="_delete_"),              # Удалить статью
    path('search', views.search, name='_search_'),                  # Поиск статьи
    path('check', views.addArticleFromFile, name="_check_"),        # Сбор статей с диска
]
