from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.pydantic_v1 import BaseModel, Field
from contextlib import asynccontextmanager
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import selfarxiv
import redis
import os
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware

# ollama_server = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
redis_server = os.getenv("REDIS_SERVER", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
HOST = os.getenv("HOST", "127.0.0.1")
# embeddings = OllamaEmbeddings(base_url=ollama_server)

class Keywords(BaseModel):

    keywords: list = Field(description="The keywords generated from the description")

counter_db = redis.Redis(host=redis_server, port=redis_port, db=0) # string
user_rec_db = redis.Redis(host=redis_server, port=redis_port, db=1) # hash
idea_db = redis.Redis(host=redis_server, port=redis_port, db=2) # hash
suggest_db = redis.Redis(host=redis_server, port=redis_port, db=3) # hash
paper_sketch_db = redis.Redis(host=redis_server, port=redis_port, db=4) # hash

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     _ = requests.post(f"{ollama_server}/api/pull", json={"name": "nomic-embed-text"})
#     _ = requests.post(f"{ollama_server}/api/pull", json={"name": "jina/jina-embeddings-v2-snall-en"})

@app.get("/")
def read_root():
    """
    A function that handles the root endpoint.

    Returns:
        dict: A dictionary with the message "Hello: World".
    """
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8081) # In docker need to change to 0.0.0.0