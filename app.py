#* Librerías

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#* Carga de datos
df = pd.read_csv("./data/finances_clean.csv")

#* Configuración de la página
st.set_page_config(layout="wide")

st.sidebar.title("Secciones")
secciones = ["Resumen General", "Distribuciones Financieras", "Correlaciones entre Variables", "Visualizaciones"]
option = st.sidebar.selectbox("Selecciona una sección", secciones)


#* Numero de Empresas, Numero de Sectores, Estadisticos globales
if option == "Resumen General":

    st.title("Análisis de las Empresas del S&P 500")
    st.subheader("Resumen General")
    
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            c1, c2 = st.columns(2)

        with c1:
            # Número de Empresas
            st.metric(label="Número de Empresas", value=f"{df['Symbol'].nunique()}")
        with c2:
            # Número de Sectores
            st.metric(label="Número de Sectores", value=f"{df['Sector'].nunique()}")
        
        st.divider()

        # Estadísticos globales
        st.subheader("Datos descriptivos globales")
        df_numerico = df.select_dtypes(include=['number'])
        st.dataframe(df_numerico.describe().T, use_container_width=True)


    with col2:
        metricas_num = df.select_dtypes(include=['number']).columns.tolist()
        variable_compartiva = st.selectbox("Métrica para comparar sectores:", metricas_num)
        
        # Agrupa por sector y calcula el describe de esa métrica para todos
        tabla_sectores_completa = df.groupby("Sector")[variable_compartiva].describe()
        st.dataframe(tabla_sectores_completa, use_container_width=True)
        
        st.divider()

        sectores = df["Sector"].unique()
        variable_sector = st.selectbox("Selecciona un sector: ", sectores)

        st.markdown(f"**Detalle expandido del Sector seleccionado:** *{variable_sector}*")
        df_individual = df[df["Sector"] == variable_sector].select_dtypes(include=['number'])
        st.dataframe(df_individual.describe().T, use_container_width=True)

#* Distribuciones Financieras
if option == "Distribuciones Financieras":
    st.title("Análisis de las Empresas del S&P 500")
    
    metricas_num = df.select_dtypes(include=['number']).columns.tolist()
    variable_dist = st.selectbox("Selecciona una métrica para visualizar su distribución:", metricas_num)

    col1, col2 = st.columns(2)

    with col1:
        # Histograma
        st.subheader("Histograma")
        plt.figure(figsize=(10, 6))
        sns.histplot(df[variable_dist], kde=True, bins=30)
        plt.title(f"Distribución de {variable_dist}")
        plt.xlabel(variable_dist)
        plt.ylabel("Frecuencia")
        st.pyplot(plt)
        plt.clf()

    with col2:
        # Boxplot
        st.subheader("Boxplot")
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=df[variable_dist])
        plt.title(f"Boxplot de {variable_dist}")
        plt.ylabel(variable_dist)
        st.pyplot(plt)
        plt.clf()

    col1, col2 = st.columns([3,2])

    with col1:
        st.subheader("Boxplot por Sector")
        plt.figure(figsize=(12, 8))
        sns.boxplot(x=df["Sector"], y=df[variable_dist])
        plt.title(f"Boxplot de {variable_dist} por Sector")
        plt.xlabel("Sector")
        plt.ylabel(variable_dist)
        plt.xticks(rotation=45)
        st.pyplot(plt)
        plt.clf()

    with col2:
        st.subheader("Estadísticos por Sector")
        tabla_sectores = df.groupby("Sector")[variable_dist].describe()
        st.dataframe(tabla_sectores, use_container_width=True)
    

#* Correlaciones entre Variables
if option == "Correlaciones entre Variables":
    st.title("Análisis de las Empresas del S&P 500")
    col1, col2 = st.columns(2)

    with col1:
        pass

    with col2:
        pass

#* Visualizaciones PCA, visualización MDS
if option == "Visualizaciones":
    st.title("Análisis de las Empresas del S&P 500")
    col1, col2 = st.columns(2)

    with col1:
        pass

    with col2:
        pass
