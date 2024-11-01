# src/preprocessing.py

import pandas as pd
import re
from bs4 import BeautifulSoup
import nltk
from typing import List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nltk.download('punkt', quiet=True)

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing HTML tags, converting to lowercase, and removing non-alphabetic characters.

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

    # Drop rows with missing 'text' values
    df = df.dropna(subset=["text"])
    # Fill missing 'title' values with empty strings
    df["title"] = df["title"].fillna("")
    # Clean 'text' and 'title' columns
    df['text'] = df['text'].apply(preprocess_text)
    df['title'] = df['title'].apply(preprocess_text)
    # Ensure data types
    df['rating'] = df['rating'].astype(int)
    df['verified_purchase'] = df['verified_purchase'].astype(bool)
    # Convert 'timestamp' to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    logger.info("DataFrame preprocessed completed.")
    return df
