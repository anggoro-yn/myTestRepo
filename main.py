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
df = df.sort_values(by='Tanggal', ascending=False)

# Mengambil kolom 'Tanggal' dan memasukkannya ke dalam list 'tanggal_pengukuran'
tanggal_pengukuran = df['Tanggal'].tolist()

#st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.sidebar.image('LogoAPF.png')
    st.header('Pilihan')
    tanggal_dipilih = st.selectbox('Pilihan tanggal:', tanggal_pengukuran)

st.title('PT Asia Pacific Fiber Tbk')
st.markdown("## Monitoring Konsumsi Listrik Harian")
st.write(df)
st.write(tanggal_dipilih)

# Menampilkan data sesuai dengan tanggal yang dipilih
nilai_pln = df.loc[df['Tanggal'] == tanggal_dipilih, 'PLN Meter'].values[0]
nilai_apf = df.loc[df['Tanggal'] == tanggal_dipilih, 'APF Meter (ION)'].values[0]
nilai_poy = df.loc[df['Tanggal'] == tanggal_dipilih, 'POY'].values[0]

st.metric(label='PLN Meter', value=nilai_pln)
st.metric(label='APF Meter (ION)', value=nilai_apf)
st.metric(label='POY', value=nilai_poy)

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
