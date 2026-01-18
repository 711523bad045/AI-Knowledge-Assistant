import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploaded, setUploaded] = useState(false);

  const backendUrl = "http://127.0.0.1:8000";

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${backendUrl}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("File uploaded and processed!");
      setUploaded(true);
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    }
  };

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);
    setAnswer("");

    try {
      const res = await axios.get(`${backendUrl}/ask`, {
        params: { question },
      });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("Error getting answer from server");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>📄 AI Knowledge Assistant</h1>
      <p className="subtitle">Upload a document and chat with it using offline AI</p>

      {/* Upload Card */}
      <div className="card">
        <h2>📤 Upload Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile}>Upload & Process</button>
        {uploaded && <p className="success">✅ Document ready for questions</p>}
      </div>

      {/* Chat Card */}
      <div className="card">
        <h2>💬 Ask a Question</h2>
        <input
          className="question-input"
          type="text"
          placeholder="Ask something from the document..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={askQuestion}>Ask</button>

        <div className="answer-box">
          {loading ? (
            <p className="thinking">🤔 Thinking...</p>
          ) : answer ? (
            <p>{answer}</p>
          ) : (
            <p className="hint">Answer will appear here...</p>
          )}
        </div>
      </div>

      <footer>
        <p>🚀 Built with React + FastAPI + FAISS + Offline AI</p>
      </footer>
    </div>
  );
}

export default App;
