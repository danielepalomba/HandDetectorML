import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib

dt = pd.read_csv('merged-dataset.csv')

X = dt.drop(['result'], axis = 1)
y = dt['result']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

cols = X_train.columns

scaler = MinMaxScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train = pd.DataFrame(X_train, columns=[cols])
X_test = pd.DataFrame(X_test, columns=[cols])

model = RandomForestClassifier(n_estimators=100 ,random_state= 42)
model.fit(X_train, y_train)
prediction = model.predict(X_test)

print('Training set score: {:.4f}'.format(model.score(X_train, y_train)))
print('Test set score: {:.4f}'.format(model.score(X_test, y_test)))

print('Accuracy score: {:.4f}'.format(accuracy_score(y_test, prediction)))

joblib.dump(model, 'model.joblib')
joblib.dump(scaler, 'scaler.joblib')