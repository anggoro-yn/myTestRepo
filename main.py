import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

#
# Load dataset
#
hour_df = pd.read_csv('hour.csv')

# Mengatur konfigurasi halaman
st.set_page_config(
    page_title="Analisis Data Bike Sharing",
    page_icon="🚲",
    layout="wide",  # Mengatur layout menjadi wide (lebih lebar)
    initial_sidebar_state="expanded"  # Menampilkan sidebar dalam kondisi terbuka
)

with st.sidebar:
    # Menambahkan logo perusahaan
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

#
# MAIN PAGE
#

st.title('Analisa Bike Sharing Dataset')

st.markdown(
    """
    <div>
        <p style="font-size: 16px; color: black;">Aplikasi ini melakukan analisa terhadap dataset bike sharing. Dataset yang digunakan menunjukkan pemakaian sepeda pada tahun 2011 dan 2012.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.header('Pola Pemakaian Sepeda Berdasar Musim dan Bulan')

pembuka_1 = '''\
Analisa pertama yang akan kita lakukan adalah melihat pola pemakaian sepeda per musim dan bulan. Melalui analisa ini \
kita ingin melihat hubungan antara musim dengan pemakaian sepeda. Manfaat dilakukannya analisa ini adalah kita bisa \
merencakanan penyediaan sepeda secara optimal dan rencana perawatan rutin. ')\
'''
st.write(pembuka_1)

# Membuat select box dengan beberapa opsi
option_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total']
)

if option_1 == 'Per tahun':
    tab1, tab2 = st.tabs(['Musim', 'Bulan'])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Menghitung rata-rata 'cnt' per season dan per tahun
            avg_cnt_per_season_year = hour_df.groupby(['season', 'yr'])['cnt'].mean().reset_index()
            
            # Mengubah kolom 'yr' menjadi nama tahun yang lebih jelas
            avg_cnt_per_season_year['yr'] = avg_cnt_per_season_year['yr'].replace({0: '2011', 1: '2012'})
            
            # Membuat bar chart menggunakan seaborn
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(ax=ax, x='season', y='cnt', hue='yr', data=avg_cnt_per_season_year)
            
            # Mengubah label pada sumbu x
            season_labels = {0: 'Dingin', 1: 'Semi', 2: 'Panas', 3: 'Gugur'}
            ax.set_xticklabels([season_labels.get(i, 'Unknown') for i in avg_cnt_per_season_year['season'].unique()])
            
            # Menambahkan judul dan label
            ax.set_title('Rata-rata Penggunaan Sepeda per Musim untuk Tahun 2011 dan 2012', fontsize=16)
            ax.set_xlabel('Musim', fontsize=12)
            ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda', fontsize=12)
        
            # Mengatur batas maksimum sumbu y
            ax.set_ylim(0, 300)
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
    
        with col2:
            # Membuat figure untuk boxplot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Membuat boxplot dengan hue berdasarkan tahun (yr)
            sns.boxplot(x='season', y='cnt', hue='yr', data=hour_df, ax=ax)
            
            # Menambahkan judul dan label pada grafik
            ax.set_title('Penggunaan Sepeda per Musim untuk Tahun 2011 dan 2012', fontsize=16)
            ax.set_xlabel('Musim', fontsize=12)
            ax.set_ylabel('Jumlah Penggunaan Sepeda', fontsize=12)
            
            # Mengubah label pada sumbu x untuk musim
            ax.set_xticklabels(['Dingin', 'Semi', 'Panas', 'Gugur'])
            
            # Menampilkan grafik di Streamlit
            st.pyplot(fig)
    with tab2:
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
            #season_labels = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
            #ax.set_xticklabels([season_labels[i] for i in avg_cnt_per_season['season']], rotation=0)
            
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
Berdasar visualisasi di atas, kita bisa melihat bahwa terdapat hubungan yang erat antara pemakaian sepeda dan musim yang sedang terjadi. \
Kita bisa melihat bahwa pemakaian terendah pada musim dingin, sedangkan pemakaian tertinggi di saat musim panas. Di musim semi dan musim gugur, \
pemakaian relatif tinggi, walaupun tidak setinggi di musim panas.

Visualisasi menggunakan boxplot menunjukkan bahwa ada cukup banyak nilai outlier. Hal ini berarti bahwa di musim dingin, saat pemakaian sepeda \
secara rata-rata rendah, ada saat-saat tertentu di mana ada tingkat pemakaian yang tinggi, bahkan melebihi rata-rata pemakaian di musim semi, \
panas dan gugur. 
'''

rekomendasi_1 ='''\
Berdasarkan temuan di atas, ada beberapa hal yang bisa ditindaklanjuti, yaitu:
1. Memfokuskan perawatan rutin tahunan di musim dingin agar saat masuk musim semi, sepeda-sepeda yang akan digunakan sudah kembali \
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
