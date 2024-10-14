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

# Menampilkan tanggal
st.metric(label="Tanggal", value=tanggal_dipilih.strftime('%Y-%m-%d'))

# Menampilkan data sesuai dengan tanggal yang dipilih
nilai_pln = df.loc[df['Tanggal'] == tanggal_dipilih, 'PLN Meter'].values[0]
nilai_apf = df.loc[df['Tanggal'] == tanggal_dipilih, 'APF Meter (ION)'].values[0]
nilai_Sum_APF = df.loc[df['Tanggal'] == tanggal_dipilih, 'SUM ALL APF Area'].values[0]

# Mencari nilai untuk satu hari sebelum tanggal_dipilih
tanggal_sebelumnya = tanggal_dipilih - pd.Timedelta(days=1)
nilai_pln_sebelumnya = df.loc[df['Tanggal'] == tanggal_sebelumnya, 'PLN Meter'].values[0]
nilai_apf_sebelumnya = df.loc[df['Tanggal'] == tanggal_sebelumnya, 'APF Meter (ION)'].values[0]
nilai_Sum_APF_sebelumnya = df.loc[df['Tanggal'] == tanggal_sebelumnya, 'Sum ALL APF Area'].values[0]


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='PLN Meter', value=nilai_pln)
    st.metric(label='PLN Meter', value=nilai_pln_sebelumnya)
with col2:
    st.metric(label='APF Meter (ION)', value=nilai_apf)
    st.metric(label='APF Meter (ION)', value=nilai_apf_sebelumnya)
with col3:
    st.metric(label='Sum ALL APF Area', value=nilai_Sum_APF)
    st.metric(label='Sum ALL APF Area', value=nilai_Sum_APF_sebelumnya)

# Memilih nilai tertinggi dari kolom 'Tanggal'
tanggal_tertinggi = df['Tanggal'].max()



# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
