import { useState } from "react";
import "./index.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`
      );
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Error connecting to backend");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>AI Knowledge Assistant</h1>
      <p>Ask questions from IT documents</p>

      <input
        type="text"
        placeholder="Enter your question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div className="answer-box">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
