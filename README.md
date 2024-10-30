# Project-Template
## Researcher-Service Installation Guide

### Installation Methods


1. Create and activate a Python virtual environment and install required packages:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

2. Fill in .env
    ```
    cp .env-example .env
   ```
   fill in GCP_MYSQL_CONNECTION_STRING

2. Launch the backend service:
   ```
   pip3 install -r requirements.txt
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Deploy to GCP cloud run

1. Fill in credentials in .env-example(please don't commit credentials into git)

2. Deploy to GCP cloud run
   ```
   gcloud run deploy researcher-profile --port 8080 --source .
   ```