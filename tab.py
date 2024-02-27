import streamlit as st
 
st.title('My Application')
 
# Create tabs
tab_titles = ['Topic A', 'Topic B', 'Topic C']
tab1, tab2, tab3 = st.tabs(tab_titles)
 
# Add content to each tab
with tab1:
    st.header('Topic A')
    st.write('Topic A content')
 
with tab2:
    st.header('Topic B')
    st.write('Topic B content')
 
with tab3:
    st.header('Topic C')
    st.write('Topic C content')