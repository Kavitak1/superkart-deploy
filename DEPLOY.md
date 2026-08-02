# SuperKart — Deployment Guide

Two decoupled services, wired together by `docker-compose.yml`:

- **Backend** (`backend_files/`) — Flask REST API + serialized model, port **7860**
- **Frontend** (`frontend_files/`) — Streamlit UI, port **8501**, calls the backend via `BACKEND_URL`

> **Note on Hugging Face Spaces:** as of 2026, HF only hosts **Docker/Gradio/Streamlit**
> Spaces on the **PRO** tier (free accounts get *Static* Spaces only, which can't run a
> model). So we deploy on **GitHub Codespaces**, which is free and matches the rubric's
> *"forwarded URL"* requirement. (If you have HF PRO, see Option B.)

---

## Option A — GitHub Codespaces (free, recommended)

### 1. Put these files in a GitHub repository

You need `backend_files/`, `frontend_files/`, `docker-compose.yml`, and `.devcontainer/`
in a GitHub repo. Easiest via the web:

1. Go to https://github.com/new → create a repo, e.g. **`superkart-deploy`** (Public is fine).
2. On the new repo page, click **uploading an existing file**.
3. From your machine, open the `superkart_project/` folder and drag in:
   - the `backend_files/` folder (includes `superkart_model.joblib`)
   - the `frontend_files/` folder
   - `docker-compose.yml`
   - the `.devcontainer/` folder (contains `devcontainer.json`)
4. Commit the upload.

> The 29 MB model uploads fine through the GitHub web uploader (limit is 100 MB/file).

### 2. Open a Codespace

On the repo page: **Code ▾ → Codespaces → Create codespace on main**.
Wait for it to build (the devcontainer enables Docker and forwards ports 7860 & 8501).

### 3. Build and run both containers

In the Codespace terminal:

```bash
docker compose up --build
```

Leave it running. You'll see the Flask backend start on 7860 and Streamlit on 8501.

### 4. Make the ports public and grab the forwarded URLs

Open the **Ports** tab (bottom panel of the Codespace):

1. Right-click **port 7860** → **Port Visibility → Public**. Copy its **forwarded URL**
   (looks like `https://<name>-7860.app.github.dev`). **This is your backend URL.**
2. Do the same for **port 8501** — that's your **frontend (Streamlit) URL**; open it to use the app.

### 5. Test it

- Open the **8501** URL → use the **Single Prediction** and **Batch Prediction** tabs.
- Or hit the backend directly:

```bash
curl https://<name>-7860.app.github.dev/
# -> "SuperKart Sales Prediction API is running..."
```

---

## Option B — Hugging Face Spaces (only if you have PRO)

Each folder already contains `app.py`, `requirements.txt`, `Dockerfile`, and a `README.md`
with the required `sdk: docker` frontmatter. With a PRO account:

```bash
# from superkart_project/  (uses the project venv)
export HF_TOKEN=hf_...your_write_token...
export HF_USER=your-hf-username
./.venv/bin/python push_to_hf.py both
```

Then in the **frontend Space → Settings → Variables and secrets** add
`BACKEND_URL = https://<user>-superkart-backend.hf.space` (no trailing slash).

---

## Final step — record the URLs in the notebook, then re-export HTML

1. Open `SuperKart_Full_Code_Solution.ipynb` → *"Pushing Deployment Files"* section and
   replace the placeholders with your **public** URLs:
   - backend → the **7860** forwarded URL (or backend Space URL)
   - frontend → the **8501** forwarded URL (or frontend Space URL)
2. *(Optional but recommended)* In the *"Inferencing using the Flask API"* section, set
   `model_root_url` to your **public backend URL** to demonstrate online + batch inference
   against the live deployment (instead of the local backend used in the executed run).
3. Re-export the HTML:

```bash
# from superkart_project/
HOME="$PWD/.home" ./.venv/bin/python -m nbconvert --to html SuperKart_Full_Code_Solution.ipynb
```

Submit `SuperKart_Full_Code_Solution.html` with the public URLs visible.

---

## Quick smoke test (any deployment)

```bash
# Online (single)
curl -X POST "$BACKEND_URL/v1/predict" -H "Content-Type: application/json" \
  -d '{"Product_Weight":12.66,"Product_Sugar_Content":"Low Sugar","Product_Allocated_Area":0.027,"Product_MRP":117.08,"Store_Size":"Medium","Store_Location_City_Type":"Tier 2","Store_Type":"Supermarket Type2","Product_Id_char":"FD","Store_Age_Years":16,"Product_Type_Category":"Non Perishables"}'

# Batch (CSV upload)
curl -X POST "$BACKEND_URL/v1/predictbatch" -F "file=@Batch_Data_SuperKart.csv"
```
