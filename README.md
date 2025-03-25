# 🧠 Multimodal RAG Chatbot

A lightweight GenAI-powered chatbot that enables users to **upload PDF documents** and ask **contextual questions** based on the document's content, including **text, tables, and images**.

---

## 🚀 Features

- 📄 Upload and process high-resolution PDFs  
- 🧠 Summarize text, tables, and images using LLMs (GPT-4o, LLaMA-3)  
- 🔎 Multi-vector retrieval using ChromaDB + InMemoryStore  
- 💬 Context-aware question answering with a custom RAG chain  
- ⚡ Real-time, async Flask + AJAX-based web interface  
- 🔐 Secure API key handling using `.env`  

---

## 🛠️ Tech Stack

- **Frontend**: HTML, JavaScript (AJAX)  
- **Backend**: Python, Flask  
- **LLMs**: OpenAI (GPT-4o), Groq (LLaMA-3.1)  
- **Retrieval**: LangChain, ChromaDB, UUID mapping  
- **PDF Processing**: `unstructured`, base64 images + HTML tables  

---

## 📦 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/multimodal-rag-chatbot.git
   cd multimodal-rag-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API keys in `.env`**
   ```ini
   OPENAI_API_KEY=your_openai_key
   GROQ_API_KEY=your_groq_key
   ```

4. **Run the Flask app**
   ```bash
   python app.py
   ```
   Visit: [http://localhost:8000](http://localhost:8000)

---

---

## 📁 Folder Structure
```bash
├── app.py                  # Flask application
├── templates/
│   └── index.html          # Chat UI
├── static/
│   └── style.css           # Simple CSS styling
├── multimodalrag/
│   ├── data_loading_processing.py
│   ├── data_transformation.py
│   ├── data_storing.py
│   └── data_retrieval.py
├── uploads/                # Uploaded PDFs
```

---

## 📌 Future Improvements that I plan to work on

- Support for DOCX, PPTX, and Excel
- Build a more profound UI using React JS
- Dockerize for scalable deployment

---

## 📝 License
This project is licensed under the **MIT License**.
