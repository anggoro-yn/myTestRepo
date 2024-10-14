import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('data.csv', delimiter=';')
data.drop(columns=['1'], inplace=True)
data.drop(columns=['Unnamed: 15'], inplace=True)
data['Tanggal'] = pd.to_datetime(data['Tanggal']) + pd.DateOffset(hours=8)

#st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.sidebar.image('LogoAPF.png')
    st.header('Pilihan')
    pilihan_01 = st.selectbox('Pilihan:', ['a','b','c'])

st.title('PT Asia Pacific Fiber Tbk')
st.markdown("## Monitoring Konsumsi Listrik Harian")

# Memilih nilai tertinggi dari kolom 'Tanggal'
tanggal_tertinggi = data['Tanggal'].max()

# Menampilkan nilai tertinggi di st.metric
st.metric(label="Tanggal", value=tanggal_tertinggi.strftime('%Y-%m-%d'), delta = -10)

st.write(data)

# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
