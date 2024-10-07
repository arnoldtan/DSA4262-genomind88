from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import pandas as pd

train = pd.read_json('train_set_1.json', orient='records', lines=True)
test = pd.read_json('test_set_1.json', orient='records', lines=True)

trainY = train['label']
trainX = train.loc[:, '-1_len':'+1_mean']
testY = test['label']
testX = test.loc[:, '-1_len':'+1_mean']

scalar = StandardScaler()
trainXScaled = scalar.fit_transform(trainX)
print(trainXScaled)

model = LogisticRegression(random_state=1)
model.fit(trainXScaled, trainY)

y_pred = model.predict(testX)