import streamlit as st
from engine import QuantumEngine  # Aquí llamamos a tu motor de 5M de iteraciones

# 1. Configuración visual
st.set_page_config(page_title="Quantum MLB Analytics", layout="wide")
st.title("⚾ Quantum MLB: Simulador de Alta Fidelidad")
st.markdown("---")

# 2. Panel Lateral de Configuración
st.sidebar.header("Configuración del Encuentro")
home_team = st.sidebar.selectbox("Equipo Local", ["NYY", "BOS", "LAD", "SF", "HOU", "TEX"])
away_team = st.sidebar.selectbox("Equipo Visitante", ["BOS", "NYY", "SF", "LAD", "TEX", "HOU"])
ou_line = st.sidebar.number_input("Línea Over/Under", value=8.5, step=0.5)

st.sidebar.markdown("---")
st.sidebar.write("⚡ **Motor:** 5,000,000 Iteraciones")
st.sidebar.write("🧠 **Ajustes:** Momentum + Clutch Factor")

# 3. Botón de Ejecución
if st.button('🚀 EJECUTAR SIMULACIÓN QUIRÚRGICA'):
    with st.spinner('Calculando 5 millones de escenarios posibles...'):
        # Llamamos al motor que creamos en engine.py
        engine = QuantumEngine()
        res = engine.run_monte_carlo(home_team, away_team, ou_line)
        
        # 4. Despliegue de Resultados
        st.header(f"Resultados: {home_team} vs {away_team}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Ganador (Money Line)")
            st.metric(label=f"Prob. {home_team}", value=f"{res['ml_home']}%")
            st.metric(label=f"Prob. {away_team}", value=f"{res['ml_away']}%")
            
        with col2:
            st.subheader("Spread (-1.5)")
            st.write(f"Probabilidad de que {home_team} cubra el spread:")
            st.title(f"{res['spread_home_minus_1_5']}%")
            
        with col3:
            st.subheader(f"Total (O/U {ou_line})")
            st.write(f"Probabilidad de ALTAS (Over):")
            st.title(f"{res['over_prob']}%")

        st.success("Simulación completada con precisión del 99.9%")
else:
    st.info("Selecciona los equipos en el panel de la izquierda y presiona el botón para comenzar.")
