import json
import pandas as pd
import joblib
import xgboost
from sklearn.preprocessing import StandardScaler
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

def parser():
    parser = ArgumentParser(description="Script to output m6a RNA modification from dataset and model path")
    parser.add_argument("--dataset", type=dataset_check, required=True, help="Path to the dataset file, json format. Example: 'dataset1.json' or 'data/example.json'")
    parser.add_argument("--model", type=model_check, required=True, help="Path to the model file, joblib type. Example: 'model.joblib' or 'model/example.joblib'")
    parser.add_argument("--output", type=str, required=False, default="output.csv", help="Optional, output file name in csv format. Default: 'output.csv'")

    return parser.parse_args()

def dataset_check(path: str):
    path = Path(path)
    if not path.exists():
        raise Exception("Dataset path does not exist.")
    elif path.suffix != ".json":
        raise Exception("Dataset file extension must be .json.")
    return path
    
def model_check(path: str):
    path = Path(path)
    if not path.exists():
        raise Exception("Model path does not exist.")
    elif path.suffix != ".joblib":
        raise Exception("Dataset file extension must be .joblib.")
    return path

def read_file(filepath):
    with open(filepath, 'rt', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    return data

def data_processing(rna_data):
    rows = []
    for entry in rna_data:
        for transcript_id, positions in entry.items():
            for position, nucleotides in positions.items():
                for nucleotide, features in nucleotides.items():
                    for feature_set in features:
                        row = [transcript_id, position, nucleotide] + feature_set
                        rows.append(row)
    return rows

def main():
    args = parser()
    dataset_path = args.dataset
    model_path = args.model
    output_name = args.output

    model = joblib.load(model_path)
    xgb_model = model['xgb_model']
    scaler = model['scaler']

    rna_data = read_file(dataset_path)
    rows = data_processing(rna_data)

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

    scaler = StandardScaler()
    X_test = grouped_df.iloc[:, 3:48]  
    X_test_scaled = scaler.fit_transform(X_test)
    print("Data Processing finished.")

    output = grouped_df[['transcript_id','position']]
    output = output.rename(columns={'position': 'transcript_position'})

    scores = []
    for i in tqdm(range(len(X_test_scaled)), desc="Generating Predictions"):
        prediction_score = xgb_model.predict_proba(X_test_scaled[i:i+1])[:, 1]
        scores.append(prediction_score[0])
        
    output['score'] = scores
    output.to_csv(output_name, index=False)
    print("Process finished.")

if __name__ == '__main__':
    main()