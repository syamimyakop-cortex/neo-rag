import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
# RetrievalQA removed due to import issues

class RAGService:
    def __init__(self):
        self.vector_store = None
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # Initialize Ollama with a lightweight model. 
        # Switched to 'tinyllama' for lower memory usage (requires ~600MB).
        print("Initializing RAG Service with model: tinyllama")
        self.llm = OllamaLLM(model="tinyllama") 

    def load_pdf(self, file_path: str):
        """Loads a PDF and creates a vector store from it."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        self.vector_store = FAISS.from_documents(texts, self.embeddings)
        return len(texts)

    def query(self, question: str):
        """Queries the vector store."""
        if not self.vector_store:
            return "Please upload a PDF first."
            
        # Custom RAG implementation to avoid import issues
        try:
            # Retrieve relevant documents
            docs = self.vector_store.similarity_search(question, k=4)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Construct prompt
            prompt = f"""Answer the question based only on the following context:

{context}

Question: {question}
"""
            # Generate answer
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"


