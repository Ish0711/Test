import streamlit as st
 
st.title('My Application')
 
# Function to get tab content from server
def get_tab_content():
    return [
        {'title': 'Topic A', 'content': 'Topic A content'},
        {'title': 'Topic B', 'content': 'Topic B content'},
        {'title': 'Topic C', 'content': 'Topic C content'},
    ]
 
# Pull tab content from server
tab_contents = get_tab_content()
 
# Create tabs
tab_names = [content['title'] for content in tab_contents]
tabs = st.tabs(tab_names)
 
# Iterate through each tab and build content
for tab, tab_content in zip(tabs, tab_contents):
    with tab:
        st.header(tab_content['title'])
        st.write(tab_content['content'])