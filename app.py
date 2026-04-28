import streamlit as st
from engine import QuantumEngine

# Configuración básica de la interfaz
st.set_page_config(page_title="Quantum MLB Analytics", layout="wide")

st.title("⚾ Quantum MLB Analytics")
st.subheader("Simulador Quirúrgico de 5,000,000 de Iteraciones")
st.write("---")

# Panel de entrada de datos
with st.sidebar:
    st.header("Parámetros del Juego")
    home_t = st.selectbox("Equipo Local", ["NYY", "LAD", "HOU", "ATL", "PHI", "TEX"])
    away_t = st.selectbox("Equipo Visitante", ["BOS", "SF", "SEA", "NYM", "CHC", "TOR"])
    linea_ou = st.number_input("Línea de Carreras (O/U)", value=8.5, step=0.5)
    st.write("---")
    st.caption("Motor de simulación Monte Carlo v2.0")

# Botón de ejecución y área de resultados
if st.button('🚀 EJECUTAR ANÁLISIS CUÁNTICO', use_container_width=True):
    # Creamos un contenedor limpio para los resultados
    resultado_area = st.container(border=True)
    
    with st.spinner('Procesando 5,000,000 de escenarios...'):
        try:
            # Ejecutamos el motor
            engine = QuantumEngine()
            res = engine.run_monte_carlo(home_t, away_t, linea_ou)
            
            # Mostramos los datos de forma organizada
            with resultado_area:
                st.write(f"### Proyecciones Finales: {away_t} vs {home_t}")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Prob. Victoria (Local)", f"{res['ml_home']}%")
                    st.progress(res['ml_home']/100)
                
                with col2:
                    st.metric("Cubre Spread (-1.5)", f"{res['spread_home_minus_1_5']}%")
                    st.progress(res['spread_home_minus_1_5']/100)
                    
                with col3:
                    st.metric(f"Altas / Over ({linea_ou})", f"{res['over_prob']}%")
                    st.progress(res['over_prob']/100)
                
                st.success("Cálculo completado sin errores de interfaz.")
                
        except Exception as e:
            st.error(f"Falla técnica en el motor: {str(e)}")
else:
    st.info("Configura los equipos en la izquierda y presiona el botón para iniciar.")
