import streamlit as st
from engine import QuantumEngine

# 1. Configuración de la página (Solo se ejecuta una vez)
st.set_page_config(page_title="Quantum MLB Analytics", layout="wide")

# Estilo para evitar que la interfaz se mueva bruscamente
st.markdown("""<style> div.block-container { padding-top: 2rem; } </style>""", unsafe_allow_html=True)

st.title("⚾ Quantum MLB: Simulador de Alta Fidelidad")
st.write("---")

# 2. Panel Lateral de Configuración
with st.sidebar:
    st.header("Configuración")
    home_team = st.selectbox("Equipo Local", ["NYY", "BOS", "LAD", "SF", "HOU", "TEX"], key="home")
    away_team = st.selectbox("Equipo Visitante", ["BOS", "NYY", "SF", "LAD", "TEX", "HOU"], key="away")
    ou_line = st.number_input("Línea Over/Under", value=8.5, step=0.5, key="ou")
    st.write("---")
    st.info("⚡ Motor: 5M de Iteraciones")

# 3. Función Fragmentada (Esto evita el error de 'removeChild')
@st.fragment
def render_simulation():
    if st.button('🚀 EJECUTAR SIMULACIÓN QUIRÚRGICA', use_container_width=True):
        # Contenedor estático para evitar conflictos de nodos
        main_container = st.container(border=True)
        
        with st.spinner('Procesando datos cuánticos...'):
            try:
                engine = QuantumEngine()
                res = engine.run_monte_carlo(home_team, away_team, ou_line)
                
                with main_container:
                    st.subheader(f"📊 Análisis: {away_team} @ {home_team}")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Money Line (Home)", f"{res['ml_home']}%")
                        st.progress(res['ml_home']/100)
                    
                    with col2:
                        st.metric("Spread (-1.5)", f"{res['spread_home_minus_1_5']}%")
                        st.progress(res['spread_home_minus_1_5']/100)
                        
                    with col3:
                        st.metric(f"Total Over {ou_line}", f"{res['over_prob']}%")
                        st.progress(res['over_prob']/100)
                    
                    st.success("Cálculo estabilizado.")
            except Exception as e:
                st.error(f"Error en el motor: {str(e)}")

# Llamamos a la función
render_simulation()
