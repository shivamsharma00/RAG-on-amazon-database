# src/vector_search.py

from pymongo.collection import Collection
from .vectorization import generate_embeddings
from .database import get_mongo_client
from typing import List, Dict
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def search_reviews(query: str, top_k: int = 5) -> List[Dict]:
    """
    Search for reviews similar to the query text.
    
    Args:
        query (str): The query text to search for.
        top_k (int): The number of top results to return.
        
    Returns:
        List[Dict]: A list of dictionaries containing the search results.
    """

    # Generate embeddings for the query
    query_embedding = generate_embeddings([query])[0].tolist()
    

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['AmazonDataset']
    collection = db['reviews']

    # Check if embeddings exist in the collection
    if not collection.count_documents({'embedding': {'$exists': True}}):
        logger.error("No documents found with 'embedding' field in the collection.")
        return []

    # Aggergation pipeline
    pipeline = [
        {
            "$search": {
                'index': 'embedding_index',
                'knnBeta': {
                    'vector': query_embedding,
                    'path': 'embedding',
                    'k': top_k
                }
            }
        },
        {
            "$project": {
                'title': 1,
                'text': 1,
                'score': {
                    '$meta': 'searchScore'
                },
                '_id': 1
            }
        }
    ]

    # Execute the query 
    logger.info(f"Executing vector search query ...")
    try:
        # Execute the aggregation pipeline
        results = list(collection.aggregate(pipeline))
        logger.info(f"Vector search query executed successfully.")
        return results
    except Exception as e:
        logger.error(f"Error executing vector search query: {e}")
        return []
