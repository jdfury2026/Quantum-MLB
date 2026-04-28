import pandas as pd
import numpy as np
import datetime
import sys

# Intentamos importar pybaseball de forma segura
try:
    from pybaseball import schedule_and_record, mlb_api
except ImportError:
    pass

class QuantumEngine:
    def __init__(self):
        self.iterations = 5000000 

    def get_momentum_multiplier(self, team):
        # Función simplificada para evitar errores de conexión iniciales
        return 1.0

    def run_monte_carlo(self, home_team, away_team, ou_line):
        # 1. Definir expectativas de carreras (Lambdas)
        # En una versión futura, estos datos vendrán de los stats reales de hoy
        home_lambda = 4.5
        away_lambda = 4.2
        
        # 2. Generación de 5,000,000 de juegos simultáneos usando NumPy (Velocidad Luz)
        home_scores = np.random.poisson(home_lambda, self.iterations)
        away_scores = np.random.poisson(away_lambda, self.iterations)
        
        # 3. Cálculos de Probabilidad
        home_wins = np.sum(home_scores > away_scores)
        prob_ml_home = (home_wins / self.iterations) * 100
        
        # Probabilidad de cubrir Spread -1.5
        home_covers = np.sum((home_scores - 1.5) > away_scores)
        prob_spread_home = (home_covers / self.iterations) * 100
        
        # Probabilidad de Over (Altas)
        total_runs = home_scores + away_scores
        prob_over = (np.sum(total_runs > ou_line) / self.iterations) * 100

        return {
            "ml_home": round(prob_ml_home, 2),
            "ml_away": round(100 - prob_ml_home, 2),
            "spread_home_minus_1_5": round(prob_spread_home, 2),
            "over_prob": round(prob_over, 2)
        }
