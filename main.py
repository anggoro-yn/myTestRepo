import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
#data = pd.read_csv('data.csv', delimiter=';')

st.set_page_config(layout="wide")

# Sidebar for facilitator selection
st.sidebar.header('Option')
selected_fasilitator = st.sidebar.selectbox('Pilih Kelompok Fasilitator:', ['a','b','c'])




# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
