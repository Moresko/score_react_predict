from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
from predict_utils import calculate_team_form

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
model = joblib.load("model.pkl")
team_encoder = joblib.load("team_encoder.pkl")
ref_encoder = joblib.load("ref_encoder.pkl")

# Load data
football_data = pd.read_csv("premier_league.csv")
football_data.dropna(inplace=True)
football_data['Date'] = pd.to_datetime(football_data['Date'])
football_data['Result'] = football_data['FTR'].map({'H': 1, 'D': 0, 'A': -1})

class MatchInput(BaseModel):
    home_team: str
    away_team: str
    referee: str
    date: str

@app.post("/predict")
def predict(input: MatchInput):
    try:
        home_id = team_encoder.transform([input.home_team])[0]
        away_id = team_encoder.transform([input.away_team])[0]
    except ValueError:
        return {"error": "Invalid team"}

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

    return {"prediction": result_map[pred], "raw_value": int(pred)}
