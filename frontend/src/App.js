import React, { useState } from "react";

function App() {
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [referee, setReferee] = useState("");
  const [date, setDate] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    const payload = {
      home_team: homeTeam,
      away_team: awayTeam,
      referee: referee,
      date: date,
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
        setPrediction(null);
      } else {
        setPrediction(data.prediction);
        setError(null);
      }
    } catch (err) {
      console.error(err);
      setError("Something went wrong");
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1> Match Predictor</h1>

      <label>Domáci: </label>
      <input value={homeTeam} onChange={(e) => setHomeTeam(e.target.value)} />
      <br /><br />

      <label>Hostia: </label>
      <input value={awayTeam} onChange={(e) => setAwayTeam(e.target.value)} />
      <br /><br />

      <label>Rozhodca: </label>
      <input value={referee} onChange={(e) => setReferee(e.target.value)} />
      <br /><br />

      <label>Dátum: </label>
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <br /><br />

      <button onClick={handlePredict}>Predict</button>

      <hr />
      {prediction && <h3>🔮 Prediction: {prediction}</h3>}
      {error && <p style={{ color: "red" }}>⚠️ {error}</p>}
    </div>
  );
}

export default App;
