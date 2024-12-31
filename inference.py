# # inference.py
#import locale
#locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

import streamlit as st
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import pandas as pd
from PIL import Image

from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
import nltk
import string
import csv
import re
import os

# nltk.download('punkt')
# nltk.download('punkt_tab')
# Cek apakah resource 'punkt' tersedia
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    # print("Resource 'punkt' sudah terunduh.")
except LookupError:
    # print("Resource 'punkt' belum terunduh. Mengunduh sekarang...")
    nltk.download('punkt')
    nltk.download('punkt_tab')
    # print("Resource 'punkt' telah berhasil diunduh.")


from sentimen import text_prepros
from sentimen import word_tokenize_wrapper
from sentimen import lexicon_to_dict
from sentimen import non_financial

# import Crypto

# @st.cache_data

lexicon = lexicon_to_dict("LM-SA-2020.csv", ",", 1)

# @st.cache_data

# # Muat model dan scaler
# model = joblib.load('ratu_best_model.joblib')
# scaler = StandardScaler()
scaler=joblib.load('ratu_scalers_x.pkl')

@st.cache_data
def load_model():
    return joblib.load('ratu_best_model.joblib')

def run_simulasi_app():
# # UI untuk input
    st.title("Halaman Prediksi")
    
    # alur : upload pdf, isi start page, end page, isi tahun,
    # isi finance
    # predict
    
    START_PAGE_IN_PDF = st.number_input('Halaman Awal', min_value=1, max_value=1000, step=1, value=24)
    END_PAGE_IN_PDF = st.number_input('Halaman Akhir', min_value=1, max_value=1000, step=1, value=29)
    TAHUN = st.number_input('Tahun', min_value=1900, max_value=2024, step=1, value=2000)
        
    
    # Judul halaman
    st.subheader("Upload File PDF")

    # Membuat uploader untuk file PDF
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Menampilkan nama file yang diupload
        st.write(f"File '{uploaded_file.name}' berhasil diupload!")

        # Membaca file PDF
        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        st.write(f"Jumlah halaman: {num_pages}")

        # Menampilkan teks dari halaman pertama (misalnya)
        page = reader.pages[0]
        text = page.extract_text()

        # Menampilkan teks dari halaman pertama
        st.write("Isi halaman pertama:")
        st.text(text)
        
        # ubah disini
        # FILENAME = "AALI_Annual Report_2020.pdf"
        FILENAME =uploaded_file.name
    
        text = ""
        try:
            reader = PdfReader(uploaded_file)
            meta = reader.metadata
            for page in reader.pages[START_PAGE_IN_PDF-1:END_PAGE_IN_PDF]: # IF READ CERTAIN PAGE OF REPORT
                text += " " + page.extract_text()
        except Exception as exc:
            print(TAHUN, FILENAME)
            print(exc)

        # preprocessing
        text = text_prepros(text)
        text = word_tokenize_wrapper(text)
        print(text)

        # if st.button('Ekstrak'):
        result = non_financial(FILENAME, TAHUN, text, lexicon)
        finance = pd.DataFrame(result, index=[0])
        df_finance = pd.DataFrame(columns=['file_name', 'tahun', 'score_constraining', 'score_uncertainty', 'score_strongModal', 'score_litigious', 'score_negative', 'score_positive', 'score_weakModal'])
        df_finance = pd.concat([df_finance, finance], ignore_index=True)
        st.data_editor(df_finance)
        cont= finance.iloc[0]['score_constraining']
                # unct = st.number_input('Uncertainty', min_value=0.0, max_value=52.0, step=0.01)
        unct=finance.iloc[0]['score_uncertainty']
                # strng = st.number_input('Strongmodal', min_value=0.0, max_value=29.0, step=0.01)
        strng=finance.iloc[0]['score_strongModal']
                # litt = st.number_input('Litigious', min_value=0.0, max_value=101.0, step=0.01)
        litt= finance.iloc[0]['score_litigious']
                    # Kolom terakhir (setelah kedua kolom), inputan untuk 'Negative', 'Positive', 'Weak', dan 'Main Industry'
                # neg = st.number_input('Negative', min_value=0.0, max_value=251.0, step=0.01)
        neg = finance.iloc[0]['score_negative']
                # pos = st.number_input('Positive', min_value=0.0, max_value=167.0, step=0.01)
        pos=finance.iloc[0]['score_positive']
                # weak = st.number_input('Weakmodal', min_value=0.0, max_value=20.0, step=0.01)
        weak=finance.iloc[0]['score_weakModal']   
            # Membuat dua kolom
        col1, col2 = st.columns(2)

            # Kolom pertama (col1)
        with col1:
                # omset = float(st.number_input('Omset', min_value=0.0, max_value=99000000000.00, step=0.1))
            omset=float(st.text_input('Omset', '10000000'))
            roa = float(st.number_input('Return on Assets (roa)', min_value=0.0, max_value=0.6, step=0.01))
            roe = st.number_input('Return on Equity (roe)', min_value=0.0, max_value=2.6, step=0.01)
            pm = st.number_input('Profit Margin (pm)', min_value=0.0, max_value=100.0, step=0.01)
                 
            # Kolom kedua (col2)
        with col2:
            gpm = st.number_input('Gross Profit Margin (gpm)', min_value=0.0, max_value=1.0, step=0.01)
            cr = st.number_input('Current Ratio (cr)', min_value=0.0, max_value=1400.0, step=0.1)
            der = st.number_input('Debt to Equity Ratio (der)', min_value=0.0, max_value=191.0, step=0.1)
            dar = st.number_input('Debt to Asset Ratio (dar)', min_value=0.0, max_value=1.0, step=0.01)
                # cont = st.number_input('Constraining', min_value=0.0, max_value=65.0, step=0.01)
        main_industry = st.selectbox('Main Industry', ['Umum / General', 'Keuangan dan Syariah / Financial and Sharia', 'Pembiayaan / Financing'])
    
            
            # Mengubah kategori menjadi numerik
        main_industry_numeric = {
            'Umum / General': 3, 
            'Keuangan dan Syariah / Financial and Sharia': 1, 
            'Pembiayaan / Financing': 2
            }

            # Mengambil nilai numerik yang sesuai dengan pilihan main_industry
        main_industry_value = main_industry_numeric.get(main_industry, None)

            # inverse
            # st.write(neg)
            
        neg_inverse = 0- neg
        weak_inverse = 0- weak
        cons_inverse = 0-cont
        unct_inverse = 0-unct
        litt_inverse = 0-litt
            
            # hasil inputan
        input_data_user = np.array([roa, roe, pm, gpm, cr, der, dar, cont, unct, strng, litt,
                neg, pos, weak, main_industry_value])

            
            
            # Mengumpulkan input menjadi array
        input_data = np.array([roa, roe, pm, gpm, cr, der, dar, cons_inverse, unct_inverse, strng, litt_inverse,
                neg_inverse, pos, weak_inverse, main_industry_value])

            # # Standarisasi inputan
        input_data_scaled = scaler.transform([input_data])
        
        # # Pastikan session_state telah menyimpan nilai prediksi dan status prediksi
        # if 'prediction' not in st.session_state:
        #     st.session_state.prediction = None  # Menyimpan hasil prediksi dalam session state

        # if 'predicted' not in st.session_state:
        #     st.session_state.predicted = False  # Menyimpan status apakah prediksi sudah dilakukan
           
            # Prediksi dengan model
        if st.button('Prediksi') :
            try:
                st.write('Data Inputan')
                judul_columns_user=['roa', 'roe', 'pm', 'gpm', 'cr', 'der', 'dar', 'cons', 'unct', 
                                            'strng', 'litt_inverse','neg', 'pos', 'weak', 'main_industry_value']

                data_frame_user = pd.DataFrame(input_data_user.reshape(1, -1), columns=judul_columns_user)
                st.dataframe(data_frame_user)
                        
                st.write('Data hasil inverse')
                judul_columns = ['roa', 'roe', 'pm', 'gpm', 'cr', 'der', 'dar', 'cons_inverse', 'unct_inverse',
                                'strng', 'litt_inverse','neg_inverse', 'pos', 'weak_inverse', 'main_industry_value']
                data_frame = pd.DataFrame(input_data.reshape(1, -1), columns=judul_columns)
                st.dataframe(data_frame)
                        
                st.write('Data hasil scaled')
                data_frame_scaled = pd.DataFrame(input_data_scaled.reshape(1, -1), columns=judul_columns)
                st.dataframe(data_frame_scaled)
                        
                        
                # Prediksi
                
                prediction_array = load_model().predict(input_data_scaled)  # Model akan mengembalikan array
                st.session_state.prediction = prediction_array[0]  # Ambil nilai prediksi pertama
                st.session_state.predicted = True  # Tandai bahwa prediksi sudah dilakukan

                # Hasil prediksi dan pembentukan teks
                prediction = st.session_state.prediction
                # formatted_prediction = locale.format_string("%0.2f", prediction, grouping=True)
                
                # Menampilkan hasil dalam bentuk teks
                st.warning(f"Prediksi efisiensi kinerja perusahaan adalah:  {prediction:,.2f}", icon="✅")
                
                # st.warning(f"Prediksi efisiensi kinerja perusahaan adalah:  {formatted_prediction}", icon="✅")
                

                # Menghitung laba
                laba = prediction * omset
                # formatted_laba = locale.format_string("%0.2f", laba, grouping=True)
                # st.success(f"Laba yang diprediksi adalah: Rp. {formatted_laba}", icon="✅")
                st.success(f"Laba yang diprediksi adalah: Rp. {laba:,.2f}", icon="✅")   
            except Exception as e:
                st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")
           