# Análisis de Empresas del S&P 500

### Dirreción donde se aloja en línea:
https://stocks-analysis-escom.streamlit.app

## Descripción del Proyecto

Aplicación interactiva construida con **Streamlit** para explorar y analizar datos financieros de las empresas del índice S&P 500. La herramienta permite visualizar distribuciones, correlaciones y comparativas entre empresas y sectores de forma intuitiva.

---

## Características Principales

- **Resumen General**: Visión general del número de empresas, sectores y estadísticos globales
- **Distribuciones Financieras**: Análisis de distribuciones de métricas financieras
- **Correlaciones entre Variables**: Matriz de correlaciones entre variables financieras
- **Visualizaciones**: Gráficos interactivos comparativos por sector

---

## Estructura del Proyecto

```
.
├── app.py                              # Aplicación principal Streamlit
├── requirements.txt                    # Dependencias del proyecto
├── README.md                           # Este archivo
└── data/
    ├── finances.csv                    # Dataset completo de S&P 500
    ├── finances_clean.csv              # Dataset procesado
    └── exploration_S&P_500.ipynb       # Notebook de exploración EDA y procesamiento
```

---

## Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**:
   ```bash
   git clone https://github.com/marcoBartolo55/stocks-analysis.git
   ```

2. **Crear un entorno virtual**:
   ```bash
   python -m venv .venv
   ```

3. **Activar el entorno virtual**:
   - En Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Cómo Ejecutar

Para iniciar la aplicación Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501` en tu navegador.

---

## Dependencias Principales

| Librería | Versión | Propósito |
|----------|---------|-----------|
| **streamlit** | - | Framework para interfaces web interactivas |
| **pandas** | 3.0.3 | Manipulación y análisis de datos |
| **matplotlib** | 3.11.0 | Visualización estática de gráficos |
| **seaborn** | - | Gráficos estadísticos de alto nivel |
| **numpy** | 2.4.6 | Operaciones numéricas |
| **plotly** | 6.8.0 | Gráficos interactivos |

---

## Secciones de la Aplicación

### 1. **Resumen General**
Muestra métricas clave del dataset:
- Total de empresas en el S&P 500
- Número de sectores representados
- Estadísticos descriptivos (media, mediana, desviación estándar, etc.)
- Comparativa de métricas financieras por sector

### 2. **Distribuciones Financieras**
Visualización de distribuciones de variables financieras con opción de seleccionar métricas específicas para análisis profundo.

### 3. **Correlaciones entre Variables**
Matriz de correlaciones entre todas las variables numéricas del dataset con visualización en heatmap.

### 4. **Visualizaciones**
Gráficos comparativos interactivos entre empresas y sectores para explorar relaciones entre variables.

---

## Datos Utilizados

### Fuente
- Dataset: S&P 500 Companies with Financial Information
- Origen: https://www.kaggle.com/datasets/paytonfisher/sp-500-companies-with-financial-information
- Ubicación: finances_clean.csv

### Variables Principales
- **Symbol**: Símbolo de cotización de la empresa
- **Sector**: Sector económico de la empresa
- Métricas financieras: Precio, volumen, ratios financieros, etc.

---

## Jupyter Notebook

Para exploración y análisis exploratorio de datos (EDA):

```bash
jupyter notebook data/exploration_S&P_500.ipynb
```

---

## Autores
@marcoBartolo55

@Valeria14022001

---
