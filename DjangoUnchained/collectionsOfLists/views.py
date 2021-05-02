from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .models import Student


# Create your views here. Ok
def viewPageList(request):
    queryRequest = Student.objects.all()
    return render(request, "templates/list.html", {"student": queryRequest})


def viewPageAdditional(request):
    return render(request, "templates/additional.html")


def getStudent(request):
    queryResponse = {}
    for student in Student.objects.all():
        queryResponse.setdefault(str(student.averageMark), Student.__str__(student))
    return HttpResponse(str(queryResponse).encode("utf-8"))


def addStudent(request):
    if request.method == 'POST':
        fstName = request.POST.get("fstNameInput")
        secName = request.POST.get("secNameInput")
        patronymic = request.POST.get("patronymicInput")
        averageMark = request.POST.get("markInput")
        if (fstName or secName or patronymic or averageMark) == '':
            messages.error(request, 'Incorrect Data')
            return render(request, "templates/addStudent.html")
        else:
            print(fstName + secName + patronymic + averageMark)
            god = Student(fstName=fstName, secName=secName, patronymic=patronymic,
                          averageMark=averageMark)
            god.save()
            messages.info(request, 'Successful send to Server')
            return render(request, "templates/additional.html")
    else:
        return HttpResponse(status=500)
