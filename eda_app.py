import streamlit as st 
import pandas as pd 
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

# Data Viz Pkgs
import matplotlib.pyplot as plt 
# import matplotlib
# matplotlib.use('Agg')
import seaborn as sns
# import plotly.express as px


@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    return df

def normalize(data):
    scaler = MinMaxScaler()
    ndf = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    return ndf


def run_eda_app():
    st.subheader("EDA Section")
    data_='df_all.xlsx'
    # submenu = st.sidebar.selectbox("Submenu",['Data Awal'])
    if data_ is not None:
        df=pd.read_excel(data_)
        # if submenu == 'Data Awal':
        # with st.expander('Top 10'):
        def extract_tahun(id_value):
            # Mengambil 4 digit terakhir, jika panjangnya kurang dari 4 karakter, kembalikan NaN
            if len(id_value) >= 4:
                return int(id_value[-4:])
            else:
                return None

           # Mengaplikasikan fungsi pada kolom 'ID' untuk membuat kolom 'tahun'
        df_tahun = df.copy()
        df_tahun['tahun'] = df_tahun['ID'].apply(extract_tahun)

            # Pastikan ada nilai pada kolom tahun
        df_tahun = df_tahun.dropna(subset=['tahun'])

            # Mengurutkan berdasarkan 'tahun' dan 'Laba Komprehensif'
        df_sorted = df_tahun.sort_values(by=['tahun', 'Laba Komprehensif'], ascending=[True, False])

            # Mengelompokkan data berdasarkan tahun
        grouped = df_sorted.groupby('tahun')
           
        # Membuat expander utama "Top 10"
        with st.expander('Top 10'):
            # Menampilkan top 10 untuk setiap tahun dalam satu blok
            for tahun in grouped.groups:
                try:
                    # Cek apakah tahun valid
                    if pd.isna(tahun):
                        st.warning(f"Tahun {tahun} tidak valid, melewatkan...")
                        continue  # Lanjutkan ke iterasi berikutnya jika tahun tidak valid

                    # Menampilkan tahun dan data top 10 untuk tahun tersebut
                    st.write(f"Top 10 {tahun}")  # Menampilkan sub-header untuk tahun
                    # Ambil 10 data teratas untuk tahun tersebut
                    data_tahun = grouped.get_group(tahun)
                    st.dataframe(data_tahun.head(10))  # Menampilkan data top 10
                except Exception as e:
                    # Jika ada error, tampilkan pesan kesalahan
                    st.error(f"Error saat menampilkan data untuk tahun {tahun}: {e}") 
                
                
                    
        with st.expander('Tabel'):
            st.dataframe(df)
                
            
        

        with st.expander("Tipe Data"):
           st.dataframe(df.dtypes)
               

        with st.expander("Ukuran Data"):
            st.dataframe(df.shape)

        with st.expander('Statistik Deskiptif'):
            st.dataframe(df.describe().transpose())

            # with st.expander('Analisis Distribusi'):
            # 	col1,col2 = st.columns([2,2])
            # 	with col1:
            # 		#with st.expander ('Dist Plot of Distibrution'):
            # 			st.write('Distribusi EPS')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="EPS", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Jumlah WP Badan')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="WP_BADAN", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi WP OP Pengusaha')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="WP_OP_PENGUSAHA", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Jumlah Account Representative')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="JUMLAH_AR", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Kepatuhan Penyampaian SPT')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="KEPATUHAN_SPT", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Pertumbuhan Penerimaan')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="PERTUMBUHAN_PENERIMAAN", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Jumlah SP2DK Cair')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="SP2DK_CAIR", kde=True, palette="deep")
            # 			st.pyplot(fig)


            # 	with col2:
            # 		#with st.expander ('Dist Plot of Distibrution'):
            # 			st.write('Distribusi WP OP Karyawan')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="WP_OP_KARYAWAN", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Jumlah Fungsional Pemeriksa')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="JUMLAH_FPP", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Realisasi Anggaran')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="REALISASI_ANGGARAN", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Capaian Penerimaan Pajak')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="CAPAIAN_PENERIMAAN", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Jumlah SP2DK Terbit')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="SP2DK_TERBIT", kde=True, palette="deep")
            # 			st.pyplot(fig)

            # 			st.write('Distribusi Jumlah Pemeriksaan Selesai')
            # 			fig, ax = plt.subplots(figsize=(5,3))
            # 			sns.histplot(data=df, x="PEMERIKSAAN_SELESAI", kde=True, palette="deep")
            # 			st.pyplot(fig)
        data_kolom=df[['EPS', 'Laba Komprehensif','Asset','ROA','Ekuitas','ROE']]
            

           

        with st.expander("Outlier"):

            fig, ax = plt.subplots()
            sns.boxplot(data=df, orient='h', ax=ax)
            ax.set_title('Boxplot')
                #ax.set_xlabel('Keterangan Sumbu X')
                #ax.set_ylabel('Keterangan Sumbu Y')
            st.pyplot(fig)

            df_norm = normalize(data_kolom)
            fig, ax = plt.subplots()
            sns.boxplot(data=df_norm, orient='h', ax=ax)
            ax.set_title('Boxplot Normalisasi')
                #ax.set_xlabel('Keterangan Sumbu X')
                #ax.set_ylabel('Keterangan Sumbu Y')
            st.pyplot(fig)

        with st.expander("Korelasi"):
                
            numeric_df =  df[['EPS', 'Laba Komprehensif','Asset','ROA','Ekuitas','ROE']]

                # Check if there are any numeric columns
            if not numeric_df.empty:
                corr = numeric_df.corr()  # Calculate correlation matrix

                    # Create heatmap
                fig, ax = plt.subplots()
                sns.heatmap(corr, cmap='coolwarm', annot=True, ax=ax, annot_kws={"size": 5})
                ax.set_title('Matriks Korelasi')
                plt.xticks(rotation=80)

                    # Display the plot in Streamlit
                st.pyplot(fig)
            else:
                st.write("Tidak ada kolom numerik untuk dihitung korelasinya.")

                # Optional: Add a test message
                
        