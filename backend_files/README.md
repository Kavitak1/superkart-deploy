---
title: SuperKart Backend API
emoji: 🛒
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# SuperKart — Sales Prediction API (Backend)

A Flask REST API that serves the serialized SuperKart model
(`superkart_model.joblib`, a preprocessing + RandomForest pipeline).

## Endpoints

| Method | Path                | Purpose                              |
|--------|---------------------|--------------------------------------|
| GET    | `/`                 | Health check                         |
| POST   | `/v1/predict`       | Online (single) inference — JSON     |
| POST   | `/v1/predictbatch`  | Batch inference — uploaded CSV file  |

## Expected feature columns

`Product_Weight`, `Product_Sugar_Content`, `Product_Allocated_Area`,
`Product_MRP`, `Store_Size`, `Store_Location_City_Type`, `Store_Type`,
`Product_Id_char`, `Store_Age_Years`, `Product_Type_Category`

## Example — online inference

```bash
curl -X POST "$BACKEND_URL/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"Product_Weight":12.66,"Product_Sugar_Content":"Low Sugar",
       "Product_Allocated_Area":0.027,"Product_MRP":117.08,
       "Store_Size":"Medium","Store_Location_City_Type":"Tier 2",
       "Store_Type":"Supermarket Type2","Product_Id_char":"FD",
       "Store_Age_Years":16,"Product_Type_Category":"Non Perishables"}'
# -> {"prediction": 2897.97}
```

## Run locally

```bash
docker build -t superkart-backend .
docker run -d -p 7860:7860 superkart-backend
```

The container listens on port **7860** (the standard Hugging Face Spaces port).
