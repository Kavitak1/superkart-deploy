"""SuperKart sales-prediction Flask API (backend)."""
from flask import Flask, request, jsonify
import pandas as pd
import joblib

superkart_api = Flask("superkart_api")

# Load the serialized preprocessing + model pipeline once at startup
model = joblib.load("superkart_model.joblib")

# Exact feature columns the pipeline expects
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
    "Product_MRP", "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]


@superkart_api.get("/")
def home():
    return "SuperKart Sales Prediction API is running. Use POST /v1/predict or /v1/predictbatch."


@superkart_api.post("/v1/predict")
def predict():
    """Online inference: single JSON record -> single prediction."""
    data = request.get_json()
    input_df = pd.DataFrame([data])[FEATURES]
    prediction = float(model.predict(input_df)[0])
    return jsonify({"prediction": round(prediction, 2)})


@superkart_api.post("/v1/predictbatch")
def predict_batch():
    """Batch inference: uploaded CSV file -> one prediction per row."""
    file = request.files["file"]
    input_df = pd.read_csv(file)[FEATURES]
    predictions = model.predict(input_df)
    result = {str(i): round(float(p), 2) for i, p in enumerate(predictions)}
    return jsonify(result)


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)
