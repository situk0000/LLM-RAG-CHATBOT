# 🤖 RAG Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot that lets you upload PDF documents and ask questions about their content. Built with FastAPI, LangChain, and modern embeddings.

<img width="1899" height="873" alt="image" src="https://github.com/user-attachments/assets/8530e736-2566-4274-b139-2dcf65a62cb6" />


## 🌟 Features

- **📄 PDF Upload**: Drag & drop or click to upload PDF documents
- **🔍 Smart Search**: Uses semantic search with embeddings to find relevant content
- **💬 Natural Q&A**: Ask questions in natural language and get accurate answers
- **📖 Source Attribution**: See which pages the answers come from
- **🚀 Fast Processing**: Instant document processing and embedding
- **💾 Vector Database**: FAISS-based vector store for efficient retrieval
- **🎨 Beautiful UI**: Modern, responsive web interface

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.109.0
- LangChain 0.1.0
- LangChain Community 0.0.13
- FAISS 1.7.4 (Vector Database)
- Sentence Transformers 2.5.0 (Embeddings)
- PDFPlumber 0.11.0 (PDF Processing)

**Frontend:**
- HTML5 / CSS3
- Vanilla JavaScript
- Responsive Design

**LLM Integration:**
- OpenAI API compatibility
- LM Studio support (local inference)

## 📋 Requirements

```
Python 3.9+
FastAPI==0.109.0
uvicorn[standard]==0.27.0
langchain==0.1.0
langchain-community==0.0.13
langchain-openai==0.0.2
sentence-transformers==2.5.0
faiss-cpu==1.7.4
pdfplumber==0.11.0
pydantic==2.7.4
python-dotenv==1.0.0
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/situk0000/LLM-RAG-CHATBOT.git
cd rag-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start LM Studio (Optional)
If you want to use a local LLM:
- Download [LM Studio](https://lmstudio.ai/)
- Load a model (e.g., tinyllama-1.1b-chat-v1.0)
- Start the local server on port 1234

### 4. Run the Backend
```bash
uvicorn main:app --reload
```

Backend will be available at: `http://localhost:8000`

### 6. Open the Frontend
- Open `index.html` in your browser
- Or serve it with a local server:
```bash
python -m http.server 8001
```

Then open: `http://localhost:8001`

## 📝 Usage

1. **Upload a PDF**
   - Drag & drop your PDF into the upload area
   - Or click to browse and select a file

2. **Ask Questions**
   - Type your question in the input box
   - Click "Send" or press Enter
   - The chatbot will search the document and provide an answer

3. **View Sources**
   - Each answer shows the page numbers it came from
   - Click on sources to navigate to relevant sections

4. **Reset**
   - Click the "Reset" button to clear the document and start over

## 📂 Project Structure

```
rag-chatbot/
├── main.py                 # FastAPI backend
├── index.html             # Frontend UI
├── requirements.txt       # Python dependencies
├── uploads/              # Uploaded PDFs (auto-created)
└── README.md            # This file
```

## 🔧 Configuration

### Backend Settings (main.py)

```python
# LLM Configuration
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"] = "lm-studio"

### Frontend Settings (index.html)

```javascript
const API_BASE = "http://localhost:8000";  // Backend URL
```

## 🐛 Troubleshooting

### Backend not connecting
- Ensure FastAPI server is running: `uvicorn main:app --reload`
- Check that port 8000 is available
- Verify CORS is enabled in `main.py`

### LM Studio connection failed
- Make sure LM Studio is running on `http://localhost:1234`
- Verify a model is loaded in LM Studio
- Check the API base URL in `main.py`

### No response from queries
- Verify a document is uploaded
- Check browser console (F12) for errors
- Ensure backend logs show successful query processing

### Slow embedding generation
- Sentence Transformers download model on first run (~100MB)
- Subsequent runs will be faster
- Consider using GPU if available

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License 

## ✨ Features Coming Soon

- [ ] Support for multiple documents
- [ ] Document management dashboard
- [ ] Chat history
- [ ] Custom model selection
- [ ] Export conversations
- [ ] Batch processing
- [ ] API rate limiting


## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for RAG framework
- [FastAPI](https://fastapi.tiangolo.com/) for backend
- [HuggingFace](https://huggingface.co/) for embeddings
- [FAISS](https://github.com/facebookresearch/faiss) for vector search

---
## Author
Situ Kumari - situk0000
