import streamlit as st
import pandas as pd



 
st.title('Workarea')
 
# Create tabs
tab_titles = ['Metadata', 'Data', 'Associations', 'SQLs']
tabs = st.tabs(tab_titles)
df = pd.read_csv('customers-100.csv') 
# Add content to the Data Preprocessing tab
with tabs[0]:
    st.header('Metadata')
    #df = conn.query("select * From TEST_DATA.INFORMATION_SCHEMA.COLUMNS where Table_name = 'STOCK_TEST'")
    df_meta = {'Table_Catalog':'TEST_DATA','Table_Schema':'TEST_SCHEMA','Table_Name':'CUSTOMERS',
               'Table_Columns': df.columns,'Data_Type':df.dtypes,'Column_Attributes':df.columns.astype,'Details':df.isnull}    
    st.write(pd.DataFrame(data=df_meta))
    #st.write(df.columns)
    st.write(df.describe())
    st.write('This is where you can preprocess your data.')
 
# Add content to the Model Training tab
with tabs[1]:
    st.header('Data')
    st.dataframe(df)
    #st.write('This is where you can train your model.')
 
# Add content to the Model Evaluation tab
with tabs[2]:
    st.header('Associations')
    #st.write('This is where you can evaluate your model.')
 
# Add content to the Results Visualization tab
with tabs[3]:
    st.header('SQLs')
    #df = conn.query("select get_ddl('Table','TEST_DATA.TEST_SCHEMA.STOCK_TEST')")
    st.write( 'CREATE TABLE "TEST_DATA"."TEST_SCHEMA"."CUSTOMERS" ( Index VARCHAR,Customer Id VARCHAR , First Name VARCHAR , Last Name VARCHAR , Company VARCHAR , City VARCHAR , Country VARCHAR , Phone 1 VARCHAR , Phone 2 VARCHAR , Email VARCHAR , Subscription Date VARCHAR , Website VARCHAR )')
    #st.write('This is where you can visualize your results.')