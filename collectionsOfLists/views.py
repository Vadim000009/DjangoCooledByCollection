from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here. Ok
def listOfStudents(request):
    return HttpResponse("OK")


def getAllStudents(request):
    return HttpResponse("OK")


def addStudentsToList(request):
    return HttpResponse("OK")

