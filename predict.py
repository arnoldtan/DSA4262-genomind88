import gzip
import json
import pandas as pd
import joblib

model = joblib.load('model.joblib')
xgb_model = model['xgb_model']
scaler = model['scaler']

dataset = 'dataset1.json.gz'

with gzip.open(dataset, 'rt', encoding='utf-8') as f:
    rna_data = [json.loads(line) for line in f]

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

X_test = grouped_df.iloc[:, 3:48]  
X_test_scaled = scaler.transform(X_test)

output = grouped_df[['transcript_id','position']]
output = output.rename(columns={'position': 'transcript_position'})
output['score'] = xgb_model.predict_proba(X_test_scaled)[:, 1]
output.to_csv('output.csv', index=False)