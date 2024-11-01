# src/api.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from.vector_search import search_reviews
from .rag import generate_answer
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

class Query(BaseModel):
    text: str
    top_k: int = 5


@app.post('/search')
async def search_endpoint(query: Query):
    """
    Search for reviews based on a query.
    """
    results = search_reviews(query.text, query.top_k)
    return {"results": results}

@app.post('/generate')
async def generate_endpoint(query: Query):
    """
    Generate an answer based on a query.
    """
    answer = generate_answer(query.text, query.top_k)
    return {"answer": answer}
