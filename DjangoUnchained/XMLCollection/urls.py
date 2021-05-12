from django.urls import path
from . import views


urlpatterns = [
    path("", views.getMoreArticles, name="_start_"),
    path('<str:any>.xml', views.getArticle, name="_article_"),
    path('change/add', views.addArticle, name="_add_"),
    path('change/save', views.save, name="_save_"),
    path('change/delete', views.delete, name="_delete_"),
]