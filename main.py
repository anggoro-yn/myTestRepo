import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Fungsi untuk membuat grafik pemakaian listrik dalam sepuluh hari terakhir
def buat_grafik_kwh(df, column_name, nilai_rata2, judul):
    # Membuat grafik batang
    fig, ax = plt.subplots(figsize=(10, 6))

    # Menentukan nilai maksimum, minimum, dan tanggal terbaru
    max_value = df[column_name].max()
    min_value = df[column_name].min()
    latest_date = df['Tanggal'].max()
    
    colors = []
    for index, row in df.iterrows():
        if row['Tanggal'] == latest_date:
            colors.append('turquoise')  # Warna untuk tanggal terbaru
        elif row[column_name] == max_value:
            colors.append('crimson')  # Warna untuk nilai y maksimal
        elif row[column_name] == min_value:
            colors.append('limegreen')  # Warna untuk nilai y minimal
        else:
            colors.append('lightgray')  # Warna untuk batang lainnya            

    bars = ax.bar(df['Tanggal'], df[column_name], color=colors)

    # Menambahkan garis horizontal putus-putus
    ax.axhline(y=nilai_rata2, color='black', linestyle='--') 

    # Mengatur warna batang untuk tanggal terakhir
    #bars[0].set_color('cyan')
    
    # Mengatur posisi tick label di tengah batang
    ax.set_xticks(df['Tanggal'])
    ax.set_xticklabels(df['Tanggal'].dt.strftime('%Y-%m-%d'), rotation=90, ha='center')
    
    # Menghitung batas sumbu y
    min_value = df[column_name].min()
    max_value = df[column_name].max()
    y_min = min_value - 0.01 * min_value
    y_max = max_value + 0.01 * max_value

    # Mengatur batas sumbu y
    ax.set_ylim(y_min, y_max)

    # Menambahkan label dan judul
    plt.xlabel('Tanggal')
    plt.ylabel('MWh')
    plt.title(judul)
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

    # Memberikan catatan
    st.write("Note:Y-axis doesn't start from zero to emphasize fluctuation.")
    # Tulisan "Highest", "Lowest", dan "Latest" dalam satu baris dengan warna berbeda
    st.markdown("""
    <p>
        <span style="color:crimson;">Highest </span> 
        <span style="color:limegreen;"> Lowest </span> 
        <span style="color:turquoise;"> Latest </span>
        <span style="color:black;"> - - - (average)</span> 
    </p>
    """, unsafe_allow_html=True)

def hitungDataDitampilkan(df, tanggal_awal, tanggal_akhir):
    # Menyaring data untuk sepuluh hari terakhir
    df_10_hari = df[(df['Tanggal'] >= tanggal_awal) & (df['Tanggal'] <= tanggal_akhir)]
    #st.write(df)
    #st.write(df_10_hari)
    # Hitung rata-rata untuk setiap kolom, kecuali kolom 'Tanggal'
    mean_values = df_10_hari.drop(columns=["Tanggal"]).mean()
    # Bulatkan setiap nilai rata-rata ke dua desimal dan buat dictionary
    dict_rata2 = {key: round(value, 2) for key, value in mean_values.items()}
    # Menambahkan kolom 'Tanggal' kembali ke dictionary tanpa perubahan
    dict_rata2['Tanggal'] = df_10_hari['Tanggal'].tolist()
    # Tampilkan dictionary menggunakan Streamlit
    #st.write(dict_rata2)

    
    # Menampilkan data sesuai dengan tanggal yang dipilih
    # Filter dataframe berdasarkan tanggal tertentu
    df_filtered = df[df["Tanggal"] == tanggal_akhir]
    # Buat dictionary dari data yang difilter
    dict_data_tanggal = df_filtered.drop(columns=["Tanggal"]).iloc[0].to_dict()
    # Tampilkan dictionary menggunakan Streamlit
    #st.write(dict_data_tanggal)

    # Mencari nilai untuk satu hari sebelum tanggal_dipilih
    tanggal_sebelumnya = tanggal_akhir - pd.Timedelta(days=1)
    # Filter dataframe berdasarkan tanggal tertentu
    df_filtered = df[df["Tanggal"] == tanggal_sebelumnya]
    # Buat dictionary dari data yang difilter
    dict_data_tanggal_sebelumnya = df_filtered.drop(columns=["Tanggal"]).iloc[0].to_dict()
    # Tampilkan dictionary menggunakan Streamlit
    #st.write(dict_data_tanggal_sebelumnya)

    #mencari delta value
    # Membuat dictionary dict_c dengan key yang sama dan value adalah hasil pengurangan value dict_A dengan value dict_B
    dict_delta = {key: round(dict_data_tanggal[key] - dict_data_tanggal_sebelumnya[key],2) for key in dict_data_tanggal}
    # Tampilkan dictionary dict_c menggunakan Streamlit
    #st.write(dict_delta)
    
    return df_10_hari, dict_rata2, dict_data_tanggal, dict_data_tanggal_sebelumnya, dict_delta

