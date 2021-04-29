from django.urls import path
from . import views


urlpatterns = [
    path('', views.listOfStudents, name='students'),
    path('', views.addStudentsToList, name='students'),
    path('', views.getAllStudents, name='students'),
]