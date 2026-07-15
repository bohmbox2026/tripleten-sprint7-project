import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página avanzada
st.set_page_config(page_title="Dashboard Integral de Vehículos", layout="wide")

st.title("🚗 Dashboard Integral: Análisis Financiero, Temporal y Técnico")
st.markdown("Esta aplicación unifica el estudio de precios y kilometraje con las métricas de permanencia en el mercado y configuraciones de motor.")

# 1. Función consolidada para cargar y limpiar todas las variables necesarias
@st.cache_data
def cargar_datos_completos():
    # Obtiene la ruta absoluta de la carpeta donde vive este archivo 'app.py'
    # (En este caso, apuntará a: .../tripleten_sprint7_project)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construimos la ruta subiendo un nivel (al directorio raíz del proyecto) 
    # y bajando hacia la carpeta 'data/raw'
    ruta_csv = os.path.join(current_dir, "..", "data", "raw", "vehicles_us.csv")
    
    # Cargamos el dataframe usando la ruta absoluta construida
    df = pd.read_csv(ruta_csv)
    
    # Limpieza de variables técnicas (Versión 3)
    df['cylinders'] = df['cylinders'].fillna(df['cylinders'].mode()[0]).astype(int).astype(str) + " Cilindros"
    df['fuel'] = df['fuel'].fillna('Otros')
    
    # Limpieza de variables mecánicas y de estado (Versión 2)
    df['is_4wd'] = df['is_4wd'].fillna(0).map({1.0: '4WD', 0.0: '2WD'})
    df['paint_color'] = df['paint_color'].fillna('No especificado')
    df['model_year'] = df['model_year'].fillna(df['model_year'].median())
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())
    
    return df

df = cargar_datos_completos()

# 2. Controladores e Interfaz de Filtros (Barra Lateral)
st.sidebar.header("⚙️ Filtros de Control Global")

# Filtro por tipo de transmisión
transmisiones = sorted(df['transmission'].dropna().unique())
transmisiones_sel = st.sidebar.multiselect("Tipo de Transmisión:", transmisiones, default=transmisiones)

# Filtro por tipo de combustible
combustibles = sorted(df['fuel'].unique())
combustibles_sel = st.sidebar.multiselect("Tipo de Combustible:", combustibles, default=combustibles)

# Rango de Años del Modelo (Slider doble)
anio_min, anio_max = int(df['model_year'].min()), int(df['model_year'].max())
rango_anios = st.sidebar.slider("Años del Modelo:", anio_min, anio_max, (2000, anio_max))

# Filtrado definitivo del DataFrame
df_filtrado = df[
    (df['transmission'].isin(transmisiones_sel)) & 
    (df['fuel'].isin(combustibles_sel)) &
    (df['model_year'].between(rango_anios[0], rango_anios[1]))
]

# 3. KPIs del Negocio (Indicadores Clave)
m_total, m_precio, m_dias, m_km = st.columns(4)
with m_total:
    st.metric("Autos en Catálogo", f"{len(df_filtrado):,}")
with m_precio:
    st.metric("Precio Mediano", f"${df_filtrado['price'].median():,.0f}")
with m_dias:
    st.metric("Permanencia Promedio", f"{df_filtrado['days_listed'].mean():.1f} días")
with m_km:
    st.metric("Kilometraje Mediano", f"{df_filtrado['odometer'].median():,.0f} mi")

st.markdown("---")

# 4. Estructura de Navegación por Pestañas (Organización Visual)
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Dimensión Económica (Precios)", 
    "⏱️ Ciclo de Venta (Tiempo)", 
    "🏅 Condiciones de Mercado", 
    "📊 Configuración Técnica (Motor)"
])

# --- PESTAÑA 1: Análisis de Dispersión y Precios (Versión 2) ---
with tab1:
    st.subheader("Análisis de Costos en relación con el Uso y Tracción")
    fig_scatter_precio = px.scatter(
        df_filtrado,
        x='odometer',
        y='price',
        color='is_4wd',
        hover_data=['model', 'model_year'],
        title="Precio de Venta vs. Kilometraje por Tipo de Tracción",
        labels={'odometer': 'Kilometraje (Millas)', 'price': 'Precio ($)', 'is_4wd': 'Tracción'},
        opacity=0.5
    )
    st.plotly_chart(fig_scatter_precio, use_container_width=True)

# --- PESTAÑA 2: Histograma de Días y Permanencia (Versión 3) ---
with tab2:
    st.subheader("Distribución Temporal de los Anuncios Activos")
    
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        fig_hist_tiempo = px.histogram(
            df_filtrado,
            x='days_listed',
            nbins=50,
            color_discrete_sequence=['#ff4b4b'],
            title="¿Cuánto tiempo tarda un vehículo en venderse?",
            labels={'days_listed': 'Días Publicado', 'count': 'Número de Anuncios'}
        )
        st.plotly_chart(fig_hist_tiempo, use_container_width=True)
        
    with col_t2:
        st.markdown("#### Relación: Edad del Auto vs Días Publicado")
        fig_scatter_tiempo = px.scatter(
            df_filtrado[df_filtrado['model_year'] >= 1990],
            x='model_year',
            y='days_listed',
            color='fuel',
            opacity=0.4,
            labels={'model_year': 'Año del Modelo', 'days_listed': 'Días en Mercado', 'fuel': 'Combustible'}
        )
        st.plotly_chart(fig_scatter_tiempo, use_container_width=True)

# --- PESTAÑA 3: Precio Promedio por Condición con Viridis (Versión 2) ---
with tab3:
    st.subheader("Comportamiento Financiero según el Estado Declarado")
    df_agrupado = df_filtrado.groupby('condition')['price'].mean().reset_index()
    
    fig_bar_condicion = px.bar(
        df_agrupado,
        x='condition',
        y='price',
        color='price',
        color_continuous_scale='Viridis',  # Forzado de paleta explícito para entornos interactivos
        title="Costo Promedio del Vehículo según su Condición",
        labels={'condition': 'Condición del Auto', 'price': 'Precio Promedio ($)'}
    )
    st.plotly_chart(fig_bar_condicion, use_container_width=True)

# --- PESTAÑA 4: Estructura Técnica y Cilindradas (Versión 3) ---
with tab4:
    st.subheader("Composición Mecánica del Inventario")
    df_apilado = df_filtrado.groupby(['cylinders', 'fuel']).size().reset_index(name='total')
    
    fig_bar_tecnico = px.bar(
        df_apilado,
        x='cylinders',
        y='total',
        color='fuel',
        barmode='stack',
        title="Distribución de Tipos de Combustible dentro de cada Categoría de Motor",
        labels={'cylinders': 'Motorización', 'total': 'Total de Autos', 'fuel': 'Combustible'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_bar_tecnico, use_container_width=True)

st.markdown("---")

# 5. Explorador de datos crudos (Versión 3)
with st.expander("👀 Inspeccionar Subconjunto de Datos Filtrados"):
    st.dataframe(df_filtrado[['model', 'model_year', 'price', 'odometer', 'cylinders', 'fuel', 'days_listed']].head(100))
