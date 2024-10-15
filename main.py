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

# Mengkonversi kolom 'PLN Meter' dan kolom lainnya ke float
df['PLN Meter'] = df['PLN Meter'].str.replace(',', '.').astype(float)
df['APF Meter (ION)'] = df['APF Meter (ION)'].str.replace(',', '.').astype(float)
df['POY'] = df['POY'].str.replace(',', '.').astype(float)
df['TX 1'] = df['TX 1'].str.replace(',', '.').astype(float)
df['TX 2'] = df['TX 2'].str.replace(',', '.').astype(float)
df['WRP'] = df['WRP'].str.replace(',', '.').astype(float)
df['TX 3'] = df['TX 3'].str.replace(',', '.').astype(float)
#df['TX 4 (+Doubling)'] = df['TX 4 (+Doubling)'].str.replace(',', '.').astype(float)
df['PP'] = df['PP'].str.replace(',', '.').astype(float)
df['SP3 Compressor'] = df['SP3 Compressor'].str.replace(',', '.').astype(float)
df['TX 2 Compressor'] = df['TX 2 Compressor'].str.replace(',', '.').astype(float)
df['SUM ALL APF Area'] = df['SUM ALL APF Area'].str.replace(',', '.').astype(float)
df['EMS'] = df['EMS'].str.replace(',', '.').astype(float)

# User tool
admin_user = False
general_user = False
dict_user = {'anggoro' : 'password01' ,'rahul':'password02','siska':'password03'}
dict_name = {'anggoro' : 'Anggoro Yudho Nuswantoro' ,'rahul': 'Rahul Bankar','siska':'Siska Rahmawati'}

#st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.sidebar.image('LogoAPF.png')
    st.header('Pilihan')
    tanggal_dipilih = st.selectbox('Pilihan tanggal:', tanggal_pengukuran)
    
    # Menentukan rentang tanggal untuk sepuluh hari terakhir
    tanggal_awal = tanggal_dipilih - pd.Timedelta(days=9)
    tanggal_akhir = tanggal_dipilih

    name = st.text_input("Nama Anda")
    secret_code = st.text_input("secret code Anda", type="password")
    try:
        correct_secret_code = dict_user[name]
    except Exception as e:
        correct_secret_code = 'incorrect code !!!!!!!!'
    else:
        if name != '' and secret_code != '':
            if correct_secret_code == secret_code :
                if name == 'anggoro':
                    admin_user = True
                    general_user = False
                else:
                    general_user = True
                    admin_user = False
            else:
                admin_user = False
                general_user = False
        else:
            admin_user = False
            general_user = False

    if st.button('Log out'):
        name = ''
    

if admin_user or general_user:

    st.markdown("Selamat datang " + dict_name[name])
    st.title('PT Asia Pacific Fiber Tbk')
    st.markdown("## Monitoring Konsumsi Listrik Harian")
    st.write(df)
    
    # Menampilkan tanggal
    st.metric(label="Tanggal", value=tanggal_dipilih.strftime('%Y-%m-%d'))

    # Menyaring data untuk sepuluh hari terakhir
    df_10_hari = df[(df['Tanggal'] >= tanggal_awal) & (df['Tanggal'] <= tanggal_akhir)]
    
    # Menghitung rata-rata untuk sepuluh hari terakhir
    nilai_pln_rata2 = df_10_hari['PLN Meter'].mean()
    nilai_apf_rata2 = df_10_hari['APF Meter (ION)'].mean()
    nilai_Sum_APF_rata2 = df_10_hari['SUM ALL APF Area'].mean()
    nilai_ems_rata2 = df_10_hari['EMS'].mean()

     # Menampilkan data sesuai dengan tanggal yang dipilih
    nilai_pln = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'PLN Meter'].values[0])
    nilai_apf = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'APF Meter (ION)'].values[0])
    nilai_Sum_APF = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'SUM ALL APF Area'].values[0])
    nilai_ems = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'EMS'].values[0])
    
    # Mencari nilai untuk satu hari sebelum tanggal_dipilih
    tanggal_sebelumnya = tanggal_dipilih - pd.Timedelta(days=1)
    nilai_pln_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'PLN Meter'].values[0])
    nilai_apf_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'APF Meter (ION)'].values[0])
    nilai_Sum_APF_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'SUM ALL APF Area'].values[0])
    nilai_ems_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'EMS'].values[0])
    
    #mencari delta value
    delta_PLN = round(nilai_pln - nilai_pln_sebelumnya, 2)
    delta_APF = round(nilai_apf - nilai_apf_sebelumnya, 2)
    delta_Sum_APF = round(nilai_Sum_APF - nilai_Sum_APF_sebelumnya, 2)
    delta_ems = round(nilai_ems - nilai_ems_sebelumnya, 2)
    
    # add a border
    st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
    # Subjudul
    st.markdown('## Pemakaian Listrik APF Total')
    st.markdown('Berdasarkan pencatatan kWhmeter di GI PLN, GI APF dan Total Pemakaian Seluruh Plant')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label='PLN Meter', value=nilai_pln, delta = delta_PLN)
    with col2:
        st.metric(label='APF Meter (ION)', value=nilai_apf, delta = delta_APF)
    with col3:
        st.metric(label='Sum ALL APF Area', value=nilai_Sum_APF, delta = delta_Sum_APF)
    with col4:
        st.metric(label='EMS', value=nilai_ems, delta = delta_ems)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label='PLN Meter Rata-rata (10 hari)', value=round(nilai_pln_rata2, 2))
    with col2:
        st.metric(label='APF Meter (ION) Rata-rata (10 hari)', value=round(nilai_apf_rata2, 2))
    with col3:
        st.metric(label='Sum ALL APF Area Rata-rata (10 hari)', value=round(nilai_Sum_APF_rata2, 2))
    with col4:
        st.metric(label='EMS Rata-rata (10 hari)', value=round(nilai_ems_rata2, 2))
    
    # Memilih nilai tertinggi dari kolom 'Tanggal'
    tanggal_tertinggi = df['Tanggal'].max()

    # add a border
    st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)

    # Subjudul
    st.markdown('## Pemakaian listrik masing-masing plant')
    st.markdown('Berdasarkan pencatatan kWhmeter di masing-masing plant')

    # Menghitung rata-rata untuk sepuluh hari terakhir
    nilai_poy_rata2 = df_10_hari['POY'].mean()

     # Menampilkan data sesuai dengan tanggal yang dipilih
    nilai_poy = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'POY'].values[0])
    
    # Mencari nilai untuk satu hari sebelum tanggal_dipilih
    nilai_poy_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'POY'].values[0])
    
    #mencari delta value
    delta_poy = round(nilai_poy - nilai_poy_sebelumnya, 2)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label='POY Plant', value=nilai_poy, delta = delta_poy)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label='POY Plant Rata-rata (10 hari)', value=round(nilai_poy_rata2, 2))
    
    
    # add a border
    st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)

    


else:
    st.markdown('#### Anda tidak memiliki otorisasi untuk melihat halaman ini!')

# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
