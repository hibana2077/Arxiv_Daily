from langchain_core.pydantic_v1 import BaseModel, Field
from contextlib import asynccontextmanager
from langchain_groq import ChatGroq
from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from fastapi.responses import JSONResponse
import selfarxiv
import redis
import os
import uvicorn
import re
from fastapi.middleware.cors import CORSMiddleware

# ollama_server = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
redis_server = os.getenv("REDIS_SERVER", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
HOST = os.getenv("HOST", "127.0.0.1")
GROQ_API_TOKEN = os.getenv("GROQ_API_TOKEN", "YOUR_GROQ_API")
# embeddings = OllamaEmbeddings(base_url=ollama_server)

class PaperInfo(BaseModel):
    Innovation_or_Breakthrough: str = Field(..., title="Innovation or Breakthrough of the paper")

counter_db = redis.Redis(host=redis_server, port=redis_port, db=0) # string
daily_check_db = redis.Redis(host=redis_server, port=redis_port, db=1) # set

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

@app.get("/daily-cs-papers")
def fetch_daily_cs_papers(year: int, month: int, day: int):
    """
    A function that fetches daily CS papers from arXiv.

    Args:
        year (int): The year of the date.
        month (int): The month of the date.
        day (int): The day of the date.

    Returns:
        dict[str,list[dict]]: A dictionary with the fetched papers.
    """
    filted_papers = []
    date = datetime(year, month, day)
    papers = selfarxiv.fetch_daily_cs_papers(date)
    pattern = re.compile(r'(?:Accept.*?\b(?:CVPR|ECCV|NeurIPS|ICML|ICLR|AAAI|KDD|ACL|NAACL|EMNLP|ICCV|SIGGRAPH)\b|\b(?:CVPR|ECCV|NeurIPS|ICML|ICLR|AAAI|KDD|ACL|NAACL|EMNLP|ICCV|SIGGRAPH)\b)', re.IGNORECASE)
    
    for paper in papers:
        if pattern.search(paper["arxiv_comment"]):
            filted_papers.append(paper)
    
    filted_papers = filted_papers[:5]
    if len(filted_papers) == 0:
        filted_papers = papers[:5]
    print(f"Function name: fetch_daily_cs_papers, filted_papers: {filted_papers}")
    chat = ChatGroq(
        temperature=0,
        model="gemma2-9b-it",
        # model="llama3-70b-8192",
        groq_api_key=GROQ_API_TOKEN,
    )
    structured_llm = chat.with_structured_output(PaperInfo)

    final_papers = []

    for paper in filted_papers:
        out_put = structured_llm.invoke(f"Please description the innovation or breakthrough of the Paper Summary: {paper['summary']}")
        print(f"Function name: fetch_daily_cs_papers, output: {out_put}")
        paper["Innovation_or_Breakthrough"] = out_put.Innovation_or_Breakthrough

        final_papers.append(paper)
    print(f"Function name: fetch_daily_cs_papers, final_papers: {final_papers}")
    return {"papers": final_papers}

@app.post("/daily_check")
def daily_check(data: dict):
    """
    A function that checks if the daily papers have been fetched.

    Returns:
        dict: A dictionary with the message "Daily papers have been fetched".
    """
    year = data["year"]
    month = data["month"]
    day = data["day"]
    date = datetime(year, month, day)
    date_str = date.strftime("%Y-%m-%d")
    key = f"{date_str}_fetched"
    daily_check_db.sadd(key, "fetched")
    return {"message": "DB updated"}

@app.get("/daily_check")
def get_daily_check(year: int, month: int, day: int):
    """
    A function that checks if the daily papers have been fetched.

    Returns:
        dict: A dictionary with the message "Daily papers have been fetched".
    """
    date = datetime(year, month, day)
    date_str = date.strftime("%Y-%m-%d")
    key = f"{date_str}_fetched"
    return {"fetched": daily_check_db.sismember(key, "fetched")}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8081) # In docker need to change to 0.0.0.0