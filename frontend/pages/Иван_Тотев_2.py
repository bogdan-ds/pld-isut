import streamlit as st

from common import show_term, totev2


st.set_page_config(page_title="Иван Тотев 2")
st.sidebar.header("Иван Тотев 2")
st.write(f"# Строителни разрешения Иван Тотев втори мандат"
         f": {totev2['start']} - {totev2['end']}")
show_term(totev2)
