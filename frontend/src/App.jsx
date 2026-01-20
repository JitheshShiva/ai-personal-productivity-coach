import { useState } from "react";

function App() {
  // ---------------- Scroll Hint ----------------
  const [showScrollHint, setShowScrollHint] = useState(false);

  // ---------------- Form state ----------------
  const [goals, setGoals] = useState("");
  const [hours, setHours] = useState(8);
  const [startTime, setStartTime] = useState("09:00");
  const [energyLevel, setEnergyLevel] = useState("medium");

  // ---------------- UI state ----------------
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // ---------------- API call ----------------
  const generatePlan = async () => {
    setShowScrollHint(true);
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("https://ai-personal-productivity-coach.onrender.com/generate-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          goals: goals.split(",").map((g) => g.trim()),
          available_hours: Number(hours),
          distractions: ["phone", "social media"],
          start_time: startTime,
          energy_level: energyLevel,
        }),
      });

      if (!response.ok) throw new Error();

      const data = await response.json();
      setResult(data);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-background">
      <div className="center-wrapper">
        <div className="app-card">
          <h1>AI Personal Productivity Coach 🙇‍♂️</h1>
          <p className="subtitle">Turn your time into focused progress</p>

          {/* ----------- Form ----------- */}
          <label>Daily Goals (comma separated)</label>
          <input
            value={goals}
            onChange={(e) => setGoals(e.target.value)}
            placeholder="Study, Workout, Project work"
          />

          <label>Available Hours</label>
          <input
            type="number"
            value={hours}
            min="1"
            max="24"
            onChange={(e) => setHours(e.target.value)}
          />

          <label>Start Time</label>
          <input
            type="time"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />

          <label>Energy Level</label>
          <select
            value={energyLevel}
            onChange={(e) => setEnergyLevel(e.target.value)}
          >
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <button onClick={generatePlan} disabled={loading}>
            {loading ? "Generating Plan..." : "Generate Plan"}
          </button>

          {/* ----------- Scroll Hint ----------- */}
          {showScrollHint && (
            <div className="scroll-hint">
              ↓ Scroll down to see your plan
            </div>
          )}

          {/* ----------- Error ----------- */}
          {error && <div className="result-card error">{error}</div>}

          {/* ----------- Result ----------- */}
          {result && (
            <div className="result-card">
              <h3>Priority Order</h3>
              <ul>
                {result.priority_order.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>

              <h3>Schedule</h3>
              <ul>
                {result.schedule.map((b, i) => (
                  <li key={i}>
                    <strong>
                      {b.start_time} – {b.end_time}
                    </strong>{" "}
                    · {b.task}
                  </li>
                ))}
              </ul>

              <h3>Productivity Tips</h3>
              <ul>
                {result.tips.map((t, i) => (
                  <li key={i}>{t}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;



