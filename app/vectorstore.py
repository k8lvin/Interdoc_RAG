import chromadb #our vector database
from chromadb.utils import embedding_functions

#PersistentClient means chroma writes everything on the disk in this folder
# even if you stop server , later on your uploaded documents are still there 
client = chromadb.PersistentClient(path="./data/chromadb")

#creating an embedding function - 
#something chroma can call automatically everytime we add or search to turn text into vector
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-V2")

#collection in chromadb is like a table in database
#get_or_create_collection if a collection named documents already exists reuse it else create a new one
collection = client.get_or_create_collection(name="documents", embedding_function=embedding_fn)

# saves chunks into the vectorstore (vector db)
def add_chunks(doc_id: str, chunks: list[str]):
    #creates a unique id for every chunk
    #chromadb requires every stored item to have a unique id
    ids = [f"{doc_id} {i}"for i in range(len(chunks))]
    
    #creates metadata dictionary for each chunk
    # "source" which file this chunk came from
    #"chunk_index" - position of this chunk within the file
    metadatas = [{"source":doc_id, "chunk_index": i} for i in range(len(chunks))]
    
    #actually inserts data into the chromadb
    # documents=chunks  - the raw text (gets embedded automatically using embedding_fn )
    collection.add(documents=chunks, metadatas=metadatas, id=ids)
    #return count of chunks that were added
    return len(chunks)

#Search_chunks finds the closest chunks to a question
# query is the question text. top k - how many of the closest chunks to return
def search_chunk(query:str, top_k: int = 4):
    return collection.query(query_texts=[query], n_results=top_k)