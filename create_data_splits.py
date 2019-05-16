# coding: utf-8

from sklearn.model_selection import train_test_split
import pandas as pd

DATASET_LABELS={
        "clarin": "Clarin", 
        "semeval": "SemEval", 
        "airline": "Airline", 
        "gop_debate": "GOP", 
        "hcr": "Healthcare", 
        "obama_debate": "Obama", 
        }

df = pd.read_csv("./data/joined_data_all.txt", sep="\t")
print(df.shape)

df.dataset = df.dataset.apply(lambda x: DATASET_LABELS[x])
print(df.dataset.value_counts())

for dataset in df.dataset.unique():
    if dataset in {"SemEval", "Healthcare"}:
        print(dataset, "skipping")
        continue
    df_t = df[(df.dataset == dataset) & (df.language == "english")]
    df_train, df_test = train_test_split(df_t, test_size=0.2, random_state=1337, stratify=df_t.label)
    df_train, df_dev = train_test_split(df_train, test_size=0.1, random_state=1337, stratify=df_train.label)
    df.loc[df_train.index, "datasplit"] = "train"
    df.loc[df_dev.index, "datasplit"] = "dev"
    df.loc[df_test.index, "datasplit"] = "test"
    print(dataset, df_train.shape, df_dev.shape, df_test.shape)
    
df_t = df[(df.language == "english")].pivot_table(index="dataset", columns="datasplit", values="tid", aggfunc=len)
print(df_t)
df_t = df[(df.language == "english")].pivot_table(index="dataset", columns=["datasplit", "label"], values="tid", aggfunc=len)
print(df_t)
df.to_csv("./data/data_with_train_dev_test_split.txt", sep="\t", index=False)
