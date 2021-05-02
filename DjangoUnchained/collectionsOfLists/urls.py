from django.urls import path
from . import views


urlpatterns = [
    path('', views.viewPageList, name='_ViewPageList_'),
    path('addStudPage/', views.viewPageAdditional, name='_ViewPageAdd_'),
    path('add/', views.addStudent, name='_addStudent_'),
    path('get/', views.getStudent, name='_getStudent_'),
]
