import pickle
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# raw = pd.read_csv(".\DjangoUnchained\XMLCollection\ML\\TFIDF.csv")
# svmClassifier = SVC()
# X = np.asarray(raw.values[:, 0:-1], dtype=np.float32)
# Y = np.empty(0, dtype=np.int8)
# for catName in raw['CATEGORY']:
#     if catName == 'коронавирус':
#         Y = np.append(Y, 0)
#     elif catName == 'религия':
#         Y = np.append(Y, 1)
#     elif catName == 'криминал':
#         Y = np.append(Y, 2)
# svmClassifier.fit(X, Y)
# pickle.dump(svmClassifier, open("modelSVM.dat", 'wb')
path = ".\DjangoUnchained\XMLCollection\ML\\"
model = "TFIDF.csv"
loadClassifier = pickle.load(open(path + model, 'rb'))
print(1)