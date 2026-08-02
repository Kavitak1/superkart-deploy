"""SuperKart sales-forecast Streamlit frontend."""
import os
import pandas as pd
import requests
import streamlit as st

# Backend base URL. Locally use the Flask container; in Codespaces/HF Spaces
# set BACKEND_URL to the forwarded backend URL (no trailing slash).
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:7860")

st.set_page_config(page_title="SuperKart Sales Forecast", page_icon="🛒", layout="centered")
st.title("🛒 SuperKart — Product Sales Revenue Forecast")
st.caption("Predict Product_Store_Sales_Total for a product-store combination.")

single_tab, batch_tab = st.tabs(["Single Prediction", "Batch Prediction"])

with single_tab:
    st.subheader("Online (single) inference")
    col1, col2 = st.columns(2)
    with col1:
        product_weight = st.number_input("Product Weight", 1.0, 50.0, 12.66, 0.01)
        product_mrp = st.number_input("Product MRP", 10.0, 500.0, 117.08, 0.01)
        product_area = st.number_input("Product Allocated Area", 0.0, 1.0, 0.027, 0.001, format="%.3f")
        store_age = st.number_input("Store Age (Years)", 0, 60, 16, 1)
        sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    with col2:
        id_char = st.selectbox("Product Id Char", ["FD", "NC", "DR"])
        type_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type",
                                  ["Departmental Store", "Supermarket Type1",
                                   "Supermarket Type2", "Food Mart"])

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": sugar,
            "Product_Allocated_Area": product_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": city,
            "Store_Type": store_type,
            "Product_Id_char": id_char,
            "Store_Age_Years": store_age,
            "Product_Type_Category": type_cat,
        }
        try:
            r = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=30)
            st.success(f"Predicted sales: {r.json()['prediction']}")
        except Exception as e:
            st.error(f"Request failed: {e}")

with batch_tab:
    st.subheader("Batch inference")
    st.write("Upload a CSV with the 10 feature columns to score many rows at once.")
    up = st.file_uploader("Upload CSV", type="csv")
    if up is not None and st.button("Predict Batch"):
        try:
            files = {"file": up.getvalue()}
            r = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files, timeout=60)
            preds = r.json()
            input_df = pd.read_csv(up)
            input_df["Predicted_Sales"] = [preds[str(i)] for i in range(len(input_df))]
            st.dataframe(input_df)
        except Exception as e:
            st.error(f"Request failed: {e}")
