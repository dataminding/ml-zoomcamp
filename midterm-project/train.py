import sys

import requests
import shutil
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from datetime import datetime
import uuid

RANDOM_STATE = 111
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"
FILENAME = URL.split("/")[-1]
DATA_FOLDER = "data"
MODEL_FOLDER = "models"
CSV_FILEPATH = os.path.join(DATA_FOLDER, "hour.csv")


def download_data(url=URL, folder=DATA_FOLDER):
    csv_filename = "hour.csv"
    local_filepath_zip = os.path.join(DATA_FOLDER, FILENAME)
    local_filepath_hourly_csv = os.path.join(DATA_FOLDER, csv_filename)

    print(f"Downloading zipped data from {url}...")
    resp = requests.get(URL)
    resp.raise_for_status()

    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(local_filepath_zip, "wb") as zipin:
        zipin.write(resp.content)
    print(f"\tFile saved under {local_filepath_zip}. Decompressing file..")
    shutil.unpack_archive(local_filepath_zip, extract_dir=folder)
    if csv_filename in os.listdir(folder):
        print(f"\tFile can be found under {local_filepath_hourly_csv}")
        return local_filepath_hourly_csv
    else:
        raise Exception(f"Error while getting or decompressing source data")


def calculate_rmse(y_val, y_pred):
    return round(mean_squared_error(y_val, y_pred, squared=False), 3)


