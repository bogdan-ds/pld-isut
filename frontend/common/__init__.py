import re

import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from typing import Tuple


infra_strings = ["ЕВН", "Община Пловдив", "Електроразпределение",
                 "БТК", "МЕГАЛАН"]

ziko = {
    "start": "12-11-2019",
    "end": "12-11-2023"
}

totev1 = {
    "start": "30-10-2011",
    "end": "25-10-2015"
}

totev2 = {
    "start": "25-10-2015",
    "end": "10-11-2019"
}

slavcho = {
    "start": "1-11-2007",
    "end": "1-11-2011"
}


@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    df = pd.read_pickle(filename)
    return df


@st.cache_data
def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(["Изглед", "Карта", "Година", "Район"], axis=1, inplace=True)

    df["Дата"].replace("-", "01-01-1970", inplace=True)
    df["Дата"] = pd.to_datetime(df['Дата'])

    df["Възложител"].replace("ОБЩИНА ПЛОВДИВ", "Община Пловдив", inplace=True)
    df["Възложител"].replace("1.Община Пловдив", "Община Пловдив", inplace=True)
    df["Възложител"].replace("1.ОБЩИНА ПЛОВДИВ", "Община Пловдив", inplace=True)
    df["Възложител"].replace("Общ.-ЕВН България ЕлектроразпределениеАД",
                             '1.ОБЩИНА ПЛОВДИВ 2."ЕВН БЪЛГАРИЯ '
                             'Електроразпределение" АД', inplace=True)
    df["Възложител"].replace(
        '1. ОБЩИНА ПЛОВДИВ 2."ЕВН БЪЛГАРИЯ Електроразпределение" АД',
        '1.ОБЩИНА ПЛОВДИВ 2."ЕВН БЪЛГАРИЯ Електроразпределение" АД',
        inplace=True)

    return df


def infra_filter(row: pd.Series) -> bool:
    if type(row["Възложител"]) == str:
        for string in infra_strings:
            hit = re.search(rf"{string}", row["Възложител"], re.IGNORECASE)
            if hit:
                return True
    return False


def get_term_dfs(input_df: pd.DataFrame,
                 start_date: str,
                 end_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    term_df = input_df[(input_df['Дата'] > start_date) &
                       (input_df['Дата'] < end_date)]
    infra_filtered = term_df.apply(infra_filter, axis=1)
    infra_df = term_df[infra_filtered]
    others = term_df[~infra_filtered]
    return infra_df, others


def show_term(mayor: dict):
    df = load_data("../isut-df-18022023-15-07.pkl")
    df = preprocess_df(df)
    infra_df, others = get_term_dfs(df, mayor["start"], mayor["end"])
    for i, df in enumerate([infra_df, others]):
        if i == 0:
            st.markdown(f"## Инфраструктурни строителни "
                        f"разрешения: *{len(df)}*")
            df = df.set_index("Номер")
            st.write(df)
        elif i == 1:
            st.markdown(f"## Всички останали строителни "
                        f"разрешения: *{len(df)}*")
            df = df.set_index("Номер")
            st.write(df)
        st.markdown("## Списък с уникални възложители")
        st.write(df["Възложител"].value_counts())

    trace1 = go.Histogram(x=others["Дата"], name='Всички останали',
                          opacity=0.75)
    trace2 = go.Histogram(x=infra_df["Дата"], name='Инфраструктурни',
                          opacity=0.55)
    fig = go.Figure(data=[trace1, trace2])
    fig.update_layout(barmode='overlay')
    st.plotly_chart(fig)


