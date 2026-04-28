import sys
import pandas as pd
import numpy as np
import datetime

# Forzamos al sistema a buscar las librerías instaladas
try:
    from pybaseball import schedule_and_record, mlb_api
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pybaseball"])
    from pybaseball import schedule_and_record, mlb_api

class QuantumEngine:
    def __init__(self):
        self.iterations = 5000000
class QuantumEngine:
    def __init__(self):
        self.iterations = 5000000 
        
    def get_todays_games(self):
        """Obtiene los juegos y pitchers probables para hoy"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            # Consultamos la API oficial de MLB
            schedule = mlb_api.get_schedule(date=today)
            games_today = []
            for game in schedule:
                games_today.append({
                    "game_id": game.get('game_pk'),
                    "home": game.get('home_name'),
                    "away": game.get('away_name'),
                    "venue": game.get('venue_name'),
                    "status": game.get('status')
                })
            return games_today
        except Exception as e:
            print(f"Error en API: {e}")
            return []

    def get_momentum_multiplier(self, team_abbreviation, year=2026):
        try:
            data = schedule_and_record(year, team_abbreviation).tail(10)
            results = [1 if x == 'W' else 0 for x in data['W/L']]
            if not results: return 1.0
            weights = np.arange(1, len(results) + 1)
            momentum_idx = np.sum(np.array(results) * weights) / np.sum(weights)
            return 1 + (momentum_idx - 0.5) * 0.10
        except:
            return 1.0

    def run_monte_carlo(self, home_team, away_team, over_under_line):
        # Lógica de simulación 5M
        home_final_lambda = 4.5 * self.get_momentum_multiplier(home_team)
        away_final_lambda = 4.1 * self.get_momentum_multiplier(away_team)

        home_sim = np.random.poisson(home_final_lambda, self.iterations)
        away_sim = np.random.poisson(away_final_lambda, self.iterations)

        home_wins = np.sum(home_sim > away_sim)
        prob_ml_home = (home_wins / self.iterations) * 100
        home_covers = np.sum((home_sim - 1.5) > away_sim)
        prob_spread_home = (home_covers / self.iterations) * 100
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
