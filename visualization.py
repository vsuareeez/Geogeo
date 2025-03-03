import plotly.express as px
import streamlit as st

def mostrar_grafico_evolucion(df, indicador_nombre):
    if df.empty:
        st.warning("No hay datos disponibles para mostrar")
        return
    
    try:
        fig = px.line(
            df,
            x="Año",
            y="Valor",
            color="País",
            markers=True,
            title=f"<b>{indicador_nombre}</b>",
            labels={'Valor': 'Valor', 'Año': 'Año'},
            height=500
        )
        # Corrección aquí: cerrar correctamente el update_layout
        fig.update_layout(
            hovermode="x unified",
            legend_title_text='País',
            xaxis=dict(tickmode='linear', dtick=5),
            yaxis=dict(title=indicador_nombre)
        )  # <-- Paréntesis faltante añadido
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar gráfico: {str(e)}")

def mostrar_mapa_coropletico(df, indicador_nombre):
    """Muestra mapa coroplético con validación de datos"""
    if df.empty:
        return
    
    try:
        último_año = df['Año'].max()
        df_filtrado = df[df['Año'] == último_año]
        
        if df_filtrado.empty:
            st.warning(f"No hay datos para {último_año}")
            return
            
        fig = px.choropleth(
            df_filtrado,
            locations="Código",
            color="Valor",
            hover_name="País",
            color_continuous_scale="Viridis",
            title=f"<b>{indicador_nombre} ({último_año})</b>",
            height=500
        )
        fig.update_geos(
            showcountries=True,
            showcoastlines=True,
            projection_type="natural earth"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar mapa: {str(e)}")