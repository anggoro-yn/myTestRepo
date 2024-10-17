import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Fungsi untuk membuat grafik pemakaian listrik dalam sepuluh hari terakhir
def buat_grafik_kwh(column_name, nilai_rata2, judul):
    # Membuat grafik batang
    fig, ax = plt.subplots(figsize=(10, 6))

    # Menentukan nilai maksimum, minimum, dan tanggal terbaru
    max_value = df_10_hari[column_name].max()
    min_value = df_10_hari[column_name].min()
    latest_date = df_10_hari['Tanggal'].max()
    
    colors = []
    for index, row in df_10_hari.iterrows():
        if row['Tanggal'] == latest_date:
            colors.append('turquoise')  # Warna untuk tanggal terbaru
        elif row[column_name] == max_value:
            colors.append('crimson')  # Warna untuk nilai y maksimal
        elif row[column_name] == min_value:
            colors.append('limegreen')  # Warna untuk nilai y minimal
        else:
            colors.append('lightgray')  # Warna untuk batang lainnya            

    bars = ax.bar(df_10_hari['Tanggal'], df_10_hari[column_name], color=colors)

    # Menambahkan garis horizontal putus-putus
    ax.axhline(y=nilai_rata2, color='black', linestyle='--') 

    # Mengatur warna batang untuk tanggal terakhir
    #bars[0].set_color('cyan')
    
    # Mengatur posisi tick label di tengah batang
    ax.set_xticks(df_10_hari['Tanggal'])
    ax.set_xticklabels(df_10_hari['Tanggal'].dt.strftime('%Y-%m-%d'), rotation=90, ha='center')
    
    # Menghitung batas sumbu y
    min_value = df_10_hari[column_name].min()
    max_value = df_10_hari[column_name].max()
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
    # Hitung rata-rata untuk setiap kolom
    elec_dict_rata2 = df_10_hari.mean().round(2).to_dict()
    # Tampilkan dictionary menggunakan Streamlit
    st.write(elec_dict_rata2)
    # Hitung rata-rata untuk setiap kolom
    mean_values = df_10_hari.mean()
    
    # Bulatkan ke dua desimal
    rounded_mean_values = mean_values.round(2)
    
    # Convert to dictionary
    elec_dict_rata2 = rounded_mean_values.to_dict()
    
    # Menampilkan data sesuai dengan tanggal yang dipilih
    # Filter dataframe berdasarkan tanggal tertentu
    df_filtered = df[df["Tanggal"] == tanggal_akhir]
    # Buat dictionary dari data yang difilter
    dict_data_tanggal = df_filtered.drop(columns=["Tanggal"]).iloc[0].to_dict()
    # Tampilkan dictionary menggunakan Streamlit
    st.write(dict_data_tanggal)

    # Mencari nilai untuk satu hari sebelum tanggal_dipilih
    tanggal_sebelumnya = tanggal_akhir - pd.Timedelta(days=1)
    # Filter dataframe berdasarkan tanggal tertentu
    df_filtered = df[df["Tanggal"] == tanggal_sebelumnya]
    # Buat dictionary dari data yang difilter
    dict_data_tanggal_sebelumnya = df_filtered.drop(columns=["Tanggal"]).iloc[0].to_dict()
    # Tampilkan dictionary menggunakan Streamlit
    st.write(dict_data_tanggal_sebelumnya)

    #mencari delta value
    # Membuat dictionary dict_c dengan key yang sama dan value adalah hasil pengurangan value dict_A dengan value dict_B
    dict_delta = {key: round(dict_data_tanggal[key] - dict_data_tanggal_sebelumnya[key],2) for key in dict_data_tanggal}
    # Tampilkan dictionary dict_c menggunakan Streamlit
    st.write(dict_delta)
    
    return elec_dict_rata2, dict_data_tanggal, dict_data_tanggal_sebelumnya, dict_delta

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

        # Menyaring data untuk sepuluh hari terakhir
        prod_df_10_hari = prod_df[(prod_df['Tanggal'] >= tanggal_awal) & (prod_df['Tanggal'] <= tanggal_akhir)]
        
        # Menghitung rata-rata untuk sepuluh hari terakhir
        nilai_SP4_rata2 = prod_df_10_hari['SP4'].mean()

        # Menampilkan data sesuai dengan tanggal yang dipilih
        nilai_SP4 = prod_df.loc[prod_df['Tanggal'] == tanggal_dipilih, 'SP4'].values[0]
        
        # Mencari nilai untuk satu hari sebelum tanggal_dipilih
        tanggal_sebelumnya = tanggal_dipilih - pd.Timedelta(days=1)
        nilai_SP4_sebelumnya = prod_df.loc[prod_df['Tanggal'] == tanggal_sebelumnya, 'SP4'].values[0]
        
        #mencari delta value
        delta_SP4 = round(nilai_SP4 - nilai_SP4_sebelumnya, 2)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='SP 4', value=nilai_SP4, delta = delta_SP4) 
    
    with tabElec:
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("## Daily Electricity Dashboard")
        with col2:    
            # Menampilkan tanggal
            st.metric(label="Date", value=tanggal_dipilih.strftime('%d-%m-%Y'))

        st.markdown("Values are shown in MWh (Megawatthour), unless it is stated differently explicitly")

        comment01 = '''
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
        '''
        
        elec_dict_rata2, elec_dict_data_tanggal, elec_dict_data_tanggal_sebelumnya, elec_dict_delta = hitungDataDitampilkan(elec_df, tanggal_awal, tanggal_akhir)
        
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
        # Subjudul
        st.markdown('## Total Electricity Consumption')
        st.markdown('Based on kWhmeter recording at GI PLN, GI APF and Total Plant recording')
    
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
            st.metric(label='PLN Meter', value=round(elec_dict_rata2['PLN Meter'],2))
        with col2:
            st.metric(label='APF Meter (ION)', value=round(elec_dict_rata2['APF Meter (ION)'],2))
        with col3:
            st.metric(label='SUM ALL APF Area', value=elec_dict_rata2['SUM ALL APF Area'])
        with col4:
            st.metric(label='EMS', value=elec_dict_rata2['EMS'])
  
        with st.expander("Click to open electricity consumption chart for 10 days"):
            tab1, tab2, tab3, tab4 = st.tabs(["PLN Meter","ION Meter","APF Sum","EMS"])
            with tab1:
                buat_grafik_kwh('PLN Meter', nilai_pln_rata2, 'Konsumsi listrik berdasar kWhmeter PLN dalam 10 hari terakhir')
            with tab2:
                buat_grafik_kwh('APF Meter (ION)', nilai_apf_rata2, 'Konsumsi listrik berdasar kWhmeter APF dalam 10 hari terakhir')
            with tab3:
                buat_grafik_kwh('SUM ALL APF Area', nilai_Sum_APF_rata2, 'Jumlah Pemakaian Listrik Seluruh Plant dalam 10 hari terakhir')
            with tab4:
                buat_grafik_kwh('EMS', nilai_ems_rata2, 'Konsumsi listrik berdasar EMS dalam 10 hari terakhir')
    
    
        # Memilih nilai tertinggi dari kolom 'Tanggal'
        tanggal_tertinggi = df['Tanggal'].max()
    
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
    
        # Subjudul
        st.markdown('## Plant Electricity consumption')
        st.markdown('Based on kWhmeter recording in each plant')
    
        # Menghitung rata-rata untuk sepuluh hari terakhir
        nilai_poy_rata2 = df_10_hari['POY'].mean()
        nilai_pp_rata2 = df_10_hari['PP'].mean()
        nilai_tx1_rata2 = df_10_hari['TX 1'].mean()
        nilai_tx2_rata2 = df_10_hari['TX 2'].mean()
        nilai_tx3_rata2 = df_10_hari['TX 3'].mean()
        nilai_tx4_rata2 = df_10_hari['TX 4 (+Doubling)'].mean()
        nilai_wrp_rata2 = df_10_hari['WRP'].mean()
        nilai_sp3_rata2 = df_10_hari['SP3 Compressor'].mean()
        nilai_tx2c_rata2 = df_10_hari['TX 2 Compressor'].mean()
    
         # Menampilkan data sesuai dengan tanggal yang dipilih
        nilai_poy = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'POY'].values[0])
        nilai_pp = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'PP'].values[0])
        nilai_tx1 = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'TX 1'].values[0])
        nilai_tx2 = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'TX 2'].values[0])
        nilai_tx3 = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'TX 3'].values[0])
        nilai_tx4 = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'TX 4 (+Doubling)'].values[0])
        nilai_wrp = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'WRP'].values[0])
        nilai_sp3 = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'SP3 Compressor'].values[0])
        nilai_tx2c = float(df.loc[df['Tanggal'] == tanggal_dipilih, 'TX 2 Compressor'].values[0])
        
        # Mencari nilai untuk satu hari sebelum tanggal_dipilih
        nilai_poy_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'POY'].values[0])
        nilai_pp_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'PP'].values[0])
        nilai_tx1_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'TX 1'].values[0])
        nilai_tx2_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'TX 2'].values[0])
        nilai_tx3_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'TX 3'].values[0])
        nilai_tx4_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'TX 4 (+Doubling)'].values[0])
        nilai_wrp_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'WRP'].values[0])
        nilai_sp3_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'SP3 Compressor'].values[0])
        nilai_tx2c_sebelumnya = float(df.loc[df['Tanggal'] == tanggal_sebelumnya, 'TX 2 Compressor'].values[0])
        
        #mencari delta value
        delta_poy = round(nilai_poy - nilai_poy_sebelumnya, 2)
        delta_pp = round(nilai_pp - nilai_pp_sebelumnya, 2)
        delta_tx1 = round(nilai_tx1 - nilai_tx1_sebelumnya, 2)
        delta_tx2 = round(nilai_tx2 - nilai_tx2_sebelumnya, 2)
        delta_tx3 = round(nilai_tx3 - nilai_tx3_sebelumnya, 2)
        delta_tx4 = round(nilai_tx4 - nilai_tx4_sebelumnya, 2)
        delta_wrp = round(nilai_wrp - nilai_wrp_sebelumnya, 2)
        delta_sp3 = round(nilai_sp3 - nilai_sp3_sebelumnya, 2)
        delta_tx2c = round(nilai_tx2c - nilai_tx2c_sebelumnya, 2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label='POY Plant', value=nilai_poy, delta = delta_poy)
        with col2:
            st.metric(label='PP Plant', value=nilai_pp, delta = delta_pp)
    
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label='POY Plant Rata-rata (10 hari)', value=round(nilai_poy_rata2, 2))
        with col2:
            st.metric(label='PP Plant Rata-rata (10 hari)', value=round(nilai_pp_rata2, 2))
    
        
        # add a border
        st.markdown("""<hr style="border:1px dashed gray">""", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='TX 1 Plant', value=nilai_tx1, delta = delta_tx1)
        with col2:
            st.metric(label='TX 2 Plant', value=nilai_tx2, delta = delta_tx2)
        with col3:
            st.metric(label='TX 3 Plant', value=nilai_tx3, delta = delta_tx3)
        with col4:
            st.metric(label='TX 4 & Doubling Plant', value=nilai_tx4, delta = delta_tx4)
    
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label='TX1 Plant Rata-rata (10 hari)', value=round(nilai_tx1_rata2, 2))
        with col2:
            st.metric(label='TX2 Plant Rata-rata (10 hari)', value=round(nilai_tx2_rata2, 2))
        with col3:
            st.metric(label='TX3 Plant Rata-rata (10 hari)', value=round(nilai_tx3_rata2, 2))
        with col4:
            st.metric(label='TX4 & Doubling Plant Rata-rata (10 hari)', value=round(nilai_tx4_rata2, 2))
        
        # add a border
        st.markdown("""<hr style="border:1px dashed gray">""", unsafe_allow_html=True)
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='WRP', value=nilai_wrp, delta = delta_wrp)
        with col2:
            st.metric(label='SP3 Compressor', value=nilai_sp3, delta = delta_sp3)
        with col3:
            st.metric(label='TX2 Compressor', value=nilai_tx2c, delta = delta_tx2c)
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='WRP Plant Rata-rata (10 hari)', value=round(nilai_wrp_rata2, 2))
        with col2:
            st.metric(label='SP3 Compressor Rata-rata (10 hari)', value=round(nilai_sp3_rata2, 2))
        with col3:
            st.metric(label='TX2 Compressor Rata-rata (10 hari)', value=round(nilai_tx2c_rata2, 2))
    
        with st.expander("Click to open electricity consumption chart for 10 days"):
            tabPOY, tabPP, tabTX1, tabTX2, tabTX3, tabTX4, tabWRP, tabSP3, tabTX2C = st.tabs(["POY", "PP", "TX1", "TX2", "TX3", "TX4", "WRP", "SP3 Comp", "TX2 Comp"])
            with tabPOY:
                buat_grafik_kwh('POY', nilai_poy_rata2, 'Konsumsi listrik Plant POY dalam 10 hari terakhir')
            with tabPP:
                buat_grafik_kwh('PP', nilai_pp_rata2, 'Konsumsi listrik Plant PP dalam 10 hari terakhir')
            with tabTX1:
                buat_grafik_kwh('TX 1', nilai_tx1_rata2, 'Konsumsi listrik Plant TX 1 dalam 10 hari terakhir')
            with tabTX2:
                buat_grafik_kwh('TX 2', nilai_tx2_rata2, 'Konsumsi listrik Plant TX 2 dalam 10 hari terakhir')
            with tabTX3:
                buat_grafik_kwh('TX 3', nilai_tx3_rata2, 'Konsumsi listrik Plant TX 3 dalam 10 hari terakhir')
            with tabTX4:
                buat_grafik_kwh('TX 4 (+Doubling)', nilai_tx4_rata2, 'Konsumsi listrik Plant TX 4 dalam 10 hari terakhir')
            with tabWRP:
                buat_grafik_kwh('WRP', nilai_wrp_rata2, 'Konsumsi listrik Recycling Plant dalam 10 hari terakhir')
            with tabSP3:
                buat_grafik_kwh('SP3 Compressor', nilai_sp3_rata2, 'Konsumsi listrik Compressor SP3  dalam 10 hari terakhir')
            with tabTX2C:
                buat_grafik_kwh('TX 2 Compressor', nilai_tx2c_rata2, 'Konsumsi listrik Compressor TX 2  dalam 10 hari terakhir')
    
        
        # add a border
        st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
    
        st.write(df)


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
