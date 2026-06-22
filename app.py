
#* Librerías
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import MDS

#* Carga de datos
df = pd.read_csv("./data/finances_clean.csv")

#* Configuración de la página
st.set_page_config(layout="wide")

st.sidebar.title("Secciones")
secciones = ["Resumen General", "Distribuciones Financieras", "Correlaciones entre Variables", "Visualizaciones", "Perfil Empresa"]
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

    st.divider()

    st.subheader("Valores atípicos de Empresas")
    st.divider()

    st.subheader("Valores atípicos de Empresas")
    
    outliers = []
    for sector in df["Sector"].unique():
        df_sector = df[df["Sector"] == sector]
        
        Q1 = df_sector[variable_dist].quantile(0.25)
        Q3 = df_sector[variable_dist].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_sector = df_sector[(df_sector[variable_dist] < lower_bound) | (df_sector[variable_dist] > upper_bound)]
        outliers.append(outliers_sector)
    
    outliers_df = pd.concat(outliers)
    
    top_10_outliers = outliers_df.sort_values(by=variable_dist, ascending=False).head(10)
    
    st.markdown("**Top 10 Empresas con Valores Más Atípicos del Mercado:**")
    st.dataframe(top_10_outliers[["Symbol", "Name", "Sector", variable_dist]], use_container_width=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=df, x="Sector", y=variable_dist, alpha=0.5, label="Empresas", ax=ax)
    
    sns.scatterplot(data=top_10_outliers, x="Sector", y=variable_dist, color="red", s=100, label="Top 10 Atípicas", ax=ax)
    
    ax.set_title(f"Valores Atípicos de {variable_dist} por Sector")
    ax.set_xlabel("Sector")
    ax.set_ylabel(variable_dist)
    plt.xticks(rotation=90, ha='right')
    
    st.pyplot(fig)
    plt.close(fig)

#* Correlaciones entre Variables
if option == "Correlaciones entre Variables":
    st.title("Análisis de las Empresas del S&P 500")

    style_corr = ["coolwarm", "viridis", "plasma", "inferno", "magma"]
    selected_style = st.selectbox("Selecciona un estilo de color para la matriz de correlación:", style_corr)

    correlation_type = ["Pearson", "Spearman"]
    selected_correlation = st.selectbox("Selecciona el tipo de correlación:", correlation_type)

    df_numerico = df.select_dtypes(include=['number'])

    plt.figure(figsize=(12, 8))
    if selected_correlation == "Pearson":
        corr_matrix = df_numerico.corr(method='pearson')
        plt.title("Matriz de Correlación (Pearson)")
        plt.imshow(corr_matrix, cmap=selected_style, interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=90)
        plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
        st.pyplot(plt)
        plt.clf()

    elif selected_correlation == "Spearman":
        corr_matrix = df_numerico.corr(method='spearman')
        plt.title("Matriz de Correlación (Spearman)")
        plt.imshow(corr_matrix, cmap=selected_style, interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=90)
        plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
        st.pyplot(plt)
        plt.clf()

    #! Depreceated
    elif selected_correlation == "Kendall":
        corr_matrix = df_numerico.corr(method='kendall')
        plt.title("Matriz de Correlación (Kendall)")
        plt.imshow(corr_matrix, cmap=selected_style, interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=90)
        plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
        st.pyplot(plt)
        plt.clf()

    st.divider()

    st.subheader("Gráficos de Dispersión entre Variables")

    variable_x = st.selectbox("Selecciona la variable para el eje X:", df_numerico.columns.tolist())
    variable_y = st.selectbox("Selecciona la variable para el eje Y:", df_numerico.columns.tolist())

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=variable_x, y=variable_y, hue="Sector", alpha=0.7)
    plt.title(f"Gráfico de Dispersión entre {variable_x} y {variable_y}")
    plt.xlabel(variable_x)
    plt.ylabel(variable_y)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt)
    plt.clf()


#* Visualizaciones PCA, visualización MDS
if option == "Visualizaciones":
    st.title("Análisis de las Empresas del S&P 500")

    metodo_visualizacion = ["PCA", "MDS"]
    selected_metodo = st.selectbox("Selecciona el método de visualización:", metodo_visualizacion)

    from sklearn.preprocessing import StandardScaler
    df_numerico = df.select_dtypes(include=['number'])
    X_scaled = StandardScaler().fit_transform(df_numerico)

    df_proyeccion = df.copy()

    if selected_metodo == "PCA":
        pca = PCA(n_components=2)
        coordenadas = pca.fit_transform(X_scaled)
        df_proyeccion["EjeX"] = coordenadas[:, 0]
        df_proyeccion["EjeY"] = coordenadas[:, 1]
    else:
        mds = MDS(n_components=2, random_state=42)
        coordenadas = mds.fit_transform(X_scaled)
        df_proyeccion["EjeX"] = coordenadas[:, 0]
        df_proyeccion["EjeY"] = coordenadas[:, 1]

    col1, col2 = st.columns([3, 2])

    with col2:
        st.header("Métricas del Modelo")
        
        if selected_metodo == "PCA":
            st.subheader("**Varianza Explicada por Componentes:**")
            varianza_explicada = pca.explained_variance_ratio_
            st.write(f"Componente 1: {varianza_explicada[0]:.2%}")
            st.write(f"Componente 2: {varianza_explicada[1]:.2%}")
            st.write(f"Varianza Total Explicada: {varianza_explicada.sum():.2%}")
        else:
            st.header("**Métricas de Calidad del Modelo MDS:**")
            st.metric(label="Stress del Modelo", value=f"{mds.stress_:.4f}")
            st.subheader("Convergencia del Algoritmo")
            st.write(f"• **Iteraciones requeridas:** {mds.n_iter_}")

        st.divider()

        st.header("Localizar Empresas")
        empresa = st.selectbox("Selecciona una empresa para localizar:", df_proyeccion["Name"].tolist())
        
        empresa_data = df_proyeccion[df_proyeccion["Name"] == empresa].iloc[0]
        coord_x = empresa_data["EjeX"]
        coord_y = empresa_data["EjeY"]

        if selected_metodo == "PCA":
            st.subheader(f"**Coordenadas PCA de {empresa_data['Symbol']}:**")
            st.write(f"PC1: {coord_x:.4f}")
            st.write(f"PC2: {coord_y:.4f}")
        else:
            st.subheader(f"**Coordenadas MDS de {empresa_data['Symbol']}:**")
            st.write(f"Dim1: {coord_x:.4f}")
            st.write(f"Dim2: {coord_y:.4f}")


    with col1:
        fig, ax = plt.subplots(figsize=(10, 7))
        
        sns.scatterplot(
            data=df_proyeccion, 
            x="EjeX", 
            y="EjeY", 
            hue="Sector", 
            alpha=0.5, 
            ax=ax
        )
        
        ax.scatter(
            coord_x, 
            coord_y, 
            color="#ff1d1d",
            s=300,
            marker="*",
            edgecolor="white",
            linewidth=2,
            label=f"📍 {empresa_data['Symbol']}"
        )
        
        titulo_grafica = "Visualización PCA" if selected_metodo == "PCA" else "Visualización MDS"
        ax.set_title(f"{titulo_grafica} - Buscando: {empresa_data['Symbol']}")
        ax.set_xlabel("Componente Principal 1" if selected_metodo == "PCA" else "Dimensión 1")
        ax.set_ylabel("Componente Principal 2" if selected_metodo == "PCA" else "Dimensión 2")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        st.pyplot(fig)
        plt.close(fig)
        

