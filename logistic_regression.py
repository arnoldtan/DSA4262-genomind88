from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd

train = pd.read_json('train_set_1.json', orient='records', lines=True)
test = pd.read_json('test_set_1.json', orient='records', lines=True)

trainY = train['label']
trainX = train['-1_len':'+1_mean']
testY = test['label']
testX = test['-1_len':'+1_mean']

scalar = StandardScaler()
scalar.fit_transform()

model = LogisticRegression(random_state=1)
model.fit(trainX, trainY)

y_pred = model.predict(testX)