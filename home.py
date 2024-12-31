

import streamlit as st 
import streamlit.components.v1 as stc 
from PIL import Image

from eda_app import run_eda_app



# from prep_app import run_prep_app
# from klaster_app import run_cl_app
# from dea_app import run_dea_app
# from regresi import run_regresi_app


from inference import run_simulasi_app

st.set_page_config(page_title="Prediksi Kinerja Keuangan",
		   page_icon="📈",
		   layout="wide")



html_temp = """
		<div style="background-color:#3872fb;padding:5px;border-radius:10px">
		<h3 style="color:white;text-align:center;font-family:arial;">Prediksi Kinerja Keuangan </h3>
		<h3 style="color:white;text-align:center;"></h3>
		<h4 style="color:white;text-align:center;font-family:arial;">--Prototype--</h4>
		</div>
		"""

def main():
	#st.title("ML Web App with Streamlit")
	stc.html(html_temp)

	menu = ["Home","EDA","Simulasi Prediksi","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		# st.subheader("Home")
		st.write("""
			#### Prediksi Kinerja Keuangan
			Disusun oleh : Ratu Najmil Huda
			###### Sebagai salah satu syarat untuk memperoleh gelar Magister Komputer pada Universitas Budiluhur
			""")
		image='gambar_depan.jpg'
		st.image(image, use_container_width=True)
		st.markdown("""
			<div style="text-align:left;">
				<h4>App Content</h4>
				<ul>
					<li>EDA Section: Exploratory Data Analysis of Data</li>
					<li>Inference Section: ML Predictor App</li>
				</ul>
			</div>
		""", unsafe_allow_html=True)
		
	elif choice == "EDA":
		run_eda_app()

	elif choice == "Simulasi Prediksi":
		run_simulasi_app()


	else:
		st.subheader("About")
		st.text("Prototype ini dibuat menggunakan framework streamlit dengan bahasa pemrograman python")
		

if __name__ == '__main__':
	main()