import streamlit as st

from common import show_term, ziko


st.set_page_config(page_title="Здравко Димиров")
st.sidebar.header("Здравко Димитров")
st.write(f"# Строителни разрешения Здравко "
         f"Димитров: {ziko['start']} - {ziko['end']}")
show_term(ziko)
