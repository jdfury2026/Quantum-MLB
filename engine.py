import pandas as pd
import numpy as np
from pybaseball import pitching_stats, batting_stats, schedule_and_record
from datetime import datetime

class QuantumEngine:
  from pybaseball import schedule_and_record, statcast_pitcher, mlb_api
import datetime

def get_todays_games(self):
    """Obtiene los juegos, estadios y pitchers probables para hoy"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        # Consultamos la API oficial de MLB a través de pybaseball
        schedule = mlb_api.get_schedule(date=today)
        games_today = []
        
        for game in schedule:
            games_today.append({
                "game_id": game['game_pk'],
                "home": game['home_name'],
                "away": game['away_name'],
                "venue": game['venue_name'],
                "status": game['status']
            })
        return games_today
    except:
        return []
        
    # --- MÓDULO: MOMENTUM (Inercia de Racha) ---
    def get_momentum_multiplier(self, team_abbreviation, year=2026):
        try:
            # Obtenemos los últimos 10 juegos
            data = schedule_and_record(year, team_abbreviation).tail(10)
            results = [1 if x == 'W' else 0 for x in data['W/L']]
            
            if not results: return 1.0
            
            # Ponderación: Los juegos recientes valen más (1 a 10)
            weights = np.arange(1, len(results) + 1)
            momentum_idx = np.sum(np.array(results) * weights) / np.sum(weights)
            
            # Ajuste máximo de +/- 5%
            return 1 + (momentum_idx - 0.5) * 0.10
        except:
            return 1.0

    # --- MÓDULO: RESILIENCIA (Clutch Factor) ---
    def get_clutch_adjustment(self, avg_normal, avg_high_leverage):
        """Ajusta según la capacidad de rendir bajo presión"""
        if avg_normal == 0: return 1.0
        resilience = (avg_high_leverage / avg_normal) - 1
        # Aplicamos un peso moderado al factor psicológico
        return 1 + (resilience * 0.5)

    # --- MÓDULO: MOTOR MONTE CARLO ---
    def run_monte_carlo(self, home_team, away_team, over_under_line):
        # 1. Obtención de estadísticas base (Simulado para el ejemplo)
        # En producción, aquí conectarías pybaseball.pitching_stats
        home_exp_runs = 4.5  # Carreras esperadas base
        away_exp_runs = 4.1

        # 2. Aplicar Momentum
        home_mom = self.get_momentum_multiplier(home_team)
        away_mom = self.get_momentum_multiplier(away_team)
        
        # 3. Aplicar Factores de Ajuste (Momentum + Simulación de Clutch)
        home_final_lambda = home_exp_runs * home_mom
        away_final_lambda = away_exp_runs * away_mom

        print(f"⚙️ Procesando {self.iterations} simulaciones para {home_team} vs {away_team}...")

        # --- SIMULACIÓN VECTORIZADA (Cerebro del Sistema) ---
        # Usamos distribución de Poisson para generar 5 millones de marcadores posibles
        home_sim = np.random.poisson(home_final_lambda, self.iterations)
        away_sim = np.random.poisson(away_final_lambda, self.iterations)

        # --- CÁLCULO DE PROBABILIDADES ---
        # Money Line
        home_wins = np.sum(home_sim > away_sim)
        prob_ml_home = (home_wins / self.iterations) * 100
        
        # Spread / Run Line (-1.5)
        home_covers = np.sum((home_sim - 1.5) > away_sim)
        prob_spread_home = (home_covers / self.iterations) * 100
        
        # Over/Under
        total_runs = home_sim + away_sim
        prob_over = (np.sum(total_runs > over_under_line) / self.iterations) * 100

        return {
            "home_team": home_team,
            "away_team": away_team,
            "ml_home": round(prob_ml_home, 2),
            "ml_away": round(100 - prob_ml_home, 2),
            "spread_home_minus_1_5": round(prob_spread_home, 2),
            "over_prob": round(prob_over, 2),
            "ou_line": over_under_line
        }

# --- PRUEBA RÁPIDA ---
if __name__ == "__main__":
    engine = QuantumEngine()
    # Ejemplo: Yankees vs Red Sox con línea de 8.5
    resultado = engine.run_monte_carlo("NYY", "BOS", 8.5)
    print(resultado)
