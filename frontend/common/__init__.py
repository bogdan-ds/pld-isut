import pandas as pd
import plotly.graph_objs as go
import streamlit as st


from .filtering import infra_filter, get_infra_other_split, \
    municipality_filter, apply_filter_to_df


ziko = {
    "start": "12-11-2019",
    "end": "12-11-2023",
    "name": "Здравко Димитров"
}

totev1 = {
    "start": "30-10-2011",
    "end": "25-10-2015",
    "name": "Иван Тотев 1"
}

totev2 = {
    "start": "25-10-2015",
    "end": "10-11-2019",
    "name": "Иван Тотев 2"
}

slavcho = {
    "start": "1-11-2007",
    "end": "1-11-2011",
    "name": "Славчо Атанасов"
}

mayors = [ziko, totev1, totev2, slavcho]


@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    df = pd.read_pickle(filename)
    return df


@st.cache_data
def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(["Изглед", "Карта", "Година", "Район"], axis=1, inplace=True)

    df["Дата"].replace("-", "01-01-1970", inplace=True)
    df["Дата"] = pd.to_datetime(df['Дата'], infer_datetime_format=True)

    df["Възложител"].replace("ОБЩИНА ПЛОВДИВ", "Община Пловдив", inplace=True)
    df["Възложител"].replace("ОБЩИНА ПЛОДВИВ", "Община Пловдив", inplace=True)
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


def show_term(mayor: dict):
    df = load_data("isut-df-18022023-15-07.pkl")
    df = preprocess_df(df)
    municipality_df = get_municipal_df(ziko)
    st.markdown(f"# Разрешения с Община "
                f"Пловдив сред възложителите: *{len(municipality_df)}*")
    municipality_df = municipality_df.set_index("Номер")
    st.write(municipality_df)
    infra_df, others = get_infra_other_split(df, mayor["start"],
                                             mayor["end"], infra_filter)
    st.markdown(f"# Общо всички разрешения: *{len(infra_df) + len(others)}*")
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


def get_municipal_df(mayor: dict) -> pd.DataFrame:
    df = load_data("isut-df-18022023-15-07.pkl")
    df = preprocess_df(df)
    term_df = df[(df['Дата'] > mayor["start"]) & (df['Дата'] < mayor["end"])]
    filtered_column = apply_filter_to_df(term_df, municipality_filter)
    municipality_df = term_df[filtered_column]
    return municipality_df


