import streamlit as st

from common import show_term, slavcho


st.set_page_config(page_title="Славчо Атанасов")
st.sidebar.header("Славчо Атанасов")
st.write(f"# Строителни разрешения Славчо Атанасов"
         f": {slavcho['start']} - {slavcho['end']}")
show_term(slavcho)
