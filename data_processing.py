import json
import ast
import pandas as pd
from typing import Dict
import re

def read_file(filename):
    with open(filename, 'r') as file:
        dataset = []
        for line in file:
            data = json.loads(line)
            dataset.append(data)
    return dataset

def categorize(dataset, label_set):
    data = {
        "trans_id": [],
        "pos": [],
        "nuc": [],
        "-1_len": [],
        "-1_std": [],
        "-1_mean": [],
        "0_len": [],
        "0_std": [],
        "0_mean": [],
        "+1_len": [],
        "+1_std": [],
        "+1_mean": [],
        "label": []
    }

    line_num = 0
    for line in dataset:
        line_num += 1
        for transcript, positions in line.items():
            for pos, nucleotide_dict in positions.items():
                label = label_set[line_num][-2]
                for nucleotide_seq, reads_list in nucleotide_dict.items():
                    for read in reads_list[0:1]:
                        data["trans_id"].append(transcript)
                        data["pos"].append(pos)
                        data["nuc"].append(nucleotide_seq)
                        data["-1_len"].append(read[0])
                        data["-1_std"].append(read[1])
                        data["-1_mean"].append(read[2])
                        data["0_len"].append(read[3])
                        data["0_std"].append(read[4])
                        data["0_mean"].append(read[5])
                        data["+1_len"].append(read[6])
                        data["+1_std"].append(read[7])
                        data["+1_mean"].append(read[8])
                        data["label"].append(label)

    return pd.DataFrame(data)

def main():
    filename = 'dataset0.json'
    dataset = read_file(filename)
    label_set = open("data.info.labelled", 'r').readlines()
    df = categorize(dataset, label_set)
    df.to_json('dataset0_processed_single_read.json', orient='records', lines=True)
    train_set = df.sample(frac=0.7, random_state=1)
    test_set = df.drop(train_set.index)

    train_set.to_json('train_set_1.json', orient='records', lines=True)
    test_set.to_json('test_set_1.json', orient='records', lines=True)


if __name__ == '__main__':
    main()