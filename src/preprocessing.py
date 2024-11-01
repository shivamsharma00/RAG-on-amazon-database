# src/preprocessing.py

import pandas as pd
import re
from bs4 import BeautifulSoup
import nltk
from typing import List
import logging
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from dask import delayed, compute
from nltk.corpus import stopwords


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing HTML tags, converting to lowercase, 
    and removing non-alphabetic characters, and removing stop words.

    Args:
        text (str): The text to preprocess.

    Returns:
        str: The preprocessed text.
    """

    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    # Join tokens back into a single string
    text = ' '.join(tokens)

    return text

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess a DataFrame by cleaning text data and handling missing values.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        
    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    
    logger.info("Preprocessing DataFrame...")
    ddf = dd.from_pandas(df, npartitions=16)
    
    # Drop rows with missing 'text' values
    ddf = ddf.dropna(subset=["text"])
    
    # Fill missing 'title' values with empty strings
    if "title" in ddf.columns:
        ddf["title"] = ddf["title"].fillna("")
        # Clean title column
        ddf["title"] = ddf["title"].apply(preprocess_text, meta=("title", "object"))


    # Clean 'text' column
    ddf['text'] = ddf['text'].apply(preprocess_text, meta=("text", "object"))

    # Ensure data types
    if "rating" in ddf.columns:
        ddf['rating'] = ddf['rating'].fillna(0).astype(int)

    # Ensure boolean type for 'verified_purchase'
    if "verified_purchase" in ddf.columns:
        ddf['verified_purchase'] = ddf['verified_purchase'].fillna(False).astype(bool)

    # Convert 'timestamp' to datetime
    if "timestamp" in ddf.columns:
        ddf['timestamp'] = dd.to_datetime(ddf['timestamp'])

    with ProgressBar():
        result_df = ddf.compute()

    logger.info("DataFrame preprocessed completed.")
    
    return result_df