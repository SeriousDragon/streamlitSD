import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np


st.title("Котировки Apple")
st.markdown(
    "Приложение для просмотра котировок Apple (AAPL) с использованием yfinance."
)

with st.sidebar.expander("Параметры (Apple)"):
    today = dt.date.today()
    default_start = today - dt.timedelta(days=90)
    start_date = st.date_input("Начало периода", default_start, key="a_start")
    end_date = st.date_input("Конец периода", today, key="a_end")
ticker = "AAPL"

@st.cache_data
def load_data_yf(ticker: str, start: dt.date, end: dt.date):
    df = yf.download(ticker, start=start, end=end)
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            pass
    return df

with st.spinner("Загружаем данные..."):
    df = load_data_yf(ticker, start_date, end_date)

if df.empty:
    st.warning(
        "Нет данных за выбранный период — попробуйте расширить период или проверьте тикер."
    )
else:
    st.subheader("Таблица котировок")
    st.dataframe(df, use_container_width=True, height=360)

    st.subheader("Линейный график")
    if "Close" in df.columns:
        st.line_chart(df["Close"])
    else:
        st.warning("В данных нет колонки 'Close' — график невозможен.")

