import pickle
from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
import warnings

MODEL_FILEPATH = "capstone_model.pickle"
TRANSFORMER_FILEPATH = "capstone_transformer.pickle"

FEATURES_AND_DEFAULTS = {
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
    "title": "unknown",
    "telecommuting": 0,
    "has_company_logo": 0,
    "has_questions": 0,
}

warnings.filterwarnings("ignore")

app = Flask("fake_job_posting_detector")

with open(MODEL_FILEPATH, "rb") as mdp:
    model = pickle.load(mdp)

with open(TRANSFORMER_FILEPATH, "rb") as trp:
    transformer = pickle.load(trp)


def substitute_unknown_values(request_data):

    for feature, default in FEATURES_AND_DEFAULTS.items():
        if (
            feature not in request_data
            or len(str(request_data[feature])) < 1
            or request_data[feature] is None
        ):
            request_data[feature] = default
    return request_data


def transform_input_data(input_data):
    df = pd.DataFrame.from_records(data=[input_data], columns=FEATURES_AND_DEFAULTS)
    return transformer.transform(df)


@app.route("/detect", methods=["POST"])
def predict():
    request_data = request.get_json()

    subd_data = substitute_unknown_values(request_data)
    X = transform_input_data(subd_data)
    prediction = model.predict(X)[0]

    pred_str = "YES" if prediction == 1 else "NO"
    return jsonify(
        {"job_title": subd_data["title"], "is_job_posting_fraudlent": pred_str}
    )


@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"api_status": "alive"})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=9911)
