import os
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd

# Load dataset
def load_data():
    data = pd.read_csv('phishing.csv')
    print("Columns in dataset:", data.columns)
    
    X = data.drop('class', axis=1)  # Update 'class' if needed
    y = data['class']  # Target column ('class' or another)
    
    return X, y

# Store the results of the model's performance
ML_Model = []
accuracy = []
f1_score = []
recall = []
precision = []

def storeResults(model, a, b, c, d):
    ML_Model.append(model)
    accuracy.append(round(a, 3))
    f1_score.append(round(b, 3))
    recall.append(round(c, 3))
    precision.append(round(d, 3))

# Train the Decision Tree model
def train_model():
    # Load data
    X, y = load_data()
    
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Instantiate and train the Decision Tree model
    tree = DecisionTreeClassifier(max_depth=30)
    tree.fit(X_train, y_train)

    # Predict using the trained model
    y_train_tree = tree.predict(X_train)
    y_test_tree = tree.predict(X_test)

    # Compute metrics for training and test sets
    acc_train_tree = metrics.accuracy_score(y_train, y_train_tree)
    acc_test_tree = metrics.accuracy_score(y_test, y_test_tree)
    f1_score_train_tree = metrics.f1_score(y_train, y_train_tree)
    f1_score_test_tree = metrics.f1_score(y_test, y_test_tree)
    recall_score_train_tree = metrics.recall_score(y_train, y_train_tree)
    recall_score_test_tree = metrics.recall_score(y_test, y_test_tree)
    precision_score_train_tree = metrics.precision_score(y_train, y_train_tree)
    precision_score_test_tree = metrics.precision_score(y_test, y_test_tree)

    # Print metrics
    print("Decision Tree : Accuracy on training Data: {:.3f}".format(acc_train_tree))
    print("Decision Tree : Accuracy on test Data: {:.3f}".format(acc_test_tree))
    print()
    print("Decision Tree : f1_score on training Data: {:.3f}".format(f1_score_train_tree))
    print("Decision Tree : f1_score on test Data: {:.3f}".format(f1_score_test_tree))
    print()
    print("Decision Tree : Recall on training Data: {:.3f}".format(recall_score_train_tree))
    print("Decision Tree : Recall on test Data: {:.3f}".format(recall_score_test_tree))
    print()
    print("Decision Tree : precision on training Data: {:.3f}".format(precision_score_train_tree))
    print("Decision Tree : precision on test Data: {:.3f}".format(precision_score_test_tree))

    # Store results using the helper function
    storeResults('Decision Tree', acc_test_tree, f1_score_test_tree, recall_score_test_tree, precision_score_test_tree)

    # Create 'pickle' directory if it doesn't exist
    os.makedirs('pickle', exist_ok=True)
    
    # Save the trained model as a .pkl file
    with open('pickle/model.pkl', 'wb') as model_file:
        pickle.dump(tree, model_file)
    print("Model saved to pickle/model.pkl")

if __name__ == '__main__':
    train_model()
