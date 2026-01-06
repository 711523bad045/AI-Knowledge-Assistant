import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

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
      alert("File uploaded successfully!");
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
      setAnswer("Error getting answer");
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
      <h1>📄 AI Knowledge Assistant</h1>

      <hr />

      <h3>1️⃣ Upload Document (PDF / TXT)</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={uploadFile}>Upload</button>

      <hr />

      <h3>2️⃣ Ask Question</h3>
      <input
        style={{ width: "100%", padding: 10 }}
        type="text"
        placeholder="Ask something from the document..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <br /><br />
      <button onClick={askQuestion}>Ask</button>

      <hr />

      <h3>🧠 Answer:</h3>
      {loading ? <p>Thinking...</p> : <p>{answer}</p>}
    </div>
  );
}

export default App;
