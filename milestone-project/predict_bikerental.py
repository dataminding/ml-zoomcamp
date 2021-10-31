import numpy as np
import pickle
from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
import warnings

MODEL_LOCATION = "./models/milestone_model.pickle"

FEATURES = [
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

SEASONS = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
DAYS = {
    0: "sunday",
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
}
ALTERNATIVE_DAY_NAMES = [dy[:3] for dy in DAYS.values()]

warnings.filterwarnings("ignore")

app = Flask("bike_rental_predictor")

with open(MODEL_LOCATION, "rb") as mdp:
    model = pickle.load(mdp)


def validate_input_data(input_data):

    if not all([f in input_data.keys() for f in FEATURES]):
        raise Exception(
            f"one or more features of {FEATURES} are missing from the input {input_data}"
        )

    if (
        input_data["season"] not in SEASONS.values()
        and input_data["season"] not in SEASONS.keys()
    ):
        raise Exception(f"season should be one of {SEASONS}\n input data: {input_data}")

    if (
        input_data["weekday"] not in DAYS.values()
        and input_data["weekday"] not in DAYS.keys()
        and input_data["weekday"] not in ALTERNATIVE_DAY_NAMES
    ):
        raise Exception(
            f"weekday should be one of {DAYS} or {ALTERNATIVE_DAY_NAMES}\ninput data: {input_data}"
        )


def transform_input_data(input_data):

    transformed = input_data.copy()

    if input_data["season"] in SEASONS.values():
        transformed["season"] = [
            k for k, v in SEASONS.items() if input_data["season"] == v
        ][0]

    if input_data["weekday"].lower() in ALTERNATIVE_DAY_NAMES:
        transformed["weekday"] = [
            k for k, v in DAYS.items() if input_data["weekday"].lower() == v[:3]
        ][0]

    if input_data["weekday"].lower() in DAYS.values():
        transformed["weekday"] = [
            k for k, v in DAYS.items() if input_data["weekday"].lower() == v
        ][0]

    # normalization constants are given by the creator of the dataset
    transformed["temp"] = round(input_data["temp"] / 41, 4)
    transformed["atemp"] = round(input_data["atemp"] / 41, 4)
    transformed["hum"] = round(input_data["hum"] / 100, 4)
    transformed["windspeed"] = round(input_data["windspeed"] / 100, 4)

    # reordering the dict to correspond feature order of the trained model
    reordered = dict()
    for feat in FEATURES:
        reordered[feat] = transformed[feat]

    return transformed


def transform_predicted_data(cnt_rentals):
    return np.expm1(cnt_rentals)


@app.route("/predict", methods=["POST"])
def predict():
    request_data = request.get_json()
    validate_input_data(request_data)
    hourly_data = transform_input_data(request_data)

    X = pd.DataFrame.from_records(hourly_data, index=[0])
    predicted = model.predict(X)[0]
    transformed_predicted = round(transform_predicted_data(predicted), 2)

    return jsonify({"predicted_rentals_cnt": transformed_predicted})


@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"api_status": "alive"})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=9911)
