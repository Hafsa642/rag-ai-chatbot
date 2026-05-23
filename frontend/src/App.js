import React, {useState,useRef,useEffect} from "react";
import axios from "axios";
import "./App.css";
import robot from "./assets/chatbot.png";
function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [started, setStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const fileInputRef = React.useRef(null);
  const chatEndRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
   const handleFileUpload = async (event) => {

  const file = event.target.files[0];
  setSelectedFile(file);
  if (!file) return;

  const formData = new FormData();

  formData.append("file", file);

  try {

    await axios.post(
      "http://localhost:8000/upload",
      formData
    );

    alert("File uploaded successfully!");

  } catch (error) {

    console.error(error);

    alert("Upload failed");

  }
};
  const sendMessage = async () => {

    if (!question.trim()) return;
    const currentQuestion = question;

const userMessage = {
  type: "user",
  text: currentQuestion,
  file: selectedFile
};

    setMessages((prev) => [...prev, userMessage]);

    setLoading(false);
    setQuestion("");
    setSelectedFile(null);
    try {

      const response = await axios.post(
       "http://localhost:8000/chat",
       {
          question: currentQuestion
        }
      );

      const botMessage = {
        type: "bot",
        text: response.data.answer,
        sources: response.data.sources
      };

      setMessages((prev) => [...prev, botMessage]);

    } catch (error) {

      console.error(error);

    }

    setLoading(true);
  };

useEffect(() => {

  chatEndRef.current?.scrollIntoView({
    behavior: "smooth"
  });

}, [messages, loading]);

  if (!started) {

  return (

    <div className="landing-page">

      <div className="landing-card">

        <img
          src={robot}
          alt="Robot"
          className="robot-image"
        />
       <div className="landing-content">
        <h1>
          How may I help you today?
        </h1>

        <button
          className="start-btn"
          onClick={() => setStarted(true)}
        >
          Get Started
        </button>
         </div>

      </div>

    </div>

  );
}

  return (

  <div className="container">

    <div className="header">

      <h1 className="title">
        AI Research Assistant
      </h1>

      <p className="subtitle">
        Powered by RAG • LLaMA • LangChain
      </p>

    </div>

    <div className="chat-box">

     {messages.map((msg, index) => (

    <div
      key={index}
      className={msg.type}
    >

      {msg.file && (

        <div className="chat-file">

          <div className="chat-file-icon">
            📄
          </div>

          <div className="chat-file-name">
            {msg.file.name}
          </div>

        </div>

      )}

      <p>{msg.text}</p>

      {msg.sources && msg.sources.length > 0 && (

        <div className="sources">

          <strong>Sources:</strong>

          {msg.sources.map((source, i) => (

            <div key={i}>

              {source.source} | Page {source.page}

            </div>

          ))}

        </div>

      )}

    </div>

  ))}
  <div ref={chatEndRef}></div>

</div>
<div className="input-box">

  <button
    className="attach-btn"
    onClick={() => fileInputRef.current.click()}
  >
    📎
  </button>

  <input
    type="file"
    ref={fileInputRef}
    style={{ display: "none" }}
    onChange={handleFileUpload}
  />

  {selectedFile && (

    <div className="input-preview-file">

      <div className="preview-file-icon">
        📄
      </div>

      <div className="preview-file-name">
        {selectedFile.name}
      </div>

    </div>

  )}

  <input
    type="text"
    placeholder="Ask anything..."
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
    onKeyDown={(e) => {
      if (e.key === "Enter") {
        sendMessage();
      }
    }}
  />
  <button
  className="send-btn"
  onClick={sendMessage}
>
  ➤
</button>
</div>

</div>
);
}

export default App;
