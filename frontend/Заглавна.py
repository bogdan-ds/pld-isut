import streamlit as st
import plotly.graph_objs as go

from common import mayors, get_municipal_df


def intro() -> None:
    st.write("# Строителни разрешения по кметски мандат, Община Пловдив")
    st.sidebar.success("Изберете мандат")
    st.markdown(
        """
        Визуализация на строителните разрешения с възложител Община Пловдив, 
        както и разделяне на всички строителни разрешения по това дали 
        по-вероятно са инфраструктурни или неинфраструктурни.
        
        В края на страницата е представена диаграма на разрешенията с възложител
        Община Пловдив, разделени по кметски мандати.
        
        Отделните страници съдържат по-детайлна разбивка на разрешенията.
        

        **👈 Изберете кметски мандат от менюто в ляво.

        ### Източник

        - [ИСУТ Пловдив](http://isut.plovdiv.bg:998/map_default.phtml)
    """
    )

    municipal_dfs = dict()
    for mayor in mayors:
        municipal_dfs[mayor["name"]] = get_municipal_df(mayor)

    fig = go.Figure()
    for mayor in mayors:
        fig.add_trace(
            go.Bar(
                x=[mayor["name"]],
                y=[len(municipal_dfs[mayor["name"]])],
                name=mayor["name"],
            )
        )

    fig.update_layout(
        title="Строителни разрешения по кметски мандат с възложител "
              "Община Пловдив",
        xaxis_title="Кметски мандат",
        yaxis_title="Брой разрешения",
    )
    st.plotly_chart(fig)





st.set_page_config(
    page_title="Строителни разрешения",
)
intro()
