# src/vectorization.py

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import logging
from dask.diagnostics import ProgressBar
from dask import delayed, compute

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
    
    model = SentenceTransformer(model_name, device='cpu')

    batch_size = 64

    # Split texts into batches
    batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]

    @delayed
    def encode_batch(batch):
        return model.encode(batch, show_progress_bar=False)

    # Create a list of delayed tasks
    tasks = [encode_batch(batch) for batch in batches]

    # Execute tasks in parallel
    with ProgressBar():
        results = compute(*tasks, scheduler='processes')

    # Concatenate the results
    embeddings = np.vstack(results)

    logger.info(f"Embeddings generated successfully.")

    return embeddings

