import streamlit as st
from shillelagh.backends.apsw.db import connect
import shillelagh
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Enactus HR Dashboard",
    page_icon="📊",
    layout = 'wide'  
)

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

# ------------ {connection} --------------------------
@st.cache(allow_output_mutation=True)
def get_database_connection():
    return connect(":memory:")

conn = get_database_connection()

@st.cache(ttl=600, hash_funcs={shillelagh.backends.apsw.db.Connection: hash})
def run_query(query, connection):
    df = pd.read_sql(query,connection)
    return df
# --------------------------------------------------------------
sheet_url = st.secrets["public_gsheets_url"]
data = run_query(f"""select * from "{sheet_url}";""", conn)
