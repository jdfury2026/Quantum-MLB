import pandas as pd
import numpy as np
import datetime

# Importación ultra-segura
try:
    import pybaseball
    from pybaseball import mlb_api
except Exception:
    pass

class QuantumEngine:
    def __init__(self):
        self.iterations = 5000000 

    def run_monte_carlo(self, home_team, away_team, ou_line):
        # Valores base para asegurar que el simulador funcione 
        # mientras se descargan datos reales
        home_lambda = 4.4
        away_lambda = 4.1
        
        # Simulación Monte Carlo de 5M
        home_scores = np.random.poisson(home_lambda, self.iterations)
        away_scores = np.random.poisson(away_lambda, self.iterations)
        
        home_wins = np.sum(home_scores > away_scores)
        prob_ml_home = (home_wins / self.iterations) * 100
        
        home_covers = np.sum((home_scores - 1.5) > away_scores)
        prob_spread_home = (home_covers / self.iterations) * 100
        
        total_runs = home_scores + away_scores
        prob_over = (np.sum(total_runs > ou_line) / self.iterations) * 100

        return {
            "ml_home": round(prob_ml_home, 2),
            "ml_away": round(100 - prob_ml_home, 2),
            "spread_home_minus_1_5": round(prob_spread_home, 2),
            "over_prob": round(prob_over, 2)
        }
