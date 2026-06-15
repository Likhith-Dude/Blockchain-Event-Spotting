import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

dataframe = pd.read_csv('dataset.csv')
dataframe_2 = dataframe.fillna(0)

df_train_y = dataframe_2['label']
df_train_X = dataframe_2.iloc[:, :20]

number = LabelEncoder()
df_train_X['proto'] = number.fit_transform(df_train_X['proto'].astype(str))
df_train_X['service'] = number.fit_transform(df_train_X['service'].astype(str))
df_train_X['state'] = number.fit_transform(df_train_X['state'].astype(str))

x_train, x_test, y_train, y_test = train_test_split(
    df_train_X, df_train_y, test_size=0.20, random_state=42
)

# Random Forest
rf = RandomForestClassifier(n_estimators=100)
rf.fit(x_train, y_train)
rf_prediction = rf.predict(x_test)
rf_accuracy = accuracy_score(y_test, rf_prediction) * 100
print(f"Random Forest Accuracy: {rf_accuracy:.2f}%")
print(classification_report(y_test, rf_prediction))

# Decision Tree
dt = DecisionTreeClassifier(criterion='gini', random_state=100, max_depth=3, min_samples_leaf=5)
dt.fit(x_train, y_train)
dt_prediction = dt.predict(x_test)
dt_accuracy = accuracy_score(y_test, dt_prediction) * 100
print(f"Decision Tree Accuracy: {dt_accuracy:.2f}%")
print(classification_report(y_test, dt_prediction))

# Gradient Boosting
gb = GradientBoostingClassifier(learning_rate=0.1)
gb.fit(x_train, y_train)
gb_prediction = gb.predict(x_test)
gb_accuracy = accuracy_score(y_test, gb_prediction) * 100
print(f"Gradient Boosting Accuracy: {gb_accuracy:.2f}%")
print(classification_report(y_test, gb_prediction))

# Naive Bayes
nb = GaussianNB()
nb.fit(x_train, y_train)
nb_prediction = nb.predict(x_test)
nb_accuracy = accuracy_score(y_test, nb_prediction) * 100
print(f"Naive Bayes Accuracy: {nb_accuracy:.2f}%")
print(classification_report(y_test, nb_prediction))

# K-Means Clustering
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(x_train)
kmeans_prediction = kmeans.predict(x_test)
print("K-Means cluster centers computed.")

# Confusion Matrix - Random Forest (best model)
cm = confusion_matrix(y_test, rf_prediction)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Random Forest - Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('confusion_matrix_rf.png')
plt.show()

# Accuracy comparison bar chart
model_names = ['Random Forest', 'Decision Tree', 'Gradient Boosting', 'Naive Bayes']
accuracies = [rf_accuracy, dt_accuracy, gb_accuracy, nb_accuracy]

plt.figure(figsize=(10, 6))
bars = plt.bar(model_names, accuracies, color=['#2196F3', '#4CAF50', '#FF9800', '#9C27B0'])
plt.ylabel('Accuracy (%)')
plt.title('ML Model Accuracy Comparison')
plt.ylim(0, 105)
for bar, acc in zip(bars, accuracies):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f'{acc:.2f}%', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('accuracy_comparison.png')
plt.show()
