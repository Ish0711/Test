
import streamlit as st
import snowflake.connector
from pandas import DataFrame
from streamlit_option_menu import option_menu
from streamlit_dbtree import streamlit_dbtree

st.set_page_config(page_title="Snowflake Database Portal", page_icon=":tada:", layout="wide")

conn = st.connection("snowflake")
cur = conn.cursor()

with st.sidebar:
    st.image("https://www.snowflake.com/wp-content/uploads/2022/03/SOLAR_Blog.png",use_column_width='auto')
    selected_menu = option_menu(menu_title="Snowflake DB Portal", options=["DBTree", "Database Info",  "Database Users", "Executed SQLs","Storage Usage"], 
    icons=['house', 'cloud-upload', "list-task", 'gear'],orientation="vertical")


if selected_menu == "DBTree":
 st.title("❄️ Snowflake DB Structure")
 st.write(" This app is to display information about your Snowflake database.")   
 value = streamlit_dbtree(conn)
 if value is not None:
  for sel in value:
   st.write(sel.get("id") +" IS A " +sel.get("type"))
   #st.write(sel.get("id") +" Preview Data ")
   abc=sel.get("id") 
   st.write(abc)
   storage = cur.execute("select * from " + abc ).fetchmany(size=10)
   col2 = [ x[0] for x in cur.description]
   df3 = DataFrame(storage,columns=col2)
   st.dataframe(df3)
   

 

 #conn = st.connection("snowflake")

elif selected_menu == "Database Info":
    st.title("Database Info")
    db_name=cur.execute("select current_database()").fetchone()[0]
    time = cur.execute("select current_timestamp()").fetchone()[0]
    ware = cur.execute("select current_warehouse()").fetchone()[0]
    ver = cur.execute("select current_version()").fetchone()[0]
    DB_NAME, TIME_STAMP,WAREHOUSE_NAME,VERSION = st.columns(4)
    with DB_NAME:
        st.subheader("Database Name")
        st.write(db_name)
    with TIME_STAMP:
        st.subheader("Time")
        st.write(time)
    with WAREHOUSE_NAME:
        st.subheader("Warehouse Name")
        st.write(ware)
    with VERSION:
        st.subheader("Snowflake Version")
        st.write(ver)
elif selected_menu == "Database Users":
    st.title("Snowflake users")
    users = cur.execute("select * from snowflake.account_usage.users").fetchall()
    names = [ x[0] for x in cur.description]
    df = DataFrame(users,columns=names)
    st.dataframe(df)
elif selected_menu == "Executed SQLs":
    st.title("Snowflake Executed SQL's")
    sqls = cur.execute("select * from snowflake.account_usage.query_history order by start_time").fetchall()
    col1 = [ x[0] for x in cur.description]
    df2 = DataFrame(sqls,columns=col1)
    st.dataframe(df2)
elif selected_menu == "Storage Usage":
    st.title("Snowflake Database Storage: ")
    storage = cur.execute("select * from snowflake.account_usage.storage_usage;").fetchall()
    col2 = [ x[0] for x in cur.description]
    df3 = DataFrame(storage,columns=col2)
    st.dataframe(df3)
