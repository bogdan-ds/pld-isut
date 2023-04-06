import streamlit as st

from common import ziko, show_term


st.set_page_config(page_title="Здравко Димиров")
st.sidebar.header("Здравко Димитров")
st.write(f"# Строителни разрешения с възложител Община Пловдив "
         f"през периода на действие на Здравко Димитров"
         f": {ziko['start']} - {ziko['end']}")
show_term(ziko)
