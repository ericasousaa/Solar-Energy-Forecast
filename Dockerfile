FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src
COPY data /app/data
COPY model.pkl /app/model.pkl
COPY scaler.pkl /app/scaler.pkl

EXPOSE 8000
EXPOSE 8501

CMD python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 & \
    python -m streamlit run src/dashboard.py --server.port 8501 --server.address 0.0.0.0
