from fastapi import FastAPI, Query
import pandas as pd
import joblib
import numpy as np

app = FastAPI(title="Solar Forecast API")

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

df = pd.read_csv("data/solar.csv")
df["date"] = pd.to_datetime(df["date"])

@app.get("/")
def root():
    return {"message": "Solar Forecast API - use /predict_solar"}

@app.get("/predict_solar")
def predict_solar(days: int = Query(7, description="Days ahead to forecast")):
    last_date = df["date"].iloc[-1]
    last_value = df["generation_kWh"].iloc[-1]

    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=days)

    preds = []
    lag_value = last_value

    for date in future_dates:
        temperature = 25 + np.random.normal(0, 2)
        cloudcover = 50 + np.random.normal(0, 10)
        precipitation = max(0, np.random.normal(2, 1))

        features = {
            "dayofyear": date.dayofyear,
            "month": date.month,
            "lag_1": lag_value,
            "temperature": temperature,
            "cloudcover": cloudcover,
            "precipitation": precipitation,
        }

        X_scaled = scaler.transform(pd.DataFrame([features]))
        y_pred = model.predict(X_scaled)[0]

        preds.append(y_pred)
        lag_value = y_pred

    return {
        "last_dataset_date": str(last_date.date()),
        "forecast_start": str(future_dates[0].date()),
        "forecast_end": str(future_dates[-1].date()),
        "dates": future_dates.strftime("%Y-%m-%d").tolist(),
        "forecast_kWh": np.round(preds, 2).tolist()
    }