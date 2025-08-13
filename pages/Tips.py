import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

st.title("Анализ tips.csv")
st.subheader(
    "Шаг 1 — загрузите CSV с данными чаевых или используйте демонстрационный файл по умолчанию"
)

st.markdown(
    """
**Ожидаемые названия колонок** (рекомендую привести файл к этим именам, чтобы последующие шаги работали корректно):

- `total_bill` — сумма счёта  
- `tip` — сумма чаевых  
- `sex` — пол клиента (Male/Female)  
- `smoker` — курили ли (Yes/No)  
- `day` — день недели (Thur/Fri/Sat/Sun)  
- `time` — время (Lunch/Dinner)  
- `size` — число людей за столом
"""
)

uploaded = st.file_uploader(
    "Выберите ваш tips.csv (CSV-файл). Если файл не загружен — будет загружен демонстрационный пример с GitHub.",
    type=["csv"],
)

# URL дефолтного набора (Seaborn tips)
default_url = (
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
)

tips = pd.DataFrame()

if uploaded is not None:
    try:
        tips = pd.read_csv(uploaded)
        st.success("Файл загружен из локального файла.")
    except Exception as e:
        st.error(f"Ошибка при чтении загруженного файла: {e}")
        tips = pd.DataFrame()
else:
    # Попытка загрузить демонстрационный файл по URL
    try:
        tips = pd.read_csv(default_url)
        st.info("Загружен демонстрационный файл tips.csv с GitHub.")
    except Exception as e:
        st.error(f"Не удалось загрузить демонстрационный набор по умолчанию: {e}")
        tips = pd.DataFrame()

# Предварительный просмотр
if not tips.empty:
    st.subheader("Предварительный просмотр (первые строки)")
    st.dataframe(tips.head(50), use_container_width=True, height=260)
else:
    st.warning(
        "Данные отсутствуют. Загрузите CSV или проверьте соединение с интернетом для загрузки демонстрационного файла."
    )

np.random.seed(42)
tips["time_order"] = pd.to_datetime(
    np.random.choice(pd.date_range("2023-01-01", "2023-01-31"), size=len(tips))
)
st.header("Средние чаевые за день")
if not tips.empty and "time_order" in tips.columns and "tip" in tips.columns:
    tips["time_order"] = pd.to_datetime(tips["time_order"])
    daily = tips.set_index("time_order").resample("D")["tip"].mean().dropna()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily.index, daily.values, marker=None, linestyle="-", linewidth=2)
    ax.set_title("Динамика чаевых во времени — среднее по дню", fontsize=14)
    ax.set_xlabel("Дата заказа", fontsize=12)
    ax.set_ylabel("Средние чаевые (доллары)", fontsize=12)
    plt.xticks(rotation=45)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Для графика нужны колонки 'time_order' и 'tip'.")

st.header("Распределение суммы счёта со сглаживанием")
if not tips.empty and "total_bill" in tips.columns:
    tips["total_bill"] = pd.to_numeric(tips["total_bill"], errors="coerce")
    data = tips["total_bill"].dropna()

    if data.empty:
        st.info("Колонка 'total_bill' пустая после приведения к числу.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(data, bins=20, kde=True, ax=ax, edgecolor="black", alpha=0.6)
        ax.set_title("Средняя сумма счета со сглаживанием", fontsize=14)
        ax.set_xlabel("Сумма счёта (доллары)", fontsize=12)
        ax.set_ylabel("Частота", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig)
else:
    st.info("Для построения гистограммы требуется колонка 'total_bill' в данных.")

if {"total_bill", "tip"}.issubset(tips.columns):
    st.header("Связь между суммой счёта и чаевыми")

    fig = px.scatter(
        tips,
        x="total_bill",
        y="tip",
        title="Связь между суммой счета и чаевыми",
        labels={"total_bill": "Сумма счета (доллары)", "tip": "Чаевые (доллары)"},
        opacity=0.7,
        size_max=10,
    )
    fig.update_layout(
        xaxis=dict(
            showgrid=True,  # показывать сетку по X
            gridcolor="#cccccc",  # цвет линий сетки
            gridwidth=1,  # толщина линий
        ),
        yaxis=dict(showgrid=True, gridcolor="#cccccc", gridwidth=1),
    )

    st.plotly_chart(fig)
else:
    st.info("Для графика нужны колонки 'total_bill' и 'tip'.")

if all(col in tips.columns for col in ["total_bill", "tip", "size"]):
    st.header("Связь суммы счета, чаевых и размера компании")

    fig = px.scatter(
        tips,
        x="total_bill",
        y="tip",
        size="size",
        title="Связь суммы счета, чаевых и размера компании",
        labels={
            "total_bill": "Сумма счета (доллары)",
            "tip": "Чаевые (доллары)",
            "size": "Размер компании",
        },
        size_max=15,
        opacity=0.7,
    )

    st.plotly_chart(fig)
else:
    st.warning("Для графика нужны колонки 'total_bill', 'size' и 'tip'.")
