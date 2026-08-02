# SuperKart — Sales Revenue Forecast (Deployment)

A decoupled forecasting service for SuperKart's product-store sales:

- **Backend** (`backend_files/`) — Flask REST API serving a serialized
  preprocessing + RandomForest pipeline (`superkart_model.joblib`). Port **7860**.
- **Frontend** (`frontend_files/`) — Streamlit UI with **Single** and **Batch**
  prediction tabs. Port **8501**. Calls the backend via the `BACKEND_URL` env var.

## Run it (GitHub Codespaces or local Docker)

```bash
docker compose up --build
```

- Frontend (Streamlit): http://localhost:8501
- Backend (API health): http://localhost:7860/

In a **Codespace**, open the **Ports** tab, set **7860** and **8501** to **Public**,
and use the forwarded URLs. The `.devcontainer/` config enables Docker and forwards
both ports automatically.

## API

| Method | Path               | Purpose                             |
|--------|--------------------|-------------------------------------|
| GET    | `/`                | Health check                        |
| POST   | `/v1/predict`      | Online (single) inference — JSON    |
| POST   | `/v1/predictbatch` | Batch inference — uploaded CSV file |

**Feature columns:** `Product_Weight`, `Product_Sugar_Content`,
`Product_Allocated_Area`, `Product_MRP`, `Store_Size`, `Store_Location_City_Type`,
`Store_Type`, `Product_Id_char`, `Store_Age_Years`, `Product_Type_Category`.

### Example — online inference

```bash
curl -X POST "http://localhost:7860/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"Product_Weight":12.66,"Product_Sugar_Content":"Low Sugar","Product_Allocated_Area":0.027,"Product_MRP":117.08,"Store_Size":"Medium","Store_Location_City_Type":"Tier 2","Store_Type":"Supermarket Type2","Product_Id_char":"FD","Store_Age_Years":16,"Product_Type_Category":"Non Perishables"}'
# -> {"prediction": 2897.97}
```

## Repository layout

```
.
├── docker-compose.yml        # runs backend + frontend together
├── .devcontainer/            # Codespaces: Docker + port forwarding
├── backend_files/            # Flask API, model, Dockerfile, requirements
└── frontend_files/           # Streamlit app, Dockerfile, requirements
```

See `DEPLOY.md` for full step-by-step deployment instructions.
