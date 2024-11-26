import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
import numpy  as np
import pickle
import csv

filename = './generate_dataset/dataset/dataset.csv'

def main():
    
    X,Y = load_data(filename)   
    X = np.array(X)
    y = np.array(Y)

    X_training, X_testing, y_training, y_testing = train_test_split(
    X, Y, test_size=0.4,random_state=42
    )

    models = ['gaussianNB','gbc','knn','randomforest','svc']
    # models = ['svc']
    for model_name in models:
        model = train_model(X_training,y_training,model_name)
        save_model(f'./saved_models/{model_name}.pkl',model)
        predictions = model.predict(X_testing)
        accuracy = accuracy_score(y_testing, predictions)
        print("Accuracy:", accuracy)


def save_model(filename,model):
    print("\nSaving Model...")
    with open(filename,'wb') as f:
        pickle.dump(model,f)
    print("Model saved in:",filename)

def load_model(filename):
    print("Loading Model: ",filename)
    with open(filename,'rb') as f:
        model =  pickle.load(filename)
    print("Model Loaded")
    return model
      
def load_data(filename):
    data = []
    labels = []
    print("Loading data...")
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            # print(line[:-1],line[-1])
            data.append([float(cell) for cell in line[:-1]])  # Features
            labels.append(int(line[-1]))  # Label
    
    return data,labels

def train_model(evidence, labels, model_name):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    if model_name == "knn":
        model = KNeighborsClassifier(n_neighbors=1)
    if model_name == "randomforest":
        model = RandomForestClassifier(n_estimators=100)
    if model_name == "svc":
        model = svm.SVC(probability=True)
    if model_name == "gbc":
        model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    if model_name == "gaussianNB":
        model = GaussianNB()
    print('\nTraining Model:',model_name)
    model.fit(evidence,labels)
    return model

if __name__ == "__main__":
    main()
# print(X,Y)