#* Perfil de Empresa
if option == "Perfil Empresa":

    empresa = df["Name"].unique()
    empresa_seleccionada = st.selectbox("Selecciona una empresa para ver su perfil:", empresa)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Empresa Seleccionada", value=empresa_seleccionada, border=True)

    with col2:
        st.metric(label="Sector", value=df[df["Name"] == empresa_seleccionada]["Sector"].values[0], border=True)

    with col3:
        st.metric(label="Price", value=df[df["Name"] == empresa_seleccionada]["Price"].values[0], border=True)

    with col4:
        st.metric(label="Market Cap", value=df[df["Name"] == empresa_seleccionada]["Market Cap"].values[0], border=True)

    st.divider()



    st.subheader("Métricas Financieras Comparativas")

    columnas_financieras = {
        "Price": "Precio Actual ($)",
        "Price/Earnings": "Múltiplo P/E",
        "Dividend Yield": "Rendimiento de Dividendos (%)",
        "Earnings/Share": "Ganancia por Acción (EPS)",
        "52 Week High": "Máximo 52 Semanas ($)",
        "52 Week Low": "Mínimo 52 Semanas ($)",
        "Market Cap": "Capitalización de Mercado",
        "EBITDA": "EBITDA Operativo",
        "Price/Sales": "Múltiplo P/S",
        "Price/Book": "Múltiplo P/B"
    }
            
    llaves_metrics = list(columnas_financieras.keys())

    fila_empresa = df[df["Name"] == empresa_seleccionada].iloc[0]
    ticker_empresa = fila_empresa["Symbol"]
    sector_empresa = fila_empresa["Sector"]

    df_sector = df[df["Sector"] == sector_empresa]

    datos_comparativos = []
            
    for col_cruda, col_limpia in columnas_financieras.items():
        val_empresa = fila_empresa[col_cruda]
        val_sector = df_sector[col_cruda].mean()
        val_global = df[col_cruda].mean()
                
    try:
        desviacion = ((val_empresa - val_sector) / val_sector) * 100
    except ZeroDivisionError:
        desviacion = 0.0

    datos_comparativos.append({
        "Dimensión Financiera": col_limpia,
        ticker_empresa: val_empresa,
        "Promedio Sector": val_sector,
        "Promedio S&P 500": val_global,
        "Desviación vs Sector": desviacion
        })

    df_tabla_final = pd.DataFrame(datos_comparativos).set_index("Dimensión Financiera")

    st.dataframe(
            df_tabla_final.style.format({
            ticker_empresa: "{:,.2f}",
            "Promedio Sector": "{:,.2f}",
            "Promedio S&P 500": "{:,.2f}",
            "Desviación vs Sector": "{:+.2f}%"
        }), 
         use_container_width=True
    )

    st.divider()

    st.subheader(f"Ecosistema Industrial: Sector {sector_empresa}")

    eje_x = "Market Cap"
    eje_y = "Price/Earnings"

    df_competidores = df[df["Sector"] == sector_empresa]

    fig, ax = plt.subplots(figsize=(10, 7))

    sns.scatterplot(
        data=df_competidores,
        x=eje_x,
        y=eje_y,
        alpha=0.6,
        color="#4b5563",
        s=100,
        ax=ax,
        label="Competidores del Sector"
        )

    ax.scatter(
        fila_empresa[eje_x],
        fila_empresa[eje_y],
        color="#ff1d1d",
        s=350,
        marker="*",
        edgecolor="white",
        linewidth=2,
        label=f"{ticker_empresa} (Tú)"
    )

    ax.set_title(f"Posicionamiento de {ticker_empresa} vs. Su Industria", fontsize=14, pad=15)
    ax.set_xlabel("Capitalización de Mercado (Tamaño)", fontsize=11)
    ax.set_ylabel("Múltiplo P/E (Valoración)", fontsize=11)        
        
    ax.legend(loc="best")
        
    ax.grid(True, linestyle="--", alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)
