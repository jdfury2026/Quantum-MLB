import streamlit as st
from engine import QuantumEngine

# 1. Configuración de la página
st.set_page_config(page_title="Quantum MLB Analytics", layout="wide")
st.title("⚾ Quantum MLB: Simulador de Alta Fidelidad")
st.markdown("---")

# 2. Panel Lateral
st.sidebar.header("Configuración")
# Nota: En el futuro esto vendrá de get_todays_games, 
# por ahora lo mantenemos simple para probar que el motor funcione.
home_team = st.sidebar.selectbox("Equipo Local", ["NYY", "BOS", "LAD", "SF", "HOU", "TEX"])
away_team = st.sidebar.selectbox("Equipo Visitante", ["BOS", "NYY", "SF", "LAD", "TEX", "HOU"])
ou_line = st.sidebar.number_input("Línea Over/Under", value=8.5, step=0.5)

# 3. Lógica del Botón y Despliegue (LA VERSIÓN CORREGIDA)
if st.button('🚀 EJECUTAR SIMULACIÓN QUIRÚRGICA'):
    # Creamos un contenedor vacío para limpiar errores previos del navegador
    placeholder = st.container() 
    
    with st.spinner('Calculando 5 millones de escenarios...'):
        try:
            # Llamamos al motor
            engine = QuantumEngine()
            res = engine.run_monte_carlo(home_team, away_team, ou_line)
            
            # Dibujamos TODO dentro del contenedor 'placeholder'
            with placeholder:
                st.header(f"Resultados: {home_team} vs {away_team}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("Money Line")
                    st.metric(f"Prob. {home_team}", f"{res['ml_home']}%")
                    st.metric(f"Prob. {away_team}", f"{res['ml_away']}%")
                    
                with col2:
                    st.subheader("Spread (-1.5)")
                    st.metric("Probabilidad", f"{res['spread_home_minus_1_5']}%")
                    
                with col3:
                    st.subheader(f"Total (O/U {ou_line})")
                    st.metric("Prob. Over", f"{res['over_prob']}%")
                
                st.success("✅ Simulación completada con éxito.")
                
        except Exception as e:
            st.error(f"Hubo un error en el motor: {e}")
else:
    st.info("Selecciona los equipos y presiona el botón para iniciar el análisis cuántico.")
