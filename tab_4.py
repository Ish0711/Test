import streamlit as st
 
st.title('My Dashboard')
 
# Create tabs
tab_titles = ['User Inputs', 'Data Display', 'Data Analysis']
tabs = st.tabs(tab_titles)
 
# Add content to each tab
with tabs[0]:
    st.header('User Inputs')
    st.text_input('Enter some text')
    st.number_input('Enter a number')
 
with tabs[1]:
    st.header('Data Display')
    st.table({'column1': [1, 2, 3], 'column2': [4, 5, 6]})
 
with tabs[2]:
    st.header('Data Analysis')
    st.line_chart([1, 2, 3, 4, 5])