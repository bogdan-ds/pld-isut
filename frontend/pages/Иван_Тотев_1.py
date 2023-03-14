import streamlit as st

from common import show_term, totev1


st.set_page_config(page_title="Иван Тотев 1")
st.sidebar.header("Иван Тотев 1")
st.write(f"# Строителни разрешения Иван Тотев първи мандат"
         f": {totev1['start']} - {totev1['end']}")
show_term(totev1)
