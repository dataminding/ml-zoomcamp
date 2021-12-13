import sys

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
import pickle

DIRECT_DOWNLOAD_URL = (
    "https://drive.google.com/uc?export=download&id=1VYo_Xb-RzwrHf0rcmpbMDcPSnRbdsqQn"
)
FILEPATH = "fake_job_postings.csv"
MODEL_FILEPATH = "capstone_model.pickle"
TRANSFORMER_FILEPATH = "capstone_transformer.pickle"
RANDOM_STATE = 444
NA_REPLACEMENTS = {
    "department": "unknown",
    "employment_type": "unknown",
    "salary_range": "unknown",
    "company_profile": "unknown",
    "description": "unknown",
    "requirements": "unknown",
    "benefits": "unknown",
    "required_education": "Unspecified",
    "required_experience": "Not Applicable",
    "country": "unknown",
    "state": "unknown",
    "city": "unknown",
    "function": "other",
    "industry": "unknown",
}


def download_and_save_data(url=DIRECT_DOWNLOAD_URL, filepath=FILEPATH):
    print(f"Downloading dataset from {url}...")
    resp = requests.get(url)
    resp.raise_for_status()
    with open(filepath, "w") as outf:
        outf.write(resp.content.decode("utf-8"))
        print(f"Dataset saved to {filepath}")


def load_and_preprocess(filepath=FILEPATH):
    print(f"Reading and preprocessing dataset...")

    df_raw = pd.read_csv(filepath, header=0)
    df_raw.drop("job_id", axis=1, inplace=True)
    df_raw.reset_index(drop=True, inplace=True)
    df_pre = df_raw.copy()
    df_pre[["country", "state", "city"]] = df_raw["location"].str.split(
        ",", n=2, expand=True
    )
    df_pre = df_pre.replace(r"^\s*$", "unknown", regex=True)
    df_pre.drop("location", axis=1, inplace=True)

    for col, replmnt in NA_REPLACEMENTS.items():
        df_pre[col].fillna(replmnt, inplace=True)
    print(f"Reading and preprocessing done.")
    return df_pre


def split_and_train(df):
    df_train, df_test = train_test_split(
        df, test_size=0.2, random_state=RANDOM_STATE, stratify=df["fraudulent"]
    )
    df_train.reset_index(drop=True, inplace=True)
    y_train = df_train.fraudulent
    df_train.drop("fraudulent", axis=1, inplace=True)

    col_transformations = [
        (
            "numerical",
            "passthrough",
            ["telecommuting", "has_company_logo", "has_questions"],
        ),
        (
            "categories",
            OneHotEncoder(dtype="int32"),
            ["employment_type", "required_experience", "required_education"],
        ),
        ("department", CountVectorizer(min_df=30, dtype="int32"), "department"),
        ("industry", CountVectorizer(min_df=30, dtype="int32"), "industry"),
        ("function", CountVectorizer(min_df=30, dtype="int32"), "function"),
        ("salary_range", CountVectorizer(min_df=20, dtype="int32"), "salary_range"),
        ("country", CountVectorizer(min_df=40, dtype="int32"), "country"),
        ("state", CountVectorizer(min_df=40, dtype="int32"), "state"),
        ("city", CountVectorizer(min_df=30, dtype="int32"), "city"),
        (
            "title",
            TfidfVectorizer(lowercase=True, stop_words="english", min_df=30),
            "title",
        ),
        (
            "company_profile",
            TfidfVectorizer(lowercase=True, stop_words="english", min_df=30),
            "company_profile",
        ),
        (
            "requirements",
            TfidfVectorizer(lowercase=True, stop_words="english", min_df=40),
            "requirements",
        ),
        (
            "description",
            TfidfVectorizer(lowercase=True, stop_words="english", min_df=50),
            "description",
        ),
        (
            "benefits",
            TfidfVectorizer(lowercase=True, stop_words="english", min_df=30),
            "benefits",
        ),
    ]
    print(f"Transforming dataframe...")

    transformer = ColumnTransformer(col_transformations, remainder="drop")
    transformer.fit(df_train)
    X_train = transformer.transform(df_train)

    dtclf = DecisionTreeClassifier(
        max_depth=27, min_samples_split=5, min_samples_leaf=1, random_state=RANDOM_STATE
    )
    print(f"Running training...")

    dtclf.fit(X_train, y_train)
    print(f"training done.")

    return dtclf, transformer


def save_model(model, model_path=MODEL_FILEPATH):
    with open(model_path, "wb") as pf:
        pickle.dump(model, pf)
        print(f"Model saved to {model_path}")

def save_transformer(transformer, path=TRANSFORMER_FILEPATH):
    with open(path, "wb") as pf:
        pickle.dump(transformer, pf)
        print(f"Transformer saved to {path}")


if __name__ == "__main__":

    assert (
        len(sys.argv) > 1
    ), "Please supply an integer flag (1 or 0) showing if you want to download the dataset or not"

    if len(sys.argv) == 3:
        model_filepath = sys.argv[1]
    else:
        model_filepath = MODEL_FILEPATH

    if bool(int(sys.argv[1])):
        download_and_save_data()
    df = load_and_preprocess(filepath=FILEPATH)
    model, transformer = split_and_train(df)
    save_model(model)
    save_transformer(transformer)
    print(f"train script finished.")