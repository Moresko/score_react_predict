# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib as jb
from predict_utils import calculate_team_form

app = FastAPI()

# Load trained model + encoders
model = jb.load("model.pkl")
team_encoder = jb.load("team_encoder.pkl")
ref_encoder = jb.load("ref_encoder.pkl")

# Load full dataset to compute form
football_data = pd.read_csv("premier_league.csv")
football_data.dropna(inplace=True)
football_data['Date'] = pd.to_datetime(football_data['Date'], errors='coerce')
football_data['Result'] = football_data['FTR'].map({'H': 1, 'D': 0, 'A': -1})

# Request schema
class MatchInput(BaseModel):
    home_team: str
    away_team: str
    referee: str
    date: str  # ISO format

@app.post("/predict")
def predict_match(input: MatchInput):
    try:
        home_id = team_encoder.transform([input.home_team])[0]
        away_id = team_encoder.transform([input.away_team])[0]
    except ValueError:
        return {"error": "Unknown team name."}

    referee_id = (
        ref_encoder.transform([input.referee])[0]
        if input.referee in ref_encoder.classes_
        else -1
    )

    match_date = pd.to_datetime(input.date)

    home_form = calculate_team_form(football_data, input.home_team, match_date)
    away_form = calculate_team_form(football_data, input.away_team, match_date)

    row = pd.DataFrame([{
        "HomeID": home_id,
        "AwayID": away_id,
        "RefereeID": referee_id,
        "Month": match_date.month,
        "Year": match_date.year,
        "HomeAvgGoals": home_form[0],
        "HomeAvgConceded": home_form[1],
        "HomeWinRate": home_form[2],
        "AwayAvgGoals": away_form[0],
        "AwayAvgConceded": away_form[1],
        "AwayWinRate": away_form[2],
    }])

    pred = model.predict(row)[0]
    result_map = {1: "🏠 Home Win", 0: "🤝 Draw", -1: "✈️ Away Win"}
    return {
        "prediction": result_map[pred],
        "raw_value": int(pred)
    }
