from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name=u"Заголовок")
    category = models.CharField(max_length=15, verbose_name=u"Категория")
    date = models.CharField(max_length=20, verbose_name=u"Дата публикации")
    text = models.CharField(max_length=16777215, null=True, blank=True, verbose_name=u"Текст статьи")
    tags = models.CharField(max_length=400, null=True, blank=True, verbose_name=u"Теги")
    keyWords = models.CharField(max_length=400, null=True, blank=True, verbose_name=u"Ключевые слова")
    url = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Ссылка")
    objects = models.Manager()

    #def __str__(self):
    #    return str(self.id) + self.title
