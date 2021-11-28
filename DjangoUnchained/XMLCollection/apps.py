import pickle
from django.apps import AppConfig


def loaderClassification():
    path, model = ".\DjangoUnchained\XMLCollection\ML\\", "Data.dat"
    Classification = pickle.load(open(path + model, 'rb'))
    print("Classificator loaded!")
    return Classification


load = loaderClassification()


class XmlcollectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'XMLCollection'
