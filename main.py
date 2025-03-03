import streamlit as st
from data_fetcher import obtener_datos
from visualization import mostrar_grafico_evolucion, mostrar_mapa_coropletico

# Configuración de página
st.set_page_config(
    page_title="Analizador Global",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración CSS personalizada
st.markdown("""
    <style>
    .header-text {
        font-size: 2.5rem !important;
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .stSelectbox > div > div {
        border: 2px solid #1f77b4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Datos de configuración
PAISES = {
    "Argentina": "ARG",
    "Brasil": "BRA",
    "Chile": "CHL",
    "México": "MEX",
    "Estados Unidos": "USA",
    "Canadá": "CAN",
    "Alemania": "DEU",
    "Francia": "FRA",
    "China": "CHN",
    "India": "IND"
}

INDICADORES = {
    "PIB per cápita (USD)": "NY.GDP.PCAP.CD",
    "Esperanza de vida (años)": "SP.DYN.LE00.IN",
    "Población total": "SP.POP.TOTL"
}

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    # Selector de países
    paises_seleccionados = st.multiselect(
        "Seleccionar países:",
        options=list(PAISES.keys()),
        default=["Chile", "Argentina"],
        max_selections=5
    )
    
    # Selector de indicador
    indicador_seleccionado = st.selectbox(
        "Seleccionar indicador:",
        options=list(INDICADORES.keys())
    )
    
    # Selector de rango de años
    año_inicio, año_fin = st.slider(
        "Seleccionar rango de años:",
        min_value=1960,
        max_value=2023,
        value=(2000, 2020)
    )

# Contenido principal
st.markdown('<div class="header-text">🌍 Analizador de Indicadores Globales</div>', unsafe_allow_html=True)

if paises_seleccionados and indicador_seleccionado:
    # Obtener datos
    codigos_paises = [PAISES[p] for p in paises_seleccionados]
    codigo_indicador = INDICADORES[indicador_seleccionado]
    
    with st.spinner('Cargando datos...'):
        df = obtener_datos(codigos_paises, codigo_indicador, año_inicio, año_fin)
    
    if not df.empty:
        # Layout principal
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### 📈 Evolución Histórica")
            mostrar_grafico_evolucion(df, indicador_seleccionado)
        
        with col2:
            st.markdown("### 🗺️ Distribución Geográfica")
            mostrar_mapa_coropletico(df, indicador_seleccionado)
            
            # Estadísticas rápidas
            st.markdown("### 📊 Datos Clave")
            último_año = df['Año'].max()
            st.metric(
                label=f"Valor promedio ({último_año})",
                value=f"{df[df['Año'] == último_año]['Valor'].mean():.2f}"
            )
    else:
        st.warning("No se encontraron datos para la selección actual")
        
else:
    st.info("Por favor seleccione al menos un país y un indicador")

# Footer
st.markdown("---")
st.markdown("**Fuente de datos:** Banco Mundial | **Última actualización:** 2024")