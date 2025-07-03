# predict_utils.py
import numpy as np
import pandas as pd

def calculate_team_form(df, team_name, match_date, N=5):
    past_matches = df[
        ((df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)) &
        (df['Date'] < match_date)
    ].sort_values(by='Date', ascending=False).head(N)

    goals_scored, goals_conceded, results = [], [], []

    for _, row in past_matches.iterrows():
        if row['HomeTeam'] == team_name:
            goals_scored.append(row['FTHG'])
            goals_conceded.append(row['FTAG'])
            results.append(row['Result'])
        else:
            goals_scored.append(row['FTAG'])
            goals_conceded.append(row['FTHG'])
            results.append(-row['Result'])

    if len(past_matches) == 0:
        return [0, 0, 0]

    avg_goals = np.mean(goals_scored)
    avg_conceded = np.mean(goals_conceded)
    win_rate = sum(1 for r in results if r == 1) / len(results)

    return [avg_goals, avg_conceded, win_rate]
