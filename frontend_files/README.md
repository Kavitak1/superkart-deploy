---
title: SuperKart Sales Forecast
emoji: 🛒
colorFrom: green
colorTo: blue
sdk: docker
app_port: 8501
pinned: false
---

# SuperKart — Sales Revenue Forecast (Frontend)

A Streamlit app that calls the SuperKart Flask backend for
**online (single)** and **batch** sales predictions.

## Configuration

The app reads the backend base URL from the `BACKEND_URL` environment
variable (no trailing slash). Set it to your **public backend Space URL**:

- In the Space UI: **Settings → Variables and secrets → New variable**
  - Name: `BACKEND_URL`
  - Value: `https://<your-user>-superkart-backend.hf.space`

If unset, it defaults to `http://localhost:7860` (useful for local runs).

## Features

- **Single Prediction** tab — fill the product/store form → get an instant forecast.
- **Batch Prediction** tab — upload a CSV of the 10 feature columns → get a
  predictions table.

## Run locally (against a local backend)

```bash
docker build -t superkart-frontend .
docker run -d -p 8501:8501 -e BACKEND_URL=http://host.docker.internal:7860 superkart-frontend
```

The container listens on port **8501**.
