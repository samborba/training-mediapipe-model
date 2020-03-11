import os
import pickle
import pandas as pd
import numpy as np
from sklearn import neighbors
from sklearn.model_selection import train_test_split

DATA_FOLDER_PATH = os.path.abspath("data")
TRAINING_DATASET = DATA_FOLDER_PATH + "/" + "dataset.csv"
MODEL_BINARY_DESTINATION = os.path.abspath("src/model")

df = pd.read_csv(TRAINING_DATASET, index_col=False)

X = np.array(df.drop(['class'], 1))
y = np.array(df['class'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = neighbors.KNeighborsClassifier()
clf.fit(X_train, y_train)

knnPickle = open(MODEL_BINARY_DESTINATION + "/" + "knnclassifier_file", "wb")
pickle.dump(clf, knnPickle)
