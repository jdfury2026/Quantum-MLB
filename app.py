import streamlit as st
from engine import QuantumEngine

# 1. Configuración de la página
st.set_page_config(
    page_title="Quantum MLB Analytics",
    page_icon="⚾",
    layout="wide"
)

# Estilo personalizado para mejorar la visualización
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚾ Quantum MLB: Simulador de Alta Fidelidad")
st.subheader("Análisis Probabilístico basado en 5,000,000 de Iteraciones")
st.write("---")

# 2. Panel Lateral de Configuración
with st.sidebar:
    st.header("Configuración del Encuentro")
    home_t = st.selectbox("Equipo Local", ["NYY", "LAD", "HOU", "ATL", "PHI", "TEX", "BOS", "CHC"], key="home_team")
    away_t = st.selectbox("Equipo Visitante", ["BOS", "SF", "SEA", "NYM", "TOR", "SD", "NYY", "LAD"], key="away_team")
    linea_ou = st.number_input("Línea de Carreras (Over/Under)", value=8.5, step=0.5)
    st.write("---")
    st.info("💡 Este simulador utiliza un motor Monte Carlo para proyectar resultados tras 5 millones de escenarios posibles.")

# 3. Lógica Principal y Despliegue de Resultados
if st.button('🚀 EJECUTAR ANÁLISIS CUÁNTICO', use_container_width=True):
    # Contenedor para agrupar visualmente los resultados
    resultado_area = st.container(border=True)
    
    with st.spinner('Calculando escenarios cuánticos...'):
        try:
            # Ejecutamos el motor de simulación
            engine = QuantumEngine()
            res = engine.run_monte_carlo(home_t, away_t, linea_ou)
            
            with resultado_area:
                st.write(f"## 📊 Pronóstico Final: {away_t} vs {home_t}")
                
                # SECCIÓN 1: GANADOR DIRECTO (MONEY LINE)
                st.markdown("### 🏆 Probabilidad de Victoria (Money Line)")
                col_away, col_home = st.columns(2)
                
                with col_away:
                    st.metric(label=f"Visitante: {away_t}", value=f"{res['ml_away']}%")
                    st.progress(res['ml_away']/100)
                    st.caption(f"Probabilidad de triunfo para {away_t}")
                
                with col_home:
                    st.metric(label=f"Local: {home_t}", value=f"{res['ml_home']}%")
                    st.progress(res['ml_home']/100)
                    st.caption(f"Probabilidad de triunfo para {home_t}")
                
                st.write("---")
                
                # SECCIÓN 2: MERCADOS ESPECIALES (SPREAD Y TOTALES)
                col_spread, col_total = st.columns(2)
                
                with col_spread:
                    st.markdown(f"### 🏟️ Hándicap (Spread -1.5)")
                    st.metric(f"Cubre {home_t}", f"{res['spread_home_minus_1_5']}%")
                    st.write(f"Probabilidad de que **{home_t}** gane por una diferencia mayor a 1.5 carreras.")
                    
                with col_total:
                    st.markdown(f"### 📈 Totales (O/U {linea_ou})")
                    st.metric("Probabilidad de ALTAS (Over)", f"{res['over_prob']}%")
                    st.write(f"Probabilidad de que el marcador total supere las **{linea_ou}** carreras.")
                
                st.success(f"✅ Simulación de 5,000,000 de juegos completada con éxito.")
                
        except Exception as e:
            st.error(f"Se detectó un error en el motor de cálculo: {str(e)}")
else:
    st.info("Ajusta los equipos en el menú lateral y presiona el botón para generar el pronóstico.")
