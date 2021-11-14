import pickle

from django.apps import AppConfig


path = ".\DjangoUnchained\XMLCollection\ML\\"
model = "TFIDF.dat"
loadClassifier = pickle.load(open(path + model, 'rb'))
print("Classifer loaded!")


class XmlcollectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'XMLCollection'
