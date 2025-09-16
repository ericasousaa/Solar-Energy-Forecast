import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Solar Energy Forecast",
    page_icon="🔆",
    layout="wide"
)

st.title("Solar Energy Forecasting Dashboard")
st.markdown(
    """
    This dashboard provides short-term forecasts of solar energy generation (kWh).
    The model is based on historical solar radiation and climate features.
    """
)

st.sidebar.header("Forecast Settings")
days = st.sidebar.slider("Days ahead", 3, 30, 7)

if st.sidebar.button("Generate Forecast"):
    url = f"http://localhost:8000/predict_solar?days={days}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df_forecast = pd.DataFrame({
            "Date": pd.to_datetime(data["dates"]),
            "Forecast (kWh)": data["forecast_kWh"]
        })

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Forecast Start", data["forecast_start"])
        with col2:
            st.metric("Forecast End", data["forecast_end"])

        fig = px.line(
            df_forecast, 
            x="Date", y="Forecast (kWh)",
            markers=True, 
            title=f"Forecast for {days} Days Ahead"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Forecast Data")
        st.dataframe(df_forecast, use_container_width=True)
    else:
        st.error("API request failed.")
