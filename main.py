import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('data.csv', delimiter=';')
df.drop(columns=['Unnamed: 14'], inplace=True)

# Mengubah kolom 'Tanggal' menjadi tipe datetime
df['Tanggal'] = pd.to_datetime(df['Tanggal']) + pd.DateOffset(hours=8)

# Mengurutkan dataframe berdasarkan kolom 'Tanggal' secara descending
df = df.sort_values(by='Tanggal', ascending=

# Mengambil kolom 'Tanggal' dan memasukkannya ke dalam list 'tanggal_pengukuran'
tanggal_pengukuran = df['Tanggal'].tolist()

#st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.sidebar.image('LogoAPF.png')
    st.header('Pilihan')
    pilihan_tanggal = st.selectbox('Pilihan:', tanggal_pengukuran)

st.title('PT Asia Pacific Fiber Tbk')
st.markdown("## Monitoring Konsumsi Listrik Harian")
st.write(data)

# Memilih nilai tertinggi dari kolom 'Tanggal'
tanggal_tertinggi = data['Tanggal'].max()

# Menampilkan nilai tertinggi di st.metric
st.metric(label="Tanggal", value=tanggal_tertinggi.strftime('%Y-%m-%d'))

col1, col2, col3 = st.columns(3)
with col1:
    nilai_pln = data.loc[data['Tanggal'] == tanggal_tertinggi, "PLN Meter"].values[0]
    st.metric(label="PLN Meter", value=nilai_pln.strftime('%Y-%m-%d'))


# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