# Load dataset

# Load lectricity dataset
elec_df = pd.read_csv('data.csv', delimiter=';')
elec_df.drop(columns=['Unnamed: 14'], inplace=True)
# Mengubah kolom 'Tanggal' menjadi tipe datetime
elec_df['Tanggal'] = pd.to_datetime(elec_df['Tanggal']) + pd.DateOffset(hours=8)
# Mengurutkan dataframe berdasarkan kolom 'Tanggal' secara descending
elec_df = elec_df.sort_values(by='Tanggal', ascending=False)
# Mengkonversi kolom 'PLN Meter' dan kolom lainnya ke float
# List of columns to be converted
columns_to_convert = [
    'PLN Meter', 'APF Meter (ION)', 'POY', 'TX 1', 'TX 2', 'WRP', 
    'TX 3', 'TX 4 (+Doubling)', 'PP', 'SP3 Compressor', 
    'TX 2 Compressor', 'SUM ALL APF Area', 'EMS'
]
# Loop untuk mengkonversi semua kolom
for col in columns_to_convert:
    elec_df[col] = elec_df[col].str.replace(',', '.').astype(float)



# Load Production dataset
prod_df = pd.read_csv('product.csv', delimiter=';')
# Mengubah kolom 'Tanggal' menjadi tipe datetime
prod_df['Tanggal'] = pd.to_datetime(prod_df['Tanggal']) + pd.DateOffset(hours=8)
# Mengurutkan dataframe berdasarkan kolom 'Tanggal' secara descending
prod_df = prod_df.sort_values(by='Tanggal', ascending=False)
# Mengkonversi kolom numerik ke float
# List of columns to be converted
columns_to_convert = [
    'SP4', 'M1', 'M2', 'T1', 'T2', 'T3 (In house POY)', 
    'T3 (Outsource POY)', 'T3', 'T4 (In house POY)', 'T4 (Outsource POY)', 
    'T4', 'DBL', 'Total', 'Marketable'
]
# Loop untuk mengkonversi semua kolom
for col in columns_to_convert:
    prod_df[col] = prod_df[col].str.replace(',', '.').astype(float)

# Mengambil kolom 'Tanggal' dan memasukkannya ke dalam list 'tanggal_pengukuran'
tanggal_pengukuran = elec_df['Tanggal'].tolist()
tanggal_dipilih = tanggal_pengukuran[0]

# User tool
admin_user = False
general_user = False
name = 'Guest'
dict_user = {'anggoro' : 'password01' ,'rahul':'password02','siska':'password03'}
dict_name = {'anggoro' : 'Anggoro Yudho Nuswantoro' ,'rahul': 'Rahul Bankar','siska':'Siska Rahmawati'}

# Menset page layout
#st.set_page_config(layout="wide")

#################################
# SIDE BAR
#################################
with st.sidebar:
    st.header('User Authentification and Authorizaton')
    name = st.text_input("Username")
    secret_code = st.text_input("Password", type="password")
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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Log in'):
            pass
    with col2:
        if st.button('Log out'):
            admin_user = False
            general_user = False

    st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
    

