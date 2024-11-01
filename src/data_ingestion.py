# src/data_ingestion.py

import pandas as pd
from typing import Optional, List
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_paths: List[str], nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Load data from multiple JSONL files into a pandas DataFrame.
    
    Args:
        file_paths (List[str]): The paths to the JSONL files.
        nrows (Optional[int]): The number of rows to load from the file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the loaded data.
    """
    dataframes = []
    for file_path in file_paths:
        logger.info(f"Loading data from {file_path}...")
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.jsonl':
            df = pd.read_json(file_path, lines=True, nrows=nrows)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path, nrows=nrows)
        elif file_extension == '.txt':
            df = pd.read_csv(file_path, delimiter='\t', header=None, names=['text'], nrows=nrows)
        else:
            logger.error(f"Unsupported file format: {file_extension}")
            continue
        dataframes.append(df)
        logger.info(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
    combined_df = pd.concat(dataframes, ignore_index=True)
    logger.info(f"Combined data loaded successfully with {combined_df.shape[0]} rows and {combined_df.shape[1]} columns.")
    return combined_df