from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from app.ingestion import extract_text, chunk_text
from app.vectorstore import add_chunks, search_chunk
from app.rag import generate_answer
app = FastAPI(title="Document Intelligence Api")


class QueryRequest(BaseModel):
    question: str
    top_k : int = 4
    

@app.get("/")
def root():
    return {"status":"Alive"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = file.read()
    text = extract_text(file.filename, contents)
    #chunks - list of text chunks ambed and store
    chunks = chunk_text(text)
    #n- integer count of chunks that were successfully added
    n =add_chunks(doc_id=file.filename, chunks=chunks)
    #return json response back to whoever calls/upload endpoint
    return {"filename": file.filename, "chunks_created":n}

@app.post("/query")
async def query_documents(request:QueryRequest):
    results = search_chunk(request.question, top_k=request.top_k)
    return generate_answer(request.question,results)