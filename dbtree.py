import streamlit as st
import snowflake.connector
from pandas import DataFrame
from streamlit_option_menu import option_menu
from streamlit_dbtree import streamlit_dbtree
import pandas as pd
from ydata_profiling import ProfileReport
#import ipywidgets
#from pydantic_settings import BaseSettings
import streamlit.components.v1 as components
from IPython.core.display import display,HTML
from bs4 import BeautifulSoup
 
def read_html_with_beautiful_soup(file_path):
    # Read HTML file
    with open(file_path, 'r') as f:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(f, 'html.parser')
    # Find all tables in the HTML
    tables = soup.find_all('table')
    # Read tables into DataFrame using read_html()
    df = pd.read_html(str(tables))[0]
    return df
#import pandas_profiling as pp
st.set_page_config(page_title="Snowflake Database Portal", page_icon=":tada:", layout="wide")

conn = st.connection("snowflake")
cur = conn.cursor()
db_name=cur.execute("select current_database()").fetchone()[0]
schema_name = cur.execute("select current_schema()").fetchone()[0]
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
   table_name=sel.get("id")
   st.write(table_name) 
   st.subheader('Workarea')
   # Create tabs
   tab_titles = ['Metadata', 'Data', 'Associations', 'SQLs']
   tabs = st.tabs(tab_titles)

   
   with tabs[0]:
        st.header('Metadata')
        df = conn.query("select t1.*,t2.*exclude(COLUMN_NAME),t3.*exclude(REF_COLUMN_NAME) From " + db_name +".INFORMATION_SCHEMA.COLUMNS t1 left join (select TAG_NAME,TAG_VALUE,COLUMN_NAME from table("+db_name+".information_schema.tag_references_all_columns('"+table_name +"', 'table')))t2 on t1.Column_name = t2.Column_name left join (select POLICY_NAME,POLICY_KIND,REF_COLUMN_NAME,POLICY_STATUS from table(information_schema.policy_references(policy_name => '"+db_name+"."+schema_name+".stock_ssn_mask')))t3 On t1.Column_Name = t3.REF_COLUMN_NAME where CONCAT_WS('.',t1.TABLE_CATALOG,t1.TABLE_SCHEMA,t1.TABLE_NAME) = '"+table_name+"'")
        df=pd.DataFrame(df)
        filter = st.multiselect('Data_Type_Filter',df['DATA_TYPE'].unique())
        if filter == []:
            new_df = df
        else:
            new_df = df[df.DATA_TYPE.isin(filter)]
        st.dataframe(new_df)
     
   with tabs[1]:
        st.header('Data')
        df = conn.query("select * from " + table_name)
        df.columns = df.columns.str.replace('Price', 'Price 💲')
        profile = ProfileReport(df,title = "Trending_Stocks")
        st.write(df)
        my_report = profile.to_file("my_report.html")
        html_file_path = 'my_report.html'
        # Read HTML file using BeautifulSoup with read_html()
        df_profile = read_html_with_beautiful_soup(html_file_path)
        st.subheader('Data Profile')
        st.write(df_profile)
        #st.write(pd.read_html("my_report.html"))
        
         
   with tabs[2]:
        st.header('Associations')
         
   with tabs[3]:
        st.header('SQLs')
        df = conn.query("select get_ddl('Table'," + "'" + table_name + "')")
        st.write(df)
         

 

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