#################################
# MAIN PAGE
#################################

col1, col2 = st.columns([3,1])
with col1:
    st.title('PT Asia Pacific Fiber Tbk')
with col2:
    st.image('LogoAPF.png', use_column_width=True)

if admin_user or general_user:

    # Memilih tanggal
    col1, col2 = st.columns([3,1])
    with col1:
        # Welcome greeting
        st.markdown("Welcome " + dict_name[name])
        st.markdown("Please choose a date : ")
    with col2:
        tanggal_dipilih = st.selectbox('Date :', tanggal_pengukuran, key="tanggal")
    # Menentukan rentang tanggal untuk sepuluh hari terakhir
    tanggal_awal = tanggal_dipilih - pd.Timedelta(days=9)
    tanggal_akhir = tanggal_dipilih

    # Tab untuk memilih dashboard
    tabElec, tabProduct  = st.tabs(["Electricity", "Product"])
    with tabProduct:
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("## Daily Production Dashboard")
        with col2:    
            # Menampilkan tanggal
            st.metric(label="Date", value=tanggal_dipilih.strftime('%d-%m-%Y'))

        st.markdown("Values are shown in MT (Metric Tonnes), unless it is stated differently explicitly")
        
        # Hitung data-data yang dibutuhkan untuk ditampilkan
        prod_df_10_hari, prod_dict_rata2, prod_dict_data_tanggal, prod_dict_data_tanggal_sebelumnya, prod_dict_delta = hitungDataDitampilkan(prod_df, tanggal_awal, tanggal_akhir)
        
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
        # Subjudul
        st.markdown('## Marketable Production')
        #st.markdown('Based on kWhmeter recording at GI PLN, GI APF and Total Plant recording, showing daily consumption and 10-day average.')
    
        st.metric(label='Marketable', value=prod_dict_data_tanggal['Marketable'], delta = prod_dict_delta['Marketable'])
        buat_grafik_kwh(prod_df_10_hari, 'Marketable', prod_dict_rata2['Marketable'], 'Marketable Production')
        
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)

        with st.expander("Click to open electricity consumption chart for 10 days"):
            tab1, tab2, tab3, tab4 = st.tabs(["PLN Meter","ION Meter","APF Sum","EMS"])
            with tab1:
                buat_grafik_kwh(elec_df_10_hari, 'PLN Meter', elec_dict_rata2['PLN Meter'], 'Electrical Consumption Based on PLN KWhmeter')
            with tab2:
                buat_grafik_kwh(elec_df_10_hari, 'APF Meter (ION)', elec_dict_rata2['APF Meter (ION)'], 'Electrical Consumption Based on APF KWhmeter')
            with tab3:
                buat_grafik_kwh(elec_df_10_hari, 'SUM ALL APF Area', elec_dict_rata2['SUM ALL APF Area'], 'Electrical Consumption Based on All Plants Total Reading')
            with tab4:
                buat_grafik_kwh(elec_df_10_hari, 'EMS', elec_dict_rata2['EMS'], 'Electrical Consumption Based on EMS')
    
    with tabElec:
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("## Daily Electricity Dashboard")
        with col2:    
            # Menampilkan tanggal
            st.metric(label="Date", value=tanggal_dipilih.strftime('%d-%m-%Y'))

        st.markdown("Values are shown in MWh (Megawatthour), unless it is stated differently explicitly")
        
        # Hitung data-data yang dibutuhkan untuk ditampilkan
        elec_df_10_hari, elec_dict_rata2, elec_dict_data_tanggal, elec_dict_data_tanggal_sebelumnya, elec_dict_delta = hitungDataDitampilkan(elec_df, tanggal_awal, tanggal_akhir)
        
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
        # Subjudul
        st.markdown('## Total Electricity Consumption')
        st.markdown('Based on kWhmeter recording at GI PLN, GI APF and Total Plant recording, showing daily consumption and 10-day average.')
    
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='PLN Meter', value=elec_dict_data_tanggal['PLN Meter'], delta = elec_dict_delta['PLN Meter'])
        with col2:
            st.metric(label='APF Meter (ION)', value=elec_dict_data_tanggal['APF Meter (ION)'], delta = elec_dict_delta['APF Meter (ION)'])
        with col3:
            st.metric(label='SUM ALL APF Area', value=elec_dict_data_tanggal['SUM ALL APF Area'], delta = elec_dict_delta['SUM ALL APF Area'])
        with col4:
            st.metric(label='EMS', value=elec_dict_data_tanggal['EMS'], delta = elec_dict_delta['EMS'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='Avg PLN Meter', value=elec_dict_rata2['PLN Meter'])
        with col2:
            st.metric(label='Avg APF Meter (ION)', value=elec_dict_rata2['APF Meter (ION)'])
        with col3:
            st.metric(label='Avg SUM ALL APF Area', value=elec_dict_rata2['SUM ALL APF Area'])
        with col4:
            st.metric(label='Avg EMS', value=elec_dict_rata2['EMS'])
  
        with st.expander("Click to open electricity consumption chart for 10 days"):
            tab1, tab2, tab3, tab4 = st.tabs(["PLN Meter","ION Meter","APF Sum","EMS"])
            with tab1:
                buat_grafik_kwh(elec_df_10_hari, 'PLN Meter', elec_dict_rata2['PLN Meter'], 'Electrical Consumption Based on PLN KWhmeter')
            with tab2:
                buat_grafik_kwh(elec_df_10_hari, 'APF Meter (ION)', elec_dict_rata2['APF Meter (ION)'], 'Electrical Consumption Based on APF KWhmeter')
            with tab3:
                buat_grafik_kwh(elec_df_10_hari, 'SUM ALL APF Area', elec_dict_rata2['SUM ALL APF Area'], 'Electrical Consumption Based on All Plants Total Reading')
            with tab4:
                buat_grafik_kwh(elec_df_10_hari, 'EMS', elec_dict_rata2['EMS'], 'Electrical Consumption Based on EMS')
    
    
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)

        # SUB JUDUL
        st.markdown('## Plant Electricity consumption')
        st.markdown('Based on kWhmeter recording in each plant, showing daily consumption and 10-day average.')

        # PIE CHART PEMAKAIAN LISTRIK PER PLANT
        # Key yang ingin di-drop
        keys_to_drop = ['EMS', 'SUM ALL APF Area', 'APF Meter (ION)', 'PLN Meter']
        
        # Menggunakan dictionary comprehension untuk membuat dictionary baru tanpa key yang di-drop
        filtered_dict = {key: value for key, value in elec_dict_data_tanggal.items() if key not in keys_to_drop}

        # Ekstrak label dan nilai dari dictionary
        labels = list(filtered_dict.keys())
        values = list(filtered_dict.values())
        
        # Buat pie chart menggunakan Matplotlib
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%',colors = ['lightblue', 'lightgreen', 'lightcoral', 'gold', 'violet', 'turquoise', 'lime', 'orange', 'plum'])
        #ax.set_title('Pie Chart dari Dictionary')
        
        # Tampilkan pie chart di Streamlit
        st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label='POY', value=elec_dict_data_tanggal['POY'], delta = elec_dict_delta['POY'])
        with col2:
            st.metric(label='PP', value=elec_dict_data_tanggal['PP'], delta = elec_dict_delta['PP'])
    
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label='Avg POY', value=elec_dict_rata2['POY'])
        with col2:
            st.metric(label='Avg PP', value=elec_dict_rata2['PP'])
        
        # add a border
        st.markdown("""<hr style="border:1px dashed gray">""", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='TX 1', value=elec_dict_data_tanggal['TX 1'], delta = elec_dict_delta['TX 1'])
        with col2:
            st.metric(label='TX 2', value=elec_dict_data_tanggal['TX 2'], delta = elec_dict_delta['TX 2'])
        with col3:
            st.metric(label='TX 3', value=elec_dict_data_tanggal['TX 3'], delta = elec_dict_delta['TX 3'])
        with col4:
            st.metric(label='TX 4 & Doubling Plant', value=elec_dict_data_tanggal['TX 4 (+Doubling)'], delta = elec_dict_delta['TX 4 (+Doubling)'])
    
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='Avg TX1 Plant', value=elec_dict_rata2['TX 1'])
        with col2:
            st.metric(label='Avg TX2 Plant', value=elec_dict_rata2['TX 2'])
        with col3:
            st.metric(label='Avg TX3 Plant', value=elec_dict_rata2['TX 3'])
        with col4:
            st.metric(label='Avg TX4 & DoublingPlant', value=elec_dict_rata2['TX 4 (+Doubling)'])
        
        # add a border
        st.markdown("""<hr style="border:1px dashed gray">""", unsafe_allow_html=True)
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='WRP', value=elec_dict_data_tanggal['WRP'], delta = elec_dict_delta['WRP'])
        with col2:
            st.metric(label='SP3 Compressor', value=elec_dict_data_tanggal['SP3 Compressor'], delta = elec_dict_delta['SP3 Compressor'])
        with col3:
            st.metric(label='TX 2 Compressor', value=elec_dict_data_tanggal['TX 2 Compressor'], delta = elec_dict_delta['TX 2 Compressor'])
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='Avg WRP', value=elec_dict_rata2['WRP'])
        with col2:
            st.metric(label='Avg SP3 Compressor', value=elec_dict_rata2['SP3 Compressor'])
        with col3:
            st.metric(label='Avg TX 2 Compressor', value=elec_dict_rata2['TX 2 Compressor'])
    
        with st.expander("Click to open electricity consumption chart for 10 days"):
            tabPOY, tabPP, tabTX1, tabTX2, tabTX3, tabTX4, tabWRP, tabSP3, tabTX2C = st.tabs(["POY", "PP", "TX1", "TX2", "TX3", "TX4", "WRP", "SP3 Comp", "TX2 Comp"])
            with tabPOY:
                buat_grafik_kwh(elec_df_10_hari, 'POY', elec_dict_rata2['POY'], 'POY Electrical Consumption')
            with tabPP:
                buat_grafik_kwh(elec_df_10_hari, 'PP', elec_dict_rata2['POY'], 'PP Electrical Consumption')
            with tabTX1:
                buat_grafik_kwh(elec_df_10_hari, 'TX 1', elec_dict_rata2['TX 1'], 'TX 1 Electrical Consumption')
            with tabTX2:
                buat_grafik_kwh(elec_df_10_hari, 'TX 2', elec_dict_rata2['TX 2'], 'TX 2 Electrical Consumption')
            with tabTX3:
                buat_grafik_kwh(elec_df_10_hari, 'TX 3', elec_dict_rata2['TX 3'], 'TX 3 Electrical Consumption')
            with tabTX4:
                buat_grafik_kwh(elec_df_10_hari, 'TX 4 (+Doubling)', elec_dict_rata2['TX 4 (+Doubling)'], 'TX 4 & Doubling Electrical Consumption')
            with tabWRP:
                buat_grafik_kwh(elec_df_10_hari, 'WRP', elec_dict_rata2['WRP'], 'WRP Electrical Consumption')
            with tabSP3:
                buat_grafik_kwh(elec_df_10_hari, 'SP3 Compressor', elec_dict_rata2['SP3 Compressor'], 'SP3 Compressor Electrical Consumption')
            with tabTX2C:
                buat_grafik_kwh(elec_df_10_hari, 'TX 2 Compressor', elec_dict_rata2['TX 2 Compressor'], 'TX 2 Compressor Electrical Consumption')
    
        
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
    
        st.write(elec_df)


else:
    # Welcome greeting
    st.markdown("Welcome Guest. ")
    st.markdown('#### You are not authorized to view the webpage. Please login first!')

# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
