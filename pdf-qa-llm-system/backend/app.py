from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from typing import List, Optional



print("=" * 60)
print("🚀 Starting RAG Chatbot Backend")
print("=" * 60)

# Try different import methods based on LangChain version
try:
    from langchain_community.document_loaders import PDFPlumberLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.prompts import PromptTemplate
    from langchain.chains import RetrievalQA
    from langchain_openai import ChatOpenAI

    print("✅ Using new LangChain imports")
except ImportError:
    try:
        from langchain.document_loaders import PDFPlumberLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.prompts import PromptTemplate
        from langchain.chains import RetrievalQA
        from langchain.chat_models import ChatOpenAI

        print("✅ Using old LangChain imports")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Please run: pip install langchain langchain-community langchain-openai")
        exit(1)

# Initialize FastAPI app
app = FastAPI(title="RAG Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
vector_store = None
qa_chain = None
current_document = None

# LM Studio Configuration
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"] = "lm-studio"

print("✅ Configuration loaded")


# Request/Response Models
class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[int]] = []


class UploadResponse(BaseModel):
    filename: str
    message: str
    chunks: int


# Helper function to initialize the RAG pipeline
def initialize_rag_pipeline(pdf_path: str):
    global vector_store, qa_chain

    print(f"\n📄 Loading PDF: {pdf_path}")
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} pages")

    print("🔪 Chunking documents...")
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    documents = text_splitter.split_documents(docs)
    print(f"✅ Created {len(documents)} chunks")

    print("🧠 Creating vector store...")
    vector_store = FAISS.from_documents(documents, embeddings)
    print("✅ Vector store created")

    print("🤖 Initializing LLM...")
    llm = ChatOpenAI(
        model_name="tinyllama-1.1b-chat-v1.0",
        temperature=0.7,
        openai_api_base=os.environ["OPENAI_API_BASE"],
        openai_api_key=os.environ["OPENAI_API_KEY"],
        request_timeout=60,
    )

    # Create QA chain
    prompt_template = """Use the following context to answer the question. If you cannot find the answer in the context, say "I don't have enough information to answer that question."

Context: {context}

Question: {question}

Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )

    print("✅ RAG pipeline initialized")

    return len(documents)


# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "RAG Chatbot API is running! 🚀",
        "status": "active",
        "document_loaded": current_document is not None,
        "endpoints": {
            "docs": "/docs",
            "upload": "POST /upload",
            "query": "POST /query",
            "reset": "DELETE /reset"
        }
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    global current_document

    print(f"\n📤 Received upload: {file.filename}")

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Create uploads directory
    os.makedirs("uploads", exist_ok=True)

    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"✅ File saved: {file_path}")

        # Initialize RAG pipeline
        chunks = initialize_rag_pipeline(file_path)
        current_document = file.filename

        response = {
            "filename": file.filename,
            "message": "Document processed successfully",
            "chunks": chunks
        }
        
        print(f"✅ Sending response: {response}")
        
        return UploadResponse(**response)
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    global qa_chain

    print(f"\n❓ Query: {request.query}")

    if qa_chain is None:
        raise HTTPException(
            status_code=400,
            detail="No document loaded. Please upload a PDF first."
        )

    try:
        result = qa_chain({"query": request.query})

        # Extract page numbers
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                if hasattr(doc, 'metadata') and 'page' in doc.metadata:
                    sources.append(doc.metadata['page'] + 1)

        print(f"✅ Answer generated")

        return QueryResponse(
            answer=result["result"],
            sources=list(set(sources))
        )
    except Exception as e:
        print(f"❌ Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.delete("/reset")
async def reset():
    global vector_store, qa_chain, current_document

    print("\n🔄 Resetting system...")
    vector_store = None
    qa_chain = None
    current_document = None

    if os.path.exists("uploads"):
        shutil.rmtree("uploads")

    print("✅ Reset complete")
    return {"message": "System reset successfully"}


@app.on_event("startup")
async def startup_event():
    print("\n" + "=" * 60)
    print("✅ SERVER STARTED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📍 Server URL: http://localhost:8000")
    print("📚 API Docs:   http://localhost:8000/docs")
    print("\n⚠️  IMPORTANT: Make sure LM Studio is running on port 1234!")
    print("=" * 60 + "\n")


# Main entry point
if __name__ == "__main__":
    import uvicorn

    print("\n🎬 Starting Uvicorn server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )