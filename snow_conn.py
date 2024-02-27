import streamlit as st
from snowflake.snowpark import Session

conn = st.connection("snowflake")
df = conn.query("select current_warehouse()")
st.write(df)