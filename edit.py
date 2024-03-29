import pandas as pd
import json
import streamlit as st
import time
from snowflake.snowpark import Session
from snowflake.connector.pandas_tools import write_pandas

import pandas as pd
import json
import streamlit as st
from snowflake.snowpark import Session
import time

if 'snowflake_connection' not in st.session_state:
    # connect to Snowflake
    with open('creds.json') as f:
        connection_parameters = json.load(f)
    st.session_state.snowflake_connection = Session.builder.configs(connection_parameters).create()
    session = st.session_state.snowflake_connection
else:
    session = st.session_state.snowflake_connection

st.set_page_config(layout="centered", page_title="Data Editor", page_icon="🧮")
st.title("Snowflake Table Editor ❄️")
st.caption("This is a demo of the `st.experimental_data_editor`.")

def get_dataset():
    # load messages df
    df = session.table("STOCK_TEST")

    return df

dataset = get_dataset()

with st.form("data_editor_form"):
    st.caption("Edit the dataframe below")
    edited = st.data_editor(dataset, use_container_width=True, num_rows="dynamic")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    try:
        session.write_pandas(edited, "STOCK_TEST",overwrite= True)
        st.write(edited)
        st.success("Table updated")
        time.sleep(100)
    except:
        st.warning("Error updating table")
        time.sleep(100)
    st.rerun()