from django.urls import path
from . import views, viewsNLP


handler400 = "XMLCollection.views.custom_bad_request_view"
handler403 = "XMLCollection.views.custom_permission_denied_view"
handler404 = "XMLCollection.views.custom_page_not_found_view"
handler500 = "XMLCollection.views.custom_error_view"


urlpatterns = [
    path("", views.getArticles, name="_article_list_"),             # Получить все статьи
    path('id=<int:any>', views.getArticle, name="_article_"),       # Получить определённую статью
    path('add', views.addArticle, name="_add_"),                    # Создать статью
    path('save', views.saveArticle, name="_save_"),                 # Сохранить статью
    path('delete', views.delArticle, name="_delete_"),              # Удалить статью
    path('search', views.search, name='_search_'),                  # Поиск статьи
    path('check', views.addArticleFromFile, name="_check_"),        # Сбор статей с диска
    path('prepare', viewsNLP.preparedLearnNLP, name="_learn_"),     # Подготовка обучения
    path('study', viewsNLP.studyMLFromNLP, name="_study_"),         # Обучалочка
    path('exam=<int:any>', viewsNLP.MLclassif, name="_exam_"),      # Экзамен
]
