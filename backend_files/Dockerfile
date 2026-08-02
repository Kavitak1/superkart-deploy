FROM python:3.10-slim

WORKDIR /app

# libgomp1 is required by XGBoost at runtime
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:superkart_api"]
