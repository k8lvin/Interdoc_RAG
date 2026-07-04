## Document Intelligence API 
## Vector Database & RAG 

### Day 1 goals( End of session checklists) 

- explain in your own words, what an embedding is and why similar meanings end up as nearby vectors 
- explain difference between keyword search and vector(semantic) search 
- upload a real file through your own API endpoint  and have it chunked and stored. 
- explain why chunk overlap matters 
- run a search query against your stored chunks and get back relevant results - with zero AI/LLM involved 
- and again You should be able to know exactly what is still missing to turn this into a real "'chat with your documents product" (hio ni kesho)


```
interdoc/ 
	|--app/
		|---- ingestion.py
		|---- vectorstore.py
		|---- main.py 
        |---- rag.py
	|--data/
		|---- chromadb
```

-> ingestion.py - extracting text from a file and splitting it into chunks
-> vectorestore.py - turning chunks into vectors and storing them in database (ChromaDB)
-> main.py - holds our fastAPI endpoint , that wires everything together 

~ last week - FastAPI intro (we built an API that talked to a database of rows and columns). Today - Vector Database (we build an API that talke to a database of meaning) 


## I want us to be able to REDRAW these three idea from memory by end of the session.
1)	Embeddings
-	An Embedding is a piece of text turned into a list of numbers (a vector) , such that text with similar MEANING ends up close together in that number space.
-	‘Cat’ and ‘dog’ - end up near each other 
-	‘Cat; and ‘docs’ - end far apart 
2)	Vector search
-	Is just nearest-neighbour search in that number space . 
-	Take a question, embed it into the same number space, then find which stored vectors are closest. 
3)	RAG(Retrieval-Augmented Generation) 
-	Retrieve the relevant chunks first, THEN paste them into the LLM’s prompt, so it answer using your data instead of guessing from what it memorised during training. 
Question → [embed] → [search vectors] → top-k chunks → [stuff into prompt] → LLM → Answer + sources 

### FILE 1 - app/ingestion.py 
-	One job - Take raw bytes from an uploaded file and turn them into a list of clean text chunks, ready to be embedded 

*Chunk overlap* is a crucial technique in Retrieval-Augmented Generation (RAG) and vector search where a small portion of text from the end of one chunk is repeated at the beginning of the next chunk. 

Text = "A vector database is a specialized type of database that stores data as mathematical arrays of numbers called vector embeddings. Instead of relying on exact text or keyword matches, it allows AI systems and applications to search for information based on semantic meaning or conceptual similarity."

Total chunks are 5 
Chunk 1 = “'A vector database is a specialized type of database that stores data as mathematical arrays'”

Chunk 2 = “'stores data as mathematical arrays of numbers called vector embeddings. Instead of relying on exact'”

Chunk 3 = “ 'Instead of relying on exact text or keyword matches, it allows AI systems and applications'”

Chunk 4 = “ 'allows AI systems and applications to search for information based on semantic meaning or conceptual'”

Chunk 5 = “'on semantic meaning or conceptual similarity.'” 
Chunk size =300, overlap = 50
words: [0………………………………………………………1000]
Chunk 1: [0………………….300]
Chunk 2:        [250…………………………….550]
Chunk 3:             [500……………………………800]
Chunk 4:                           [750……………………………..1000]


### FILE 2 - app/vectorstore.py (embed + store in ChromaDB)
-	This is where chunks actually become vectors and get saved somewhere we can search later 
-	1) sentence-transformers - turns text into numbers 2) ChromaDB - stores those numbers and know how to searchthem

### FILE 3 app/main.py 
-	This is where FastAPI lives 
-	Where the other two files are wired together. 


## Document Intelligence API 
 
### Closing the loop - Real RAG  
 
-Previous session we proved retrieval works on its own. (we could find the right 
chunks for a question , with no AI model involved) 
-Today we take those retrieved chunks, hand them to an LLM with careful 
instructions, and get back a real answer.  
 
 
### FILE 4 -app/rag.py 
-Building a grounded prompt and calling the LLM(OpenAI, Groq, Openrouter)   
 
Update the file app/main.py 
-Add the /query endpoint that ties retrieval and generation together  
 
### FILE 4 rag.py - prompt building + the LLM call  
-1) build a prompt that forces the model to answer ONLY from the chunks we 
give it  
-2) call an LLM with that prompt - get answers from documents   
 
Question = the user’s question e.g “Where is the company based” 
Chunks - list of text strings retrieved from ChromaDB 
Metadatas = list metadatas dictionaries for those chunks e.g [{“source”: 
“company.txt”, “chunk_index” : 1},......]  
 
enumerate - just adds a counter to our iterable , start=1 , (1, 2,3,4…..) 
meta[“source”] - the file name - company.txt 
meta[“chunk_index”] - which chunk number within that file  
\n - puts the chunk text on a new line below  
 
Context = “\n\n”.join(blocks) 
-Joins all the blocks into one big string, with a blank line between each block.  
-The ‘knowledge base’ you hand to the LLM 
 
[Source 1: Company.txt , chunk 0] 
Datapulse ai is headquartered in Nai……….. 
 
[Source 2: Company.txt, chunk 1] 
Week 1: Environment setup,.......... 
  
response: The entire payload returned by the AI endpoint. 
.choices: A list of potential answers generated by the model. By default, the API 
generates one answer, stored at index 0. 
.message: The specific object containing the AI's response. 
.content: The actual text payload (the words) the model generated 
 

