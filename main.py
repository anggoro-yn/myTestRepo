import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

######################################
# FUNGSI + DATA + DLL
######################################

# Load dataset
hour_df = pd.read_csv('hour.csv')
# Data tambahan
periode = {'season': 'Musim', 'mnth': 'Bulan', 'hr': 'Jam'}
dict_season = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
list_season = ['Dingin', 'Semi', 'Panas', 'Gugur']
dict_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
list_month = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

def tampil_barchart_pertahun(period, label):
    # Menghitung rata-rata 'cnt' per period dan per tahun
    avg_cnt_per_period_year = hour_df.groupby([period, 'yr'])['cnt'].mean().reset_index()
    
    # Mengubah kolom 'yr' menjadi nama tahun yang lebih jelas
    avg_cnt_per_period_year['yr'] = avg_cnt_per_period_year['yr'].replace({0: '2011', 1: '2012'})
    
    # Membuat bar chart menggunakan seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(ax=ax, x=period, y='cnt', hue='yr', data=avg_cnt_per_period_year)
    
    # Mengubah label pada sumbu x
    period_labels = label
    ax.set_xticklabels([period_labels.get(i, 'Unknown') for i in avg_cnt_per_period_year[period].unique()])
    
    # Menambahkan judul dan label
    ax.set_title('Rata-rata Penggunaan Sepeda per ' + periode[period] + ' untuk Tahun 2011 dan 2012', fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda', fontsize=12)

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

def tampil_barchart_total(period, label):
    # Menghitung rata-rata 'cnt' per season
    avg_cnt_per_period = hour_df.groupby(period)['cnt'].mean().reset_index()
    
    # Menentukan warna untuk setiap batang
    #colors = ['gray'] * len(avg_cnt_per_period)  # Semua batang berwarna abu-abu
    #max_index = avg_cnt_per_period['cnt'].idxmax()  # Indeks nilai maksimum
    #min_index = avg_cnt_per_period['cnt'].idxmin()  # Indeks nilai minimum
    
    # Mengubah warna batang maksimum dan minimum menjadi biru
    #colors[max_index] = 'cyan'
    #colors[min_index] = 'cyan'
    
    # Membuat bar chart menggunakan seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(ax=ax, x=period, y='cnt', data=avg_cnt_per_period) #, palette=colors)
    
    # Mengubah label pada sumbu x
    period_labels = label
    ax.set_xticklabels([period_labels[i] for i in avg_cnt_per_period[period]], rotation=0)
    
    # Menambahkan judul dan label
    ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan ' + periode[period], fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    
def tampil_boxplot_pertahun(period, label):
    # Membuat figure untuk boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Membuat boxplot dengan hue berdasarkan tahun (yr)
    sns.boxplot(x=period, y='cnt', hue='yr', data=hour_df, ax=ax)
    
    # Menambahkan judul dan label pada grafik
    periode = {'season': 'Musim', 'mnth': 'Bulan', 'hr': 'Jam'}
    ax.set_title('Penggunaan Sepeda per ' + periode[period] + ' untuk Tahun 2011 dan 2012', fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
    
    # Mengubah label pada sumbu x untuk musim
    ax.set_xticklabels(label)
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

def tampil_boxplot_total(period, label):
    # Membuat figure untuk boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Membuat boxplot
    sns.boxplot(x=period, y='cnt', data=hour_df, ax=ax)
    
    # Menambahkan judul dan label pada grafik
    ax.set_title('Penggunaan Sepeda per ' + periode[period], fontsize=16)
    ax.set_xlabel(periode[period], fontsize=12)
    ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
    
    # Mengubah label pada sumbu x untuk musim
    ax.set_xticklabels(label)
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    


######################################################
# WEBPAGE
######################################################

# Mengatur konfigurasi halaman
st.set_page_config(
    page_title="Analisis Data Bike Sharing",
    page_icon="🚲",
    layout="wide",  # Mengatur layout menjadi wide (lebih lebar)
    initial_sidebar_state="expanded"  # Menampilkan sidebar dalam kondisi terbuka
)

with st.sidebar:
    # Menambahkan logo
    st.image("logo.jpg")
    with st.expander('About this page'):
        # Menggunakan HTML dan CSS untuk membuat kotak teks dengan latar belakang berwarna
        st.markdown(
            """
            <div>
                <p style="font-size: 16px; color: black;">Dashboard ini adalah tugas akhir Pelatihan Belajar Analisis Data dengan Python, sebagai syarat kelulusan pelatihan.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.title('Analisa Bike Sharing Dataset')

st.markdown(
    """
    <div>
        <p style="font-size: 16px; color: black;">Aplikasi ini melakukan analisa terhadap dataset bike sharing. Dataset yang digunakan menunjukkan pemakaian sepeda pada tahun 2011 dan 2012.</p>
    </div>
    """,
    unsafe_allow_html=True
)

##########################
# MUSIM DAN BULAN
##########################
st.header('Pola Pemakaian Sepeda Berdasar Musim dan Bulan')

pembuka_1 = '''\
Analisa pertama yang akan kita lakukan adalah melihat pola pemakaian sepeda per musim dan bulan. Melalui analisa ini \
kita ingin melihat hubungan antara musim dan bulan dengan tingkat pemakaian sepeda. Manfaat dilakukannya analisa ini adalah kita bisa \
merencakanan penyediaan sepeda secara optimal dan rencana perawatan rutin tahunan. ')\
'''
st.write(pembuka_1)

# Membuat select box dengan beberapa opsi
option_1_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total'],
    key = 'option_1'
)

if option_1_1 == 'Per tahun':
    tab1, tab2 = st.tabs(['Musim', 'Bulan'])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('season', dict_season)
        with col2:
            tampil_boxplot_pertahun('season', list_season)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_pertahun('mnth', dict_month)
        with col2:
            tampil_boxplot_pertahun('mnth', list_month)
else:
    tab1, tab2 = st.tabs(['Musim', 'Bulan'])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('season', dict_season)
        with col2:
            tampil_boxplot_total('season', list_season)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            tampil_barchart_total('mnth', dict_month)
        with col2:
            tampil_boxplot_total('mnth', list_month)

hasil_analisa_1 = ''' \
Berdasar visualisasi di atas, kita bisa melihat bahwa terdapat hubungan yang erat antara pemakaian sepeda dan musim serta bulan yang sedang berjalan. \
Kita bisa melihat bahwa pemakaian terendah pada musim dingin, yang berlangsung dari akhir Desember sampai dengan akhir Maret, sedangkan pemakaian \
tertinggi di saat musim panas, berlangsung dari akhir Juni sampai dengan akhir September. Di musim semi dan musim gugur, \
pemakaian relatif tinggi, walaupun tidak setinggi di musim panas.

Visualisasi menggunakan boxplot menunjukkan bahwa ada cukup banyak nilai outlier. Hal ini berarti bahwa di musim dingin, saat pemakaian sepeda \
secara rata-rata rendah, ada saat-saat tertentu di mana ada tingkat pemakaian yang tinggi, bahkan melebihi rata-rata pemakaian di musim semi, \
panas dan gugur. 
'''

rekomendasi_1 ='''\
Berdasarkan temuan di atas, ada beberapa hal yang bisa ditindaklanjuti, yaitu:
1. Memfokuskan perawatan rutin tahunan di musim dingin (terutama di bulan Januari dan Februari) agar saat masuk musim semi, sepeda-sepeda yang akan digunakan sudah kembali \
dalam kondisi bagus dan dapat bertahan hingga musim dingin berikutnya.
2. Mengatur penyediaan sepeda di musim dingin agar tidak terlalu banyak sepeda yang _idle_ tak terpakai, namun tetap memastikan bahwa \
tersedia cukup sepeda jika terjadi lonjakan pemakaian.
3. Mengatur penyediaan sepeda di musim semi hingga musim gugur agar selalu tersedia cukup sepeda untuk digunakan para pengguna yang secara rata-rata cukup tinggi.
'''

st.write(hasil_analisa_1)
st.write(rekomendasi_1)

# 
# JAM DAN HARI
#
st.header('Pola Pemakaian Sepeda Berdasar Jam dan Hari')

pembuka_2 = '''\
Analisa berikutnya yang akan kita lakukan adalah melihat pola pemakaian sepeda berdasarkan jam dan hari pemakaian. Melalui analisa ini \
kita ingin melihat hubungan antara jam dan hari pemakaian dengan tingkat pemakaian sepeda. Manfaat dilakukannya analisa ini adalah kita bisa \
merencakanan penyediaan sepeda secara optimal dan rencana perawatan rutin harian dan mingguan. ')\
'''
st.write(pembuka_2)

# Membuat select box dengan beberapa opsi
option_2_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total'],
    key='option_2'
)

if option_2_1 == 'Per tahun':
    tabJam, tabHari = st.tabs(['Jam', 'Hari'])
    with tabJam:
        col1, col2 = st.columns(2)
        with col1:
            # Menghitung rata-rata 'cnt' per jam dan per tahun
            avg_cnt_per_hour_year = hour_df.groupby(['hr', 'yr'])['cnt'].mean().reset_index()
            
            # Mengubah kolom 'yr' menjadi nama tahun yang lebih jelas
            avg_cnt_per_hour_year['yr'] = avg_cnt_per_hour_year['yr'].replace({0: '2011', 1: '2012'})
            
            # Membuat bar chart menggunakan seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(ax=ax, x='hr', y='cnt', hue='yr', data=avg_cnt_per_hour_year)
            
            # Mengubah label pada sumbu x
            #season_labels = {0: 'Dingin', 1: 'Semi', 2: 'Panas', 3: 'Gugur'}
            #ax.set_xticklabels([season_labels.get(i, 'Unknown') for i in avg_cnt_per_season_year['season'].unique()])
            
            # Menambahkan judul dan label
            ax.set_title('Rata-rata Penggunaan Sepeda per Jam untuk Tahun 2011 dan 2012', fontsize=16)
            ax.set_xlabel('Jam', fontsize=12)
            ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda', fontsize=12)
        
            # Mengatur batas maksimum sumbu y
            #ax.set_ylim(0, 300)
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
    
        with col2:
            # Membuat figure untuk boxplot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Membuat boxplot dengan hue berdasarkan tahun (yr)
            sns.boxplot(x='hr', y='cnt', hue='yr', data=hour_df, ax=ax)
            
            # Menambahkan judul dan label pada grafik
            ax.set_title('Penggunaan Sepeda per Jam untuk Tahun 2011 dan 2012', fontsize=16)
            ax.set_xlabel('Jam', fontsize=12)
            ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
            
            # Mengubah label pada sumbu x untuk musim
            #ax.set_xticklabels(['Dingin', 'Semi', 'Panas', 'Gugur'])
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
    with tabHari:
        col1, col2 = st.columns(2)
        with col1:
            # Menghitung rata-rata 'cnt' per bulan dan per tahun
            avg_cnt_per_month_year = hour_df.groupby(['mnth', 'yr'])['cnt'].mean().reset_index()
            
            # Mengubah kolom 'yr' menjadi nama tahun yang lebih jelas
            avg_cnt_per_month_year['yr'] = avg_cnt_per_month_year['yr'].replace({0: '2011', 1: '2012'})
            
            # Membuat bar chart menggunakan seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(ax=ax, x='mnth', y='cnt', hue='yr', data=avg_cnt_per_month_year)
            
            # Mengubah label pada sumbu x
            # season_labels = {0: 'Dingin', 1: 'Semi', 2: 'Panas', 3: 'Gugur'}
            # ax.set_xticklabels([season_labels.get(i, 'Unknown') for i in avg_cnt_per_season_year['season'].unique()])
            
            # Menambahkan judul dan label
            ax.set_title('Rata-rata Penggunaan Sepeda per bulan untuk Tahun 2011 dan 2012', fontsize=16)
            ax.set_xlabel('Bulan', fontsize=12)
            ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda', fontsize=12)
        
            # Mengatur batas maksimum sumbu y
            ax.set_ylim(0, 350)
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
        with col2:
            # Membuat figure untuk boxplot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Membuat boxplot dengan hue berdasarkan tahun (yr)
            sns.boxplot(x='mnth', y='cnt', hue='yr', data=hour_df, ax=ax)
            
            # Menambahkan judul dan label pada grafik
            ax.set_title('Penggunaan Sepeda per Bulan untuk Tahun 2011 dan 2012', fontsize=16)
            ax.set_xlabel('Bulan', fontsize=12)
            ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
            
            # Mengubah label pada sumbu x untuk musim
            ax.set_xticklabels(['Dingin', 'Semi', 'Panas', 'Gugur'])
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)


else:
    tab1, tab2 = st.tabs(['Musim', 'Bulan'])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Menghitung rata-rata 'cnt' per season
            avg_cnt_per_season = hour_df.groupby('season')['cnt'].mean().reset_index()
            
            # Menentukan warna untuk setiap batang
            #colors = ['gray'] * len(avg_cnt_per_season)  # Semua batang berwarna abu-abu
            #max_index = avg_cnt_per_season['cnt'].idxmax()  # Indeks nilai maksimum
            #min_index = avg_cnt_per_season['cnt'].idxmin()  # Indeks nilai minimum
            
            # Mengubah warna batang maksimum dan minimum menjadi biru
            #colors[max_index] = 'cyan'
            #colors[min_index] = 'cyan'
            
            # Membuat bar chart menggunakan seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(ax=ax, x='season', y='cnt', data=avg_cnt_per_season) #, palette=colors)
            
            # Mengubah label pada sumbu x
            season_labels = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
            ax.set_xticklabels([season_labels[i] for i in avg_cnt_per_season['season']], rotation=0)
            
            # Menambahkan judul dan label
            ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan Musim', fontsize=16)
            ax.set_xlabel('Musim', fontsize=12)
            ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)
            
            # Mengatur batas maksimum sumbu y
            ax.set_ylim(0, 300)
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
        with col2:
            # Membuat figure untuk boxplot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Membuat boxplot dengan hue berdasarkan tahun (yr)
            sns.boxplot(x='season', y='cnt', data=hour_df, ax=ax)
            
            # Menambahkan judul dan label pada grafik
            ax.set_title('Penggunaan Sepeda per Musim', fontsize=16)
            ax.set_xlabel('Musim', fontsize=12)
            ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
            
            # Mengubah label pada sumbu x untuk musim
            ax.set_xticklabels(['Dingin', 'Semi', 'Panas', 'Gugur'])
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            # Menghitung rata-rata 'cnt' per season
            avg_cnt_per_month = hour_df.groupby('mnth')['cnt'].mean().reset_index()
            
            # Menentukan warna untuk setiap batang
            #colors = ['gray'] * len(avg_cnt_per_month)  # Semua batang berwarna abu-abu
            #max_index = avg_cnt_per_month['cnt'].idxmax()  # Indeks nilai maksimum
            #min_index = avg_cnt_per_month['cnt'].idxmin()  # Indeks nilai minimum
            
            # Mengubah warna batang maksimum dan minimum menjadi biru
            #colors[max_index] = 'cyan'
            #colors[min_index] = 'cyan'
            
            # Membuat bar chart menggunakan seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(ax=ax, x='mnth', y='cnt', data=avg_cnt_per_month) #, palette=colors)
            
            # Mengubah label pada sumbu x
            month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
            ax.set_xticklabels([month_labels[i] for i in avg_cnt_per_month['mnth']], rotation=0)
            
            # Menambahkan judul dan label
            ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan Bulan', fontsize=16)
            ax.set_xlabel('Bulan', fontsize=12)
            ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)
            
            # Mengatur batas maksimum sumbu y
            ax.set_ylim(0, 300)
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
        with col2:
            # Membuat figure untuk boxplot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Membuat boxplot dengan hue berdasarkan tahun (yr)
            sns.boxplot(x='mnth', y='cnt', data=hour_df, ax=ax)
            
            # Menambahkan judul dan label pada grafik
            ax.set_title('Penggunaan Sepeda per Bulan', fontsize=16)
            ax.set_xlabel('Bulan', fontsize=12)
            ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
            
            # Mengubah label pada sumbu x untuk musim
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep','Okt','Nov','Des'])
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)


hasil_analisa_1 = ''' \
Berdasar visualisasi di atas, kita bisa melihat bahwa terdapat hubungan yang erat antara pemakaian sepeda dan musim serta bulan yang sedang berjalan. \
Kita bisa melihat bahwa pemakaian terendah pada musim dingin, yang berlangsung dari akhir Desember sampai dengan akhir Maret, sedangkan pemakaian \
tertinggi di saat musim panas, berlangsung dari akhir Juni sampai dengan akhir September. Di musim semi dan musim gugur, \
pemakaian relatif tinggi, walaupun tidak setinggi di musim panas.

Visualisasi menggunakan boxplot menunjukkan bahwa ada cukup banyak nilai outlier. Hal ini berarti bahwa di musim dingin, saat pemakaian sepeda \
secara rata-rata rendah, ada saat-saat tertentu di mana ada tingkat pemakaian yang tinggi, bahkan melebihi rata-rata pemakaian di musim semi, \
panas dan gugur. 
'''

rekomendasi_1 ='''\
Berdasarkan temuan di atas, ada beberapa hal yang bisa ditindaklanjuti, yaitu:
1. Memfokuskan perawatan rutin tahunan di musim dingin (terutama di bulan Januari dan Februari) agar saat masuk musim semi, sepeda-sepeda yang akan digunakan sudah kembali \
dalam kondisi bagus dan dapat bertahan hingga musim dingin berikutnya.
2. Mengatur penyediaan sepeda di musim dingin agar tidak terlalu banyak sepeda yang _idle_ tak terpakai, namun tetap memastikan bahwa \
tersedia cukup sepeda jika terjadi lonjakan pemakaian.
3. Mengatur penyediaan sepeda di musim semi hingga musim gugur agar selalu tersedia cukup sepeda untuk digunakan para pengguna yang secara rata-rata cukup tinggi.
'''

st.write(hasil_analisa_1)
st.write(rekomendasi_1)


print('##################################################################')
print('##################################################################')
print('##################################################################')
print('##################################################################')

string100 = '''

# Filter data untuk tahun pertama (yr = 0)
hour_df_year1 = hour_df[hour_df['yr'] == 0]

# Menghitung rata-rata 'cnt' per season hanya untuk tahun pertama
avg_cnt_per_season = hour_df_year1.groupby('season')['cnt'].mean().reset_index()

# Menentukan warna untuk setiap batang
colors = ['gray'] * len(avg_cnt_per_season)  # Semua batang berwarna abu-abu
max_index = avg_cnt_per_season['cnt'].idxmax()  # Indeks nilai maksimum
min_index = avg_cnt_per_season['cnt'].idxmin()  # Indeks nilai minimum

# Mengubah warna batang maksimum dan minimum menjadi biru
colors[max_index] = 'cyan'
colors[min_index] = 'cyan'

# Membuat bar chart menggunakan seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(ax=ax, x='season', y='cnt', data=avg_cnt_per_season, palette=colors)

# Mengubah label pada sumbu x
season_labels = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
ax.set_xticklabels([season_labels[i] for i in avg_cnt_per_season['season']], rotation=0)

# Menambahkan judul dan label
ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan Musim pada Tahun Pertama', fontsize=16)
ax.set_xlabel('Musim', fontsize=12)
ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)

# Mengatur batas maksimum sumbu y
ax.set_ylim(0, 300)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Filter data untuk tahun kedua (yr = 1)
hour_df_year1 = hour_df[hour_df['yr'] == 1]

# Menghitung rata-rata 'cnt' per season hanya untuk tahun pertama
avg_cnt_per_season = hour_df_year1.groupby('season')['cnt'].mean().reset_index()

# Menentukan warna untuk setiap batang
colors = ['gray'] * len(avg_cnt_per_season)  # Semua batang berwarna abu-abu
max_index = avg_cnt_per_season['cnt'].idxmax()  # Indeks nilai maksimum
min_index = avg_cnt_per_season['cnt'].idxmin()  # Indeks nilai minimum

# Mengubah warna batang maksimum dan minimum menjadi biru
colors[max_index] = 'cyan'
colors[min_index] = 'cyan'

# Membuat bar chart menggunakan seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(ax=ax, x='season', y='cnt', data=avg_cnt_per_season, palette=colors)

# Mengubah label pada sumbu x
season_labels = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
ax.set_xticklabels([season_labels[i] for i in avg_cnt_per_season['season']], rotation=0)

# Menambahkan judul dan label
ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan Musim pada Tahun Pertama', fontsize=16)
ax.set_xlabel('Musim', fontsize=12)
ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)

# Mengatur batas maksimum sumbu y
ax.set_ylim(0, 300)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

'''


########################




##########################





# Menambahkan footer atau caption di bagian bawah aplikasi
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
