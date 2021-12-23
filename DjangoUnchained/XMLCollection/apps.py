import pickle
from django.apps import AppConfig


def loaderClassification():
    path, model = ".\DjangoUnchained\XMLCollection\ML\\", "Data.dat"
    try:
        Classification = pickle.load(open(path + model, 'rb'))
        print("Модель классификатора загружена!")
    except FileNotFoundError:
        print("Ошибка! Модель классификатора " + str(model) + " не найдена!\n"
                    "Классификатор работать не будет. Требуется перезапуск ")
        Classification = 0
    return Classification


load = loaderClassification()


class XmlcollectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'XMLCollection'
