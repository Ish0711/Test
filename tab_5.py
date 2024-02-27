import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
 
# Load some data
#%cd C:\\Users\\ishan.gupta\\Downloads
data = pd.read_csv('data.csv')
 
st.title('My Data Visualization Application')
 
# Create tabs
tab_titles = ['Metrics', 'Plot', 'Chart', 'Input']
tabs = st.tabs(tab_titles)
 
# Add content to each tab
with tabs[0]:
    st.header('Metrics')
    st.metric('Metric 1', 123)
    st.metric('Metric 2', 456)
 
with tabs[1]:
    st.header('Plot')
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'])
    st.pyplot(fig)
 
with tabs[2]:
    st.header('Chart')
    st.line_chart(data)
 
with tabs[3]:
    st.header('Input')
    st.text_input('Enter some text')
    st.number_input('Enter a number')