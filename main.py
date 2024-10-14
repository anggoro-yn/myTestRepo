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

    name = st.text_input("Nama Anda")
    st.write(f"Nama Anda adalah {name}")
    secret_code = st.text_input("secret code Anda")
    st.write(f"Nama Anda adalah {secret_code}")

st.title('PT Asia Pacific Fiber Tbk')
st.markdown("## Monitoring Konsumsi Listrik Harian")
st.write(df)

# Menampilkan tanggal
st.metric(label="Tanggal", value=tanggal_dipilih.strftime('%Y-%m-%d'))

# Menampilkan data sesuai dengan tanggal yang dipilih
nilai_pln = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'PLN Meter'].values[0].replace(',','.'))
nilai_apf = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'APF Meter (ION)'].values[0].replace(',','.'))
nilai_Sum_APF = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'SUM ALL APF Area'].values[0].replace(',','.'))

# Mencari nilai untuk satu hari sebelum tanggal_dipilih
tanggal_sebelumnya = tanggal_dipilih - pd.Timedelta(days=1)
nilai_pln_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'PLN Meter'].values[0].replace(',','.'))
nilai_apf_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'APF Meter (ION)'].values[0].replace(',','.'))
nilai_Sum_APF_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'SUM ALL APF Area'].values[0].replace(',','.'))

#mencari delta value
delta_PLN = round(nilai_pln - nilai_pln_sebelumnya, 2)
delta_APF = round(nilai_apf - nilai_apf_sebelumnya, 2)
delta_Sum_APF = round(nilai_Sum_APF - nilai_Sum_APF_sebelumnya, 2)

st.markdown('## Pemakaian Listrik APF Total')
st.markdown('Berdasarkan pencatatan kWhmeter di GI PLN, GI APF dan Total Pemakaian Seluruh Plant')
# add a border
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='PLN Meter', value=nilai_pln, delta = delta_PLN)
with col2:
    st.metric(label='APF Meter (ION)', value=nilai_apf, delta = delta_APF)
with col3:
    st.metric(label='Sum ALL APF Area', value=nilai_Sum_APF, delta = delta_Sum_APF)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='PLN Meter', value=nilai_pln_sebelumnya)
with col2:
    st.metric(label='APF Meter (ION)', value=nilai_apf_sebelumnya)
with col3:
    st.metric(label='Sum ALL APF Area', value=nilai_Sum_APF_sebelumnya)
# add a border
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)

# Memilih nilai tertinggi dari kolom 'Tanggal'
tanggal_tertinggi = df['Tanggal'].max()



# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
