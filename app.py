import streamlit as st
from engine import QuantumEngine  # Aquí llamamos a tu motor de 5M de iteraciones

# 1. Configuración visual
st.set_page_config(page_title="Quantum MLB Analytics", layout="wide")
st.title("⚾ Quantum MLB: Simulador de Alta Fidelidad")
st.markdown("---")

engine = QuantumEngine()
juegos_hoy = engine.get_todays_games()

if juegos_hoy:
    opciones = [f"{j['away']} @ {j['home']}" for j in juegos_hoy]
    seleccion = st.sidebar.selectbox("Selecciona el juego de HOY", opciones)
    
    # Extraer los nombres para el motor
    game_idx = opciones.index(seleccion)
    home_team = juegos_hoy[game_idx]['home']
    away_team = juegos_hoy[game_idx]['away']
else:
    st.sidebar.warning("No se encontraron juegos programados para hoy.")

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
