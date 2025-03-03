import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def obtener_datos(paises_codigos, indicador_codigo, año_inicio, año_fin):
    """Obtiene datos del Banco Mundial con validación mejorada"""
    try:
        # Construir URL con parámetros validados
        if not all([paises_codigos, indicador_codigo, año_inicio <= año_fin]):
            raise ValueError("Parámetros inválidos")
            
        url = f"https://api.worldbank.org/v2/country/{';'.join(paises_codigos)}/indicator/{indicador_codigo}?format=json&date={año_inicio}:{año_fin}&per_page=1000"
        
        # Manejo de errores HTTP
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # Validar estructura de respuesta
        if not isinstance(data, list) or len(data) < 2:
            return pd.DataFrame()
        
        registros = []
        for item in data[1]:
            try:
                if item['value'] is not None:
                    registros.append({
                        "País": item['country']['value'],
                        "Código": item['countryiso3code'],
                        "Año": int(item['date']),
                        "Valor": round(float(item['value']), 2)
                    })
            except (KeyError, TypeError, ValueError):
                continue
                
        if not registros:
            return pd.DataFrame()
            
        df = pd.DataFrame(registros)
        return df.sort_values('Año').drop_duplicates()
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return pd.DataFrame()