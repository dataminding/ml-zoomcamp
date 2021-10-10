import pickle
from flask import Flask, request, jsonify
import os

ENV = os.getenv("ENV", "local").lower()

"""The base Docker image used for Q6 contains the model and the transformer already, 
    while for Q3-Q4 belongs an other model and I stored the transformer and model in a dedicated folder"""
if ENV == "docker":
    base_path = "."
    with open(f"{base_path}/model2.bin", "rb") as modf:
        model = pickle.load(modf)

else:
    base_path = "models-transformers"
    with open(f"{base_path}/model1.bin", "rb") as modf:
        model = pickle.load(modf)

with open(f"{base_path}/dv.bin", "rb") as dvf:
        dv = pickle.load(dvf)


app = Flask('churn')

@app.route('/predict', methods=['POST'])
def predict_churn():
    customer = request.get_json()
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)
    churn = y_pred[0, 1]
    churn_bool = bool(churn>=0.5)

    return jsonify({
        "churn_probability": float(churn),
        "churn_decision": churn_bool
    })