def train_model(source_filepath):

    features = [
        "season",
        "mnth",
        "hr",
        "holiday",
        "weekday",
        "workingday",
        "weathersit",
        "temp",
        "atemp",
        "hum",
        "windspeed",
    ]
    perf_metrics = list()

    overall_best_rmse = 1000000

    # reading the data
    df = pd.read_csv(source_filepath, header=0)

    df["cnt"] = np.log1p(df.cnt)

    # creating train/test datasets
    df_train, df_test = train_test_split(df, test_size=0.3, random_state=RANDOM_STATE)

    df_train = df_train.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    X_train = df_train[features]
    y_train = df_train.cnt

    X_val = df_test[features]
    y_val = df_test.cnt

    def run_ridge_experiment(alpha):
        ridge = Ridge(alpha=alpha, random_state=RANDOM_STATE)

        ridge.fit(X_train, y_train)

        y_pred_rdg = ridge.predict(X_val)

        return calculate_rmse(y_val, y_pred_rdg), ridge

    def run_lasso_experiment(alpha):
        lasso = Lasso(alpha=alpha, random_state=RANDOM_STATE)
        lasso.fit(X_train, y_train)

        y_pred_lss = lasso.predict(X_val)

        return calculate_rmse(y_val, y_pred_lss), lasso

    # using the sklearn defaults for min_samples_split and min_samples_lead
    def run_treeregressor_experiment(
        max_depth, min_samples_split=2, min_samples_leaf=1
    ):
        trgr = DecisionTreeRegressor(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=RANDOM_STATE,
        )
        trgr.fit(X_train, y_train)
        y_pred_trgr = trgr.predict(X_val)
        return calculate_rmse(y_val, y_pred_trgr), trgr

    def run_rfr_experiment(max_depth, min_samples_split=2, min_samples_leaf=1):
        rfr = RandomForestRegressor(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )
        rfr.fit(X_train, y_train)
        y_pred_rfr = rfr.predict(X_val)
        return calculate_rmse(y_val, y_pred_rfr), rfr

    print(f"Starting training experiments..........\n\t ......linear regression......")
    # training linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred_lre = model.predict(X_val)

    rmse_lre = calculate_rmse(y_val, y_pred_lre)
    perf_metrics.append(
        {"model_name": str(model), "model": model, "tuning": None, "rmse": rmse_lre}
    )
    if rmse_lre < overall_best_rmse:
        overall_best_rmse = rmse_lre
    print(f"\tlinear regression, RMSE: {rmse_lre}")

    print(f"\n...........Ridge...........")
    alphas = [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.5, 0.6, 1]
    for a in alphas:
        rmse, ridge = run_ridge_experiment(a)
        if rmse < overall_best_rmse:
            overall_best_rmse = rmse
        print(f"\tRidge, alpha={a} : RMSE: {rmse}")
        perf_metrics.append(
            {
                "model_name": str(ridge),
                "model": ridge,
                "tuning": {"alpha": a},
                "rmse": rmse,
            }
        )

    print(f"\n...........Lasso...........")
    # Lasso with alpha==0 would be LinearRegression
    for a in [a for a in alphas if a > 0]:
        res, lasso = run_lasso_experiment(a)
        if res < overall_best_rmse:
            overall_best_rmse = res
        print(f"\tLasso, alpha={a} : RMSE: {res}")
        perf_metrics.append(
            {
                "model_name": str(lasso),
                "model": lasso,
                "tuning": {"alpha": a},
                "rmse": res,
            }
        )

    print(f"\n...........Decision tree regressor...........\n\t\ttuning max_depth....")
    depths = range(1, 15)
    min_splits = [2, 3, 5, 10, 15, 50, 100, 150, 200]
    min_leafs = [1, 5, 10, 15, 20, 50, 100, 200]

    best_rmse = 10000
    best_depth = None
    for d in depths:
        _rmse, _model = run_treeregressor_experiment(max_depth=d)
        if _rmse < best_rmse:
            best_rmse = _rmse
            best_depth = d
            if _rmse < overall_best_rmse:
                overall_best_rmse = _rmse
        print(f"\tDecisionTreeRegressor, max_depth={d} : RMSE: {_rmse}")
        perf_metrics.append(
            {
                "model_name": str(_model),
                "model": _model,
                "tuning": {"max_depth": d},
                "rmse": _rmse,
            }
        )

    print("\t\ttuning min_samples_split....")
    for s in min_splits:
        _rmse, _mdl = run_treeregressor_experiment(max_depth=10, min_samples_split=s)
        if _rmse < best_rmse:
            best_rmse = _rmse
            best_mss = s
            if _rmse < overall_best_rmse:
                overall_best_rmse = _rmse
        tuning_params = {"max_depth": 10, "min_samples_split": s}
        print(f"\tDecisionTreeRegressor, {tuning_params} : RMSE: {_rmse}")
        perf_metrics.append(
            {
                "model": _mdl,
                "model_name": str(_mdl),
                "tuning": tuning_params,
                "rmse": _rmse,
            }
        )

    print("\t\ttuning min_samples_leaf....")
    best_msl = None

    for l in min_leafs:
        _rmse, _mdlml = run_treeregressor_experiment(
            max_depth=10, min_samples_split=15, min_samples_leaf=l
        )
        if _rmse < best_rmse:
            best_rmse = _rmse
            best_msl = l
            if _rmse < overall_best_rmse:
                overall_best_rmse = _rmse
        tuning = {"max_depth": 10, "min_samples_split": 15, "min_samples_leaf": l}
        print(f"\tDecisionTreeRegressor, {tuning} : RMSE: {_rmse}")
        perf_metrics.append(
            {
                "model": _mdlml,
                "model_name": str(_mdlml),
                "tuning": tuning,
                "rmse": _rmse,
            }
        )

    print(f"\n...........Random forest regressor...........\n\t\ttuning max_depth....")
    depths = range(1, 25)
    min_splits = [2, 3, 5, 10, 15, 50, 100, 150, 200]
    min_leafs = [1, 5, 10, 15, 20, 50, 100, 200]

    best_rmse_rfr = 10000
    best_depth_rfr = None
    for d in depths:
        _rmse, _rfr = run_rfr_experiment(max_depth=d)
        if _rmse < best_rmse_rfr:
            best_rmse_rfr = _rmse
            best_depth_rfr = d
            if _rmse < overall_best_rmse:
                overall_best_rmse = _rmse
        print(f"RandomForestRegressor, max_depth={d} : RMSE: {_rmse}")
        perf_metrics.append(
            {
                "model_name": str(_rfr),
                "model": _rfr,
                "tuning": {"max_depth": d},
                "rmse": _rmse,
            }
        )

    print(f"\t\t best max_depth value: {best_depth_rfr} with RMSE of {best_rmse_rfr}")
    print("\t\ttuning min_samples_leaf....")
    best_rmse_rfr2 = 10000
    best_msl_rfr = -1
    best_depth_rfr2 = 111111

    for ml in min_leafs:
        for depth in [16, 18, 19, 22]:
            _rmse, _rf = run_rfr_experiment(max_depth=depth, min_samples_leaf=ml)
            if _rmse < best_rmse_rfr2:
                best_rmse_rfr2 = _rmse
                best_depth_rfr2 = depth
                best_msl_rfr = ml
                if _rmse < overall_best_rmse:
                    overall_best_rmse = _rmse
            tuning = {"max_depth": depth, "min_samples_leaf": ml}
            print(f"RandomForestRegressor, {tuning} , RMSE: {_rmse}")
            perf_metrics.append(
                {"model_name": str(_rf), "model": _rf, "tuning": tuning, "rmse": _rmse}
            )
    print(
        f"\n\t best result: max_depth={best_depth_rfr2}, min_samples_leaf={best_msl_rfr} ,RMSE= {best_rmse_rfr2}"
    )

    print("\t\ttuning min_samples_split....")
    best_rmse_rfr_mss = 10000
    best_mss = -1
    best_depth_mss = 111111

    for ms in min_splits:
        _rmse, _rrr = run_rfr_experiment(
            max_depth=22, min_samples_split=ms, min_samples_leaf=1
        )
        if _rmse < best_rmse_rfr_mss:
            best_rmse_rfr_mss = _rmse
            best_mss = ms
            if _rmse < overall_best_rmse:
                overall_best_rmse = _rmse
        tuning = {"max_depth": 22, "min_samples_leaf": 1, "min_samples_split": ms}
        print(f"RandomForestRegressor, {tuning} , RMSE: {_rmse}")
        perf_metrics.append(
            {"model": _rrr, "model_name": str(_rrr), "tuning": tuning, "rmse": _rmse}
        )
    print(f"\n\t best result: min_samples_split={best_mss} ,RMSE= {best_rmse_rfr_mss}")

    print(f"............selecting the best model..........")
    print(
        f"the following models have the lowest RMSE. Returning the first one in the list as best model..."
    )
    df_perf = pd.DataFrame.from_dict(perf_metrics)
    df_perf = df_perf[df_perf.rmse == overall_best_rmse]
    df_best_models = df_perf.sort_values(by="rmse", ascending=True)
    print(df_best_models[["model_name", "tuning", "rmse"]])

    return df_best_models["model"].head(1)


def export_model(model, model_folder, model_filename):
    model_filepath = os.path.join(os.getcwd(), model_folder, f"{model_filename}.pickle")

    os.makedirs(model_folder, exist_ok=True)
    with open(model_filepath, "wb") as modelfile:
        pickle.dump(model, modelfile)

    print(f"Model saved to {model_filepath}")

    return model_filepath


if __name__ == "__main__":
    model_folder = MODEL_FOLDER

    if len(sys.argv) == 2:
        model_filename = sys.argv[1]
    else:
        model_filename = (
            f"{datetime.utcnow().strftime('%Y%m%dT%H%M')}_{uuid.uuid1().hex[:8]}"
        )

    download_data()

    best_model = train_model(CSV_FILEPATH)

    export_model(best_model, model_folder, model_filename)
