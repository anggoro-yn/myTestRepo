import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
hour_df = pd.read_csv('hour.csv')

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.jpg")
    # Menggunakan HTML dan CSS untuk membuat kotak teks dengan latar belakang berwarna
    st.markdown(
        """
        <div style="background-color: #a9a9a9; padding: 10px; border-radius: 5px;">
            <p style="font-size: 16px; color: black;">Dashboard ini adalah tugas akhir Pelatihan Belajar Analisis Data dengan Python, sebagai syarat kelulusan pelatihan.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title('Analisa Bike Sharing Dataset')

# Membuat select box dengan beberapa opsi
option_1 = st.selectbox(
    'Pilihan analisa : ',
    ['Per tahun','Total']
)

if option_1 == 'Per tahun':

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


else:

    # Menghitung rata-rata 'cnt' per season
    avg_cnt_per_season = hour_df.groupby('season')['cnt'].mean().reset_index()
    
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
    ax.set_title('Rata-rata Jumlah Pemakaian Berdasarkan Musim', fontsize=16)
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Pemakaian', fontsize=12)
    
    # Mengatur batas maksimum sumbu y
    ax.set_ylim(0, 300)
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)


print('##################################################################')
print('##################################################################')
print('##################################################################')
print('##################################################################')

string1 = '''

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
