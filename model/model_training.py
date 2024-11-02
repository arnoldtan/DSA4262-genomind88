dataset = 'dataset0.json.gz'
labels = 'data.info.labelled'


import gzip
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import joblib


with gzip.open(dataset, 'rt', encoding='utf-8') as f:
    rna_data = [json.loads(line) for line in f]

labels_df = pd.read_csv(labels, header=None, names=['gene_id', 'transcript_id', 'transcript_position', 'label'])

rows = []

for entry in rna_data:
    for transcript_id, positions in entry.items():
        for position, nucleotides in positions.items():
            for nucleotide, features in nucleotides.items():
                for feature_set in features:
                    row = [transcript_id, position, nucleotide] + feature_set
                    rows.append(row)

columns = ['transcript_id', 'position', 'nucleotide'] + [f'feature_{i+1}' for i in range(9)]  
rna_df = pd.DataFrame(rows, columns=columns)

agg_funcs = {
    'feature_1': ['mean', 'median', 'min', 'max', 'std'],
    'feature_2': ['mean', 'median', 'min', 'max', 'std'],
    'feature_3': ['mean', 'median', 'min', 'max', 'std'],
    'feature_4': ['mean', 'median', 'min', 'max', 'std'],
    'feature_5': ['mean', 'median', 'min', 'max', 'std'],
    'feature_6': ['mean', 'median', 'min', 'max', 'std'],
    'feature_7': ['mean', 'median', 'min', 'max', 'std'],
    'feature_8': ['mean', 'median', 'min', 'max', 'std'],
    'feature_9': ['mean', 'median', 'min', 'max', 'std'],
}


grouped_df = rna_df.groupby(['transcript_id', 'position','nucleotide']).agg(agg_funcs)
grouped_df.columns = [f"{feature}_{stat}" for feature, stat in grouped_df.columns]
grouped_df.reset_index(inplace=True)
final_df = grouped_df.merge(labels_df, left_on=['transcript_id', 'position'], right_on=['transcript_id', 'transcript_position'], how='left')

#gene based split
unique_genes = final_df['gene_id'].unique()
train_genes, test_genes = train_test_split(unique_genes, test_size=0.2, random_state=42)

train_df = final_df[final_df['gene_id'].isin(train_genes)]
test_df = final_df[final_df['gene_id'].isin(test_genes)]

# Features and labels for training
X_train = train_df.iloc[:, 3:48]
y_train = train_df['label']

# Features and labels for testing
X_test = test_df.iloc[:, 3:48]
y_test = test_df['label']

y_train = y_train.astype(int)  
y_test = y_test.astype(int) 

# Scale the features 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SMOTE
X_train_smote, y_train_smote = SMOTE(random_state=42).fit_resample(X_train_scaled, y_train)

xgb_model = xgb.XGBClassifier(
    objective='binary:logistic',   
    eval_metric='logloss',         
    random_state=42,               
    colsample_bytree=1.0,           
    gamma=0,                        
    learning_rate=0.2,              
    max_depth=7,                    
    min_child_weight=1,             
    n_estimators=300,               
    subsample=0.8                   
)

#cross-validation
cv_scores = cross_val_score(xgb_model, X_train_smote, y_train_smote, cv=5, scoring='average_precision')

# Display the mean and standard deviation of cross-validation
print(f'Mean PR AUC for 5-fold CV: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')

# Fit the model on the training data
xgb_model.fit(X_train_smote, y_train_smote)


model = {
    'xgb_model': xgb_model,
    'scaler': scaler
}

joblib.dump(model, 'model.joblib')