# src/rag.py

from transformers import pipeline
from .vector_search import search_reviews
from typing import List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_answer(query: str, top_k: int = 5) -> str:
    """
    Generate an answer based on a query using a RAG pipeline.

    Args:
        query (str): The query text to generate an answer for.
        top_k (int): The number of top results to return.
        
    Returns:
        str: The generated answer.
    """

    # Retrieve relevant documents 
    relevant_reviews = search_reviews(query, top_k)
    # Concatenate the text of the retrieved documents
    context = ' '.join([review['text'] for review in relevant_reviews])

    # Initialize the text generation pipeline
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

    # Prepare the input for generation
    input_text = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"

    # Generate the answer
    logger.info(f"Generating answer ...")
    answer = generator(input_text, max_length=150, do_sample=True)
    answer = answer[0]['generated_text']

    return answer
