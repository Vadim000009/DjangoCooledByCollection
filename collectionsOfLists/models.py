from django.db import models


# Create your models here. Spok bro
class Student(models.Model):
    fstName = models.CharField("Student name", max_length=40)
    secName = models.CharField("Student surname", max_length=80)
    patronymic = models.CharField("Student patronymic", max_length=50)
    averageMark = models.FloatField("Average mark")

    def __str__(self):
        return str(self.fstName) + str(self.secName) + str(self.patronymic) + str(self.averageMark)
