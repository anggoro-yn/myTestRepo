import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('hour.csv', delimiter=';')

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.jpg")
    # Menggunakan HTML dan CSS untuk membuat kotak teks dengan latar belakang berwarna
    st.markdown(
        """
        <div style="background-color: 'cyan'; padding: 10px; border-radius: 5px;">
            <p style="font-size: 16px; color: black;">Ini adalah kotak teks dengan latar belakang berwarna cyan.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title('Visualisasi Kelulusan dan Progress Peserta')


# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
