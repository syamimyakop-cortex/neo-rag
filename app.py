import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rag_engine import RAGService

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize RAG Service
rag_service = RAGService()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Welcome to Neo-Science RAG. Go to /static/index.html to use the app."})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print(f"Received upload request for file: {file.filename}")
    try:
        # Save the uploaded file temporarily
        file_location = f"temp_{file.filename}"
        print(f"Saving to {file_location}")
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        # Process the PDF
        print("Processing PDF...")
        num_chunks = rag_service.load_pdf(file_location)
        print(f"PDF processed. Chunks: {num_chunks}")
        
        # Clean up
        os.remove(file_location)
        
        return {"message": "File uploaded and processed successfully", "chunks": num_chunks}
    except Exception as e:
        print(f"Error processing upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        answer = rag_service.query(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
