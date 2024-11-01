# src/vectorization.py

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_embeddings(texts: List[str], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Generate embeddings for a list of texts using a pre-trained model.

    Args:
        texts (List[str]): The list of texts to generate embeddings for.
        model_name (str): The name of the pre-trained model to use.

    Returns:
        np.ndarray: An array of embeddings.
    """
    logger.info(f"Generating embeddings for {len(texts)} texts using model {model_name}...")
    model = SentenceTransformer(model_name)
    logger.info(f"Model {model_name} loaded successfully.")
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True)
    logger.info(f"Embeddings generated successfully.")

    return embeddings
