# src/data_ingestion.py

import pandas as pd
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Load data from a JSONL file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the JSONL file.
        nrows (Optional[int]): The number of rows to load from the file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the loaded data.
    """

    logger.info(f"Loading data from {file_path}...")
    df = pd.read_json(file_path, lines=True, nrows=nrows)
    logger.info(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df