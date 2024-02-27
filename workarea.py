import streamlit as st

from snowflake.snowpark import Session

conn = st.connection("snowflake")

#table_name = "STOCK_TEST" 
st.title('Workarea')
#st.write(conn.cursor) 
# Create tabs
tab_titles = ['Metadata', 'Data', 'Associations', 'SQLs']
tabs = st.tabs(tab_titles)

# Add content to the Data Preprocessing tab
with tabs[0]:
    st.header('Metadata')
    df = conn.query("select t1.*,t2.*exclude(COLUMN_NAME),t3.*exclude(REF_COLUMN_NAME) From TEST_DATA.INFORMATION_SCHEMA.COLUMNS t1 left join (select TAG_NAME,TAG_VALUE,COLUMN_NAME from table(TEST_DATA.information_schema.tag_references_all_columns('TEST_DATA.TEST_SCHEMA.STOCK_TEST', 'table')))t2 on t1.Column_name = t2.Column_name left join (select POLICY_NAME,POLICY_KIND,REF_COLUMN_NAME,POLICY_STATUS from table(information_schema.policy_references(policy_name => 'TEST_DATA.TEST_SCHEMA.stock_ssn_mask')))t3 On t1.Column_Name = t3.REF_COLUMN_NAME where t1.Table_name = 'STOCK_TEST'")
    st.write(df)
    #st.write('This is where you can preprocess your data.')
 
# Add content to the Model Training tab
with tabs[1]:
    st.header('Data')
    df = conn.query("select * from TEST_DATA.TEST_SCHEMA.STOCK_TEST")
    st.write(df)
    #st.write('This is where you can train your model.')
 
# Add content to the Model Evaluation tab
with tabs[2]:
    st.header('Associations')
    #st.write('This is where you can evaluate your model.')
 
# Add content to the Results Visualization tab
with tabs[3]:
    st.header('SQLs')
    df = conn.query("select get_ddl('Table','TEST_DATA.TEST_SCHEMA.STOCK_TEST')")
    st.write(df)
    #st.write('This is where you can visualize your results.')