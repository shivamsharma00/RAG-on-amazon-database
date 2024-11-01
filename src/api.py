# src/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from.vector_search import search_reviews
from .rag import generate_answer
import logging
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


app = FastAPI(title="Amazon Reviews API", description="API for searching and generating answers from Amazon reviews", version="1.0.0")
logger = logging.getLogger(__name__)

class Query(BaseModel):
    text: str
    top_k: int = 5


@app.post('/search', tags=["search"])
async def search_endpoint(query: Query):
    """
    Search for reviews based on a query.
    """
    try:
        results = search_reviews(query.text, query.top_k)
        if not results:
            raise HTTPException(status_code=404, detail="No results found")
        serialized_results = jsonable_encoder(results, custom_encoder={
            ObjectId: str
    })
        return {"results": serialized_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/generate', tags=["generate"])
async def generate_endpoint(query: Query):
    """
    Generate an answer based on a query.
    """
    try:
        answer = generate_answer(query.text, query.top_k)
        serialized_answer = jsonable_encoder(answer, custom_encoder={
            ObjectId: str
    })
        return {"answer": serialized_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
