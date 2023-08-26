from st_aggrid import AgGrid
import streamlit as st
import pandas as pd 
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
#from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from  PIL import Image





st.set_page_config(layout='wide') #Choose wide mode as the default setting

st.markdown(
    """
    <style>
    body {
        background-color: #fff;  /* Fondo blanco */
    }

    .font {
        font-size: 24px;  /* Tamaño de fuente personalizado */
        font-family: 'Arial, sans-serif';  /* Fuente personalizada */
        color: #000;  /* Color de fuente (negro) */
        padding: 10px;  /* Espaciado alrededor del texto */
        border-radius: 10px;  /* Bordes redondeados */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);  /* Sombra */
        border: 2px solid #007bff;  /* Borde azul */
    }
    </style>
    """,
    unsafe_allow_html=True
)


#Add a logo (optional) in the sidebar
logo = Image.open(r'D:\Users\jproncancio\OneDrive - Efigas S.A. E.S.P\innovaCienciaDatos\Casos2023\TMdatalandia\static\icons\efi.png')
st.sidebar.image(logo,  width=120)

#Add the expander to provide some information about the app
with st.sidebar.expander("Modo de empleo:"):
     st.write("""
        Puedes usar la aplicación de perfilado de datos para hacer una EDA o Análisis expliratorio de tus datos.
              
        1. Selecciona un archivo desde el botón <<Browse files>> del area de trabajo en la derecha para cargarlo a la aplicación.
              Tus datos serán presentados en una tabla.
              
        2. Puedes seleccionar entre dos tipos de informe (minimo y Completo) y seleccionar todas las variables o un subconjunto de variables mas pequeño para elaborar el reporte. Esta opción se encuentra en el panel de la izquierda.
              
        3. Presiona el botón de <<Generar reporte>> ubicado en la parte inferior de la tabla de la muestra de tus datos.
              Se generará un reporte Análisis Exporatorio de datos (EDA).
              
        4. Para imprimirlo o enviarlo a PDF con las teclas presiona las teclas CTR SHIFT P y selecciona la opción indicada.
     """)


st.markdown(
    """
    <style>
    .font {
        font-size: 24px;  /* Tamaño de fuente personalizado */
        font-family: 'Arial, sans-serif';  /* Fuente personalizada */
        color: #000;  /* Color de fuente (negro) */
        background-color: #fff;  /* Fondo blanco */
        padding: 10px;  /* Espaciado alrededor del texto */
        border-radius: 10px;  /* Bordes redondeados */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);  /* Sombra */
        border: 2px solid #007bff;  /* Borde azul */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<p class="font">Importa tus datos y genera un informe de perfilado de datos de manera sencilla...</p>', unsafe_allow_html=True)


uploaded_file = st.file_uploader("Carga tu archivo csv:", type=['csv'])
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    option1=st.sidebar.radio(
     '¿Qué variables deseas incluir en el reporte?',
     ('Todas las variables', 'Un subconjunto de variables'))
    
    if option1=='Todas las variables':
        df=df
    
    elif option1=='Un subconjunto de variables':
        var_list=list(df.columns)
        option3=st.sidebar.multiselect(
            'Selecciona las variable(s) que deseas incluir en el reporte.',
            var_list)
        df=df[option3]
   
    option2 = st.sidebar.selectbox(
     'Elige el Modo Minimo o el Modo Completo',
     ('Modo Minimo', 'Modo Completo'))

    if option2=='Modo Completo':
        mode='complete'
        st.sidebar.warning('El modo mínimo predeterminado deshabilita cálculos costosos como correlaciones y la detección de filas duplicadas. Cambiar al modo completo podría hacer que la aplicación se ejecute durante mucho tiempo o falle para conjuntos de datos grandes debido a los límites computacionales.')
        grid_response = AgGrid(
        df,
        editable=True, 
        height=300, 
        width='100%',
        )

    elif option2=='Modo Minimo':
        mode='minimal'

        grid_response = AgGrid(
        df,
        editable=True, 
        height=300, 
        width='100%',
        )

    updated = grid_response['data']
    df1 = pd.DataFrame(updated) 

    if st.button('Generar Reporte'):
        if mode=='complete':
            profile=ProfileReport(df,
                title="Tabla Cargada",
                progress_bar=True,
                dataset={
                    "descripción": 'Este informe de perfilado fue generado por Insights Bees',
                    "copyright_holder": 'Insights Bees',
                    "copyright_year": '2022'
                }) 
            st_profile_report(profile)
        elif mode=='minimal':
            profile=ProfileReport(df1,
                minimal=True,
                title="Tabla Cargada",
                progress_bar=True,
                dataset={
                    "description": 'Este informe de perfilado fue generado por Insights Bees',
                    "copyright_holder": 'Insights Bees',
                    "copyright_year": '2022'
                }) 
            st_profile_report(profile)  

with st.sidebar.expander("Acerca de la aplicación:"):
     st.write("""
        La aplicación de perfilado de datos fue construida por My Data Talk utilizando Streamlit y el paquete pandas_profiling. Puedes utilizar la aplicación para generar rápidamente un informe completo de perfilado de datos y análisis exploratorio sin la necesidad de escribir ningún código en Python.

              
La aplicación tiene dos modos: el modo mínimo (recomendado) y el código completo. El código completo incluye análisis más sofisticados, como análisis de correlación o interacciones entre variables, que pueden requerir cálculos más intensivos. )
     """)